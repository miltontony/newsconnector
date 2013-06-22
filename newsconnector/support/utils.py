from datetime import date, timedelta, datetime

import re
from django.db.models import Q


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


def normalize_query(query_string,
          findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
          normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary
    spaces and grouping quoted words together.
    Example:

    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

  '''
    return [normspace(' ', (t[0] or t[1]).strip())\
                for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.

  '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: ' ' + term + ' '})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
    if query is None:
        query = or_query
    else:
        query = query & or_query
    return query


def delete_old_data():
    from newsconnector.models import Article, Keyword

    d = date.today() - timedelta(days=31)

    print 'Articles: %s' % Article.objects.all().count()
    print 'keywords: %s' % Keyword.objects.all().count()

    Article.objects.filter(date_added__lt=d).delete()
    Keyword.objects.filter(date_updated__lt=d).delete()

    print 'Articles remaining: %s' % Article.objects.all().count()
    print 'keywords remaining: %s' % Keyword.objects.all().count()


def from_es_dto(obj):
    from django.utils.timesince import timesince
    from django.template.defaultfilters import truncatewords

    return {'title': obj.title,
            'score': obj.score,
            'link': obj.link,
            'content': truncatewords(obj.content, 50),
            'source': obj.source,
            'image_url': obj.image_url,
            'hash_key': obj.hash_key,
            'date': '%s ago' % timesince(obj.date),
            'date_iso': obj.date.isoformat(),
            'keywords': obj.keywords,
            'similar': [],
            'seen': [],
            }


def from_es_dict_dto(obj):
    from django.utils.timesince import timesince
    from django.template.defaultfilters import truncatewords

    return {'title': obj.get('title'),
            'score': obj.get('score'),
            'link': obj.get('link'),
            'content': truncatewords(obj.get('content'), 50),
            'source': obj.get('source'),
            'image_url': obj.get('image_url'),
            'hash_key': obj.get('hash_key'),
            'date': '%s ago' % timesince(obj.get('date')),
            'keywords': obj.get('keywords')}


def print_exception():
    import sys
    import logging

    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.error(exc_value, exc_info=True)
