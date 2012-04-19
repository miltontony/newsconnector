from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from newsconnector import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.news, name='index'),
    url(r'^sports/$', views.sports, name='sports'),
    url(r'^finance/$', views.finance, name='finance'),
    url(r'^entertainment/$', views.entertainment, name='entertainment'),
    url(r'^data/', include('newsconnector.data.urls')),
    url(r'^keyword/delete/(?P<pk>\d+)/$', views.delete_keyword, name='delete_keyword'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)
