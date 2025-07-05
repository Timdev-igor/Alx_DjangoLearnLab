from django.contrib import admin

# Register your models here.
#registerd models in admin -------LOG4
from .models import Category, Photo ,BlogPost

admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(BlogPost)