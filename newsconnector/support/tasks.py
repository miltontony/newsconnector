from newsconnector.models import (
    NewsFeed, NewsArticle, SportsFeed, SportsArticle, FinanceArticle,
    FinanceFeed, EntertainmentArticle, EntertainmentFeed, INewsArticle,
    INewsFeed, ISportsArticle, ISportsFeed, Article)
from newsconnector.support import similar, utils

from django.utils.hashcompat import md5_constructor
from django.db.models.loading import get_model

from time import mktime
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz

from pyes import ES
from pyes.queryset import generate_model
conn = ES('127.0.0.1:9200')

import json
import redis
import feedparser
import lxml.html
import logging
logger = logging.getLogger('raven')


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
                'title': utils.clean(dictArticle.title),
                'link': dictArticle.link,
                'hash_key': hash,
                'content': utils.clean(content),
                'source': source,
                'tag': cls.__name__,
                'image_url': get_image_url(dictArticle.links),
                'date': '%s' % article_date
            }
            a.title = article['title']
            a.hash_key = article['hash_key']
            a.content = article['content']
            a.source = article['source']
            a.date = article['date']
            a.image_url = article['image_url']
            a.save()
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


def update_fulltext(article):
    try:
        art = Article.objects.get(hash_key=article['hash_key'])
        if article['fulltext']:
            ratio = fuzz.token_set_ratio(
                similar.get_unicode(art.content),
                similar.get_unicode(article['fulltext']))
            if ratio >= 80:
                art.fulltext = article['fulltext']
                art.save()
    except:
        pass


def index_articles(articles_list):
    for article in articles_list:
        if not article:
            continue

        index = article.__class__.__name__.lower()
        ArticleModel = generate_model(index, "article")

        if ArticleModel.objects.filter(hash_key=article.hash_key).exists():
            logger.info('[index][skipped] ' + article.link)
            continue

        art = scrape_article(article)
        update_fulltext(art)
        conn.index(art, index, 'article')


def update_headlines():
    headlines('NewsArticle')
    headlines('SportsArticle')
    headlines('FinanceArticle')
    headlines('EntertainmentArticle')
    headlines('INewsArticle')
    headlines('ISportsArticle')


def headlines(tag, limit=200):
    def date_parser(obj):
        import datetime
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return obj

    model = get_model('newsconnector', tag)
    articles = model.objects.filter(
        main=True,
        date__gte=datetime.now()-timedelta(hours=24)
    ).order_by('-date')[:limit]

    try:
        for his in articles:
            his['similar'] = [
                similar.prepare_es_dto(a) for a in his['similar']
            ]
            his['similar'] = sorted(
                his['similar'], key=lambda s: s['date'], reverse=True)
    except:
        utils.print_exception()

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    h = [utils.from_es_dict_dto(a) for a in articles]
    h = sorted(h, key=lambda a: len(a['similar']), reverse=True)
    r.set('headlines_%s' % tag, json.dumps(h[:5], default=date_parser))
    logger.info('[headlines] %s updated' % tag)
