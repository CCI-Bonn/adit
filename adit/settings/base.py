"""
Django settings for adit project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from pathlib import Path
import environ
from celery.schedules import crontab

env = environ.Env()

# The base directory of the project (the root of the repository)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

BASE_URL = env.str("BASE_URL", default="")

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "channels",
    "adit.accounts.apps.AccountsConfig",
    "registration",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "revproxy",
    "loginas",
    "crispy_forms",
    "django_tables2",
    "rest_framework",
    "bootstrap4",
    "adit.main.apps.MainConfig",
    "adit.selective_transfer.apps.SelectiveTransferConfig",
    "adit.batch_transfer.apps.BatchTransferConfig",
    "adit.continuous_transfer.apps.ContinuousTransferConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "adit.main.middlewares.MaintenanceMiddleware",
    "adit.main.middlewares.TimezoneMiddleware",
]

# We need this as we embed Django Admin and Celery Flower in an iframe.
X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "adit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "adit.main.site.base_context_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "adit.wsgi.application"

# In production a PostgreSQL (psql://...) URL is passed by using an
# environment variable set in in docker-compose.prod.yml.
DATABASES = {"default": env.db(default="sqlite:///./adit-sqlite.db")}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOG_FOLDER = Path(env.str("LOG_FOLDER", default="./"))

# See following examples:
# https://github.com/django/django/blob/master/django/utils/log.py
# https://cheat.readthedocs.io/en/latest/django/logging.html
# https://stackoverflow.com/a/7045981/166229
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(name)-12s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %Z",
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %Z",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "log_file": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_FOLDER / "adit.log"),
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 10,
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "adit": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "pynetdicom": {"handlers": ["console"], "level": "WARNING"},
        "pydicom": {"handlers": ["console"], "level": "WARNING"},
    },
    "root": {"handlers": ["console", "log_file"], "level": "WARNING"},
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "de-de"

# We don't want to have German translations, but everything in English
USE_I18N = False

# But we still want to have dates and times localized
USE_L10N = True

USE_TZ = True

TIME_ZONE = "UTC"

# All REST API requests must come from authenticated clients
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ]
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = (BASE_DIR / "adit" / "static",)

STATIC_URL = "/static/"

STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default=(BASE_DIR / "staticfiles"))

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Where to redirect to after login
LOGIN_REDIRECT_URL = "home"

# For crispy forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

# This seems to be imporant for development on Gitpod as CookieStorage
# and FallbackStorage does not work there.
# Seems to be the same problem with Cloud9 https://stackoverflow.com/a/34828308/166229
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_SUBJECT_PREFIX = "[ADIT] "

# An Email address used by the ADIT server to notify about finished jobs and
# management notifications.
SERVER_EMAIL = env.str("DJANGO_SERVER_EMAIL", default="support@adit.test")
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# A support Email address that is presented to the users where
# they can get support.
SUPPORT_EMAIL = env.str("SUPPORT_EMAIL", default=SERVER_EMAIL)

# Also used by django-registration-redux to send account approval emails
admin_first_name = env.str("ADMIN_FIRST_NAME", default="ADIT")
admin_last_name = env.str("ADMIN_LAST_NAME", default="Admin")
admin_full_name = admin_first_name + " " + admin_last_name
ADMINS = [
    (
        admin_full_name,
        env.str("ADMIN_EMAIL", default="admin@adit.test"),
    )
]

# Settings for django-registration-redux
REGISTRATION_FORM = "adit.accounts.forms.RegistrationForm"
ACCOUNT_ACTIVATION_DAYS = 14
REGISTRATION_OPEN = True

# Channels
ASGI_APPLICATION = "adit.routing.application"

# Redis is used as Celery result backend and as LRU cache for patient IDs.
REDIS_URL = env.str("REDIS_URL", default="redis://localhost:6379/0")

# Celery
# see https://github.com/celery/celery/issues/5026 for how to name configs
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env.str("RABBITMQ_URL", default="amqp://localhost")
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_ROUTES = {
    "adit.batch_transfer.tasks.transfer_request": {"queue": "batch_transfer"},
    "adit.continuous_transfer.tasks.transfer_task": {"queue": "continuous_transfer"},
}
CELERY_BEAT_SCHEDULE = {
    "check-disk-space": {
        "task": "adit.main.tasks.check_disk_space",
        "schedule": crontab(minute=0, hour=7),  # execute daily at 7 o'clock UTC
    }
}

# Flower is integrated in ADIT by using an reverse proxy (django-revproxy).
# This allows to use the authentication of ADIT.
FLOWER_HOST = env.str("FLOWER_HOST", default="localhost")
FLOWER_PORT = env.int("FLOWER_PORT", default=5555)

###
# ADIT specific settings
###

# General ADIT settings
ADIT_AE_TITLE = env.str("ADIT_AE_TITLE", default="ADIT1")

# The delimiter of the CSV file that contains the requests for
# the batch transfer
BATCH_FILE_CSV_DELIMITER = ";"

# ADIT uses a cache for patients so that not the DICOM server must not
# always be queried. This is how many patients fit into the cache.
BATCH_PATIENT_CACHE_SIZE = 10000

# Usually a transfer job must be verified by an admin. By setting
# this option to True ADIT will schedule unverified transfers
# (and directly set the status of the job to PENDING).
BATCH_TRANSFER_UNVERIFIED = True
CONTINUOUS_TRANSFER_UNVERIFIED = True

# A timezone that is used for users of the web interface.
# It is also used by the Scheduler to calculate if a batch or
# continuous transfer should run.
SERVER_TIME_ZONE = env.str("SERVER_TIME_ZONE", default=None)
