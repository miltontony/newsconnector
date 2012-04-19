from django.db import models
from datetime import datetime

class Article(models.Model):
    hash_key = models.CharField(max_length=32, unique=True)
    date_added = models.DateTimeField(auto_now_add = True)
    date = models.DateTimeField(null=True, blank=True)
    title = models.TextField()
    link = models.TextField()
    content = models.TextField()
    source = models.TextField()

    def __unicode__(self):  # pragma: no cover
        return '%s - %s' % (self.title,  self.content)


class Keyword(models.Model):
    keyword = models.TextField()
    date_updated = models.DateTimeField(auto_now = True, default = datetime.now())
    
    def __unicode__(self):  # pragma: no cover
        return self.keyword


class RssFeed(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(default='')
    site = models.URLField(default='')
    name = models.TextField()
    
    def __unicode__(self):  # pragma: no cover
        return self.name


#------ Articles ----------
class NewsArticle(Article):
    pass

class SportsArticle(Article):
    pass

class FinanceArticle(Article):
    pass

class EntertainmentArticle(Article):
    pass


#------ Keywords ----------
class NewsKeyword(Keyword):
    pass

class SportsKeyword(Keyword):
    pass
   
class FinanceKeyword(Keyword):
    pass
   
class EntertainmentKeyword(Keyword):
    pass
        
        
#------ Feeds ----------
class NewsFeed(RssFeed):
    pass

class SportsFeed(RssFeed):
    pass

class FinanceFeed(RssFeed):
    pass
    
class EntertainmentFeed(RssFeed):
    pass
    

    