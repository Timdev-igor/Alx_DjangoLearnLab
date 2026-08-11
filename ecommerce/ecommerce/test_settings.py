# ecommerce/test_settings.py
from .settings import *

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True  # so exceptions in tasks actually fail the test, not fail silently
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'  # captures sent emails in memory for assertions