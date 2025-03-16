from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework as filters

# ListView: Retrieve all books with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    """
    View for listing all books with filtering, searching, and ordering capabilities.

    - GET: Returns a list of all books.
    - Filter by: title, author, publication_year (using exact matching)
    - Search by: title, author (using the `search` query parameter)
    - Order by: title, publication_year (using the `ordering` query parameter)

    Example Requests:
    - Filter: /api/books/?title=Example&author=John
    - Search: /api/books/?search=Example
    - Order: /api/books/?ordering=title
    """
    ...
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users

    # Add searching and ordering backends
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # Fields to search by
    search_fields = ['title', 'author']

    # Fields to order by
    ordering_fields = ['title', 'publication_year']

    def get_queryset(self):
        """
        Optionally filters the queryset based on query parameters in the URL.
        Uses exact matching for filtering.
        """
        queryset = super().get_queryset()

        # Filter by title (exact match)
        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset.filter(title=title)

        # Filter by author (exact match)
        author = self.request.query_params.get('author')
        if author is not None:
            queryset = queryset.filter(author=author)

        # Filter by publication year (exact match)
        publication_year = self.request.query_params.get('publication_year')
        if publication_year is not None:
            queryset = queryset.filter(publication_year=publication_year)

        return queryset


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