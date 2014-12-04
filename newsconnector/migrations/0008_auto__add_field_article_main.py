# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.main'
        db.add_column('newsconnector_article', 'main',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.main'
        db.delete_column('newsconnector_article', 'main')


    models = {
        'newsconnector.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fulltext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hash_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'newsconnector.entertainmentarticle': {
            'Meta': {'object_name': 'EntertainmentArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.entertainmentfeed': {
            'Meta': {'object_name': 'EntertainmentFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.financearticle': {
            'Meta': {'object_name': 'FinanceArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.financefeed': {
            'Meta': {'object_name': 'FinanceFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.inewsarticle': {
            'Meta': {'object_name': 'INewsArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.inewsfeed': {
            'Meta': {'object_name': 'INewsFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.isportsarticle': {
            'Meta': {'object_name': 'ISportsArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.isportsfeed': {
            'Meta': {'object_name': 'ISportsFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.newsarticle': {
            'Meta': {'object_name': 'NewsArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.newsfeed': {
            'Meta': {'object_name': 'NewsFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.rssfeed': {
            'Meta': {'object_name': 'RssFeed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'})
        },
        'newsconnector.sportsarticle': {
            'Meta': {'object_name': 'SportsArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.sportsfeed': {
            'Meta': {'object_name': 'SportsFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['newsconnector']