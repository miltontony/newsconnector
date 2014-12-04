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
    main = models.BooleanField(default=False)
    similar = models.ManyToManyField(
        'Article', related_name='similar_set', null=True, blank=True)
    seen = models.ManyToManyField(
        'Article', related_name='seen_set', null=True, blank=True)
    score = models.FloatField(default=0.0)

    def __unicode__(self):  # pragma: no cover
        return '%s' % self.link

    def to_json(self):
        return {
            'title': self.title,
            'link': self.link,
            'content': self.content,
            'source': self.source,
            'image_url': self.image_url if self.image_url else '',
            'hash_key': self.hash_key,
            'tag': self.__class__.__name__,
            'date': '%s' % self.date.isoformat(),
            'date_added': '%s' % self.date_added.isoformat(),
            'fulltext': self.fulltext,
            'similar': [v.hash_key for v in self.similar.all()],
            'seen': [v.hash_key for v in self.seen.all()],
        }

    @classmethod
    def from_es(cls, obj):
        return cls.objects.create(
            title=obj['title'],
            content=obj['content'],
            fulltext=obj['fulltext'],
            source=obj['source'],
            date=obj['date'],
            hash_key=obj['hash_key'],
            image_url=obj['image_url'],
            link=obj['link'],
        )


class RssFeed(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(default='')
    site = models.URLField(default='')
    name = models.TextField()

    def __unicode__(self):  # pragma: no cover
        return self.name


# ------ Articles ----------
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


# ------ Feeds ----------
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
