from datetime import datetime, timedelta
from pyes import ES
from pyes.queryset import generate_model

from newsconnector.models import (
    Article, NewsArticle, FinanceArticle, EntertainmentArticle, SportsArticle,
    INewsArticle, ISportsArticle
)


conn = ES('127.0.0.1:9200')


def delete_index():
    for model in [NewsArticle, FinanceArticle, SportsArticle,
                  EntertainmentArticle, INewsArticle, ISportsArticle]:
        index = model.__name__.lower()
        try:
            conn.indices.delete_index(index)
        except:
            pass

    conn.indices.refresh()


def create_index():
    indices = []
    for model in [NewsArticle, FinanceArticle, SportsArticle,
                  EntertainmentArticle, INewsArticle, ISportsArticle]:
        index = model.__name__.lower()
        conn.indices.create_index(index)
        indices += [index]

    conn.indices.default_indices = indices
    conn.indices.refresh()


def setup():
    conn.indices.refresh()
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
            'type': u'string'},
        u'seen': {
            'index': 'no',
            'store': 'no',
            'type': u'string'},
        u"similar": {
            "properties": {
                "content": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                },
                "date": {
                    "type": "date",
                    "format": "dateOptionalTime",
                    "index": "no",
                    "store": "no",
                },
                "date_iso": {
                    "type": "date",
                    "format": "dateOptionalTime",
                    "index": "no",
                    "store": "no",
                },
                "fulltext": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                },
                "hash_key": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                },
                "image_url": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                },
                "link": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                },
                "main": {
                    "type": "boolean",
                    "index": "no",
                    "store": "no",
                },
                "score": {
                    "type": "long",
                    "index": "no",
                    "store": "no",
                },
                "seen": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                },
                "source": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                },
                "tag": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                },
                "title": {
                    "type": "string",
                    "index": "no",
                    "store": "no",
                }
            }
        }
    }

    conn.indices.put_mapping("article", {
        'properties': mapping,
    })
    conn.indices.refresh()


def init():
    for model in [NewsArticle, FinanceArticle, SportsArticle,
                  EntertainmentArticle, INewsArticle, ISportsArticle]:
        index = model.__name__.lower()
        print 'Started %s' % index
        for a in model.objects.all():
            conn.index(a.to_json(), index, 'article')
        conn.refresh()


def backup():
    d = datetime.now() - timedelta(days=40)
    print '--- Backup started ---'
    print 'Deleting all articles in db: %s' % Article.objects.all().count()
    Article.objects.all().delete()

    for model in [NewsArticle, FinanceArticle, SportsArticle,
                  EntertainmentArticle, INewsArticle, ISportsArticle]:
        model_name = model.__name__
        ArticleModel = generate_model(model_name.lower(), "article")

        print 'Backing up %s' % model.__name__
        for a in ArticleModel.objects.filter(date__gte=d):
            model.from_es(a)
        print 'Total: %s' % str(model.objects.all().count())

    print '--- Backup complete ---'
