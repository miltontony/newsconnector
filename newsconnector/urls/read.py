from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector import views
from newsconnector.models import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.read, name='index'),
    url(r'^more/(?P<tag>\w+)/$', views.read_more, name='read_more'),
    url(r'^featured/(?P<tag>\w+)/$', views.featured_articles,
        name='featured_articles'),
    url(r'^search/$', views.search, name='search', ),
    url(r'', include('newsconnector.urls.base')),

    #mobile api
    url(r'^api/news/$', 'newsconnector.mobile.views.api_read_more',
        {'tag': 'NewsArticle'}),
    url(r'^api/sports/$', 'newsconnector.mobile.views.api_read_more',
        {'tag': 'SportsArticle'}),
    url(r'^api/finance/$', 'newsconnector.mobile.views.api_read_more',
        {'tag': 'FinanceArticle'}),
    url(r'^api/entertainment/$', 'newsconnector.mobile.views.api_read_more',
        {'tag': 'EntertainmentArticle'}),
    url(r'^api/inews/$', 'newsconnector.mobile.views.api_read_more',
        {'tag': 'INewsArticle'}),
    url(r'^api/isports/$', 'newsconnector.mobile.views.api_read_more',
        {'tag': 'ISportsArticle'}),

    url(r'^api/headlines/$', 'newsconnector.mobile.views.api_get_all_headlines'),
    url(r'^api/news/headlines/$', 'newsconnector.mobile.views.api_get_headlines',
        {'tag': 'NewsArticle'}),
    url(r'^api/sports/headlines/$', 'newsconnector.mobile.views.api_get_headlines',
        {'tag': 'SportsArticle'}),
    url(r'^api/finance/headlines/$', 'newsconnector.mobile.views.api_get_headlines',
        {'tag': 'FinanceArticle'}),
    url(r'^api/entertainment/headlines/$', 'newsconnector.mobile.views.api_get_headlines',
        {'tag': 'EntertainmentArticle'}),

    url(r'^api/inews/headlines/$', 'newsconnector.mobile.views.api_get_headlines',
        {'tag': 'INewsArticle'}),
    url(r'^api/isports/headlines/$', 'newsconnector.mobile.views.api_get_headlines',
        {'tag': 'ISportsArticle'}),
    url(r'^api/iheadlines/$', 'newsconnector.mobile.views.api_get_international_headlines'),

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

    url(r'^related/(?P<pk>\w{32})/$',
        views.related, name='related', ),
)
