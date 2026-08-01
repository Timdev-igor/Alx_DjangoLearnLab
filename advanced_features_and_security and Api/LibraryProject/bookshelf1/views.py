
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django import forms

from .forms import UserRegisterForm, ExampleForm,LibraryForm,AuthorForm
from .models import (
    Book,
    Author,
    Library,
    Librarian,
    CustomUser,
    Post,
    BookSelection,
)

# Role-checking functions
# Role-checking functions
def is_admin(user):
    return user.role == 'Admin'

def is_librarian(user):
    return user.role == 'Librarian'

def is_member(user):
    return user.role == 'Member'

def is_admin_or_librarian(user):
    return user.is_authenticated and user.role in ('Admin', 'Librarian')

# Views
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'bookshelf/admin_view.html')

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'bookshelf/librarian_view.html')

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'bookshelf/member_view.html')

# User Registration View

@login_required
def profile_view(request):
    role = request.user.role
    if role == 'Admin':
        return redirect('admin_dashboard')
    elif role == 'Librarian':
        return redirect('librarian_dashboard')
    elif role == 'Member':
        return redirect('member_dashboard')
    else:
        return render(request, 'bookshelf/profile.html', {'user': request.user})

# Role-checking functions
@login_required
def book_list(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'bookshelf/book_list.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'
    context_object_name = 'library'

class SignUpView(CreateView):
    form_class = UserRegisterForm  # Django's built-in user creation form
    success_url = reverse_lazy('login')  # Redirect to login page after successful signup
    template_name = 'bookshelf/signup.html'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

# Add a book (requires 'can_add_book' permission)**
@login_required
@user_passes_test(is_admin_or_librarian, login_url='/login/')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})


@login_required
@user_passes_test(is_admin_or_librarian, login_url='/login/')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})


@login_required
@user_passes_test(is_admin_or_librarian, login_url='/login/')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/confirm_delete.html', {'book': book})


@login_required
def book_list(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        "authors": authors,
        'can_manage': request.user.role in ('Admin', 'Librarian'),
    })

@login_required
@permission_required('bookshelf1.can_view', raise_exception=True)
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

@login_required
@permission_required('bookshelf1.can_create', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content)
        return redirect('view_posts')
    return render(request, 'create_post.html')

@login_required
@permission_required('bookshelf1.can_edit', raise_exception=True)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('view_post', post_id=post.id)
    return render(request, 'edit_post.html', {'post': post})

@login_required
@permission_required('bookshelf1.can_delete', raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('view_posts')

def search_books(request):
    query = request.GET.get('q')
    if query:
        # Use Django ORM to safely query the database
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def example_form_view(request):
    """
    View to handle the ExampleForm.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to the database or send an email)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            print(f"Name: {name}, Email: {email}, Message: {message}")  # Example processing
            return redirect('success_page')  # Redirect to a success page
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/example_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'bookshelf/register.html', {'form': form})

def success_page(request):
    return render(request, 'bookshelf/success.html')



@login_required
def select_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    BookSelection.objects.get_or_create(user=request.user, book=book)
    return redirect('my_selections')


@login_required
def my_selections(request):
    selections = BookSelection.objects.filter(user=request.user).select_related('book')
    return render(request, 'bookshelf/my_selections.html', {'selections': selections})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def add_library(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library_list')
    else:
        form = LibraryForm()
    return render(request, 'bookshelf/library_form.html', {'form': form})


@login_required
def library_list(request):
    libraries = Library.objects.all()
    return render(request, 'bookshelf/library_list.html', {
        'libraries': libraries,
        'can_manage': request.user.role == 'Admin',
    })

@login_required
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'bookshelf/author_list.html', {
        'authors': authors,
        'can_manage': request.user.role in ('Admin', 'Librarian'),
    })


@login_required
@user_passes_test(is_admin_or_librarian, login_url='/login/')
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'bookshelf/author_form.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'bookshelf/user_list.html', {'users': users})