from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # Add this line
from .models import Book
from .serializers import BookSerializer

# ListView: Retrieve all books
class BookListView(generics.ListAPIView):
    """
    View for listing all books.

    - GET: Returns a list of all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users


# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a single book by its ID.

    - GET: Returns details of a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users


# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    View for creating a new book.

    - POST: Creates a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create books


# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    View for updating an existing book.

    - PUT: Fully updates a book.
    - PATCH: Partially updates a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update books


# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    View for deleting a book.

    - DELETE: Deletes a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete books