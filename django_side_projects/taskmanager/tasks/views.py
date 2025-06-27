from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework import generics , viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#creating viewsets ViewSets provide a high-level abstraction for creating API views 
# that handle common CRUD operations on models. Instead of defining separate views

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


    @action(detail=True, methods=['post'], url_path='mark_as_important', name='Mark as Important')
    def mark_important(self, request, pk=None):
        """Custom action to mark a comment as important."""
        comment = self.get_object()
        comment.is_important = True
        comment.save()
        return Response({'status': 'Comment marked as important'})