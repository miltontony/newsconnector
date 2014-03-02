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


@login_required
def delete_keyword(request, pk):
    if(request.user.is_staff):
        keyword = get_object_or_404(Keyword, pk=pk)
        keyword.delete()
        redirect_url = request.GET.get('next', '/')
        return redirect(redirect_url)
    return redirect('/')


def search(request, articleModel=Article):
    q = request.GET.get('q', None)

    if not q or not q.strip():
        return redirect('/')

    q1 = TextQuery("content", q, operator='or')
    q2 = TextQuery("title", q, operator='or')
    q3 = TextQuery("keyword", q, boost=0.5, operator='or')
    query = BoolQuery(should=[q1, q2, q3])
    results = conn.search(Search(query=query, start=0, size=20),\
                            indexes=["newsworld"], sort='date:desc,_score')

    return render(request, 'browse.html',
                            {'sites': RssFeed.objects.all().distinct('name'),
                            'q': q,
                            'news': [from_es_dto(a) for a in results],
                            })


def featured_articles(tag):
    return get_featured_articles(get_articles(tag))


def read(request):
    print store.get_articles('NewsArticle')[0]
    return render(
        request,
        'read.html',
        {
            'news': store.get_articles('NewsArticle')[:20],
            'sports': store.get_articles('SportsArticle')[:20],
            'finance': store.get_articles('FinanceArticle')[:20],
            'entertainment': store.get_articles('EntertainmentArticle')[:20],
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
    })

    return HttpResponse(data, mimetype='application/json')


def read_more(request, tag):
    page = int(request.GET.get('page', 1))

    start = (page - 1) * 40
    stop = page * 40

    articles = store.get_articles(tag)[start:stop]

    if not page:
        return HttpResponse(json.dumps({'error': 'page not selected'}),
                            mimetype='application/json')

    return render(request, 'readmore_articles.html', {'articles': articles})
