# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FinanceFeed'
        db.create_table('newsconnector_financefeed', (
            ('rssfeed_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.RssFeed'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['FinanceFeed'])

        # Adding model 'EntertainmentFeed'
        db.create_table('newsconnector_entertainmentfeed', (
            ('rssfeed_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.RssFeed'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['EntertainmentFeed'])

        # Adding model 'SportsFeed'
        db.create_table('newsconnector_sportsfeed', (
            ('rssfeed_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.RssFeed'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['SportsFeed'])

        # Adding model 'NewsFeed'
        db.create_table('newsconnector_newsfeed', (
            ('rssfeed_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.RssFeed'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['NewsFeed'])


    def backwards(self, orm):
        
        # Deleting model 'FinanceFeed'
        db.delete_table('newsconnector_financefeed')

        # Deleting model 'EntertainmentFeed'
        db.delete_table('newsconnector_entertainmentfeed')

        # Deleting model 'SportsFeed'
        db.delete_table('newsconnector_sportsfeed')

        # Deleting model 'NewsFeed'
        db.delete_table('newsconnector_newsfeed')


    models = {
        'newsconnector.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hash_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'newsconnector.entertainmentarticle': {
            'Meta': {'object_name': 'EntertainmentArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.entertainmentfeed': {
            'Meta': {'object_name': 'EntertainmentFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.entertainmentkeyword': {
            'Meta': {'object_name': 'EntertainmentKeyword', '_ormbases': ['newsconnector.Keyword']},
            'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Keyword']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.financearticle': {
            'Meta': {'object_name': 'FinanceArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.financefeed': {
            'Meta': {'object_name': 'FinanceFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.financekeyword': {
            'Meta': {'object_name': 'FinanceKeyword', '_ormbases': ['newsconnector.Keyword']},
            'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Keyword']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 18, 14, 54, 52, 645224)', 'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.TextField', [], {})
        },
        'newsconnector.newsarticle': {
            'Meta': {'object_name': 'NewsArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.newsfeed': {
            'Meta': {'object_name': 'NewsFeed', '_ormbases': ['newsconnector.RssFeed']},
            'rssfeed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.RssFeed']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.newskeyword': {
            'Meta': {'object_name': 'NewsKeyword', '_ormbases': ['newsconnector.Keyword']},
            'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Keyword']", 'unique': 'True', 'primary_key': 'True'})
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
        },
        'newsconnector.sportskeyword': {
            'Meta': {'object_name': 'SportsKeyword', '_ormbases': ['newsconnector.Keyword']},
            'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Keyword']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['newsconnector']
