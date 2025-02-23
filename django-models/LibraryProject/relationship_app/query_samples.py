from .models import Author, Book, Library,librarian
# Use select_related() to reduce queries for ForeignKey relationships
def get_books_with_authors():
    return Book.objects.select_related('author').all()

# Use prefetch_related() for ManyToMany relationships
def get_libraries_with_books():
    return Library.objects.prefetch_related('books').all()

# Use values() to fetch only necessary fields
def get_author_names():
    return Author.objects.values_list('name', flat=True)

# Use bulk_create() for inserting multiple records efficiently
def add_multiple_books():
    books = [
        Book(title='Book 1', author_id=1),
        Book(title='Book 2', author_id=2),
    ]
    Book.objects.bulk_create(books)

# Use bulk_update() for updating multiple records efficiently
def update_book_titles():
    books = Book.objects.filter(author__name='John Doe')
    for book in books:
        book.title = 'Updated: ' + book.title
    Book.objects.bulk_update(books, ['title'])

# Use exists() instead of checking queryset length
def author_exists(name):
    return Author.objects.filter(name=name).exists()

# Use count() instead of len(queryset)
def book_count():
    return Book.objects.count()

# Use only() or defer() to optimize queries by reducing fetched fields
def get_book_titles():
    return Book.objects.only('title').all()

# Use update() for bulk updates instead of looping through objects
def mark_all_books_checked_out():
    Book.objects.update(is_checked_out=True)

def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)
    
def get_librarian_for_library(library_name):
    return Librarian.objects.get(library__name=library_name)


# Use delete() for bulk deletions instead of looping through objects
def delete_old_books():
    Book.objects.filter(publication_year__lt=2000).delete()

# Retrieve objects using indexed fields for efficiency
def get_book_by_id(book_id):
    return Book.objects.get(id=book_id)

# Avoid unnecessary ordering if not needed
def get_all_books_unordered():
    return Book.objects.order_by()
