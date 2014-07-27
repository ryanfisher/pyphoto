"""
Django settings for photo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.conf.global_settings import STATICFILES_FINDERS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

STATIC_ROOT = os.path.join(BASE_DIR, os.pardir, 'static')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# COMPRESS_ROOT = os.path.join(BASE_DIR, os.pardir, 'static')

# COMPRESS_ENABLED = False

# STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_CSS = {
    'app': {
        'source_filenames': (
            'css/normalize.css',
            'less/application.less',
        ),
        'output_filename': 'app.css',
    }
}

PIPELINE_JS = {
    'app': {
        'source_filenames': (
            'coffee/models/*.coffee',
            'coffee/collections/*.coffee',
            'coffee/routers/*.coffee',
            'coffee/views/*.coffee',
            'coffee/views/manager/*.coffee',
            'coffee/application.coffee',
        ),
        'output_filename': 'app.js',
    }
}

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

PIPELINE_COMPILERS = (
  'pipeline.compilers.coffee.CoffeeScriptCompiler',
  'pipeline.compilers.less.LessCompiler'
)

PIPELINE_COFFEE_SCRIPT_ARGUMENTS = '-b'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i0ilk+_+t3drs&gup_@%5v4asp2cn7(d_3*dcna_n_anxl+y#='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photos',
    'profiles',
    'south',
    'pipeline',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


AUTH_USER_MODEL = 'profiles.User'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/login/'

import project.settings.private as private
AWS_ACCESS_KEY = private.AWS_ACCESS_KEY
AWS_SECRET_KEY = private.AWS_SECRET_KEY

LOG_PATH = os.path.join(BASE_DIR, 'tmp', 'log', 'debug.log')
