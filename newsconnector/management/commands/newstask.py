from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Tasks to update articles'

    def handle(self, action, *args, **options):
        from newsconnector.support.tasks import update_feeds, scrape_articles

        if action == 'feeds':
            update_feeds()

        if action == 'scrape':
            scrape_articles()
