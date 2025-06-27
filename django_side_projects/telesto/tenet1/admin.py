from django.contrib import admin
from .models import Book , Library ,Author


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', )
    search_fields = ('title', 'author')

class LibraryAdmin(admin.ModelAdmin):
      list_display = ('title', )
      search_fields =('title',)




admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Library ,LibraryAdmin)
