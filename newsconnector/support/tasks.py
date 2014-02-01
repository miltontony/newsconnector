from newsconnector.models import *
from newsconnector.support.utils import *
from newsconnector.support import similar

from django.utils.hashcompat import md5_constructor
from django.core.cache import cache
from time import mktime
from datetime import datetime

from celery.task import task

import feedparser
import lxml.html
from pyes import *
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

import logging
logger = logging.getLogger(__name__)

SYSTEM_STATE_KEY = 'system_state_key'
TASK_ID_KEY = 'updatefeeds_task_key'

conn = ES('127.0.0.1:9200')


def stop_task():
    from celery import current_app as celery
    task_id = r.get(TASK_ID_KEY)
    if task_id:
        celery.control.revoke(task_id, terminate=True, signal='SIGKILL')
        logger.info('Killed: [%s]' % task_id)


def must_start_update():
    if not cache.get(SYSTEM_STATE_KEY):
        stop_task()
        return True
    logger.info('Update skipped..')
    return False


@task(ignore_result=True)
def update_feeds(force=False):
    if not must_start_update() and not force:
        return

    r.set(TASK_ID_KEY, update_feeds.request.id)
    cache.set(SYSTEM_STATE_KEY, 1, 1800)

    news_feeds = [(feed.url, feed.name)
                  for feed in NewsFeed.objects.all()]
    sports_feeds = [(feed.url, feed.name)
                    for feed in SportsFeed.objects.all()]
    fin_feeds = [(feed.url, feed.name)
                 for feed in FinanceFeed.objects.all()]
    e_feeds = [(feed.url, feed.name)
               for feed in EntertainmentFeed.objects.all()]
    inews_feeds = [(feed.url, feed.name)
                   for feed in INewsFeed.objects.all()]
    isports_feeds = [(feed.url, feed.name)
                     for feed in ISportsFeed.objects.all()]

    run_tasks(news_feeds, NewsArticle)
    similar.build('NewsArticle')

    run_tasks(sports_feeds, SportsArticle)
    similar.build('SportsArticle')

    run_tasks(fin_feeds, FinanceArticle)
    similar.build('FinanceArticle')

    run_tasks(e_feeds, EntertainmentArticle)
    similar.build('EntertainmentArticle')

    run_tasks(inews_feeds, INewsArticle)
    similar.build('INewsArticle')

    run_tasks(isports_feeds, ISportsArticle)
    similar.build('ISportsArticle')


def get_image_url(links):
    for link in links:
        if hasattr(link, 'type') and link.type == 'image/jpeg':
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
                       'date': '%s' %
                               datetime.fromtimestamp(
                                   mktime(dictArticle.published_parsed))
                       .isoformat()}
            return article
        return None

    except:
        print_exception()

    return None


def rollback_articles(articles, feedModel):
    feedModel.objects.filter(link__in=[a['link']
                                       for a in articles if a]).delete()


def run_tasks(feeds, feedModel):
    logger.info('-- Update Started: %s --' % feedModel.__name__)
    logger.info('Fetching RSS feeds.')
    new_articles = get_new_articles(feeds, feedModel)

    try:
        index_articles(new_articles)
        logger.info('Article update complete.')
        logger.info('-- Update Complete --')
    except:
        rollback_articles(new_articles, feedModel)
        logger.info('Rolling back: %s (%s)' % (
            feedModel.__name__,
            len(list(new_articles))))
        print_exception()

    conn.refresh()


def get_new_articles(feeds, feedModel):
    for feed, source in feeds:
        for entry in feedparser.parse(feed).entries:
            yield get_instance(feedModel, entry, source)


def index_articles(articles_list):
    for art in articles_list:
        if not art:
            continue
        conn.index(art, 'newsworld', 'article')
