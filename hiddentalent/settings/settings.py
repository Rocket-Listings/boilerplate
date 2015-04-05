# Django settings for hiddentalent project.

from __future__ import absolute_import
import os
from os.path import dirname, join, abspath
from os import environ
import sys
from sys import path
# import dj_database_url
# import logging
# from urlparse import urlparse
# from redisify import redisify
from .celery import *  # noqa
import mimetypes


def env_var(key, default=None, coerce=None):
    if default:
        val = environ.get(key, default)
    else:
        try:
            val = environ[key]
        except KeyError:
            logging.debug('No value found for environment variable name {}'.format(key))
            return None
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    elif coerce:
        val = coerce(val)
    return val

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

APP_DIR = dirname(dirname(abspath(__file__)))

REPO_DIR = dirname(APP_DIR)

# allow for imports in the form: `import sell.forms`
# instead of `import apps.sell.forms`.
path.append(join(APP_DIR, 'apps'))

# Modify sys.path to include the lib directory
sys.path.append(os.path.join(PROJECT_ROOT, "lib"))

ALLOWED_HOSTS = []

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

ROOT_URLCONF = 'hiddentalent.urls'

WSGI_APPLICATION = 'wsgi.application'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'America/New_York'

SECRET_KEY = env_var('DJANGO_SECRET_KEY')

SITE_ID = env_var('DJANGO_SITE_ID')

DEBUG = env_var('DJANGO_DEBUG')

PREPEND_WWW = env_var('DJANGO_PREPEND_WWW')

APPEND_SLASH = False

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

ALLOW_INDEXING = env_var('ROCKET_ALLOW_INDEXING')

DEPLOY_SLUG = env_var('ROCKET_DEPLOY_SLUG')

TEMPLATE_DEBUG = DEBUG




ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hiddentalent',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',  # Set to empty string for localhost.
        'PORT': '',  # Set to empty string for default.
        'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
    }
}


STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [join(REPO_DIR, "static", "build")]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


SECRET_KEY = env_var('DJANGO_SECRET_KEY')

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hiddentalent.wsgi.application'


TEMPLATE_DIRS = [join(APP_DIR, 'templates')]


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",


    # Required by `allauth` template tags
    "django.core.context_processors.request",
    
    # `allauth` specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    
)

AUTHENTICATION_BACKENDS = (
    
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'core',
)


EMAIL_SUBJECT_PREFIX = '[hiddentalent] '



# allauth settings
ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = "none"

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_UNIQUE_EMAIL = True

LOGIN_REDIRECT_URL = 'home'

SIGNUP_REDIRECT_URL = 'home'

# Mail settings
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'

MAILGUN_ACCESS_KEY = 'key-9flqj538z-my-qcnpc74c2wit4vibl-3'

MAILGUN_SERVER_NAME = 'notcl.com'

# Logging settings

LOG_LEVEL = env_var('ROCKET_LOG_LEVEL')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

SOCIALACCOUNT_PROVIDERS = \
    {'linkedin':
      {'SCOPE': ['r_emailaddress', 'r_fullprofile'],
       'PROFILE_FIELDS': ['id',
                         'first-name',
                         'last-name',
                         'email-address',
                         'picture-url',
                         'public-profile-url']}}
