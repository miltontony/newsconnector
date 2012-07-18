from pyes import *
from newsconnector.models import *
from datetime import date, timedelta, datetime


conn = ES('127.0.0.1:9200')


def setup():
    #conn = ES('127.0.0.1:9200')
    try:
        conn.delete_index('newsworld')
    except:
        pass

    conn.create_index("newsworld")
    conn.default_indices = ["newsworld"]

    mapping = {u'hash_key': {'index': 'not_analyzed',
                          'store': 'yes',
                          'type': u'string'},
              u'tag': {'index': 'not_analyzed',
                          'store': 'yes',
                          'type': u'string'},
              u'title': {'index': 'analyzed',
                         'type': u'string',
                         "term_vector": "with_positions_offsets"},
              u'content': {'index': 'analyzed',
                         'type': u'string',
                         "term_vector": "with_positions_offsets"},
              u'keywords': {'index': 'analyzed',
                         'index_name': 'keyword',
                         'type': u'string'},
              u'link': {'index': 'no',
                         'store': 'yes',
                         'type': u'string'},
              u'image_url': {'index': 'no',
                         'store': 'yes',
                         'type': u'string'},
              u'date': {'store': 'yes',
                         'type': u'date'},
              u'date_added': {'store': 'no',
                         'type': u'date'},
              u'source': {'index': 'not_analyzed',
                         'store': 'yes',
                         'type': u'string'}}

    conn.put_mapping("article", {'properties': mapping})

    d = date.today() - timedelta(days=7)
    print '0%'
    for a in NewsArticle.objects.filter(date__gte=d).order_by('-date'):
        conn.index(a.to_json(), 'newsworld', 'article')
    conn.refresh()
    print '25%'

    for a in SportsArticle.objects.filter(date__gte=d).order_by('-date'):
        conn.index(a.to_json(), 'newsworld', 'article')
    conn.refresh()
    print '50%'

    for a in FinanceArticle.objects.filter(date__gte=d).order_by('-date'):
        conn.index(a.to_json(), 'newsworld', 'article')
    conn.refresh()
    print '75%'

    for a in EntertainmentArticle.objects.filter(date__gte=d).order_by('-date'):
        conn.index(a.to_json(), 'newsworld', 'article')
    conn.refresh()
    print '100%'
