from rest_framework.generics import ListAPIView 
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(ModelViewSet):  # ✅ This ensures all CRUD operations are handled
    queryset = Book.objects.all()
    serializer_class = BookSerializer