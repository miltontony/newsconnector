from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Tasks to update articles'

    def handle(self, action, *args, **options):
        def default(obj):
            import datetime

            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            return obj
        from newsconnector.support.tasks import (
            update_feeds, scrape_articles, build_similar)
        from pyes.queryset import generate_model
        import json
        ArticleModel = generate_model("newsworld", "article")

        if action == 'feeds':
            update_feeds()

        if action == 'scrape':
            scrape_articles()

        if action == 'dump':
            print json.dumps(
                ArticleModel.objects.all().order_by('-date')[:40],
                default=default
            )

        if action == 'similar':
            build_similar('NewsArticle')
