from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector import views
from newsconnector.models import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.read, name='index'),
    url(r'^more/(?P<category>\d+)/$', views.read_more, name='read_more'),
    url(r'^search/$', views.search, name='search', ),
    url(r'', include('newsconnector.urls.base')),

    #url(r'^news/$', views.news, name='news'),
    url(r'^news/search/$',
        views.search,
        {'articleModel': NewsArticle},
        name='news_search', ),

    #url(r'^sports/$', views.sports, name='sports'),
    url(r'^sports/search/$',
        views.search,
        {'articleModel': SportsArticle},
        name='sports_search', ),

    #url(r'^financial/$', views.finance, name='finance'),
    url(r'^financial/search/$',
        views.search,
        {'articleModel': FinanceArticle},
        name='finance_search', ),

    #url(r'^entertainment/$', views.entertainment, name='entertainment'),
    url(r'^entertainment/search/$',
        views.search,
        {'articleModel': EntertainmentArticle},
        name='entertainment_search', ),

    url(r'^related/1/(?P<pk>\w+)/$', views.related, {'tag': 'NewsArticle', 'section_index': 1},name='related_news', ),
    url(r'^related/2/(?P<pk>\w+)/$', views.related, {'tag': 'SportsArticle', 'section_index': 2},name='related_sports', ),
    url(r'^related/3/(?P<pk>\w+)/$', views.related, {'tag': 'FinanceArticle', 'section_index': 3},name='related_finance', ),
    url(r'^related/4/(?P<pk>\w+)/$', views.related, {'ag': 'EntertainmentArticle', 'section_index': 4},name='related_entertainment', ),
)
