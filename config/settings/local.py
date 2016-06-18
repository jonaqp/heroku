from .base import *
from .base import MIDDLEWARE_CLASSES, INSTALLED_APPS

ALLOWED_HOSTS = ["*"]

env_file = str(PROJECT_ROOT.path('security/environ_dev.env'))
environ.Env.read_env(str(env_file))

DEBUG = env.bool('DEBUG_LOCAL')
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
SECRET_KEY = open(SECRET_FILE).read().strip()

SITES_DOMAIN = env('SITE_DOMAIN_LOCAL'),
SITES_SCHEME = env('SITE_SCHEME_LOCAL'),
SITES_NAME = env('SITE_NAME_LOCAL')
SITES = {
    "dev": {"domain": SITES_DOMAIN,
            "scheme": SITES_SCHEME,
            "name": SITES_NAME
            },
}
SITE_ID = "dev"

DATABASES = {
    'default': env.db("DATABASE_URL_LOCAL"),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 10

CACHES = {
    'default': env.cache('REDIS_URL')
}


DJANGO_APPS = (
    'debug_toolbar',
)
THIRD_PARTY_APPS = (
    'storages',
)
LOCAL_APPS = ()

INSTALLED_APPS += DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
CONFIG_DEFAULTS = {
    'RESULTS_CACHE_SIZE': 3,
    'SHOW_COLLAPSED': True,
    'SQL_WARNING_THRESHOLD': 100,
}
INTERNAL_IPS = [
    '127.0.0.1',
]
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_PATCH_SETTINGS = True

ADMIN_URL = env('ADMIN_URL_LOCAL')

# https://www.google.com/settings/security/lesssecureapps
EMAIL_CONFIG = env.email_url('EMAIL_URL_LOCAL',
                             default='smtp://user@:password@localhost:25')
vars().update(EMAIL_CONFIG)
