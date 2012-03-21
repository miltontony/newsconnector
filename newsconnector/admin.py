from newsconnector.models import Article
from django.contrib import admin
from django.db import models


class ArticleAdmin(admin.ModelAdmin):

    list_filter = ('source',)
    list_display = ('date_added', 'title', 'source')

admin.site.register(Article, ArticleAdmin)