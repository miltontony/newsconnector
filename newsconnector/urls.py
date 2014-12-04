from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector import views
from newsconnector.models import *

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.read, name='index'),
    url(r'^more/(?P<tag>\w+)/$', views.read_more, name='read_more'),
    url(r'^featured/(?P<tag>\w+)/$', views.featured_articles,
        name='featured_articles'),
    url(r'^search/', include('haystack.urls')),
    url(r'^api/', include('newsconnector.api.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^logout/',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'
    ),
    url(r'^health/', views.health, name='health'),
)
