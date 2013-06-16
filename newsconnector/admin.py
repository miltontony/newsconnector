from newsconnector.models import *
from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('date_added', 'link')
    ordering = ('-date_added',)


class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


admin.site.register(Article, ArticleAdmin)
admin.site.register(RssFeed, FeedAdmin)

admin.site.register(NewsFeed, FeedAdmin)
admin.site.register(SportsFeed, FeedAdmin)
admin.site.register(FinanceFeed, FeedAdmin)
admin.site.register(EntertainmentFeed, FeedAdmin)
admin.site.register(INewsFeed, FeedAdmin)
admin.site.register(ISportsFeed, FeedAdmin)

admin.site.register(NewsArticle, ArticleAdmin)
admin.site.register(SportsArticle, ArticleAdmin)
admin.site.register(FinanceArticle, ArticleAdmin)
admin.site.register(EntertainmentArticle, ArticleAdmin)
admin.site.register(INewsArticle, ArticleAdmin)
admin.site.register(ISportsArticle, ArticleAdmin)
