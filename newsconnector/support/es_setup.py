from datetime import datetime, timedelta
from pyes import ES
from pyes.queryset import generate_model
ArticleModel = generate_model("newsworld", "article")

from newsconnector.models import (
    Article, NewsArticle, FinanceArticle, EntertainmentArticle, SportsArticle,
    INewsArticle, ISportsArticle
)


conn = ES('127.0.0.1:9200')


def setup():
    #conn = ES('127.0.0.1:9200')
    try:
        conn.delete_index('newsworld')
    except:
        pass

    conn.create_index("newsworld")
    conn.default_indices = ["newsworld"]

    mapping = {
        u'hash_key': {
            'index': 'not_analyzed',
            'store': 'yes',
            'type': u'string'},
        u'tag': {
            'index': 'not_analyzed',
            'store': 'yes',
            'type': u'string'},
        u'title': {
            'index': 'analyzed',
            'type': u'string',
            "term_vector": "with_positions_offsets"},
        u'fulltext': {
            'index': 'analyzed',
            'type': u'string',
            "term_vector": "with_positions_offsets"},
        u'content': {
            'index': 'analyzed',
            'type': u'string',
            "term_vector": "with_positions_offsets"},
        u'link': {
            'index': 'no',
            'store': 'no',
            'type': u'string'},
        u'image_url': {
            'index': 'no',
            'store': 'no',
            'type': u'string'},
        u'date': {
            'store': 'yes',
            'type': u'date'},
        u'date_added': {
            'store': 'yes',
            'type': u'date'},
        u'source': {
            'index': 'no',
            'store': 'no',
            'type': u'string'}
    }

    conn.put_mapping("article", {'properties': mapping})
    conn.refresh()


def init():
    print '0%'
    for a in NewsArticle.objects.all():
        conn.index(a.to_json(), 'newsworld', 'article')
    conn.refresh()
    print '25%'

    for a in SportsArticle.objects.all():
        conn.index(a.to_json(), 'newsworld', 'article')
    conn.refresh()
    print '50%'

    for a in FinanceArticle.objects.all():
        conn.index(a.to_json(), 'newsworld', 'article')
    conn.refresh()
    print '75%'

    for a in EntertainmentArticle.objects.all():
        conn.index(a.to_json(), 'newsworld', 'article')
    conn.refresh()
    print '100%'


def backup():
    d = datetime.now() - timedelta(days=40)
    print '--- Backup started ---'
    Article.objects.all().delete()

    print 'Backing up NewsArticle'
    for a in ArticleModel.objects.filter(tag='NewsArticle', date__gte=d):
        NewsArticle.from_es(a)
    print 'Total: %s' % str(NewsArticle.objects.all().count())

    print 'Backing up SportsArticle'
    for a in ArticleModel.objects.filter(tag='SportsArticle', date__gte=d):
        SportsArticle.from_es(a)
    print 'Total: %s' % str(SportsArticle.objects.all().count())

    print 'Backing up FinanceArticle'
    for a in ArticleModel.objects.filter(tag='FinanceArticle', date__gte=d):
        FinanceArticle.from_es(a)
    print 'Total: %s' % str(FinanceArticle.objects.all().count())

    print 'Backing up EntertainmentArticle'
    for a in ArticleModel.objects.filter(tag='EntertainmentArticle', date__gte=d):
        EntertainmentArticle.from_es(a)
    print 'Total: %s' % str(EntertainmentArticle.objects.all().count())

    print 'Backing up INewsArticle'
    for a in ArticleModel.objects.filter(tag='INewsArticle', date__gte=d):
        INewsArticle.from_es(a)
    print 'Total: %s' % str(INewsArticle.objects.all().count())

    print 'Backing up ISportsArticle'
    for a in ArticleModel.objects.filter(tag='ISportsArticle', date__gte=d):
        ISportsArticle.from_es(a)
    print 'Total: %s' % str(ISportsArticle.objects.all().count())

    print '--- Backup complete ---'
