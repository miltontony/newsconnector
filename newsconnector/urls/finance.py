from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib import admin
from newsconnector import views
from newsconnector.models import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.finance, name='finance'),
    url(r'^search/$', views.search, {'articleModel': FinanceArticle},name='search', ),
    url(r'', include('newsconnector.urls.base')),
)