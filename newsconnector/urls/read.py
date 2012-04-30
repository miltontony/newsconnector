from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib import admin
from newsconnector import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.read, name='index'),
    url(r'^search/$', views.search,name='search', ),
    url(r'', include('newsconnector.urls.base')),
)