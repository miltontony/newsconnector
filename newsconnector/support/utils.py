import unicodedata
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


def clean(txt):
    return unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore')


def get_positive_words(url):
    if url.startswith('http://www.news24.com'):
        return ['article', 'col626']
    return None


def scrape(url):
    from goose import Goose
    from readability.readability import Document
    import urllib2
    ua = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    req = urllib2.Request(url, headers={
        'User-Agent': ua,
        'Accept-Encoding': 'identity',
    })
    page = unicode(urllib2.urlopen(req).read(), errors='ignore')

    pos = get_positive_words(url)
    if pos:
        html = Document(page, positive_keywords=pos).summary()
    else:
        html = Document(page).summary()
    return Goose().extract(raw_html=html).cleaned_text


def from_es_dto(obj):
    from django.template.defaultfilters import truncatewords

    return {'title': clean(obj.title),
            'score': obj.score,
            'link': obj.link,
            'content': truncatewords(clean(obj.content), 50),
            'source': obj.source,
            'fulltext': clean(obj.fulltext) or '' if hasattr(obj, 'fulltext') else '',
            'image_url': obj.image_url,
            'hash_key': obj.hash_key,
            'date': obj.date,
            'date_iso': obj.date.isoformat(),
            'keywords': obj.keywords,
            'similar': obj.similar or [] if hasattr(obj, 'similar') else [],
            'seen': obj.seen or [] if hasattr(obj, 'seen') else [],
            }


def from_es_dict_dto(obj, strip_similar=False):
    def prepare_dict_article(obj, strip_similar=False):
        from django.template.defaultfilters import truncatewords

        return {'title': clean(obj.get('title')),
                'score': obj.get('score'),
                'link': obj.get('link'),
                'main': obj.get('main', False),
                'content': truncatewords(clean(obj.get('content')), 50),
                'source': obj.get('source'),
                'fulltext': clean(obj.get('fulltext', '')),
                'image_url': obj.get('image_url'),
                'hash_key': obj.get('hash_key'),
                'date': obj.get('date'),
                'date_iso': obj.get('date').isoformat(),
                'keywords': obj.get('keywords'),
                'seen': obj.get('seen', []),
                'similar': obj.get('similar') or [] if not strip_similar else [],
                }
    obj = prepare_dict_article(obj, strip_similar)
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
    exc_type, exc_value = sys.exc_info()[:2]
    logger.error(exc_value, exc_info=True)
