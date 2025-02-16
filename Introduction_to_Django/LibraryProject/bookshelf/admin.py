from django.contrib import admin

# Register your models here.
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Display fields in list view
    search_fields = ('title', 'author')  # Enable search functionality
    list_filter = ('publication_year',)  # Add filtering by publication year

admin.site.register(Book, BookAdmin)