from django.contrib.auth import login  # This import was missing
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, Author, UserProfile
from .models import Library

# Ensure UserProfile is created when a User is registered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Role Check Functions
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"

# Role-Based Views
@user_passes_test(is_admin)
@login_required
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(is_librarian)
@login_required
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_member)
@login_required
def member_view(request):
    return render(request, "relationship_app/member_view.html")

# Functional View: List Books
def list_books(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    context = {'list_books': books, 'author_list': authors}
    return render(request, 'relationship_app/list_books.html', context)

# Detail View for Library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# User Authentication Views
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

# User Registration View
class registerView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)  # Calls the parent class method to save the form
        user = self.object  # The created user
        UserProfile.objects.create(user=user, role='Member')  # Create a user profile
        login(self.request, user)  # Log in the user immediately after registration
        return response  
    
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/signup.html'  # Make sure you have this template
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Optionally, you can perform some additional logic here, like setting roles
        response = super().form_valid(form)
        user = self.object
        # Create a default user profile with 'Member' role
        UserProfile.objects.create(user=user, role='Member')
        return response