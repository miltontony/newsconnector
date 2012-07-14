from newsconnector.support.calais import Calais
from newsconnector.support.utils import found_string, build_related
from newsconnector.models import *
from django.db import IntegrityError
from django.utils.hashcompat import md5_constructor
from time import mktime
from datetime import datetime, timedelta, date

from celery.task import task

import feedparser
import lxml.html
from lxml import etree


def get_image_url(links):
    for link in links:
        if(link.type == 'image/jpeg'):
            return link.href
    return ''


def get_instance(cls, dictArticle, source):
    a = None

    try:
        content = lxml.html.fromstring(dictArticle.description).text_content()
        hash_str = ':'.join([dictArticle.title,  content, source])\
                      .encode('ascii', 'ignore')
        hash = md5_constructor(hash_str).hexdigest()

        a, created = cls.objects.get_or_create(hash_key=hash)
        if created:
            a.title = dictArticle.title
            a.link = dictArticle.link
            a.content = content
            a.source = source
            a.image_url = get_image_url(dictArticle.links)
            a.date = datetime.fromtimestamp(mktime(dictArticle.updated_parsed))
            a.save()
            return a
        #don't save blanks
        if not a.title or not a.link:
            a.delete()
            return None
        return a

    except etree.ParseError:
        #print dictArticle.description
        pass
    except TypeError:
        #print 'Unable to save %s' % dictArticle.title
        pass
    except IntegrityError:
        #print 'Unable to save %s' % dictArticle.title
        pass

    if a:
        a.delete()
    return None


@task(ignore_result=True)
def run_tasks(feeds, feedModel, keywordModel):
    print 'Update Started.'
    print 'Updating: %s' % feedModel.__name__
    new_articles = []
    for feed, source in feeds:
        for entry in feedparser.parse(feed).entries:
            new_articles.append(get_instance(feedModel, entry, source))
    print 'Fetching complete.'
    print 'Start OpenCalais keyword fetch.'

    data = ' '.join(['%s %s' % (a.title, a.content) for a in new_articles if a])

    if data:
        print "Article count: %s" % len(new_articles)

        update_articles(new_articles, keywordModel)

        # clean keywords
        existing_slots = ['is', 'with']
        for placeholder in keywordModel.objects.all():
            if placeholder.keyword in existing_slots:
                placeholder.delete()
            else:
                existing_slots.append(placeholder.keyword)

    else:
        print '**No new articles. Update articles skipped.'

    print 'Generating featured articles.'
    build_related(feedModel, True)
    print '-- Update Complete --'
    return True


def remove_duplicate_articles():
    existing_slots = []
    for placeholder in Article.objects.all().order_by('-date_added'):
        hash_str = ':'.join([placeholder.title,  placeholder.content, placeholder.source])\
                      .encode('ascii', 'ignore')
        hash = md5_constructor(hash_str).hexdigest()
        if hash in existing_slots:
            placeholder.delete()
        else:
            existing_slots.append(hash)


def update_hash():
    existing_slots = []
    for a in Article.objects.all().order_by('-date_added'):
        hash_str = ':'.join([a.title,  a.content, a.source])\
                      .encode('ascii', 'ignore')
        hash = md5_constructor(hash_str).hexdigest()
        if hash in existing_slots:
            a.delete()
        else:
            existing_slots.append(hash)
            a.hash = hash
            a.save()


def update_articles(articles_list, keywordModel):
    for art in articles_list:
        if not art:
            continue

        data = '%s %s' % (art.title, art.content)

        if not data:
            continue

        data = data.encode('ascii', 'ignore')

        calais = Calais('r8krg8jjs9smep7c2z9jvzew', submitter="python-calais newsconnector")
        result = calais.analyze(data)

        if not hasattr(result, 'entities'):
            print 'No keywords found for [%s]' % art.title
            continue

        keywords = (a["name"].lower() for a in result.entities)

        for k in keywords:
            if not keywordModel.objects.filter(keyword=k).exists():
                try:
                    a_k = keywordModel(keyword=k)
                    a_k.save()
                    if not art.keywords.filter(pk=a_k.pk).exists():
                        art.keywords.add(a_k)
                except IntegrityError:
                    pass
            else:
                a_k = keywordModel.objects.get(keyword=k)
                if not art.keywords.filter(pk=a_k.pk).exists():
                    art.keywords.add(a_k)


def update_keywords(keywordModel=NewsKeyword, articleModel=NewsArticle):
    min_date = date.today() - timedelta(days=7)

    for word in keywordModel.objects.exclude(keyword='the').distinct():
        for a in articleModel.objects.filter(date_added__gt=min_date):
            if found_string(word.keyword, ('%s %s' % (a.title, a.content)).lower()):
                if not a.keywords.filter(pk=word.pk).exists():
                    a.keywords.add(word)
                    print "Added [%s] to [%s]" % (word.keyword, a.title)


def manual_update_articles(keywordModel=NewsKeyword, articleModel=NewsArticle):
    min_date = date.today() - timedelta(days=7)
    l = [a for a in articleModel.objects.filter(date_added__gt=min_date)]
    update_articles(l, keywordModel)
