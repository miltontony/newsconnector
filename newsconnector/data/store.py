import redis
import json


def get_articles(tag):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    articles = r.get(tag)
    return json.loads(articles) if articles else None


def get_featured_articles(tag):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    articles = r.get('featured_%s' % tag)
    return json.loads(articles) if articles else None
