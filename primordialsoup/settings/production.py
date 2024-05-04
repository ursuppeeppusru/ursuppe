from .base import *

import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = list(env('ALLOWED_HOSTS'))

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join("db.sqlite3"),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),  # Change this according to your Redis server's URL & port
        'KEY_PREFIX': env('REDIS_PREFIX'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# SITE CONFIG
SITE_NAME=env('SITE_NAME')
HEADER_TEXT=env('HEADER_TEXT')
FOOTER_TEXT=env('FOOTER_TEXT')
SOCIAL_MEDIA=env('SOCIAL_MEDIA')
SOCIAL_MEDIA_URL=env('SOCIAL_MEDIA_URL')

SETTINGS_EXPORT = [
    'SITE_NAME',
    'HEADER_TEXT',
    'FOOTER_TEXT',
    'SOCIAL_MEDIA',
    'SOCIAL_MEDIA_URL',
]

try:
    from .local import *
except ImportError:
    pass
