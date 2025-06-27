import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "experiment_1.settings")
django.setup()

from typeapp_1.models import Author, Book

# Create Authors
author1 = Author.objects.create(name="George Orwell")
author2 = Author.objects.create(name="Jane Austen")

# Create Books
book1 = Book.objects.create(title="1984", author=author1)
book2 = Book.objects.create(title="Pride and Prejudice", author=author2)
book3 = Book.objects.create(title="Animal Farm", author=author1)


# Fetch and display all books
books = Book.objects.all()
for book in books:
    print(f"{book.title} by {book.author.name if book.author else 'Unknown Author'}")

print("Database populated successfully!")

# **Delete a Book**
book_to_delete = Book.objects.filter(title="1984").first()  # Fetch book by title
if book_to_delete:
    book_to_delete.delete()
    print("\nDeleted '1984' from the database.")

