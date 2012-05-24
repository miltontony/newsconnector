from newsconnector.support.calais import Calais
from newsconnector.support.utils import found_string
from newsconnector.models import *
from django.db import IntegrityError
from django.utils.hashcompat import md5_constructor
from time import mktime
from datetime import datetime, timedelta, date

from celery.task import task

import feedparser
import lxml.html
from lxml import etree


def get_instance(cls, dictArticle, source):
    hash_str = ':'.join([dictArticle.title,  dictArticle.link])\
                  .encode('ascii', 'ignore')
    hash = md5_constructor(hash_str).hexdigest()
    a = None

    try:
        a, created = cls.objects.get_or_create(hash_key=hash)
        if created:
            a.title = dictArticle.title
            a.link = dictArticle.link
            a.content = lxml.html.fromstring(dictArticle.description).text_content()
            a.source = source
            a.date = datetime.fromtimestamp(mktime(dictArticle.updated_parsed))
            a.save()
            return a
        #don't save blanks
        if not a.title or not a.link:
            a.delete()
            return None
        return a

    except etree.ParseError:
        print dictArticle.description
    except TypeError:
        print 'Unable to save %s' % dictArticle.title
    except IntegrityError:
        print 'Unable to save %s' % dictArticle.title

    if a:
        a.delete()
    return None


@task(ignore_result=True)
def run_tasks(feeds, feedModel, keywordModel):
    new_articles = []
    for feed, source in feeds:
        for entry in feedparser.parse(feed).entries:
            new_articles.append(get_instance(feedModel, entry, source))
        print 'Fetched: %s' % feed
    print 'Fetching complete.'
    print 'Start OpenCalais keyword fetch.'

    data = ' '.join(['%s %s' % (a.title, a.content) for a in new_articles if a])

    if not data:
        return
    
    print "Article count: %s" % len(new_articles)

    update_articles(new_articles, keywordModel)

    print 'clean up keywords'
    existing_slots = ['is', 'with']
    for placeholder in keywordModel.objects.all():
        if placeholder.keyword in existing_slots:
            placeholder.delete()
        else:
            existing_slots.append(placeholder.keyword)

    print 'Update keywords for related articles'

    print 'Update complete.'


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

        print 'Keyword analysis complete.'
        print 'Save keywords.'
        keywords = [a["name"].lower() for a in result.entities]
        print 'Keywords found: %s' % keywords

        for k in keywords:
            if not keywordModel.objects.filter(keyword=k).exists():
                try:
                    a_k = keywordModel(keyword=k)
                    a_k.save()
                    if not art.keywords.filter(pk=a_k.pk).exists():
                        art.keywords.add(a_k)
                        print "[%s] added." % k
                    else:
                        print "Keyword [%s] already exists: [%s]" %\
                                (k, [x for x in art.keywords.all()])
                except IntegrityError:
                    print k
                    print keywordModel.objects.filter(keyword=k)
            else:
                a_k = keywordModel.objects.get(keyword=k)
                if not art.keywords.filter(pk=a_k.pk).exists():
                    art.keywords.add(a_k)
                    print "[%s] added." % k
                else:
                    print "Keyword [%s] already exists: [%s]" %\
                            (k, [x for x in art.keywords.all()])


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
