from newsconnector.support.calais import Calais
from newsconnector.models import *
from newsconnector.support.utils import *
from newsconnector.support import similar

from django.utils.hashcompat import md5_constructor
from django.core.cache import cache
from time import mktime
from datetime import datetime, date

from celery.task import task

import feedparser
import lxml.html
from pyes import *
import json
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

SYSTEM_STATE_KEY = 'system_state_key'
TASK_ID_KEY = 'updatefeeds_task_key'

conn = ES('127.0.0.1:9200')

def stop_task():
    from celery import current_app as celery
    task_id = r.get(TASK_ID_KEY)
    if task_id:
        celery.control.revoke(task_id, terminate=True, signal='SIGKILL')

def must_start_update():
    if not cache.get(SYSTEM_STATE_KEY):
        stop_task()
        cache.set(SYSTEM_STATE_KEY, 1, 1800)
        return True
    return False


@task(ignore_result=True)
def update_feeds():
    if not must_start_update():
        return
    r.set(TASK_ID_KEY, update_feeds.request.id)

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
    update_articles_view_cache('NewsArticle')
    similar.build('NewsArticle')

    run_tasks(sports_feeds, SportsArticle)
    update_articles_view_cache('SportsArticle')
    similar.build('SportsArticle')

    run_tasks(fin_feeds, FinanceArticle)
    update_articles_view_cache('FinanceArticle')
    similar.build('FinanceArticle')

    run_tasks(e_feeds, EntertainmentArticle)
    update_articles_view_cache('EntertainmentArticle')
    similar.build('EntertainmentArticle')

    run_tasks(inews_feeds, INewsArticle)
    update_articles_view_cache('INewsArticle')
    similar.build('INewsArticle')

    run_tasks(isports_feeds, ISportsArticle)
    update_articles_view_cache('ISportsArticle')
    similar.build('ISportsArticle')


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
    print '-- Update Started: %s --' % feedModel.__name__
    print 'Fetching RSS feeds.'
    new_articles = get_new_articles(feeds, feedModel)

    try:
        update_articles(new_articles)
        print 'Article update complete.'
        print '-- Update Complete --'
    except:
        rollback_articles(new_articles, feedModel)
        print 'Rolling back: %s (%s)' % (feedModel.__name__,
                                         len(list(new_articles)))
        print_exception()

    conn.refresh()


def get_new_articles(feeds, feedModel):
    for feed, source in feeds:
        for entry in feedparser.parse(feed).entries:
            yield get_instance(feedModel, entry, source)


def update_articles(articles_list):
    for art in articles_list:
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


def from_es_dto(obj):
    from django.template.defaultfilters import truncatewords

    return {'title': obj.title,
            'score': obj.score,
            'link': obj.link,
            'content': truncatewords(obj.content, 50),
            'source': obj.source,
            'image_url': obj.image_url,
            'hash_key': obj.hash_key,
            'date': obj.date.isoformat(),
            'keywords': obj.keywords}


def update_articles_view_cache(tag):
    try:
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        articles = get_articles(tag)
        featuredNews = get_featured_articles(articles)
        r.set(tag, json.dumps([from_es_dto(a) for a in articles]))
        r.set('featured_%s' % tag, json.dumps(featuredNews))
    except:
        print_exception()


def get_articles(tag):
    min = date.today() - timedelta(days=1)
    max = date.today() + timedelta(days=1)

    q = FilteredQuery(TermFilter("tag", tag),
            RangeFilter(qrange=ESRange('date',
                min, max, include_upper=False)))
    f = Search(query=q, start=0, size=20)
    f.facet.add_term_facet('keywords', size=50)
    r = conn.search(f, indexes=["newsworld"], sort='date:desc')

    alt_q = FilteredQuery(TermFilter("tag", tag),
            RangeFilter(qrange=ESRange('date')))
    alt_f = Search(query=alt_q, start=0, size=20)
    alt_f.facet.add_term_facet('keywords', size=50)
    alt_r = conn.search(alt_f, indexes=["newsworld"], sort='date:desc')

    return r or alt_r


def get_featured_articles(resultset):
    bucket = []
    ignore_terms = ['politics', 'south africa', 'social issues',\
                    'human interest', 'year of birth missing', 'state media',\
                    'president', 'environment', 'the sunday times',\
                    'weather', 'international relations', 'education',
                    'sports', 'tennis', 'geography', 'mass media', 'labor',\
                    'singers', 'usd', 'Business_Finance',\
                    'Disaster_Accident', 'Education', 'Entertainment_Culture',\
                    'Environment', 'Health_Medical_Pharma',\
                    'Hospitality_Recreation', 'Human Interest', 'Labor',\
                    'Law_Crime', 'Politics', 'Religion_Belief',\
                    'Social Issues', 'Sports', 'Technology_Internet',\
                    'Weather', 'War_Conflict', 'Other', 'Television',\
                    'Music']

    terms = [t for t in resultset.facets.keywords.terms\
                if t['term'].lower() not in [a.lower() for a in ignore_terms]\
                    and 'people' not in t['term'].lower()\
                    and 'television' not in t['term'].lower()\
                    and 'geography' not in t['term'].lower()]

    seen = []
    for k in terms:
        f = TermFilter("keyword", k['term'])
        articles = conn.search(Search(filter=f, start=0, size=10),\
                            indexes=["newsworld"],
                            sort='date:desc')
        if any(articles):
            feature = {'keyword': k['term'],
                            'articles': [from_es_dto(a)\
                                            for a in articles[:5]\
                                                if a]
                        }
            found = False
            for x in feature['articles']:
                if x['hash_key'] in seen:
                    found = True
                    break
            if not found:
                bucket.append(feature)
                seen += [y['hash_key'] for y in feature['articles']]

    #TODO:remove articles that appear in multiple buckets
    return bucket[:5]
