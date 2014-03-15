import redis
import json
from datetime import datetime
from pyes.queryset import generate_model
from pyes import ES
conn = ES('127.0.0.1:9200')
ArticleModel = generate_model("newsworld", "article")


def update_date(obj):
    obj['date'] = datetime.strptime(obj['date_iso'][:19], '%Y-%m-%dT%H:%M:%S')
    return obj


def get_articles(tag, limit=20, start=0):
    conn.indices.refresh('newsworld')
    return ArticleModel.objects.filter(
        tag=tag.lower()).order_by('-date')[start:limit]


def get_headlines(tag, limit=20):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    articles = r.get('headlines_%s' % tag)
    return [update_date(a) for a in json.loads(articles) if a][:limit]
