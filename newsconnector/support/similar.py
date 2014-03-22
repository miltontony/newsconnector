import json
import redis

from newsconnector.support.utils import (
    print_exception, from_es_dict_dto)

from Levenshtein import ratio
from datetime import datetime
from fuzzywuzzy import fuzz
from pyes import ES
from pyes.queryset import generate_model
ArticleModel = generate_model("newsworld", "article")

conn = ES('127.0.0.1:9200')

import logging
logger = logging.getLogger('raven')


def get_ratio(a, b):
    if not (a and b):
        return 0

    content_ratio = text_ratio = title_ratio = 0
    if a['content'] and b['content']:
        content_ratio = ratio(
            a['content'].encode('ascii', 'ignore'),
            b['content'].encode('ascii', 'ignore')
        )

    if a['fulltext'] and b['fulltext']:
        text_ratio = ratio(
            a['fulltext'].encode('ascii', 'ignore'),
            b['fulltext'].encode('ascii', 'ignore')
        )

    if a['title'] and b['title']:
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

    content_ratio = text_ratio = 0

    if art1['content'] and art2['content']:
        content_ratio = fuzz.token_set_ratio(
            art1['content'].encode('ascii', 'ignore'),
            art2['content'].encode('ascii', 'ignore')
        )
    if art1['fulltext'] and art2['fulltext']:
        text_ratio = fuzz.token_set_ratio(
            art1['fulltext'].encode('ascii', 'ignore'),
            art2['fulltext'].encode('ascii', 'ignore')
        )
    return max(content_ratio, text_ratio)


def prepare_es_dto(obj):
    obj['similar'] = []
    obj['seen'] = []
    obj['main'] = False

    if not 'date_iso' in obj:
        obj['date_iso'] = obj['date'].isoformat()
    elif isinstance(obj['date_iso'], datetime):
        obj['date_iso'] = obj['date_iso'].isoformat()

    if not 'fulltext' in obj:
        obj['fulltext'] = None
    return obj


def log_progress(index, total, distinct, tag):
    if index % 10 == 0:
        logger.info('[similar] [%s] %s/%s new:%s' % (
            tag, index, total, distinct))


def build_similar(articles, tag):
    history = []
    seen = []
    index = 0
    for a in articles:
        log_progress(index, len(articles), len(history), tag)
        a = prepare_es_dto(a)
        found_similar = False
        index += 1
        for h in history:
            try:
                if a['hash_key'] not in h['seen']:
                    sim_ratio = get_fuzzy_ratio(h, a)
                    if sim_ratio >= 70:
                        a['score'] = sim_ratio
                        a['seen'] = h['hash_key']
                        try:
                            a.save()
                        except:
                            pass

                        h['similar'].insert(0, a)
                        h['seen'].append(a['hash_key'])
                        #h = append_related(tag, h, a, 70)
                        seen.append(a['hash_key'])
                        found_similar = True
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
            if not found_similar and a['hash_key'] not in seen:
                a['main'] = True
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


def build(tag, limit=200):
    conn.indices.refresh('newsworld')
    articles = ArticleModel.objects.filter(
        tag=tag.lower()).order_by('-date')[:limit]

    history = build_similar(articles, tag)
    for a in history:
        a.save()
    conn.indices.refresh('newsworld')
    logger.info('[similar] indexing complete for: %s' % tag)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    h = [from_es_dict_dto(a, False) for a in history]
    h = sorted(h, key=lambda a: len(a['similar']), reverse=True)
    r.set('headlines_%s' % tag, json.dumps(h[:5]))
    logger.info('[similar] updated for: %s' % tag)
