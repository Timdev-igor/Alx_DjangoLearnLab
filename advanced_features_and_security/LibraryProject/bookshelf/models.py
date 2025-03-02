

# Create your models here.



from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define user roles
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractUser):
    # Define role choices
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    ]

    # Additional fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

    # Use the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username


# Automatically create a UserProfile when a new User is created
@receiver(post_save, sender=CustomUser)
def set_default_role(sender, instance, created, **kwargs):
    if created:
        instance.role = CustomUser.MEMBER
        instance.save()


# Author Model
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publication_year = models.IntegerField(default=2023)

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        ]

    def __str__(self):
        return self.title


# Library Model
class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name="libraries")

    def __str__(self):
        return self.name


# Librarian Model
class Librarian(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="librarian")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="librarians")

    def __str__(self):
        return self.user.username