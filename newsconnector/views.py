from django.shortcuts import render,  redirect
from operator import itemgetter, attrgetter

from newsconnector.models import *
from newsconnector.support.utils import get_query, build_related
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

import json
from django.http import HttpResponse

from datetime import date, timedelta, datetime


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


def search(request, articleModel = Article):
    q = request.GET.get('q', None)
    found_entries = None
    news_top = None
    news = None
    query_string = None

    if q:
        query_string = q.strip()

        entry_query = get_query(query_string, ['title', 'content', ])

        found_entries = articleModel.objects.filter(entry_query)\
                                            .order_by('-date')

    else:
        found_entries = articleModel.objects.all().order_by('-date')[:10]

    paginator = Paginator(found_entries[4:], 6)
    page = request.GET.get('page', 'none')

    try:
        paged_news = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_news = paginator.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_news = paginator.page(paginator.num_pages)
        page = int(paginator.num_pages)

    news_top = found_entries[:4]
    news = paged_news

    adjacent_pages = 3
    pages = paginator.num_pages
    page_numbers = range(max(1, page - adjacent_pages),\
                         min(pages, page + adjacent_pages) + 1)

    return render(request, 'browse.html',
                            {'sites': RssFeed.objects.all().distinct('name'),
                            'query_string': query_string,
                            'q': q,
                            'news_top': news_top,
                            'news': news,
                            'paged_news': paged_news,
                            'article_count': found_entries.count(),
                            'pages': page_numbers,
                            'show_first': 1 not in page_numbers,
                            'show_last': pages not in page_numbers,
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
                                          'latest': SportsArticle.objects.all().order_by('-date')[:10]})


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

def read(request):
    return render(request, 'read.html', {'sites': RssFeed.objects.all().distinct('name'),
                                         'news': NewsArticle.objects.all().order_by('-date')[:10],
                                         'sports': SportsArticle.objects.all().order_by('-date')[:10],
                                         'finance': FinanceArticle.objects.all().order_by('-date')[:10],
                                         'entertainment': EntertainmentArticle.objects.all().order_by('-date')[:10],
                                         'featuredNews': build_related(NewsArticle),
                                         'featuredSports': build_related(SportsArticle),
                                         'featuredFinance': build_related(FinanceArticle),
                                         'featuredEntertainment': build_related(EntertainmentArticle),
                                         })

def read_more(request, category):
    page = int(request.GET.get('page', None))
    category = int(category)

    if not page:
        return HttpResponse(json.dumps({'error': 'page not selected'}),
                            mimetype='application/json')

    articleModel = NewsArticle

    if category == 2:
        articleModel = SportsArticle
    elif category == 3:
        articleModel = FinanceArticle
    if category == 4:
        articleModel = EntertainmentArticle

    paginator = Paginator(articleModel.objects.all().order_by('-date'), 10)
    page = request.GET.get('page', 'none')

    try:
        paged_news = paginator.page(page)
    except EmptyPage:
        return HttpResponse(json.dumps({'error': 'page not found'}),
                            mimetype='application/json')

    data = json.dumps({'articles': [a.to_dto() for a in paged_news.object_list],
                       'has_next': paged_news.has_next(),
                       'next_page': paged_news.next_page_number()})

    return HttpResponse(data, mimetype='application/json')

def related(request, pk, articleModel=NewsArticle, section_index=1):
    keywords = [i.pk for i in articleModel.objects.get(pk=pk).keywords.all()]
    l = articleModel.objects.filter(keywords__in=keywords)\
                               .exclude(pk=pk)\
                               .distinct('date', 'pk')\
                               .order_by('-date', 'pk')[:20]
    articles = [a.to_related_dto(keywords) for a in l]
    s_articles = sorted(articles, key=itemgetter('rank', 'sdate'), reverse=True)

    data = {'articles': s_articles,
            'article': articleModel.objects.get(pk=pk).to_dto(),
            'section_index': section_index}
    return render(request, 'related.html', data)
