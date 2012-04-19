from newsconnector.models import *
from django.contrib import admin
from django.db import models


class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('source',)
    list_display = ('date', 'title', 'source')
    ordering = ('-date','source')

class KeywordAdmin(admin.ModelAdmin):
    search_fields = ('keyword',)
    ordering = ('-date_updated',)
    
class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    

admin.site.register(Article, ArticleAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(RssFeed, FeedAdmin)
admin.site.register(NewsFeed, FeedAdmin)
admin.site.register(SportsFeed, FeedAdmin)
admin.site.register(FinanceFeed, FeedAdmin)
admin.site.register(EntertainmentFeed, FeedAdmin)
admin.site.register(SportsArticle, ArticleAdmin)
admin.site.register(FinanceArticle, ArticleAdmin)
admin.site.register(EntertainmentArticle, ArticleAdmin)
admin.site.register(SportsKeyword, KeywordAdmin)
admin.site.register(FinanceKeyword, KeywordAdmin)
admin.site.register(EntertainmentKeyword, KeywordAdmin)