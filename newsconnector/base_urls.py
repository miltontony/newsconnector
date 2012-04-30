from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib import admin
from newsconnector import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^data/', include('newsconnector.data.urls')),
    url(r'^keyword/delete/(?P<pk>\d+)/$', views.delete_keyword, name='delete_keyword'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^cgi-sys/defaultwebpage.cgi$', redirect_to, {'url': '/'}),
)