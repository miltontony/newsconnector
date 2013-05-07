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
    return render(request,
            'read.html',
            {
             'news': store.get_articles('NewsArticle'),
             'sports': store.get_articles('SportsArticle'),
             'finance': store.get_articles('FinanceArticle'),
             'entertainment': store.get_articles('EntertainmentArticle'),
             'featuredNews': store.get_featured_articles('NewsArticle'),
             'featuredSports': store.get_featured_articles('SportsArticle'),
             'featuredFinance': store.get_featured_articles('FinanceArticle'),
             'featuredEntertainment': store.get_featured_articles('EntertainmentArticle'),
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

    if not page:
        return HttpResponse(json.dumps({'error': 'page not selected'}),
                            mimetype='application/json')

    f = TermFilter("tag", tag)
    results = conn.search(Search(filter=f, start=(page - 1) * 20, size=20),\
                        indexes=["newsworld"],
                        sort='date:desc')
    results.count()
    return render(request, 'readmore_articles.html', {'articles': [from_es_dto(a) for a in results]})


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

    f = TermFilter("tag", tag)
    results = conn.search(Search(filter=f, start=(page - 1) * 20, size=40),
                        indexes=["newsworld"],
                        sort='date:desc')
    results.count()
    return HttpResponse(json.dumps({
        'articles': [from_es_dto(a) for a in results],
        'cat': cat,
    },
        mimetype='application/json'
    ))


def related(request, pk):
    f = TermFilter("hash_key", pk)
    s = Search(filter=f, start=0, size=1)
    results = conn.search(s, indexes=["newsworld"])
    articles = None
    article = None
    for r in results:
        article = r
        q = TermsQuery("keywords", r.keywords)
        articles = conn.search(Search(q, start=0, size=11),\
                                indexes=["newsworld"],
                                sort='_score,date:desc')
        break

    n_articles = []

    try:
        if len(list(articles)) > 0:
            max_score = articles[0]._meta.score

            for a in articles:
                if a.hash_key == pk:
                    continue
                a.score = (a._meta.score / max_score) * 100
                n_articles.append(from_es_dto(a))
    except:
        pass

    data = {'articles': n_articles,
            'article': from_es_dto(article)}
    return render(request, 'related.html', data)
