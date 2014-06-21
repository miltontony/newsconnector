from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

import json

from newsconnector.models import *
from newsconnector.data import store
from newsconnector.support.utils import *
from pyes import *

conn = ES('127.0.0.1:9200')


def health(request):
    return HttpResponse("")


def date_parser(obj):
    import datetime
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


@login_required
def delete_keyword(request, pk):
    if(request.user.is_staff):
        keyword = get_object_or_404(Keyword, pk=pk)
        keyword.delete()
        redirect_url = request.GET.get('next', '/')
        return redirect(redirect_url)
    return redirect('/')


def featured_articles(tag):
    return get_featured_articles(get_articles(tag))


def read(request):
    return render(
        request,
        'read.html',
        {
            'news': store.get_articles('NewsArticle', 40),
            'sports': store.get_articles('SportsArticle', 40),
            'finance': store.get_articles('FinanceArticle', 40),
            'entertainment': store.get_articles('EntertainmentArticle', 40),
            'featuredNews': store.get_headlines('NewsArticle'),
            'featuredSports': store.get_headlines('SportsArticle'),
            'featuredFinance': store.get_headlines('FinanceArticle'),
            'featuredEntertainment': store.get_headlines('EntertainmentArticle'),
        })


def read_json(request):
    data = json.dumps({
        'news': [from_es_dict_dto(a) for a in store.get_articles('NewsArticle')],
        'sports': [from_es_dict_dto(a) for a in store.get_articles('SportsArticle')],
        'finance': [from_es_dict_dto(a) for a in store.get_articles('FinanceArticle')],
        'entertainment': [from_es_dict_dto(a) for a in store.get_articles('EntertainmentArticle')],
        #'fNews': [from_es_dto(a) for a in store.get_featured_articles('NewsArticle')],
        #'fSports': [from_es_dto(a) for a in store.get_featured_articles('SportsArticle')],
        #'fFinance': [from_es_dto(a) for a in store.get_featured_articles('FinanceArticle')],
        #'fEntertainment': [from_es_dto(a) for a in store.get_featured_articles('EntertainmentArticle')],
    }, default=date_parser)

    return HttpResponse(data, mimetype='application/json')


def read_more(request, tag):
    page = int(request.GET.get('page', 1))

    start = (page - 1) * 40
    stop = page * 40

    articles = store.get_articles(tag, stop, start)

    if not page:
        return HttpResponse(json.dumps(
            {'error': 'page not selected'}, default=date_parser),
            mimetype='application/json')

    return render(request, 'article_block.html', {'articles': articles})
