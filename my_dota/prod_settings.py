from .base_settings import *

POSTGRES_USER = 'POSTGRES_USER'
POSTGRES_PASSWORD = 'POSTGRES_PASSWORD'
POSTGRES_DB = 'POSTGRES_DB'
POSTGRES_PORT = 'POSTGRES_PORT'

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env(POSTGRES_DB),
        'USER': env(POSTGRES_USER),
        'PASSWORD': env(POSTGRES_PASSWORD),
        'HOST': 'database',
        'PORT': env(POSTGRES_PORT),
    }
}

STATIC_ROOT = 'static'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
