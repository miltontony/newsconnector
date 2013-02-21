import os.path
import djcelery

DEBUG = False
TEMPLATE_DEBUG = DEBUG

djcelery.setup_loader()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'update-feed-articles': {
        'task': 'newsconnector.support.tasks.update_feeds',
        'schedule': timedelta(minutes=30),
    },
}
CELERY_TIMEZONE = 'UTC'
CELERY_IMPORTS = ("newsconnector.support.tasks",)
CELERY_RESULT_BACKEND = "amqp"


def abspath(*args):
    """convert relative paths to absolute paths relative to PROJECT_ROOT"""
    return os.path.join(PROJECT_ROOT, *args)

ADMINS = (
     ('Milton', 'madandat@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'news',                      # Or path to database file if using sqlite3.
        'USER': 'news',                      # Not used with sqlite3.
        'PASSWORD': 'news',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Africa/Johannesburg'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = abspath('media')
MEDIA_URL = '/media/'
STATIC_ROOT = abspath('static')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    abspath('templates/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'q^(q(olk1k)z$+(tqbqm1xq1c(v8=6jtp6s2ikx7xaiwv1$_^1'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
)

ROOT_URLCONF = 'newsconnector.urls'
REMOVE_WWW_FROM_DOMAIN = True

SUBDOMAIN_URLCONFS = {
    # The format for these is 'subdomain': 'urlconf'
    None: 'newsconnector.urls.read',
    'www': 'newsconnector.urls.read',
    'news': 'newsconnector.urls.read',
    #'sports': 'newsconnector.urls.sports',
    #'finance': 'newsconnector.urls.finance',
    #'entertainment': 'newsconnector.urls.entertainment',
    #'e': 'newsconnector.urls.entertainment',
    'read': 'newsconnector.urls.read',
    'justread': 'newsconnector.urls.read',
}

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
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_URL = '/admin/'
#SESSION_COOKIE_DOMAIN = '.newsworld.co.za'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

import re
IGNORABLE_404_URLS = (
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
)
