# settings/local.py
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

AWS_IMAGE_BUCKET = "development.images.ryanfisher.io"

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "photodb",
    "USER": "",
    "PASSWORD": "",
    "HOST": "",
    "PORT": "",
  }
}

INSTALLED_APPS += ("debug_toolbar", )

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
            'filename': 'logs/development.log',
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
