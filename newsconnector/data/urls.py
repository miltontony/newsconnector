from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector.data import views
from newsconnector.models import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_news, name='data'),
    url(r'^sports/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_sports, name='data'),
    url(r'^finance/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_finance, name='data'),
    url(r'^entertainment/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_entertainment, name='data'),

    url(r'^related/1/(?P<pk>\d+)/$', views.related, {'articleModel': NewsArticle},name='related_news', ),
    url(r'^related/2/(?P<pk>\d+)/$', views.related, {'articleModel': SportsArticle},name='related_sports', ),
    url(r'^related/3/(?P<pk>\d+)/$', views.related, {'articleModel': FinanceArticle},name='related_finance', ),
    url(r'^related/4/(?P<pk>\d+)/$', views.related, {'articleModel': EntertainmentArticle},name='related_entertainment', ),
)
