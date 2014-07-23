# settings/local.py
from .base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "photodb",
    "USER": "photoapp",
    "PASSWORD": private.DB_PASSWORD,
    "HOST": "",
    "PORT": "",
  }
}

ALLOWED_HOSTS = ['photos.ryanfisher.io']

AWS_IMAGE_BUCKET = "production.images.ryanfisher.io"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/production.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'photos': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
