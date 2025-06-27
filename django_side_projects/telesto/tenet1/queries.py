import os
import django

# Setup Django manually
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")
django.setup()

from .models import Author, Book

def add_author(name):
    author, created = Author.objects.get_or_create(name=name)
    print(f"Author '{name}' added!" if created else f"Author '{name}' already exists!")
    return author

def add_book(title, author_name, price, genre):
    author = Author.objects.get(name=author_name)
    book = Book.objects.create(title=title, price=price, author=author, genre=genre)
    print(f"Book '{book.title}' added!")



if __name__ == "__main__":
    add_author("J.K. Rowling")
    add_book("Harry Potter", "J.K. Rowling", 25.99, "Fiction")
  
