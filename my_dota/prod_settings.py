from .base_settings import *

POSTGRES_USER = 'POSTGRES_USER'
POSTGRES_PASSWORD = 'POSTGRES_PASSWORD'
POSTGRES_DB = 'POSTGRES_DB'
POSTGRES_PORT = 'POSTGRES_PORT'

print('--------------')
print(os.getenv(POSTGRES_DB))
print(os.getenv(POSTGRES_USER))
print(os.getenv(POSTGRES_PASSWORD))
print(os.getenv(POSTGRES_PORT))
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv(POSTGRES_DB),
        'USER': os.getenv(POSTGRES_USER),
        'PASSWORD': os.getenv(POSTGRES_PASSWORD),
        'HOST': 'database',
        'PORT': os.getenv(POSTGRES_PORT),
    }
}

STATIC_ROOT = 'static'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
