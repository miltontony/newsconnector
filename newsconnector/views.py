from django.shortcuts import render,  redirect
from django.core.urlresolvers import reverse
from newsconnector.tasks import run_tasks
from newsconnector.models import Article, Keyword
#from newsconnector.graphing.models import GraphArticle, GraphKeyword
import json

from datetime import date, timedelta
import networkx as nx

def cron(request):
    #Article.objects.all().delete()
    
    feeds = [('http://feeds.news24.com/articles/news24/SouthAfrica/rss', 'news24.com'),
             ('http://www.timeslive.co.za/?service=rss', 'timeslive.co.za'),
             ('http://feeds.iol.co.za/rss/feed_southafrica.rss', 'iol.co.za'),
             ('http://www.ewn.co.za/Feeds/Local.aspx', 'ewn.co.za'),
             ('http://mg.co.za/rss/national', 'mg.co.za'),
             ]
    result = run_tasks.delay(feeds)
    return render(request, 'cron.html')

def index(request):             
    d = date.today()-timedelta(days=3)
    articles = Article.objects.all()
    
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
                  '$dim': 20 + len(nbrs.items()),
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
            } for k,nbrs in graph.adjacency_iter() if hasattr(k, 'keyword') and len(nbrs.items()) > 5]
           }

    return render(request, 'plain.html', {'data': json.dumps(tree)})

def found_string(str1, str2):
    return ' ' + str1 + ' ' in ' ' + str2 + ' '