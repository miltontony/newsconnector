from datetime import datetime, date
import json
import redis
#from pyes import ES
#conn = ES('127.0.0.1:9200')
#from pyes.queryset import generate_model
#ArticleModel = generate_model("newsworld", "article")
from django.db.models.loading import get_model


def get_articles(tag, limit=20, start=0):
    model = get_model('newsconnector', tag)
    return model.objects.filter(main=True).order_by('-date')[start:limit]


def get_headlines(tag, limit=5):
    model = get_model('newsconnector', tag)
    articles = model.objects.raw('''
SELECT *,
"newsconnector_article"."id",
COUNT("newsconnector_article_similar"."to_article_id") AS "headlines"
FROM "newsconnector_newsarticle"
LEFT OUTER JOIN "newsconnector_article"
    ON ("newsconnector_newsarticle"."article_ptr_id" = "newsconnector_article"."id")
LEFT OUTER JOIN "newsconnector_article_similar"
    ON ("newsconnector_article"."id" = "newsconnector_article_similar"."from_article_id")
WHERE "newsconnector_article"."date" >= '%s'
GROUP BY "newsconnector_article"."id",
         "newsconnector_newsarticle"."article_ptr_id",
         "newsconnector_article_similar"."id"
ORDER BY "headlines" DESC''' % date.today().isoformat())
    return articles[:limit]


def update_date(obj):
    if not isinstance(obj['date'], datetime):
        obj['date'] = datetime.strptime(obj['date'], "%Y-%m-%dT%H:%M:%S")
    return obj
