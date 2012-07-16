from newsconnector.support.calais import Calais
from newsconnector.support.utils import found_string, build_related
from newsconnector.models import *
from django.db import IntegrityError
from django.utils.hashcompat import md5_constructor
from time import mktime
from datetime import datetime

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
    print '-- Update Started: %s --' % feedModel.__name__
    print 'Fetching RSS feeds.'

    new_articles = get_new_articles(feeds, feedModel)

    print 'Start OpenCalais keyword fetch.'

    data = ' '.join(['%s %s' % (a.title, a.content)\
                        for a in new_articles if a])

    if data:
        keywords = get_keywords(keywordModel, data)
        print 'Keywords update complete.'
        update_articles(keywords, new_articles)
        print 'Article update complete.'
    else:
        print '**No new articles. Update articles skipped.'

    print '-- Update Complete --'


@task(ignore_result=True)
def run_build_related(feedModel):
    print 'Generating featured articles.'
    build_related(feedModel, True)
    print '-- Build Related Complete --'


def get_new_articles(feeds, feedModel):
    for feed, source in feeds:
        for entry in feedparser.parse(feed).entries:
            yield get_instance(feedModel, entry, source)


def get_keywords(keywordModel, data):
    data = data.encode('ascii', 'ignore')
    calais = Calais('r8krg8jjs9smep7c2z9jvzew')
    result = calais.analyze(data)

    temp_keys = []
    if hasattr(result, 'entities'):
        temp_keys = [a["name"].lower() for a in result.entities]

    if hasattr(result, 'socialTag'):
        temp_keys += [a["name"].lower() for a in result.socialTag]

    keywords = list(set(temp_keys))

    if len(keywords) == 0:
        print '**No keywords to process.'

    for k in keywords:
        if not keywordModel.objects.filter(keyword=k).exists():
            try:
                a_k = keywordModel(keyword=k)
                a_k.save()
            except IntegrityError:
                pass
        else:
            a_k = keywordModel.objects.get(keyword=k)

        yield a_k


def update_articles(keywords, new_articles):
    for word in keywords:
        for a in new_articles:
            if found_string(word.keyword,\
                            ('%s %s' % (a.title, a.content)).lower()):
                if not a.keywords.filter(pk=word.pk).exists():
                    a.keywords.add(word)
