from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    summary = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title