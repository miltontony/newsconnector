from celery.task import task

import feedparser

from newsconnector.models import Article, Keyword
#from newsconnector.graphing.models import GraphArticle, GraphKeyword
from newsconnector.calais import Calais

@task
def run_tasks(feeds):
    new_articles = []
    for feed, source in feeds:
        for entry in feedparser.parse(feed).entries:
            new_articles.append(Article.to_instance(entry, source))
        print 'Fetched: %s' % feed
    print 'Fetching complete.'
    print 'Start OpenCalais keyword fetch.'
    
    data = ' '.join(['%s %s' % (a.title, a.content) for a in new_articles if a])
    
    if not data:
        return
    
    data = data.encode('ascii', 'ignore')
    
    calais = Calais('r8krg8jjs9smep7c2z9jvzew', submitter="python-calais newsconnector")
    result = calais.analyze(data)
    print 'Keyword analysis complete.'
    print 'Start keyword graphing.'
    keywords = (a["name"].lower() for a in result.entities)
    [Keyword.objects.get_or_create(keyword = k) for k in keywords]
                    
    print 'Update complete.'