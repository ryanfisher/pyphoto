# settings/local.py
from .base import *

import os

from boto.s3.connection import OrdinaryCallingFormat

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

PIPELINE_LESS_BINARY = '/usr/local/bin/lessc'

INSTALLED_APPS += ('storages',)

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# STATICFILES_STORAGE = 'project.storage.CachedS3BotoStorage'
# COMPRESS_STORAGE = STATICFILES_STORAGE
# AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY
# AWS_SECRET_ACCESS_KEY = AWS_SECRET_KEY
# AWS_STORAGE_BUCKET_NAME = 'static.ryanfisher.io'
# AWS_CALLING_FORMAT = OrdinaryCallingFormat()
# AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
# AWS_IS_GZIPPED = True

# COMPRESS_URL = 'http://s3.amazonaws.com/'+ AWS_STORAGE_BUCKET_NAME + '/'
# COMPRESS_ENABLED = True
# STATIC_URL = COMPRESS_URL
# S3_URL = STATIC_URL
