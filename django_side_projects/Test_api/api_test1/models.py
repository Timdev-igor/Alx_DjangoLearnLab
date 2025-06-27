from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField(null=True, blank=True) 

    
    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)


    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]  # Show first 50 characters of the comment
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)