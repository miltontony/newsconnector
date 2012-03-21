from django.db import models
from datetime import datetime
from django.utils.hashcompat import md5_constructor

import lxml.html
    
class Article(models.Model):
    hash_key = models.CharField(max_length=32, unique=True)
    date_added = models.DateTimeField(auto_now_add = True)
    title = models.TextField()
    link = models.TextField()
    content = models.TextField()
    source = models.TextField()

    def __unicode__(self):  # pragma: no cover
        return '%s - %s' % (self.title,  self.content)
    
    @classmethod
    def to_instance(cls, dictArticle, source):
        hash_str = ':'.join([dictArticle.title,  dictArticle.link]).encode('ascii', 'ignore')
        hash = md5_constructor(hash_str).hexdigest()
        a, created = Article.objects.get_or_create(hash_key = hash)
        if created:
            a.title = dictArticle.title
            a.link = dictArticle.link
            a.content = lxml.html.fromstring(dictArticle.description).text_content()
            a.source = source
            a.save()
            return a
        return a


class Keyword(models.Model):
    keyword = models.TextField()
    
    def __unicode__(self):  # pragma: no cover
        return self.keyword