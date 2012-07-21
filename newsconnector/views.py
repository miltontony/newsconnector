from django.shortcuts import render,  redirect
from operator import itemgetter, attrgetter

from newsconnector.models import *
from newsconnector.support.utils import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

import json
from django.http import HttpResponse

from datetime import date, timedelta, datetime

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

    q1 = TextQuery("content", q, boost=2.0, operator='or')
    q2 = TextQuery("title", q, boost=1.8, operator='or')
    q3 = TextQuery("keyword", q, operator='or')
    query = BoolQuery(should=[q1, q2, q3])
    results = conn.search(Search(query=query, start=0, size=10),\
                            indexes=["newsworld"], sort='_score,date:desc')

    return render(request, 'browse.html',
                            {'sites': RssFeed.objects.all().distinct('name'),
                            'q': q,
                            'news': results,
                            })


def news(request):
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday if datetime.now().hour < 13\
                                    or datetime.now().weekday() > 4\
                                 else date.today()

    return render(request, 'index.html',
                           {'min_date': min_date,
                            'default_min_date': default_min_date,
                            'sites': NewsFeed.objects.all(),
                            'title': 'LATEST NEWS',
                            'id': 1,
                            'latest': NewsArticle.objects\
                                                 .all()\
                                                 .order_by('-date')[:10]})


def sports(request):
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday

    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': SportsFeed.objects.all(),
                                          'title': 'LATEST SPORTS NEWS',
                                          'id': 2,
                                          'latest': SportsArticle
                                                    .objects.all()
                                                    .order_by('-date')[:10]})


def finance(request):
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday

    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': FinanceFeed.objects.all(),
                                          'title': 'LATEST FINANCIAL NEWS',
                                          'id': 3,
                                          'latest': FinanceArticle.objects.all().order_by('-date')[:10]})

def entertainment(request):
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday

    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': EntertainmentFeed.objects.all(),
                                          'title': 'LATEST GOSSIP',
                                          'id': 4,
                                          'latest': EntertainmentArticle.objects.all().order_by('-date')[:10]})

def get_featured_articles(keywordModel):
    return keywordModel.objects.filter(date_updated__gte=date.today())\
                                      .annotate(count=Count('article'))\
                                      .order_by('-count')[:5]

def get_articles(tag):
    f = TermFilter("tag", tag)
    results = conn.search(Search(filter=f, start=0, size=10),\
                        indexes = ["newsworld"],
                        sort='date:desc')
    return [from_es_dto(a) for a in results]

def read(request):
    return render(request, 'read.html', {'sites': RssFeed.objects.all().distinct('name'),
                                         'news': get_articles('NewsArticle'),
                                         'sports': get_articles('SportsArticle'),
                                         'finance': get_articles('FinanceArticle'),
                                         'entertainment': get_articles('EntertainmentArticle'),
                                         'featuredNews': build_related(NewsArticle),
                                         'featuredSports': build_related(SportsArticle),
                                         'featuredFinance': build_related(FinanceArticle),
                                         'featuredEntertainment': build_related(EntertainmentArticle),
                                         })

def read_more(request, tag):
    page = int(request.GET.get('page', 1))

    if not page:
        return HttpResponse(json.dumps({'error': 'page not selected'}),
                            mimetype='application/json')

    f = TermFilter("tag", tag)
    results = conn.search(Search(filter=f, start=(page - 1) * 10, size=10),\
                        indexes = ["newsworld"],
                        sort='date:desc')
    results.count()
    data = json.dumps({'articles': [from_es_dto(a) for a in results],
                       'has_next': True,
                       'next_page': page + 1})

    return HttpResponse(data, mimetype='application/json')

def related(request, pk):
    f = TermFilter("hash_key", pk)
    results = conn.search(Search(filter=f, start=0, size=1), indexes = ["newsworld"])
    articles = None
    article = None
    for r in results:
        article = r
        q = TermsQuery("keywords", r.keywords)
        articles = conn.search(Search(q, start=0, size=11),\
                                indexes = ["newsworld"],
                                sort='_score,date:desc')
        break

    n_articles = []

    if len(list(articles)) > 0:
        max_score = articles[0]._meta.score

        for a in articles:
            if a.hash_key == pk:
                continue
            a.score = (a._meta.score / max_score) * 100
            n_articles.append(from_es_dto(a))

    data = {'articles': n_articles,
            'article': from_es_dto(article)}
    return render(request, 'related.html', data)
