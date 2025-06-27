from django.db import models

# Create your models here.
#created book model to test api
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    is_important = models.BooleanField(default=False)  # New field