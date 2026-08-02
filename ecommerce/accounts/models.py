from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the e-commerce platform.
    Keeps username for Django admin/auth compatibility, but email
    is also unique so you can authenticate by email if you wire up
    a custom auth backend later.
    """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_staff_member = models.BooleanField(
        default=False,
        help_text="Staff who manage products/orders (distinct from Django admin superuser)."
    )

    def __str__(self):
        return self.username