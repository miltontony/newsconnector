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
        ))
        db.send_create_signal('newsconnector', ['Keyword'])


    def backwards(self, orm):
        
        # Deleting model 'Article'
        db.delete_table('newsconnector_article')

        # Deleting model 'Keyword'
        db.delete_table('newsconnector_keyword')


    models = {
        'newsconnector.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hash_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'newsconnector.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['newsconnector']
