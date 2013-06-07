from django.http import HttpResponse
from newsconnector.data import store
import json
from datetime import datetime


def api_read_more(request, tag):
    page = int(request.GET.get('page', 1))

    cat = 1
    if tag == 'NewsArticle':
        cat = 1
    elif tag == 'SportsArticle':
        cat = 2
    elif tag == 'FinanceArticle':
        cat = 3
    else:
        cat = 4

    limit = (page - 1) * 40

    articles = store.get_hashed_articles(tag)[limit:]

    return HttpResponse(json.dumps({
        'articles': [update_date(a) for a in articles],
        'cat': cat,
    }),
        mimetype='application/json'
    )


def api_get_headlines(request, tag):
    cat = 1
    if tag == 'NewsArticle':
        cat = 1
    elif tag == 'SportsArticle':
        cat = 2
    elif tag == 'FinanceArticle':
        cat = 3
    else:
        cat = 4

    articles = store.get_headlines(tag)

    return HttpResponse(json.dumps({
        'articles': [update_date(a) for a in articles],
        'cat': cat,
    }),
        mimetype='application/json'
    )


def api_get_all_headlines(request):
    news = store.get_headlines('NewsArticle')[:3]
    sports = store.get_headlines('SportsArticle')[:3]
    finance = store.get_headlines('FinanceArticle')[:3]
    entertainment = store.get_headlines('EntertainmentArticle')[:3]

    return HttpResponse(json.dumps({
        'news': [update_date(a) for a in news],
        'sports': [update_date(a) for a in sports],
        'finance': [update_date(a) for a in finance],
        'entertainment': [update_date(a) for a in entertainment],
    }),
        mimetype='application/json'
    )


def update_date(obj):
    from django.utils.timesince import timesince
    d = datetime.strptime(obj['date_iso'][:19], '%Y-%m-%dT%H:%M:%S')
    obj['date'] = '%s ago' % timesince(d)
    return obj
