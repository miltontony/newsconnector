from django.shortcuts import render,  redirect
from django.core.urlresolvers import reverse
from newsconnector.models import *
from django.db.models import Min
from django.http import HttpResponse

import json

from datetime import date, timedelta, datetime

import networkx as nx

def get_min_date(min_date):
    min = datetime.fromtimestamp(int(min_date)/1000.0).date()
    min = datetime(min.year, min.month, min.day, 0, 0, 0)
    return min

def get_max_date(max_date):
    max = datetime.fromtimestamp(int(max_date)/1000.0).date()
    max = datetime(max.year, max.month, max.day, 23, 59, 59)
    return max

def get_data(request, min_date=None, max_date=None):
    data = json.dumps(build_data(get_min_date(min_date), get_max_date(max_date), \
                                 NewsArticle, NewsKeyword))
    return HttpResponse(data, mimetype='application/json')

def get_data_sports(request, min_date=None, max_date=None):
    data = json.dumps(build_data(get_min_date(min_date), get_max_date(max_date), \
                                 SportsArticle, SportsKeyword))
    return HttpResponse(data, mimetype='application/json')

def get_data_finance(request, min_date=None, max_date=None):
    data = json.dumps(build_data(get_min_date(min_date), get_max_date(max_date), \
                                 FinanceArticle, FinanceKeyword))
    return HttpResponse(data, mimetype='application/json')

def get_data_entertainment(request, min_date=None, max_date=None):
    data = json.dumps(build_data(get_min_date(min_date), get_max_date(max_date), \
                                 EntertainmentArticle, EntertainmentKeyword))
    return HttpResponse(data, mimetype='application/json')

def build_data(min_date, max_date, articleModel, keywordModel):
    articles = articleModel.objects\
                .filter(date__gte = min_date, date__lte = max_date)\
                .order_by('-date')
    
    graph = nx.DiGraph()
    
    for word in keywordModel.objects.exclude(keyword='the').distinct():
        for a in articles:
            if found_string(word.keyword, ('%s %s' % (a.title, a.content)).lower()):
                graph.add_edge(word, a)
        
    tree = {
            'id':'main_node',
            'name': 'Latest News',
            'data': [],
            'children':
            [
             {'id': k.pk, 'name': k.keyword, 'data': 
                 {
                  'count': len(nbrs.items()),
                  'articles': [{'id': 'a_%s' % a.pk, 
                             'name': a.title + ' [' + a.source +']', 
                             'children': [], 
                             'data': {'description': a.content,
                                      'link': a.link,
                                      'title': a.title,
                                      'id': a.pk,
                                      'source': a.source,
                                      'date': a.date.strftime('%a, %d %b %H:%M'),
                                      }
                            } for a, nattr in sorted(nbrs.items(), key=lambda x: x[0].date, reverse=True)],
                }
            } for k,nbrs in graph.adjacency_iter() if hasattr(k, 'keyword') and len(nbrs.items()) > 3]
           }
    return tree

def news(request):    
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday if datetime.now().hour < 13 else date.today()
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': NewsFeed.objects.all(),
                                          'title': 'LATEST NEWS',
                                          'latest': NewsArticle.objects.all().order_by('-date')[:10]})

def sports(request):    
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': SportsFeed.objects.all(),
                                          'title': 'LATEST SPORTS NEWS',
                                          'latest': SportsArticle.objects.all().order_by('-date')[:10]})

def finance(request):    
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday if datetime.now().hour < 13 else date.today()
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': FinanceFeed.objects.all(),
                                          'title': 'LATEST FINANCIAL NEWS',
                                          'latest': FinanceArticle.objects.all().order_by('-date')[:10]})

def entertainment(request):    
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday if datetime.now().hour < 13 else date.today()
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': EntertainmentFeed.objects.all(),
                                          'title': 'LATEST GOSSIP',
                                          'latest': EntertainmentArticle.objects.all().order_by('-date')[:10]})

def found_string(str1, str2):
    return ' ' + str1 + ' ' in ' ' + str2 + ' '