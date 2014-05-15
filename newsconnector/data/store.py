from datetime import datetime
import json
import redis
#from pyes import ES
#conn = ES('127.0.0.1:9200')
#from pyes.queryset import generate_model
#ArticleModel = generate_model("newsworld", "article")
from django.db.models.loading import get_model


def get_articles(tag, limit=20, start=0):
    model = get_model('newsconnector', tag)
    return model.objects.filter(main=True).order_by('-date')[start:limit]


def get_headlines(tag, limit=20):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    articles = r.get('headlines_%s' % tag)
    return [update_date(a) for a in json.loads(articles)[:limit]]


def update_date(obj):
    if not isinstance(obj['date'], datetime):
        obj['date'] = datetime.strptime(obj['date'], "%Y-%m-%dT%H:%M:%S")
    return obj
