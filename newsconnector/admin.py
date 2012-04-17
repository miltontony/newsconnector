from newsconnector.models import Article, Keyword
from django.contrib import admin
from django.db import models


class ArticleAdmin(admin.ModelAdmin):

    list_filter = ('source',)
    list_display = ('date_added', 'title', 'source')

class KeywordAdmin(admin.ModelAdmin):

    search_fields = ('keyword',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Keyword, KeywordAdmin)