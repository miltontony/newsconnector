from newsconnector.settings import *
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'update-feed-articles': {
        'task': 'newsconnector.support.tasks.update_feeds',
        'schedule': timedelta(seconds=60),
    },
    'update-redis-articles': {
        'task': 'newsconnector.support.tasks.build_similar',
        'schedule': timedelta(minutes=5),
    },
    'scrape-100-articles': {
        'task': 'newsconnector.support.tasks.scrape_articles',
        'schedule': timedelta(minutes=42),
    },
}
TIME_ZONE = CELERY_TIMEZONE = 'UTC'
CELERY_IMPORTS = ("newsconnector.support.tasks",)
CELERY_RESULT_BACKEND = "amqp"
CELERY_REDIRECT_STDOUTS = False
