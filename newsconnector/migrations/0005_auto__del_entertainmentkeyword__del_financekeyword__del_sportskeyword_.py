# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'EntertainmentKeyword'
        db.delete_table('newsconnector_entertainmentkeyword')

        # Deleting model 'FinanceKeyword'
        db.delete_table('newsconnector_financekeyword')

        # Deleting model 'SportsKeyword'
        db.delete_table('newsconnector_sportskeyword')

        # Deleting model 'Keyword'
        db.delete_table('newsconnector_keyword')

        # Deleting model 'NewsKeyword'
        db.delete_table('newsconnector_newskeyword')

        # Deleting field 'Article.date'
        db.delete_column('newsconnector_article', 'date')

        # Deleting field 'Article.hash_key'
        db.delete_column('newsconnector_article', 'hash_key')

        # Deleting field 'Article.title'
        db.delete_column('newsconnector_article', 'title')

        # Deleting field 'Article.content'
        db.delete_column('newsconnector_article', 'content')

        # Deleting field 'Article.source'
        db.delete_column('newsconnector_article', 'source')

        # Deleting field 'Article.image_url'
        db.delete_column('newsconnector_article', 'image_url')

        # Removing M2M table for field keywords on 'Article'
        db.delete_table('newsconnector_article_keywords')


    def backwards(self, orm):
        
        # Adding model 'EntertainmentKeyword'
        db.create_table('newsconnector_entertainmentkeyword', (
            ('keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Keyword'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['EntertainmentKeyword'])

        # Adding model 'FinanceKeyword'
        db.create_table('newsconnector_financekeyword', (
            ('keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Keyword'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['FinanceKeyword'])

        # Adding model 'SportsKeyword'
        db.create_table('newsconnector_sportskeyword', (
            ('keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Keyword'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['SportsKeyword'])

        # Adding model 'Keyword'
        db.create_table('newsconnector_keyword', (
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 13, 12, 58, 6, 724943), auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('newsconnector', ['Keyword'])

        # Adding model 'NewsKeyword'
        db.create_table('newsconnector_newskeyword', (
            ('keyword_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsconnector.Keyword'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('newsconnector', ['NewsKeyword'])

        # Adding field 'Article.date'
        db.add_column('newsconnector_article', 'date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Article.hash_key'
        raise RuntimeError("Cannot reverse this migration. 'Article.hash_key' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Article.title'
        raise RuntimeError("Cannot reverse this migration. 'Article.title' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Article.content'
        raise RuntimeError("Cannot reverse this migration. 'Article.content' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Article.source'
        raise RuntimeError("Cannot reverse this migration. 'Article.source' and its values cannot be restored.")

        # Adding field 'Article.image_url'
        db.add_column('newsconnector_article', 'image_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding M2M table for field keywords on 'Article'
        db.create_table('newsconnector_article_keywords', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['newsconnector.article'], null=False)),
            ('keyword', models.ForeignKey(orm['newsconnector.keyword'], null=False))
        ))
        db.create_unique('newsconnector_article_keywords', ['article_id', 'keyword_id'])


    models = {
        'newsconnector.article': {
            'Meta': {'object_name': 'Article'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {})
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
