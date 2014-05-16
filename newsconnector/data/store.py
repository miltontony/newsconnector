from datetime import datetime, timedelta
from django.db.models.loading import get_model
from django.db.models import Count


def get_articles(tag, limit=20, start=0):
    model = get_model('newsconnector', tag)
    return model.objects.filter(main=True).order_by('-date')[start:limit]


def get_headlines(tag, limit=5):
    model = get_model('newsconnector', tag)
    articles = model.objects.filter(
        date__gte=datetime.now()-timedelta(days=1)
    ).annotate(headlines=Count('similar')).order_by('-headlines')
    return articles[:limit]


def update_date(obj):
    if not isinstance(obj['date'], datetime):
        obj['date'] = datetime.strptime(obj['date'], "%Y-%m-%dT%H:%M:%S")
    return obj
