
from django.http import HttpResponse
  # Assuming you have a BookForm defined in forms.py
 # Assuming you have a Book model defined in models.py

# Role Check Functions
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login  # Import for handling user login
from django.contrib.auth.forms import UserCreationForm  # Import for user registration form
from .models import UserProfile
from .models import Book
from django.views.generic.detail import DetailView 
from .models import Library
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.decorators import permission_required


# Role-checking functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin View
# Views
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # Create a UserProfile for the user with a default role (e.g., 'Member')
            UserProfile.objects.create(user=user, role='Member')
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to the home page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Role-checking functions
@login_required
def list_books(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

# Add a book (requires 'can_add_book' permission)**
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})

# Edit a book (requires 'can_change_book' permission)**
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})

# Delete a book (requires 'can_delete_book' permission)**
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/confirm_delete.html', {'book': book})