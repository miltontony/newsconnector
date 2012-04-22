from datetime import date, timedelta, datetime
import networkx as nx

import re
from django.db.models import Q

def found_string(str1, str2):
    return ' ' + str1 + ' ' in ' ' + str2 + ' '

def get_min_date(min_date):
    min = datetime.fromtimestamp(int(min_date)/1000.0).date()
    min = datetime(min.year, min.month, min.day, 0, 0, 0)
    return min

def get_max_date(max_date):
    max = datetime.fromtimestamp(int(max_date)/1000.0).date()
    max = datetime(max.year, max.month, max.day, 23, 59, 59)
    return max

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

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query