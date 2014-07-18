# settings/local.py
from .base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.mysql",
    "NAME": os.environ['RDS_DB_NAME'],
    "USER": os.environ['RDS_USERNAME'],
    "PASSWORD": os.environ['RDS_PASSWORD'],
    "HOST": os.environ['RDS_HOSTNAME'],
    "PORT": os.environ['RDS_PORT'],
  }
}
