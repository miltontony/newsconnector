from datetime import date, timedelta, datetime


def found_string(str1, str2):
    return ' ' + str1 + ' ' in ' ' + str2 + ' '


def get_min_date(min_date):
    min = datetime.fromtimestamp(int(min_date) / 1000.0).date()
    min = datetime(min.year, min.month, min.day, 0, 0, 0)
    return min


def get_max_date(max_date):
    max = datetime.fromtimestamp(int(max_date) / 1000.0).date()
    max = datetime(max.year, max.month, max.day, 23, 59, 59)
    return max


def delete_old_data():
    from newsconnector.models import Article, Keyword

    d = date.today() - timedelta(days=31)

    print 'Articles: %s' % Article.objects.all().count()
    print 'keywords: %s' % Keyword.objects.all().count()

    Article.objects.filter(date_added__lt=d).delete()
    Keyword.objects.filter(date_updated__lt=d).delete()

    print 'Articles remaining: %s' % Article.objects.all().count()
    print 'keywords remaining: %s' % Keyword.objects.all().count()


def scrape(url):
    from goose import Goose
    from readability.readability import Document
    import urllib2
    ua = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    req = urllib2.Request(url, headers={
        'User-Agent': ua,
        'Accept-Encoding': 'identity',
    })
    page = urllib2.urlopen(req).read()
    html = Document(page).summary()
    return Goose().extract(raw_html=html).cleaned_text


def from_es_dto(obj):
    from django.utils.timesince import timesince
    from django.template.defaultfilters import truncatewords

    return {'title': obj.title,
            'score': obj.score,
            'link': obj.link,
            'content': truncatewords(obj.content, 50),
            'source': obj.source,
            'fulltext': obj.fulltext if hasattr(obj, 'fulltext') else '',
            'image_url': obj.image_url,
            'hash_key': obj.hash_key,
            'date': '%s ago' % timesince(obj.date),
            'date_iso': obj.date.isoformat(),
            'keywords': obj.keywords,
            'similar': [],
            'seen': [],
            }


def prepare_es_dto(obj):
    obj['similar'] = []
    obj['seen'] = []
    if not 'date_iso' in obj:
        obj['date_iso'] = obj['date'].isoformat()
    elif isinstance(obj['date_iso'], datetime):
        obj['date_iso'] = obj['date_iso'].isoformat()

    if not 'fulltext' in obj:
        obj['fulltext'] = None
    return obj


def from_es_dict_dto(obj, prepare_dict_article=False):
    def prepare_dict_article(obj, strip_similar=False):
        from django.utils.timesince import timesince
        from django.template.defaultfilters import truncatewords

        return {'title': obj.get('title'),
                'score': obj.get('score'),
                'link': obj.get('link'),
                'content': truncatewords(obj.get('content'), 50),
                'source': obj.get('source'),
                'fulltext': obj.get('fulltext', ''),
                'image_url': obj.get('image_url'),
                'hash_key': obj.get('hash_key'),
                'date': '%s ago' % timesince(obj.get('date')),
                'date_iso': obj.get('date').isoformat(),
                'keywords': obj.get('keywords'),
                'seen': obj.get('seen', []),
                'similar': obj.get('similar', []) if strip_similar else [],
                }
    obj = prepare_dict_article(obj, prepare_dict_article)
    obj['similar'] = [
        prepare_dict_article(s, True)
        for s in obj.get('similar', [])
    ]
    return obj


from raven.conf import setup_logging
from raven.contrib.django.raven_compat.handlers import SentryHandler
setup_logging(SentryHandler())
import sys
import logging
logger = logging.getLogger(__name__)


def print_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logger.error(exc_value, exc_info=True)
