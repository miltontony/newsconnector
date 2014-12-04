import os.path
import djcelery

DEBUG = False
TEMPLATE_DEBUG = DEBUG

djcelery.setup_loader()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def abspath(*args):
    """convert relative paths to absolute paths relative to PROJECT_ROOT"""
    return os.path.join(PROJECT_ROOT, *args)

ADMINS = (
    ('Milton', 'madandat@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'news',
        'USER': 'news',
        'PASSWORD': 'news',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TIME_ZONE = 'Africa/Johannesburg'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

ROOT_URLCONF = 'newsconnector.urls'
LOGIN_URL = '/admin/'

MEDIA_ROOT = abspath('media')
MEDIA_URL = '/media/'
STATIC_ROOT = abspath('static')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    abspath('templates/static'),
)

SECRET_KEY = 'q^(q(olk1k)z$+(tqbqm1xq1c(v8=6jtp6s2ikx7xaiwv1$_^1'

TEMPLATE_DIRS = (
    "templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'django_nose',
    'djcelery',
    'gunicorn',
    'newsconnector',
    'raven.contrib.django.raven_compat',
    'raven.contrib.django.celery',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/sites/newsconnector/logs/newsworld.log',
            'formatter': 'verbose',
            'maxBytes': 1024*1024*10,  # 5 MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    },
}

from raven.conf import setup_logging
from raven.contrib.django.raven_compat.handlers import SentryHandler

setup_logging(SentryHandler())

try:
    from newsconnector.local_settings import *
except:
    pass
