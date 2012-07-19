from newsconnector.support.calais import Calais
from newsconnector.support.utils import build_related
from newsconnector.models import *
from django.db import IntegrityError
from django.utils.hashcompat import md5_constructor
from time import mktime
from datetime import datetime

from celery.task import task

import feedparser
import lxml.html
from lxml import etree
from pyes import *


conn = ES('127.0.0.1:9200')

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

    except etree.ParseError:
        pass
    except TypeError:
        pass
    except IntegrityError:
        pass

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

    conn.refresh()
