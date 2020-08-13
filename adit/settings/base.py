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

env = environ.Env()

# The base directory of the project (where README.md is located)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "channels",
    "accounts.apps.AccountsConfig",
    "registration",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "revproxy",
    "loginas",
    "crispy_forms",
    "django_tables2",
    "bootstrap4",
    "main.apps.MainConfig",
    "selective_transfer.apps.SelectiveTransferConfig",
    "batch_transfer.apps.BatchTransferConfig",
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
    "main.middlewares.MaintenanceMiddleware",
]

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
                "main.site.inject_context",
            ],
        },
    },
]

WSGI_APPLICATION = "adit.wsgi.application"

DATABASES = {"default": env.db(default="psql://postgres@127.0.0.1:5432/postgres")}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "UTC"

# We don't want to have German translations, but everything in English
USE_I18N = False

# But we still want to have dates and times localized
USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

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

# Also used by django-registration-redux to send account approval emails
admin_first_name = env.str("ADMIN_FIRST_NAME", default="ADIT")
admin_last_name = env.str("ADMIN_LAST_NAME", default="Support")
admin_full_name = admin_first_name + " " + admin_last_name
ADMINS = [(admin_full_name, env.str("ADMIN_EMAIL", default="support@adit.test"),)]

# Settings for django-registration-redux
REGISTRATION_FORM = "accounts.forms.RegistrationForm"
ACCOUNT_ACTIVATION_DAYS = 14
REGISTRATION_OPEN = True

# Channels
ASGI_APPLICATION = "adit.routing.application"

# Celery
# see https://github.com/celery/celery/issues/5026 for how to name configs
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
REDIS_URL = env.str("REDIS_URL", default="redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_ROUTES = {"batch_transfer.tasks.batch_transfer_task": {"queue": "low"}}

# Flower is integrated in ADIT by using an reverse proxy (django-revproxy).
# This allows to use the authentication of ADIT.
FLOWER_HOST = env.str("FLOWER_HOST", default="localhost")
FLOWER_PORT = env.int("FLOWER_PORT", default=5555)

###
# ADIT specific settings
###

# General ADIT settings
ADIT_AE_TITLE = env.str("ADIT_AE_TITLE", default="ADIT")

# Static (non database) settings for batch_transfer app
ADIT_CACHE_FOLDER = env.str("ADIT_CACHE_FOLDER", "/tmp/adit_cache_folder")

# The delimiter of the CSV file that contains the requests for
# the batch transfer
BATCH_FILE_CSV_DELIMITER = ";"