import redis
import json
from datetime import datetime


def update_date(obj):
    obj['date'] = datetime.strptime(obj['date'], 'YYYY-MM-DDTHH:MM:SS')
    return obj


def get_articles(tag):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    articles = r.get(tag)
    j_articles = json.loads(articles) if articles else None
    return [update_date(a) for a in j_articles]


def get_featured_articles(tag):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    articles = r.get('featured_%s' % tag)
    j_articles = json.loads(articles) if articles else None
    return [update_date(a) for a in j_articles]
