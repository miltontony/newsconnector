from newsconnector.models import (
    NewsFeed, NewsArticle, SportsFeed, SportsArticle, FinanceArticle,
    FinanceFeed, EntertainmentArticle, EntertainmentFeed, INewsArticle,
    INewsFeed, ISportsArticle, ISportsFeed)
from newsconnector.support import similar, utils

from django.utils.hashcompat import md5_constructor
from time import mktime
from datetime import datetime

import feedparser
import lxml.html
from pyes import ES
from pyes.queryset import generate_model
ArticleModel = generate_model("newsworld", "article")

import logging
logger = logging.getLogger('raven')

conn = ES('127.0.0.1:9200')


def update_feeds(force=False):
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
    run_tasks(sports_feeds, SportsArticle)
    run_tasks(fin_feeds, FinanceArticle)
    run_tasks(e_feeds, EntertainmentArticle)
    run_tasks(inews_feeds, INewsArticle)
    run_tasks(isports_feeds, ISportsArticle)


def scrape_articles(limit=100):
    articles = ArticleModel.objects.exclude(fulltext__gt='').order_by('-date')
    count = 0
    for article in articles:
        try:
            article.fulltext = utils.scrape(article.link)
            article.save()
            print '[scraped] ', article.link
            count += 1
        except:
            print '[scrapper] [error] Unable to scrape ', article.link
            article.fulltext = article.content
            article.save()

        if limit and count >= limit:
            break


def build_similar(tag=None):
    if tag:
        return similar.build(tag)

    similar.build('NewsArticle')
    similar.build('SportsArticle')
    similar.build('FinanceArticle')
    similar.build('EntertainmentArticle')
    similar.build('INewsArticle')
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

        article_date = dictArticle.published_parsed
        if not article_date:
            article_date = datetime.now().isoformat()
        else:
            article_date = datetime.fromtimestamp(
                mktime(dictArticle.published_parsed)
            ).isoformat()

        a, created = cls.objects.get_or_create(link=dictArticle.link)
        if created:
            article = {
                'title': dictArticle.title,
                'link': dictArticle.link,
                'hash_key': hash,
                'content': content,
                'source': source,
                'tag': cls.__name__,
                'image_url': get_image_url(dictArticle.links),
                'date': '%s' % article_date
            }
            return article
        return None

    except:
        utils.print_exception()

    return None


def rollback_articles(articles, feedModel):
    feedModel.objects.filter(link__in=[a['link']
                                       for a in articles if a]).delete()


def run_tasks(feeds, feedModel):
    logger.info('[update] Started: %s --' % feedModel.__name__)
    logger.info('[update] Fetching RSS feeds.')
    new_articles = list(get_new_articles(feeds, feedModel))
    l_new_articles = len([a for a in new_articles if a])
    try:
        index_articles(new_articles)
        logger.info('[update][%s] Complete. new:%s' % (
            feedModel.__name__,
            l_new_articles))
    except:
        rollback_articles(new_articles, feedModel)
        logger.info('[update][error] Rolling back: %s (%s)' % (
            feedModel.__name__,
            l_new_articles))
        utils.print_exception()

    conn.indices.refresh('newsworld')


def get_new_articles(feeds, feedModel):
    for feed, source in feeds:
        for entry in feedparser.parse(feed).entries:
            yield get_instance(feedModel, entry, source)


def scrape_article(article):
    try:
        article['fulltext'] = utils.scrape(article['link'])
        logger.info('[scraped] ' + article['link'])
    except:
        logger.error(
            '[scrapper] [error] Unable to scrape %s' % article['link'],
            exc_info=True)
    return article


def index_articles(articles_list):
    for art in articles_list:
        if not art:
            continue
        if ArticleModel.objects.filter(hash_key=art['hash_key']).exists():
            logger.info('[index][skipped] ' + art['link'])
            continue
        art = scrape_article(art)
        conn.index(art, 'newsworld', 'article')
