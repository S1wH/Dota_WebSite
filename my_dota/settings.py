import os
from .base_settings import *

DEBUG = True
SECRET_KEY = "SECRET_KEY"
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

STATICFILES_DIRS = ("static",)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'paulgomozov@gmail.com'
EMAIL_HOST_PASSWORD = 'otfgolaieiwkfraw'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ALLOWED_HOSTS = []
