from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector.data import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_news, name='data'),
    url(r'^sports/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_sports, name='data'),
    url(r'^finance/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_finance, name='data'),
    url(r'^entertainment/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_entertainment, name='data'),
)
