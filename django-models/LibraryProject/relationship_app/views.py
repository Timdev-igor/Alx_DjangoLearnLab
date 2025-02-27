from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render , redirect
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView,TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout

# Create your views here.
from django.shortcuts import render
from .models import Book , Author

#used some functional based views
def book_list(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    context = {'book_list': books, 'author_list': authors}
    return render(request, 'books/book_list.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# User login view

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'authentication/logout.html'

class registerView(CreateView):
    form_class = UserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')

  # Redirect to login page after logout

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "authentication/signup.html"