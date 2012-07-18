from django.db import models
from datetime import datetime


class Keyword(models.Model):
    keyword = models.TextField()
    date_updated = models.DateTimeField(auto_now = True, default = datetime.now())

    def __unicode__(self):  # pragma: no cover
        return self.keyword


class Article(models.Model):
    hash_key = models.CharField(max_length=32, unique=True)
    date_added = models.DateTimeField(auto_now_add = True)
    date = models.DateTimeField(null=True, blank=True)
    title = models.TextField()
    link = models.TextField()
    image_url = models.TextField(null=True, blank=True)
    content = models.TextField()
    source = models.TextField()
    keywords = models.ManyToManyField(Keyword, blank=True, null=True)

    def __unicode__(self):  # pragma: no cover
        return '%s - %s' % (self.title,  self.content)

    def to_dto(self):
        return {'title': self.title,
                'link': self.link,
                'content': self.content,
                'source': self.source,
                'image_url': self.image_url if self.image_url else '',
                'id': self.pk,
                'date': self.date.strftime('%a, %d %b %H:%M'),
                'keywords': [k.keyword for k in self.keywords.all()[:5]]}

    def to_json(self):
        return {'title': self.title,
                'link': self.link,
                'content': self.content,
                'source': self.source,
                'image_url': self.image_url if self.image_url else '',
                'hash_key': self.hash_key,
                'tag': self.__class__.__name__,
                'date': '%s' % self.date.isoformat(),
                'keywords': [k.keyword for k in self.keywords.all()]}

    def to_related_dto(self, keywords):
        matched = [k.keyword for k in self.keywords.filter(pk__in=keywords)]
        return {'title': self.title,
                'link': self.link,
                'content': self.content,
                'source': self.source,
                'image_url': self.image_url,
                'id': self.pk,
                'date': self.date.strftime('%a, %d %b %H:%M'),
                'sdate': '%s' % self.date.isoformat(),
                'keywords': [k.keyword for k in self.keywords.all()[:5]],
                'matched': matched[:5],
                'rank': len(matched),
                'rankp': len(matched) / float(len(keywords)) * 100}


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



