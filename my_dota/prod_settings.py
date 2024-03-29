import os
from .base_settings import *

POSTGRES_USER = "POSTGRES_USER"
POSTGRES_PASSWORD = "POSTGRES_PASSWORD"
POSTGRES_DB = "POSTGRES_DB"
POSTGRES_PORT = "POSTGRES_PORT"
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = ["0.0.0.0"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv(POSTGRES_DB),
        "USER": os.getenv(POSTGRES_USER),
        "PASSWORD": os.getenv(POSTGRES_PASSWORD),
        "HOST": "database",
        "PORT": os.getenv(POSTGRES_PORT),
    }
}

SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

STATIC_ROOT = "static"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
