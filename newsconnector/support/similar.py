import json
import redis

from newsconnector.support.utils import print_exception, from_es_dto
from pyes import (ES, TermFilter, TermsQuery, Search, BoolQuery, FilteredQuery,
                  RangeFilter)
from Levenshtein import ratio
from datetime import datetime, date, timedelta
from fuzzywuzzy import fuzz

conn = ES('127.0.0.1:9200')

import logging
logger = logging.getLogger(__name__)


def get_ratio(a, b):
    if not (a and b):
        return 0

    content_ratio = ratio(
        a['content'].encode('ascii', 'ignore'),
        b['content'].encode('ascii', 'ignore')
    )
    text_ratio = ratio(
        a['fulltext'].encode('ascii', 'ignore'),
        b['fulltext'].encode('ascii', 'ignore')
    )
    title_ratio = ratio(
        a['title'].encode('ascii', 'ignore'),
        b['title'].encode('ascii', 'ignore')
    )
    return max(content_ratio, text_ratio, title_ratio)


def get_fuzzy_ratio(art1, art2):
    if not (art1 and art2):
        return 0

    if get_ratio(art1, art2) <= 0.40:
        return 0

    content_ratio = fuzz.token_set_ratio(
        art1['content'].encode('ascii', 'ignore'),
        art2['content'].encode('ascii', 'ignore')
    )
    text_ratio = fuzz.token_set_ratio(
        art1['fulltext'].encode('ascii', 'ignore'),
        art2['fulltext'].encode('ascii', 'ignore')
    )
    return max(content_ratio, text_ratio)


def build_similar(articles):
    history = []
    seen = []
    for a in articles:
        for h in history:
            try:
                sim_ratio = get_fuzzy_ratio(h, a)

                if sim_ratio >= 70 and a['hash_key'] not in h['seen']:
                    a['score'] = sim_ratio
                    a['seen'] = h['hash_key']
                    h['similar'].insert(0, a)
                    h['seen'].append(a['hash_key'])
                    #h = append_related(tag, h, a, 70)
                    seen.append(a['hash_key'])
                    break
                #else:
                #    for s in h['similar']:
                #        sim_ratio = get_fuzzy_ratio(s, a)

                #        if sim_ratio >= 70 and a['hash_key'] not in h['seen']:
                #            a['score'] = sim_ratio
                #            a['seen'] = s['hash_key']
                #            h['similar'].insert(0, a)
                #            h['seen'].append(a['hash_key'])
                #            #h = append_related(tag, h, a, 70)
                #            seen.append(a['hash_key'])
                #            break
            except:
                print_exception()

        try:
            if a['hash_key'] not in seen:
                history.append(a)
                seen.append(a['hash_key'])
        except:
            print_exception()

    try:
        for his in history:
            his['similar'] = sorted(
                his['similar'],
                key=lambda s: datetime.strptime(
                    s['date_iso'], "%Y-%m-%dT%H:%M:%S"),
                reverse=True)
    except:
        print_exception()
    return history


def build(tag):
    f = TermFilter("tag", tag.lower())
    results = conn.search(Search(filter=f, start=1, size=200),
                          indexes=["newsworld"],
                          sort='date:desc')
    results.count()
    articles = [from_es_dto(a) for a in results]

    history = build_similar(articles)
    print '[similar] correlated %s articles for %s' % (len(history), tag)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('similar_%s' % tag, json.dumps(history))

    s_history = sorted(history, key=lambda a: len(a['similar']), reverse=True)
    r.set('headlines_%s' % tag, json.dumps(s_history[:5]))
    logger.info('[similar] redis updated for: %s' % tag)


def append_related(tag, target, current, min_ratio):
    related = is_related(current['hash_key'], tag, min_ratio)
    for r in related:
        if r['hash_key'] not in target['seen']:
            target['similar'].append(r)
            target['seen'].append(r['hash_key'])
    return target


def is_related(pk, tag, min_ratio=40):
    min = date.today() - timedelta(days=7)
    max = date.today() + timedelta(days=1)

    f = TermFilter("hash_key", pk)
    s = Search(filter=f, start=0, size=1)
    results = conn.search(s, indexes=["newsworld"])
    articles = None
    for r in results:
        try:
            q1 = TermsQuery("keywords", r.keywords)
            q2 = TermsQuery("tag", [tag])
            q = BoolQuery(must=[q1, q2])
            filt = FilteredQuery(q, RangeFilter(qrange=ESRange('date', min, max, include_upper=False)))
            articles = conn.search(Search(filter=filt, start=0, size=11),
                                   indexes=["newsworld"],
                                   sort='_score,date:desc')
            break
        except:
            print_exception()

    n_articles = []

    try:
        if len(list(articles)) > 0:
            max_score = articles[0]._meta.score

            for a in articles:
                if a.hash_key == pk:
                    continue
                a.score = (a._meta.score / max_score) * 100
                if a.score >= min_ratio:
                    n_articles.append(from_es_dto(a))
    except:
        print_exception()

    return n_articles
