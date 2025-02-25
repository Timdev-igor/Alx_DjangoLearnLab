#writing the queries as stand alon codes without def
""""
from .models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = "J.K. Rowling"
author = Author.objects.get(name=author_name)  # Retrieve author object
books_by_author = Book.objects.filter(author=author)  # Filter books by author
print(f"Books by {author_name}:", list(books_by_author))

# List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print(f"Books in {library_name}:", list(books_in_library))

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(f"Librarian of {library_name}: {librarian}")
"""
from .models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)  # Retrieve author object
    return Book.objects.filter(author=author)  # Filter books by the author instance


# List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Retrieve the librarian for a library
def get_librarian_for_library(library):
    return Librarian.objects.get(library=library)  
