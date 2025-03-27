from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#created user model
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    #symmetrical=False → Ensures that if User A follows User B,
    #  it doesn’t mean User B follows User A automatically.
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def __str__(self):
        return self.username