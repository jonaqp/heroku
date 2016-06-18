from .base import *

DEBUG = True

env_file = str(PROJECT_ROOT.path('security/environ_dev.env'))
environ.Env.read_env(str(env_file))


DATABASES = {
    'default': env.db('SQLITE_URL_LOCAL')
}

# CELERY_ALWAYS_EAGER = True
# CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
# BROKER_BACKEND = 'memory'

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
ADMIN_URL = env('ADMIN_URL_LOCAL')
