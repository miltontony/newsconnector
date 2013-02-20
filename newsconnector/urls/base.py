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
    url(r'^health/', views.health, name='health'),
    url(r'^cgi-sys/defaultwebpage.cgi$', redirect_to, {'url': '/'}),
    url(r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
)
