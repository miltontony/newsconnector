from django.core.management.base import BaseCommand
from newsconnector.tasks import run_tasks

class Command(BaseCommand):
    help = 'Publish content based on the publish_on fields'

    def handle(self, **options):    
        feeds = [('http://feeds.news24.com/articles/news24/SouthAfrica/rss', 'news24.com'),
                 ('http://www.timeslive.co.za/?service=rss', 'timeslive.co.za'),
                 ('http://feeds.iol.co.za/rss/feed_southafrica.rss', 'iol.co.za'),
                 ('http://www.ewn.co.za/Feeds/Local.aspx', 'ewn.co.za'),
                 ('http://mg.co.za/rss/national', 'mg.co.za'),
                 ('http://www.thenewage.co.za/rss.aspx?cat_id=1007', 'thenewage.co.za'),
                 ('http://www.sowetanlive.co.za/news/?service=rss', 'sowetanlive.co.za'),
                 ('http://feeds.citypress.co.za/articles/CityPress/TopStories/rss', 'citypress.co.za'),
                 ]
        result = run_tasks.delay(feeds)
