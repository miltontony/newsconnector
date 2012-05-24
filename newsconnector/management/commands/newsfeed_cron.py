from django.core.management.base import BaseCommand
from newsconnector.support.tasks import run_tasks
from newsconnector.models import *


class Command(BaseCommand):
    help = 'Publish content based on the publish_on fields'

    def handle(self, **options):    
        feeds = [(feed.url, feed.name) for feed in NewsFeed.objects.all()]
        run_tasks.delay(feeds, NewsArticle, NewsKeyword)

        feeds = [(feed.url, feed.name) for feed in SportsFeed.objects.all()]
        run_tasks.delay(feeds, SportsArticle, SportsKeyword)

        feeds = [(feed.url, feed.name) for feed in FinanceFeed.objects.all()]
        run_tasks.delay(feeds, FinanceArticle, FinanceKeyword)

        feeds = [(feed.url, feed.name) for feed in EntertainmentFeed.objects.all()]
        run_tasks.delay(feeds, EntertainmentArticle, EntertainmentKeyword)
