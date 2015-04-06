from __future__ import absolute_import
from os import environ
from kombu import Exchange, Queue
from celery.schedules import crontab


# Broker settings
BROKER_URL = environ.get('CLOUDAMQP_URL')

BROKER_POOL_LIMIT = int(environ.get('DJANGO_BROKER_POOL_LIMIT', 0))

BROKER_CONNECTION_MAX_RETRIES = None

# Result settings
CELERY_RESULT_BACKEND = environ.get('OPENREDIS_URL', 'redis://')

CELERY_REDIS_MAX_CONNECTIONS = 10

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ['json']

CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True

CELERY_MESSAGE_COMPRESSION = 'gzip'

# Misc settings
CELERY_DISABLE_RATE_LIMITS = False

CELERY_ALWAYS_EAGER = False

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

CELERY_ACKS_LATE = True

CELERYD_POOL_RESTARTS = True

CELERYD_TASK_TIME_LIMIT = 180


# Logging, event and signal settings
CELERY_SEND_EVENTS = True

CELERY_SEND_TASK_SENT_EVENT = True

CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_REDIRECT_STDOUTS = False

# CELERY_REDIRECT_STDOUTS_LEVEL = 'WARNING'

# VERY EXPERIMENTAL
CELERY_DB_REUSE_MAX = -1

# Queue settings
CELERY_QUEUES = (
    Queue('fast', Exchange('fast', type='direct'), routing_key='fast'),
    Queue('slow', Exchange('slow', type='direct'), routing_key='slow'),
)

# These are likely redundant
CELERY_DEFAULT_QUEUE = 'fast'

CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'

CELERY_DEFAULT_ROUTING_KEY = 'fast'

CELERYD_FORCE_EXECV = True

CELERYBEAT_SCHEDULE = {
}

CELERY_ROUTES = {
}
