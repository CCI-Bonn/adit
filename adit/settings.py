"""
Django settings for adit project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from datetime import time

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r&!5(b4ha2a(wnc#&tv-5s)dgf#4rbj_gon5ua05a-ufs#k3ue'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_permissions',
    'debug_toolbar',
    'loginas',
    'crispy_forms',
    'django_tables2',
    'bootstrap4',
    'django_rq',
    'main.apps.MainConfig',
    'batch_transfer.apps.BatchTransferConfig'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middlewares.MaintenanceMiddleware'
]

ROOT_URLCONF = 'adit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.site.inject_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'adit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'adit_dev',
        'USER': 'gitpod',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# TODO: Maybe use a separate settings file for testing, development and
# production.
if sys.argv and ('test' in sys.argv or 'pytest' in sys.argv[0]):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# For crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

INTERNAL_IPS = ['127.0.0.1']

LOGIN_REDIRECT_URL = 'home'

# This seems to be imporant for development on Gitpod as CookieStorage
# and FallbackStorage does not work there.
# Seems to be the same problem with Cloud9 https://stackoverflow.com/a/34828308/166229
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Django RQ settings
RQ_QUEUES = {
    'default': { # used by rqscheduler
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0
    },
    'batch_transfer': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0
    }
}
RQ_SHOW_ADMIN_LINK = True

# Also used by django-registration-redux
ADMINS = [('Kai', 'kai.schlamp@med.uni-heidelberg.de'),]

# Settings for django-registration-redux
REGISTRATION_FORM = 'accounts.forms.RegistrationForm'
ACCOUNT_ACTIVATION_DAYS = 14
REGISTRATION_OPEN = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # TODO provide SMTP details, see https://docs.djangoproject.com/en/dev/topics/email/

# For Django-RQ to make all jobs run immediatly
if DEBUG:
    for _, queueConfig in RQ_QUEUES.items():
        queueConfig['ASYNC'] = False

# General ADIT settings
ADIT_AE_TITLE = 'ADIT'

# Static (non database) settings for batch_transfer app
BATCH_TRANSFER_CACHE_FOLDER = '/tmp/adit_batch_transfer'
