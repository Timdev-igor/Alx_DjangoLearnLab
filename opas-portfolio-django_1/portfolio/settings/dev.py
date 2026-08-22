import environ
from .base import *  # noqa: F401,F403
from .base import BASE_DIR

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env.dev")

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Locally, uploaded images just sit on disk under MEDIA_ROOT — no
# storage backend needed. Azure Blob Storage only kicks in on prod.py.
