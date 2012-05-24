import json
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
    list = articleModel.objects.filter(keywords__in=[i.pk\
                                                     for i in articleModel\
                                                       .objects.get(pk=pk)\
                                                       .keywords.all()])\
                               .exclude(pk=pk)\
                               .order_by('-date')[:20]
    data = json.dumps({'articles': [a.to_dto() for a in list],
                       'article': articleModel.objects.get(pk=pk).to_dto()})
    return HttpResponse(data, mimetype='application/json')
