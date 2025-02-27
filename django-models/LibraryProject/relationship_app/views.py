from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render , redirect
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView,TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, login_required

# Create your views here.
from django.shortcuts import render
from .models import Book , Author

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin view
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "roles/admin_view.html")

# Librarian view
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "roles/librarian_view.html")

# Member view
@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "roles/member_view.html")

#used some functional based views
def list_books(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    context = {'list_books': books, 'author_list': authors}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# User login view

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

class registerView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

  # Redirect to login page after logout

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "relationship_app/signup.html"