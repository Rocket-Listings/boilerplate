from __future__ import absolute_import
from celery import Celery
from django.conf import settings
from celery.signals import setup_logging
from celery.signals import celeryd_after_setup
import logging
from celery.utils.log import mlevel

app = Celery('hiddentalent')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@setup_logging.connect
def setup_logging_handler(*args, **kwargs):
    # This completely ignores all Celery logging settings
    logging.config.dictConfig(settings.LOGGING)


# @celeryd_after_setup.connect
# def setup_psychopg2_gevent(sender, instance, conf, *args, **kwargs):
    # if conf.CELERYD_POOL == 'gevent':
    #     from psycogreen.gevent import patch_psycopg
    #     patch_psycopg()
