# settings/test.py
from .base import *

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "test_photodb",
    "USER": "",
    "PASSWORD": "",
    "HOST": "",
    "PORT": "",
  }
}
