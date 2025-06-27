from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

#permissions implementation 
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_publish_post", "Can publish post"),
        ]

    def __str__(self):
        return self.title

#API///////////

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    published_date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now) 

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField()
