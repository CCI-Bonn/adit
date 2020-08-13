import sys
from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import
from .base import env

# Development settings

DEBUG = True

SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY", default="ug+cbde301nelb)(di0^p21osy3h=t$%2$-8d&0#xlyfj8&==5"
)

ALLOWED_HOSTS = []

if sys.argv and ("test" in sys.argv or "pytest" in sys.argv[0]):
    DATABASES = {
        "default": env.db("SQLITE_URL", default="sqlite:///tmp/adit-sqlite.db")
    }

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["debug_toolbar", "debug_permissions", "django_extensions"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    # LoggingPanel does not work with Django Channels, see
    # https://github.com/django/channels/issues/1204
    # https://github.com/jazzband/django-debug-toolbar/issues/1300
    # "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

CELERY_TASK_EAGER_PROPAGATES = True

INTERNAL_IPS = ["127.0.0.1"]
if env.bool("USE_DOCKER", default=False):
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]