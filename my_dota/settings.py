import os
from my_dota.base_settings import BASE_DIR

DEBUG = True

SECRET_KEY = "SECRET_KEY"

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATICFILES_DIRS = ("static",)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
