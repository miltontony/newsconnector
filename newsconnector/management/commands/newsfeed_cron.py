from django.core.management.base import BaseCommand
from newsconnector.support.tasks import run_tasks, run_build_related
from newsconnector.models import *
from celery.task import TaskSet
from datetime import datetime, timedelta


class Command(BaseCommand):
    args = '<task>'
    help = 'Publish content based on the publish_on fields'

    def cust_run_build_related(self):
        now = datetime.now()

        task_list = [run_build_related.subtask((NewsArticle,)),\
                     run_build_related.subtask((SportsArticle,),\
                        options={'eta':now + timedelta(seconds=60 * 5)}),\
                     run_build_related.subtask((FinanceArticle,),\
                        options={'eta':now + timedelta(seconds=60 * 10)}),\
                     run_build_related.subtask((EntertainmentArticle,),\
                        options={'eta':now + timedelta(seconds=60 * 15)})
                    ]
        taskset = TaskSet(tasks=task_list)
        result = taskset.apply_async()
        result.ready()
        return result.successful()

    def handle(self, *args, **options):
        if int(args[0]) == 1:  # Update featured for news
            return self.cust_run_build_related()

        news_feeds = [(feed.url, feed.name)\
                        for feed in NewsFeed.objects.all()]
        sports_feeds = [(feed.url, feed.name)\
                        for feed in SportsFeed.objects.all()]
        fin_feeds = [(feed.url, feed.name)\
                        for feed in FinanceFeed.objects.all()]
        e_feeds = [(feed.url, feed.name)\
                        for feed in EntertainmentFeed.objects.all()]

        now = datetime.now()

        task_list = [
            run_tasks.subtask((news_feeds, NewsArticle, NewsKeyword)),\
            run_tasks.subtask((sports_feeds, SportsArticle, SportsKeyword),\
                options={'eta':now + timedelta(seconds=60 * 5)}),\
            run_tasks.subtask((fin_feeds, FinanceArticle, FinanceKeyword),\
                options={'eta':now + timedelta(seconds=60 * 10)}),\
            run_tasks.subtask((e_feeds, EntertainmentArticle,\
                                EntertainmentKeyword),\
                options={'eta':now + timedelta(seconds=60 * 15)})
        ]
        taskset = TaskSet(tasks=task_list)
        result = taskset.apply_async()
        result.ready()
        result.successful()
