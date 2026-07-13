from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend


# ListCreateView: List all books (GET) and create a new one (POST)
class BookListView(generics.ListCreateAPIView):
    """
    - GET: Returns a list of all books (authenticated users only).
    - POST: Creates a new book (authenticated users only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']

    def get_queryset(self):
        queryset = super().get_queryset()

        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset.filter(title=title)

        author = self.request.query_params.get('author')
        if author is not None:
            queryset = queryset.filter(author__name=author)

        publication_year = self.request.query_params.get('publication_year')
        if publication_year is not None:
            queryset = queryset.filter(publication_year=publication_year)

        return queryset


# RetrieveUpdateDestroyView: Get, update, or delete a single book by ID
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    - GET: Returns details of a specific book.
    - PUT/PATCH: Updates a specific book.
    - DELETE: Deletes a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]