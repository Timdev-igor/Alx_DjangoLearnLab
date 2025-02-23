# Delete a Book Entry in Django ORM

## Delete the Book Instance
```python
from bookshelf.models import Book

# Retrieve the book instance
book = Book.objects.get(title="1984")

# Delete the book
book.delete()

# Confirm deletion by retrieving all books
books = Book.objects.all()
print(books)  # Expected output: <QuerySet []> if no other books exist
