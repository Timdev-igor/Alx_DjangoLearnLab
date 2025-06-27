from django.contrib import admin
from .models import Book  # Ensure this line is present

admin.site.register(Book) 
# Register your models here.
