from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.news, name='index'),
    url(r'^sports/$', views.sports, name='sports'),
    url(r'^finance/$', views.finance, name='finance'),
    url(r'^entertainment/$', views.entertainment, name='entertainment'),
    url(r'^data/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data, name='data'),
    url(r'^data/sports/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_sports, name='data'),
    url(r'^data/finance/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_finance, name='data'),
    url(r'^data/entertainment/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data_entertainment, name='data'),
    url(r'^admin/', include(admin.site.urls)),
)
