from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector import views
from newsconnector.models import *

admin.autodiscover()
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib import admin
from newsconnector import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.read, name='index'),
    url(r'^more/(?P<tag>\w+)/$', views.read_more, name='read_more'),
    url(r'^featured/(?P<tag>\w+)/$', views.featured_articles,
        name='featured_articles'),
    url(r'^search/$', views.search, name='search', ),
    url(r'^api/', include('newsconnector.api.urls')),

    url(r'^keyword/delete/(?P<pk>\d+)/$', views.delete_keyword, name='delete_keyword'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^health/', views.health, name='health'),

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
