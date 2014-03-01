from django.http import HttpResponse
from newsconnector.data import store
import json
from datetime import datetime


def parse_tag(tag):
    cat = 1
    if tag == 'NewsArticle':
        cat = 1
    elif tag == 'SportsArticle':
        cat = 2
    elif tag == 'FinanceArticle':
        cat = 3
    elif tag == 'EntertainmentArticle':
        cat = 4
    elif tag == 'INewsArticle':
        cat = 5
    elif tag == 'ISportsArticle':
        cat = 6
    else:
        raise Exception('Invalid article tag')
    return cat


def articles(request, tag):
    page = int(request.GET.get('page', 1))

    cat = parse_tag(tag)

    start = (page - 1) * 40
    stop = page * 40

    articles = store.get_articles(tag)[start:stop]

    return HttpResponse(json.dumps({
        'articles': [update_date(a) for a in articles],
        'cat': cat,
    }),
        mimetype='application/json'
    )


def headlines(request, tag):
    cat = parse_tag(tag)

    articles = store.get_headlines(tag)

    return HttpResponse(json.dumps({
        'articles': [update_date(a) for a in articles],
        'cat': cat,
    }),
        mimetype='application/json'
    )


def headlines_all(request):
    news = store.get_headlines('NewsArticle')[:3]
    sports = store.get_headlines('SportsArticle')[:3]
    finance = store.get_headlines('FinanceArticle')[:3]
    entertainment = store.get_headlines('EntertainmentArticle')[:3]

    return HttpResponse(json.dumps({
        'news': [update_date(a) for a in news],
        'sports': [update_date(a) for a in sports],
        'finance': [update_date(a) for a in finance],
        'entertainment': [update_date(a) for a in entertainment if a['hash_key'] != '8ad2589bccbe0418a4d57b5fc3e99fd3'],
    }),
        mimetype='application/json'
    )


def iheadlines_all(request):
    news = store.get_headlines('INewsArticle')[:3]
    sports = store.get_headlines('ISportsArticle')[:3]
    entertainment = store.get_headlines('EntertainmentArticle')[:3]

    return HttpResponse(json.dumps({
        'news': [update_date(a) for a in news],
        'sports': [update_date(a) for a in sports],
        'entertainment': [update_date(a) for a in entertainment if a['hash_key'] != '8ad2589bccbe0418a4d57b5fc3e99fd3'],
    }),
        mimetype='application/json'
    )


def update_date(obj):
    from django.utils.timesince import timesince
    d = datetime.strptime(obj['date_iso'][:19], '%Y-%m-%dT%H:%M:%S')
    obj['date'] = '%s ago' % timesince(d)
    return obj
