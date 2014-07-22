# settings/local.py
from .base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

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

AWS_IMAGE_BUCKET = "production.images.ryanfisher.io"
