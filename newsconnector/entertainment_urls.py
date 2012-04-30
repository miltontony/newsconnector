from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib import admin
from newsconnector import views
from newsconnector.models import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.entertainment, name='entertainment'),
    url(r'^browse/$', views.browse, {'articleModel': EntertainmentArticle},name='browse', ),
    url(r'', include('newsconnector.base_urls')),
)