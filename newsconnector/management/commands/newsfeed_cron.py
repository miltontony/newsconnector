from django.core.management.base import BaseCommand
from newsconnector.support.tasks import run_tasks
from newsconnector.models import *
from celery.task import TaskSet


class Command(BaseCommand):
    help = 'Publish content based on the publish_on fields'

    def handle(self, **options):
        news_feeds = [(feed.url, feed.name) for feed in NewsFeed.objects.all()]
        sports_feeds = [(feed.url, feed.name) for feed in SportsFeed.objects.all()]
        fin_feeds = [(feed.url, feed.name) for feed in FinanceFeed.objects.all()]
        e_feeds = [(feed.url, feed.name) for feed in EntertainmentFeed.objects.all()]

        task_list = [run_tasks.subtask((news_feeds, NewsArticle, NewsKeyword)),\
                     run_tasks.subtask((sports_feeds, SportsArticle, SportsKeyword)),\
                     run_tasks.subtask((fin_feeds, FinanceArticle, FinanceKeyword)),\
                     run_tasks.subtask((e_feeds, EntertainmentArticle, EntertainmentKeyword))
                    ]
        taskset = TaskSet(tasks=task_list)
        result = taskset.apply_async()
        result.ready()
        result.successful()
