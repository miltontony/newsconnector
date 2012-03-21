from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^cron/$', views.cron, name='cron'),
    url(r'^admin/', include(admin.site.urls)),
)
