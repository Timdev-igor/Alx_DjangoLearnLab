from django.contrib import admin

# Register your models here.
from .models import BlogPost, Comment

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'likes')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'blog_post', 'created_at')