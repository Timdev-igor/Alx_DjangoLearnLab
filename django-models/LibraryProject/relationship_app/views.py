from django.shortcuts import render , redirect
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
# Create your views here.
from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})



class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# User login view

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'authentication/logout.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')