from .base import *
import redis

ALLOWED_HOSTS = ["*"]
env_file = str(PROJECT_ROOT.path('security/environ_prod.env'))
environ.Env.read_env(str(env_file))


DEBUG = env.bool('DEBUG_PROD')
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader',
     TEMPLATES[0]['OPTIONS']['loaders']),
]
SECRET_KEY = env('SECRET_KEY')

SITES_DOMAIN = env('SITE_DOMAIN_PROD')
SITE_SCHEME = env('SITE_SCHEME_PROD')
SITES_NAME = env('SITE_NAME_PROD')
SITES = {
    "pro": {"domain": SITES_DOMAIN,
            "scheme": SITE_SCHEME,
            "name": SITES_NAME
            },
}

MIDDLEWARE_CLASSES += (
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

SITE_ID = "pro"

DATABASES = {
    'default': env.db("DATABASE_URL_PROD"),
}

DATABASES['default']['ATOMIC_REQUESTS'] = True

CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": "ec2-54-163-252-131.compute-1.amazonaws.com:14839",
         "OPTIONS": {
             "PASSWORD": 'p1j4freu50seok8jvctnkagq83i',
             "DB": 0,
         }
    }
}


SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

DJANGO_APPS = (
)

THIRD_PARTY_APPS = (
    'storages',
    'gunicorn',
)
LOCAL_APPS = ()

INSTALLED_APPS += DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

ADMIN_URL = env('ADMIN_URL_PROD')

EMAIL_CONFIG = env.email_url('EMAIL_URL_PROD')
vars().update(EMAIL_CONFIG)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if SITE_SCHEME == 'https':
    SECURE_HSTS_SECONDS = env.int('DJANGO_SECURE_HSTS_SECONDS', default=60)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --------------------AMAZON STORAGE----------------------------------

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_PRELOAD_METADATA = True
AWS_HEADERS = {
    'Cache-Control': u'max-age={0:d}, s-maxage={1:d}, must-revalidate'.format(
        AWS_EXPIRY, AWS_EXPIRY)
}

STATICFILES_LOCATION = 'static'
STATIC_URL = u"https://{0:s}/{1:s}/".format(AWS_S3_CUSTOM_DOMAIN,
                                            STATICFILES_LOCATION)
STATICFILES_STORAGE = 'core.custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = u"https://{0:s}/{1:s}/".format(AWS_S3_CUSTOM_DOMAIN,
                                           MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'core.custom_storages.MediaStorage'

