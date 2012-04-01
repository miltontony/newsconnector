from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^data/(?P<min_date>\d+)/(?P<max_date>\d+)/$', views.get_data, name='data'),
    url(r'^admin/', include(admin.site.urls)),
)
