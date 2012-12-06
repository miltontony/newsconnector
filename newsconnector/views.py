from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.http import HttpResponse

import json
from datetime import date

from newsconnector.models import *
from newsconnector.support.utils import *
from pyes import *

conn = ES('127.0.0.1:9200')


def health(request):
    return HttpResponse("")


@login_required
def delete_keyword(request, pk):
    if(request.user.is_staff):
        keyword = get_object_or_404(Keyword, pk=pk)
        keyword.delete()
        redirect_url = request.GET.get('next', '/')
        return redirect(redirect_url)
    return redirect('/')


def search(request, articleModel=Article):
    q = request.GET.get('q', None)

    q1 = TextQuery("content", q, operator='or')
    q2 = TextQuery("title", q, operator='or')
    q3 = TextQuery("keyword", q, boost=0.5, operator='or')
    query = BoolQuery(should=[q1, q2, q3])
    results = conn.search(Search(query=query, start=0, size=10),\
                            indexes=["newsworld"], sort='date:desc,_score')

    return render(request, 'browse.html',
                            {'sites': RssFeed.objects.all().distinct('name'),
                            'q': q,
                            'news': [from_es_dto(a) for a in results],
                            })


def get_articles(tag):
    min = date.today() - timedelta(days=1)
    max = date.today() + timedelta(days=1)

    q = FilteredQuery(TermFilter("tag", tag),
            RangeFilter(qrange=ESRange('date',
                min, max, include_upper=False)))
    f = Search(query=q, start=0, size=20)
    f.facet.add_term_facet('keywords', size=50)
    return conn.search(f,\
                        indexes=["newsworld"],
                        sort='date:desc')


def get_featured_articles(resultset):
    bucket = []
    ignore_terms = ['politics', 'south africa', 'social issues',\
                    'human interest', 'year of birth missing', 'state media',\
                    'president', 'environment', 'the sunday times',\
                    'weather', 'international relations', 'education',
                    'sports', 'tennis', 'geography', 'mass media', 'labor',\
                    'singers', 'usd', 'Business_Finance',\
                    'Disaster_Accident', 'Education', 'Entertainment_Culture',\
                    'Environment', 'Health_Medical_Pharma',\
                    'Hospitality_Recreation', 'Human Interest', 'Labor',\
                    'Law_Crime', 'Politics', 'Religion_Belief',\
                    'Social Issues', 'Sports', 'Technology_Internet',\
                    'Weather', 'War_Conflict', 'Other']

    terms = [t for t in resultset.facets.keywords.terms\
                if t['term'].lower() not in [a.lower() for a in ignore_terms]\
                    and 'people' not in t['term']]

    seen = []
    for k in terms:
        f = TermFilter("keyword", k['term'])
        articles = conn.search(Search(filter=f, start=0, size=10),\
                            indexes=["newsworld"],
                            sort='date:desc')
        if any(articles):
            feature = {'keyword': k['term'],
                            'articles': [from_es_dto(a)\
                                            for a in articles[:5]\
                                                if a]
                        }
            found = False
            for x in feature['articles']:
                if x['hash_key'] in seen:
                    found = True
                    break
            if not found:
                bucket.append(feature)
                seen += [y['hash_key'] for y in feature['articles']]

    #TODO:remove articles that appear in multiple buckets
    return bucket[:5]


def featured_articles(tag):
    return get_featured_articles(get_articles(tag))


def read(request):
    news = get_articles('NewsArticle')
    sports = get_articles('SportsArticle')
    finance = get_articles('FinanceArticle')
    entertainment = get_articles('EntertainmentArticle')

    return render(request,
                'read.html',
                {'sites': RssFeed.objects.all().distinct('name'),
                 'news': [from_es_dto(a) for a in news],
                 'sports': [from_es_dto(a) for a in sports],
                 'finance': [from_es_dto(a) for a in finance],
                 'entertainment': [from_es_dto(a) for a in entertainment],
                 'featuredNews': get_featured_articles(news),
                 'featuredSports': get_featured_articles(sports),
                 'featuredFinance': get_featured_articles(finance),
                 'featuredEntertainment': get_featured_articles(entertainment),
                 })


def read_more(request, tag):
    page = int(request.GET.get('page', 1))

    if not page:
        return HttpResponse(json.dumps({'error': 'page not selected'}),
                            mimetype='application/json')

    f = TermFilter("tag", tag)
    results = conn.search(Search(filter=f, start=(page - 1) * 20, size=20),\
                        indexes=["newsworld"],
                        sort='date:desc')
    results.count()
    data = json.dumps({'articles': [from_es_dto(a) for a in results],
                       'has_next': True,
                       'next_page': page + 1})

    return HttpResponse(data, mimetype='application/json')


def related(request, pk):
    f = TermFilter("hash_key", pk)
    s = Search(filter=f, start=0, size=1)
    results = conn.search(s, indexes=["newsworld"])
    articles = None
    article = None
    for r in results:
        article = r
        q = TermsQuery("keywords", r.keywords)
        articles = conn.search(Search(q, start=0, size=11),\
                                indexes=["newsworld"],
                                sort='_score,date:desc')
        break

    n_articles = []

    if len(list(articles)) > 0:
        max_score = articles[0]._meta.score

        for a in articles:
            if a.hash_key == pk:
                continue
            a.score = (a._meta.score / max_score) * 100
            n_articles.append(from_es_dto(a))

    data = {'articles': n_articles,
            'article': from_es_dto(article)}
    return render(request, 'related.html', data)
