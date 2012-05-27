import json
from operator import itemgetter, attrgetter

from django.http import HttpResponse

from newsconnector.models import *
from newsconnector.support.utils import *

def get_data_news(request, min_date=None, max_date=None):
    data = json.dumps(build_data(get_min_date(min_date), get_max_date(max_date), \
                                 NewsArticle, NewsKeyword))
    return HttpResponse(data, mimetype='application/json')

def get_data_sports(request, min_date=None, max_date=None):
    data = json.dumps(build_data(get_min_date(min_date), get_max_date(max_date), \
                                 SportsArticle, SportsKeyword))
    return HttpResponse(data, mimetype='application/json')

def get_data_finance(request, min_date=None, max_date=None):
    data = json.dumps(build_data(get_min_date(min_date), get_max_date(max_date), \
                                 FinanceArticle, FinanceKeyword))
    return HttpResponse(data, mimetype='application/json')

def get_data_entertainment(request, min_date=None, max_date=None):
    data = json.dumps(build_data(get_min_date(min_date), get_max_date(max_date), \
                                 EntertainmentArticle, EntertainmentKeyword))
    return HttpResponse(data, mimetype='application/json')

def related(request, pk, articleModel=NewsArticle):
    keywords = [i.pk for i in articleModel.objects.get(pk=pk).keywords.all()]
    l = articleModel.objects.filter(keywords__in=keywords)\
                               .exclude(pk=pk)\
                               .distinct('date','pk')\
                               .order_by('-date', 'pk')[:20]
    articles = [a.to_related_dto(keywords) for a in l]
    s_articles = sorted(articles, key=itemgetter('rank','sdate'), reverse=True)

    data = json.dumps({'articles': s_articles,
                       'article': articleModel.objects.get(pk=pk).to_dto()})
    return HttpResponse(data, mimetype='application/json')
