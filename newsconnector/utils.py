from datetime import date, timedelta, datetime
import networkx as nx

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
