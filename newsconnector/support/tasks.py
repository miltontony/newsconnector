from newsconnector.support.calais import Calais
from newsconnector.support.utils import build_related
from newsconnector.models import *
from django.utils.hashcompat import md5_constructor
from time import mktime
from datetime import datetime

from celery.task import task, TaskSet

import sys
import traceback
import feedparser
import lxml.html
from pyes import *


conn = ES('127.0.0.1:9200')


@task(ignore_result=True)
def update_feeds():
    news_feeds = [(feed.url, feed.name)\
                        for feed in NewsFeed.objects.all()]
    sports_feeds = [(feed.url, feed.name)\
                    for feed in SportsFeed.objects.all()]
    fin_feeds = [(feed.url, feed.name)\
                    for feed in FinanceFeed.objects.all()]
    e_feeds = [(feed.url, feed.name)\
                    for feed in EntertainmentFeed.objects.all()]

    task_list = [
        run_tasks.subtask((news_feeds, NewsArticle)),\
        run_tasks.subtask((sports_feeds, SportsArticle)),\
        run_tasks.subtask((fin_feeds, FinanceArticle)),\
        run_tasks.subtask((e_feeds, EntertainmentArticle))
    ]
    taskset = TaskSet(tasks=task_list)
    result = taskset.apply_async()
    result.ready()
    result.successful()


def get_image_url(links):
    for link in links:
        if(link.type == 'image/jpeg'):
            return link.href
    return ''


def get_instance(cls, dictArticle, source):
    a = None

    try:
        if not dictArticle.description:
            return

        content = lxml.html.fromstring(dictArticle.description).text_content()
        hash_str = ':'.join([dictArticle.title,  content, source])\
                      .encode('ascii', 'ignore')
        hash = md5_constructor(hash_str).hexdigest()

        a, created = cls.objects.get_or_create(link=dictArticle.link)
        if created:
            article = {'title': dictArticle.title,
            'link': dictArticle.link,
            'hash_key': hash,
            'content': content,
            'source': source,
            'tag': cls.__name__,
            'image_url': get_image_url(dictArticle.links),
            'date': '%s' %\
                    datetime.fromtimestamp(mktime(dictArticle.updated_parsed))\
                            .isoformat()}
            return article
        return None

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "Unexpected error:", exc_type
        print "Unexpected error:", exc_value
        traceback.print_tb(exc_traceback)

    return None


@task(ignore_result=True)
def run_tasks(feeds, feedModel):
    print '-- Update Started: %s --' % feedModel.__name__
    print 'Fetching RSS feeds.'
    new_articles = get_new_articles(feeds, feedModel)

    update_articles(new_articles)
    print 'Article update complete.'

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


def update_articles(articles_list):
    for art in articles_list:
        try:
            if not art:
                continue

            data = '%s %s' % (art['title'], art['content'])

            if not data:
                continue

            data = data.encode('ascii', 'ignore')

            #print 'Start OpenCalais keyword fetch.'

            calais = Calais('r8krg8jjs9smep7c2z9jvzew')
            result = calais.analyze(data)

            temp_keys = []
            if hasattr(result, 'entities'):
                temp_keys = [a["name"].lower() for a in result.entities]

            if hasattr(result, 'socialTag'):
                temp_keys += [a["name"].lower() for a in result.socialTag\
                                                if a['importance'] == '1']

            keywords = list(set(temp_keys))

            if len(keywords) > 0:
                art['keywords'] = keywords

            conn.index(art, 'newsworld', 'article')
            #print art
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "Unexpected error:", exc_type
            print "Unexpected error:", exc_value
            traceback.print_tb(exc_traceback)

    conn.refresh()
