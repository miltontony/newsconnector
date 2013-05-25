from django.http import HttpResponse
from newsconnector.data import store
import json


def api_read_more(request, tag):
    page = int(request.GET.get('page', 1))

    cat = 1
    if tag == 'NewsArticle':
        cat = 1
    elif tag == 'SportsArticle':
        cat = 2
    elif tag == 'FinanceArticle':
        cat = 3
    else:
        cat = 4

    limit = (page - 1) * 40

    return HttpResponse(json.dumps({
        'articles': store.get_hashed_articles(tag)[limit:],
        'cat': cat,
    }),
        mimetype='application/json'
    )
