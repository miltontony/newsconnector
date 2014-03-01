import redis
import json
from datetime import datetime


def update_date(obj):
    obj['date'] = datetime.strptime(obj['date_iso'][:19], '%Y-%m-%dT%H:%M:%S')
    return obj


def get_articles(tag):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    articles = r.get('similar_%s' % tag)
    return [update_date(a) for a in json.loads(articles) if a]


def get_headlines(tag):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    articles = r.get('headlines_%s' % tag)
    return [update_date(a) for a in json.loads(articles) if a]
