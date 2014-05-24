# settings/local.py
from .base import *

DEBUG = True
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

INSTALLED_APPS += ("debug_toolbar", )
