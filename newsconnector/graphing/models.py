from neo4django.db import models
import neo4django
from neo4jrestclient import client

class GraphArticle(models.NodeModel):
    article_id = models.IntegerProperty(indexed=True)
    title = models.StringProperty()
    content = models.StringProperty()
    link = models.StringProperty()
    source = models.StringProperty()
    
    def __unicode__(self):  # pragma: no cover
        return self.title
    
    def update_and_save(self, article):
        self.title = article.title
        self.content = article.content
        self.link = article.link
        self.source = article.source
        self.save()


class GraphKeyword(models.NodeModel):
    keyword = models.StringProperty()
    relates_to = models.Relationship('GraphArticle',
                                  rel_type = neo4django.Outgoing.RELATES_TO,
                                  related_name = 'is_related_to')
    
    def __unicode__(self):  # pragma: no cover
        return self.keyword
    
    def connections(self, depth=1):
        return [GraphArticle._neo4j_instance(node) \
            for node in self.node.traverse(types=[client.All.RELATES_TO], stop=depth)]