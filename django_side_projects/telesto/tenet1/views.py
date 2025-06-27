from django.shortcuts import render 
from .models import Book ,Library
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView ,TemplateView
from django.contrib.auth.views import LoginView ,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

# Create your views here.
from django.http import HttpResponse

def hello_view(request):
    """A basic function view returning a greeting message."""
    return HttpResponse("Hello, World!")

class LoginCustomView (LoginView):
    template_name = 'tenet1/login.html'
    redirect_authenticated_user = True  # Redirect already logged-in users


class LogoutCustomview (LogoutView):
    template_name= 'tenet1/logout.html' 

def get_books(request):
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, 'tenet1/book_list.html', context)

def library_view(request):
    library = Library.objects.all()
    context ={'library' :library}
    return render (request, 'tenet1/libraries.html', context)

# creating users /////////////////////////


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "tenet1/signup.html"
    success_url = reverse_lazy("login")  # Redirect after signup

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)  # Log in the user after signup
        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'tenet1/profile.html'
    
    # Redirect to login page if the user is not authenticated
    login_url = '/login/'  # Ensure this matches your LOGIN_URL in settings.py
    redirect_field_name = 'next'  # Allows redirecting back after login

