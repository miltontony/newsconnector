from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',
    url(r'^news/$', 'newsconnector.api.views.articles',
        {'tag': 'NewsArticle'}),
    url(r'^sports/$', 'newsconnector.api.views.articles',
        {'tag': 'SportsArticle'}),
    url(r'^finance/$', 'newsconnector.api.views.articles',
        {'tag': 'FinanceArticle'}),
    url(r'^entertainment/$', 'newsconnector.api.views.articles',
        {'tag': 'EntertainmentArticle'}),
    url(r'^inews/$', 'newsconnector.api.views.articles',
        {'tag': 'INewsArticle'}),
    url(r'^isports/$', 'newsconnector.api.views.articles',
        {'tag': 'ISportsArticle'}),

    url(r'^headlines/$', 'newsconnector.api.views.headlines_all'),
    url(r'^iheadlines/$', 'newsconnector.api.views.iheadlines_all'),

    url(r'^news/headlines/$', 'newsconnector.api.views.headlines',
        {'tag': 'NewsArticle'}),
    url(r'^sports/headlines/$', 'newsconnector.api.views.headlines',
        {'tag': 'SportsArticle'}),
    url(r'^finance/headlines/$', 'newsconnector.api.views.headlines',
        {'tag': 'FinanceArticle'}),
    url(r'^entertainment/headlines/$', 'newsconnector.api.views.headlines',
        {'tag': 'EntertainmentArticle'}),

    url(r'^inews/headlines/$', 'newsconnector.api.views.headlines',
        {'tag': 'INewsArticle'}),
    url(r'^isports/headlines/$', 'newsconnector.api.views.headlines',
        {'tag': 'ISportsArticle'}),
)
