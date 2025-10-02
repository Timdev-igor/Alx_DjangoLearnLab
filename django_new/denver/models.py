from django.db import models

# Create your models here.
# created photo model LOG 3
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class PlayList_Album(models.Model):
    image = models.ImageField(upload_to='blog_images/')
    title = models.TextField()
    artist_details= models.TextField()
    producer_details = models.TextField()
    release_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

class music_play(models.Model):
    image = models.ImageField(upload_to='blog_images/')
    title = models.TextField()
    