from newsconnector.support.utils import print_exception, clean
from django.db.models.loading import get_model

from Levenshtein import ratio
from datetime import datetime
from fuzzywuzzy import fuzz

from pyes.queryset import generate_model

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

    art1_c = get_unicode(art1.content)
    art2_c = get_unicode(art2.content)
    art1_f = get_unicode(art1.fulltext)
    art2_f = get_unicode(art2.fulltext)
    art1_t = get_unicode(art1.title)
    art2_t = get_unicode(art2.title)

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

    art1_c = get_unicode(art1.content)
    art2_c = get_unicode(art2.content)
    art1_f = get_unicode(art1.fulltext)
    art2_f = get_unicode(art2.fulltext)

    if art1_c and art2_c:
        content_ratio = fuzz.token_set_ratio(art1_c, art2_c)
    if art1_f and art2_f:
        text_ratio = fuzz.token_set_ratio(art1_f, art2_f)
    return max(content_ratio, text_ratio)


def prepare_es_dto(obj):
    obj['main'] = False

    if 'fulltext' not in obj:
        obj.fulltext = ''

    if 'date_iso' not in obj and isinstance(obj['date'], datetime):
        obj['date_iso'] = obj['date'].isoformat()
    elif 'date_iso' in obj and isinstance(obj['date_iso'], datetime):
        obj['date_iso'] = obj['date_iso'].isoformat()

    if 'seen' not in obj:
        obj['seen'] = []
    elif isinstance(obj['seen'], str):
        obj['seen'] = []
    elif obj['seen'] is None:
        obj['seen'] = []

    if 'similar' not in obj:
        obj['similar'] = []
    elif isinstance(obj['similar'], str):
        obj['similar'] = []
    elif obj['similar'] is None:
        obj['similar'] = []

    obj.fulltext = clean(obj.fulltext)
    obj.content = clean(obj.content)
    obj.title = clean(obj.title)

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
        found_similar = False
        index += 1

        if index > 200:
            break

        if a in seen:
            skipped.append(a)
            continue

        for h in history:
            try:
                if not h.seen.filter(pk=a.pk).exists():
                    sim_ratio = get_fuzzy_ratio(h, a)
                    if sim_ratio >= 70:
                        a.score = sim_ratio
                        a.seen = [h, ]
                        a.save()

                        h.similar = [a, ] + list(
                            h.similar.all()) + list(a.similar.all())
                        h.seen.add(a)
                        h.seen.add(*list(a.seen.all()))
                        h.save()
                        # h = append_related(tag, h, a, 70)
                        seen.append(a)
                        seen += list(a.seen.all())
                        found_similar = True

                        if a.hash_key == '94032da0f2e05ed7e6df051ec1e0e9ce':
                            print 'what!!', h.title
                        break
            except:
                print_exception()

        try:
            if not found_similar and a not in seen:
                a.main = True
                # a['similar'] = []
                # a['seen'] = []
                history.append(a)
                seen.append(a)
                seen += list(a.seen.all())
                a.save()
        except:
            print_exception()
    return history


def date_parser(obj):
    import datetime
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


def build(tag, limit=200):
    model = get_model('newsconnector', tag)
    articles = model.objects.all().order_by('-date')
    history = build_similar(articles, tag)

    ArticleModel = generate_model(tag.lower(), "article")

    for article in history:
        a = ArticleModel.objects.get(hash_key=article.hash_key)
        if 'similar' not in a:
            a['similar'] = []
        if 'seen' not in a:
            a['seen'] = []

        a['similar'] = [v.hash_key for v in a.similar.all()]
        a['seen'] = [v.hash_key for v in a.seen.all()]
        a.save()
    logger.info('[similar] indexing complete for: %s' % tag)
