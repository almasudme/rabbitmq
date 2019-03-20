from kombu import Queue
import socket

BROKER_URL='amqp://user:password@host_ipv4_address:5672/vhost'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_ACKS_LATE = True
CELERY_CREATE_MISSING_QUEUES = False
CELERY_ENABLE_UTC = False
CELERY_RESULT_BACKEND = 'rpc'
CELERY_RESULT_PERSISTENT = False
CELERY_REJECT_ON_WORKER_LOST = True
CELERY_TASK_RESULT_EXPIRES = 600
CELERY_TIMEZONE = 'US/Eastern'
# CELERY_TIMEZONE = 'America/New_York'
# CELERY_TRACK_STARTED = True 
CELERY_TASK_TRACK_STARTED = True

CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_LOG_COLOR = False
CELERYD_POOL_RESTARTS = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_REDIRECT_STDOUTS = False


CELERY_QUEUES = (
  Queue('celery',           routing_key='celery'),
  Queue('queue_name',       routing_key='queue_name',       queue_arguments={'x-max-priority': 255}),
  Queue('machinednsaddress',         routing_key='machinednsaddress',         queue_arguments={'x-max-priority': 255})
)
