from newsconnector.support.calais import Calais
from django.db import IntegrityError
from django.utils.hashcompat import md5_constructor
from time import mktime
from datetime import datetime

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

    data = data.encode('ascii', 'ignore')

    calais = Calais('r8krg8jjs9smep7c2z9jvzew', submitter="python-calais newsconnector")
    result = calais.analyze(data)
    print 'Keyword analysis complete.'
    print 'Save keywords.'
    keywords = (a["name"].lower() for a in result.entities)

    for k in keywords:
        if not keywordModel.objects.filter(keyword=k).exists():
            try:
                keywordModel(keyword=k).save()
            except IntegrityError:
                print k
                print keywordModel.objects.filter(keyword=k)

    print 'clean up keywords'
    existing_slots = ['is', 'with']
    for placeholder in keywordModel.objects.all():
        if placeholder.keyword in existing_slots:
            placeholder.delete()
        else:
            existing_slots.append(placeholder.keyword)

    print 'Update complete.'
