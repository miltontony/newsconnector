# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Article'
        db.create_table('newsconnector_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hash_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('source', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('newsconnector', ['Article'])

        # Adding model 'Keyword'
        db.create_table('newsconnector_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.TextField')()),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 4, 18, 14, 53, 21, 370652), auto_now=True, blank=True)),
        ))
        db.send_create_signal('newsconnector', ['Keyword'])

        # Adding model 'RssFeed'
        db.create_table('newsconnector_rssfeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=200)),
            ('site', self.gf('django.db.models.fields.URLField')(default='', max_length=200)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('newsconnector', ['RssFeed'])

        # Adding model 'NewsArticle'
        db.create_table('newsconnector_newsarticle', (
            ('article_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Article'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['NewsArticle'])

        # Adding model 'SportsArticle'
        db.create_table('newsconnector_sportsarticle', (
            ('article_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Article'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['SportsArticle'])

        # Adding model 'FinanceArticle'
        db.create_table('newsconnector_financearticle', (
            ('article_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Article'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['FinanceArticle'])

        # Adding model 'EntertainmentArticle'
        db.create_table('newsconnector_entertainmentarticle', (
            ('article_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Article'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['EntertainmentArticle'])

        # Adding model 'NewsKeyword'
        db.create_table('newsconnector_newskeyword', (
            ('keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Keyword'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['NewsKeyword'])

        # Adding model 'SportsKeyword'
        db.create_table('newsconnector_sportskeyword', (
            ('keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Keyword'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['SportsKeyword'])

        # Adding model 'FinanceKeyword'
        db.create_table('newsconnector_financekeyword', (
            ('keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Keyword'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['FinanceKeyword'])

        # Adding model 'EntertainmentKeyword'
        db.create_table('newsconnector_entertainmentkeyword', (
            ('keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Keyword'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['EntertainmentKeyword'])


    def backwards(self, orm):
        
        # Deleting model 'Article'
        db.delete_table('newsconnector_article')

        # Deleting model 'Keyword'
        db.delete_table('newsconnector_keyword')

        # Deleting model 'RssFeed'
        db.delete_table('newsconnector_rssfeed')

        # Deleting model 'NewsArticle'
        db.delete_table('newsconnector_newsarticle')

        # Deleting model 'SportsArticle'
        db.delete_table('newsconnector_sportsarticle')

        # Deleting model 'FinanceArticle'
        db.delete_table('newsconnector_financearticle')

        # Deleting model 'EntertainmentArticle'
        db.delete_table('newsconnector_entertainmentarticle')

        # Deleting model 'NewsKeyword'
        db.delete_table('newsconnector_newskeyword')

        # Deleting model 'SportsKeyword'
        db.delete_table('newsconnector_sportskeyword')

        # Deleting model 'FinanceKeyword'
        db.delete_table('newsconnector_financekeyword')

        # Deleting model 'EntertainmentKeyword'
        db.delete_table('newsconnector_entertainmentkeyword')


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
        'newsconnector.entertainmentkeyword': {
            'Meta': {'object_name': 'EntertainmentKeyword', '_ormbases': ['newsconnector.Keyword']},
            'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Keyword']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.financearticle': {
            'Meta': {'object_name': 'FinanceArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.financekeyword': {
            'Meta': {'object_name': 'FinanceKeyword', '_ormbases': ['newsconnector.Keyword']},
            'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Keyword']", 'unique': 'True', 'primary_key': 'True'})
        },
        'newsconnector.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 18, 14, 53, 21, 370652)', 'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.TextField', [], {})
        },
        'newsconnector.newsarticle': {
            'Meta': {'object_name': 'NewsArticle', '_ormbases': ['newsconnector.Article']},
            'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Article']", 'unique': 'True', 'primary_key': 'True'})
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
        'newsconnector.sportskeyword': {
            'Meta': {'object_name': 'SportsKeyword', '_ormbases': ['newsconnector.Keyword']},
            'keyword_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsconnector.Keyword']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['newsconnector']
