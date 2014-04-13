from django.db import models


class Article(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    link = models.TextField()
    hash_key = models.CharField(max_length=32, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    fulltext = models.TextField(null=True, blank=True)

    def __unicode__(self):  # pragma: no cover
        return '%s' % self.link


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


class INewsArticle(Article):
    pass


class ISportsArticle(Article):
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


class INewsFeed(RssFeed):
    pass


class ISportsFeed(RssFeed):
    pass
