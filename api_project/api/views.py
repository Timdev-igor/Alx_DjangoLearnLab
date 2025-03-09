from rest_framework import generics, viewsets
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated


# ListAPIView for listing books
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# ViewSet for CRUD operations
class BookViewSet(viewsets.ModelViewSet):  
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users