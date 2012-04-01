from django.shortcuts import render,  redirect
from django.core.urlresolvers import reverse
from newsconnector.models import Article, Keyword
from django.db.models import Min
from django.http import HttpResponse

import json

from datetime import date, timedelta, datetime

import networkx as nx

def get_data(request, min_date=None, max_date=None):
    min = datetime.fromtimestamp(int(min_date)/1000.0).date()
    max = datetime.fromtimestamp(int(max_date)/1000.0).date()
        
    min = datetime(min.year, min.month, min.day, 0, 0, 0)
    max = datetime(max.year, max.month, max.day, 23, 59, 59)
    print max
    
    data = json.dumps(build_data(min, max))
    return HttpResponse(data, mimetype='application/json')

def build_data(min_date, max_date):
    articles = Article.objects.filter(date__gte = min_date, date__lte = max_date)
    
    graph = nx.DiGraph()
    
    for word in Keyword.objects.all():
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
                  },
                'children': [{'id': 'a_%s' % a.pk, 
                             'name': a.title + ' [' + a.source +']', 
                             'children': [], 
                             'data': {'description': a.content,
                                      'link': a.link,
                                      'title': a.title,
                                      'id': a.pk,
                                      'source': a.source,
                                      }
                            } for a, nattr in nbrs.items()]
            } for k,nbrs in graph.adjacency_iter() if hasattr(k, 'keyword') and len(nbrs.items()) > 3]
           }
    return tree

def index(request):    
    min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    default_min_date = date.today() - timedelta(days=3)
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date if min_date <= default_min_date else min_date})

def found_string(str1, str2):
    return ' ' + str1 + ' ' in ' ' + str2 + ' '