import json
import redis

from newsconnector.support.utils import (
    print_exception, from_es_dict_dto, clean)

from Levenshtein import ratio
from datetime import datetime
from fuzzywuzzy import fuzz
from pyes import ES
from pyes.queryset import generate_model
ArticleModel = generate_model("newsworld", "article")

conn = ES('127.0.0.1:9200')

import logging
logger = logging.getLogger('raven')


def get_unicode(txt):
    if not txt:
        return ''
    try:
        txt = unicode(txt, errors="ignore")
    except:
        pass
    try:
        txt = txt.encode('ascii', 'ignore')
    except:
        pass
    return str(txt)


def get_ratio(art1, art2):
    if not (art1 and art2):
        return 0

    art1_c = get_unicode(art1['content'])
    art2_c = get_unicode(art2['content'])
    art1_f = get_unicode(art1['fulltext'])
    art2_f = get_unicode(art2['fulltext'])
    art1_t = get_unicode(art1['title'])
    art2_t = get_unicode(art2['title'])

    content_ratio = text_ratio = title_ratio = 0
    if art1_c and art2_c:
        content_ratio = ratio(art1_c, art2_c)

    if art1_f and art2_f:
        text_ratio = ratio(art1_f, art2_f)

    if art1_t and art2_t:
        title_ratio = ratio(art1_t, art2_t)

    return max(content_ratio, text_ratio, title_ratio)


def get_fuzzy_ratio(art1, art2):
    if not (art1 and art2):
        return 0

    if get_ratio(art1, art2) <= 0.40:
        return 0

    content_ratio = text_ratio = 0

    art1_c = get_unicode(art1['content'])
    art2_c = get_unicode(art2['content'])
    art1_f = get_unicode(art1['fulltext'])
    art2_f = get_unicode(art2['fulltext'])

    if art1_c and art2_c:
        content_ratio = fuzz.token_set_ratio(art1_c, art2_c)
    if art1_f and art2_f:
        text_ratio = fuzz.token_set_ratio(art1_f, art2_f)
    return max(content_ratio, text_ratio)


def prepare_es_dto(obj):
    #obj['similar'] = []
    #obj['seen'] = []
    obj['main'] = False

    if not 'fulltext' in obj:
        obj['fulltext'] = ''

    if not 'date_iso' in obj and isinstance(obj['date'], datetime):
        obj['date_iso'] = obj['date'].isoformat()
    elif 'date_iso' in obj and isinstance(obj['date_iso'], datetime):
        obj['date_iso'] = obj['date_iso'].isoformat()

    if not 'seen' in obj:
        obj['seen'] = []
    elif isinstance(obj['seen'], str):
        obj['seen'] = []
    elif obj['seen'] is None:
        obj['seen'] = []

    if not 'similar' in obj:
        obj['similar'] = []
    elif isinstance(obj['similar'], str):
        obj['similar'] = []
    elif obj['similar'] is None:
        obj['similar'] = []
        obj['similar'] = []

    obj['fulltext'] = clean(obj['fulltext'])
    obj['content'] = clean(obj['content'])
    obj['title'] = clean(obj['title'])

    return obj


def log_progress(index, total, distinct, skipped, tag):
    if index % 10 == 0:
        logger.info('[similar] [%s] %s/%s new:%s skipped:%s' % (
            tag, index, total, distinct, skipped))
        print '[similar] [%s] %s/%s new:%s skipped:%s' % (
            tag, index, total, distinct, skipped)


def build_similar(articles, tag):
    history = []
    seen = []
    skipped = []
    index = 0
    for a in articles:
        log_progress(index, len(articles), len(history), len(skipped), tag)
        a = prepare_es_dto(a)
        found_similar = False
        index += 1

        if index > 200:
            break

        if a['hash_key'] in seen:
            skipped.append(a['hash_key'])
            continue

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

                        h['similar'] = [a, ] + h['similar'] + a['similar']
                        h['seen'].append(a['hash_key'])
                        h['seen'] += [a['seen'], ]
                        #h = append_related(tag, h, a, 70)
                        seen.append(a['hash_key'])
                        seen += [a['seen'], ]
                        found_similar = True

                        if a['hash_key'] == '94032da0f2e05ed7e6df051ec1e0e9ce':
                            print 'what!!', h['title']
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
                #a['similar'] = []
                #a['seen'] = []
                history.append(a)
                seen.append(a['hash_key'])
                seen += a['seen']
        except:
            print_exception()
    return history


def date_parser(obj):
    import datetime
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


def build(tag, limit=200):
    conn.indices.refresh('newsworld')
    articles = ArticleModel.objects.filter(
        tag=tag).order_by('-date')
    history = build_similar(articles, tag)
    for a in history:
        if not 'similar' in a:
            a['similar'] = []
        if not 'seen' in a:
            a['seen'] = []
        a['similar'] = list(dict(
            (v['hash_key'], v) for v in a['similar']).values())
        a['seen'] = list(set(a['seen']))
        a.save()
    conn.indices.refresh('newsworld')
    logger.info('[similar] indexing complete for: %s' % tag)
