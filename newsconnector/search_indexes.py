from datetime import datetime, timedelta
from haystack import indexes
from newsconnector.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    fulltext = indexes.CharField(model_attr='fulltext', null=True)
    source = indexes.CharField(model_attr='source')
    date = indexes.DateTimeField(model_attr='date')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(
            #date__gte=datetime.now() - timedelta(days=1),
            date__lte=datetime.now())
