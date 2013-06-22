import json
import redis

from newsconnector.models import *
from newsconnector.support.utils import *
from pyes import *
from Levenshtein import ratio
from datetime import date

conn = ES('127.0.0.1:9200')


def get_ratio(a, b):
    a = a.encode('ascii', 'ignore')
    b = b.encode('ascii', 'ignore')
    if (a and b and a != '' and b != ''):
        return ratio(a, b)
    return 0


def build(tag):
    f = TermFilter("tag", tag)
    results = conn.search(Search(filter=f, start=1, size=200),
                          indexes=["newsworld"],
                          sort='date:desc')
    results.count()
    articles = [from_es_dto(a) for a in results]

    history = []
    seen = []
    for a in articles:
        for h in history:
            try:
                sim_ratio = get_ratio(h['content'], a['content'])
                sim_ratio_title = get_ratio(h['title'], a['title'])

                if (sim_ratio >= 0.55 or sim_ratio_title >= 0.55) and a['hash_key'] not in h['seen']:
                    a['score'] = max(sim_ratio, sim_ratio_title)
                    a['seen'] = h['hash_key']
                    h['similar'].insert(0, a)
                    h['seen'].append(a['hash_key'])
                    #h = append_related(tag, h, a, 70)
                    seen.append(a['hash_key'])
                    break
                else:
                    for s in h['similar']:
                        sim_ratio = get_ratio(s['content'], a['content'])
                        sim_ratio_title = get_ratio(s['title'], a['title'])

                        if (sim_ratio >= 0.55 or sim_ratio_title >= 0.55) and a['hash_key'] not in h['seen']:
                            a['score'] = max(sim_ratio, sim_ratio_title)
                            a['seen'] = s['hash_key']
                            h['similar'].insert(0, a)
                            h['seen'].append(a['hash_key'])
                            #h = append_related(tag, h, a, 70)
                            seen.append(a['hash_key'])
                            break
            except:
                print_exception()
#        try:
#            if a['hash_key'] not in seen:
#                a = append_related(tag, a, a, 40)
#                history.append(a)
#                seen.append(a['hash_key'])
#        except:
#            print_exception()

    try:
        for his in history:
            his['similar'] = sorted(his['similar'], key=lambda s: datetime.strptime(s['date_iso'], "%Y-%m-%dT%H:%M:%S"), reverse=True)
    except:
        print_exception()

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('similar_%s' % tag, json.dumps(history))

    s_history = sorted(history, key=lambda a: len(a['similar']), reverse=True)
    r.set('headlines_%s' % tag, json.dumps(s_history[:5]))


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
