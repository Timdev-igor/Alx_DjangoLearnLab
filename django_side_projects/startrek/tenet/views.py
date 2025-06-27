from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    # Custom action to like a blog post
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        blog_post = self.get_object()
        blog_post.likes += 1
        blog_post.save()
        return Response({'status': 'liked', 'likes': blog_post.likes})