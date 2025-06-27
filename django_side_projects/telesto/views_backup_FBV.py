"""from django.shortcuts import render 
from .models import Book ,Library
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

def hello_view(request):
    A basic function view returning a greeting message. # type: ignore
    return HttpResponse("Hello, World!")

def login_page(request):
    return render(request , 'tenet1/login.html')

def logout_page(request):
    return render(request, 'tenet1/logout.html')

def get_books(request):
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, 'tenet1/book_list.html', context)

def library_view(request):
    library = Library.objects.all()
    context ={'library' :library}
    return render (request, 'tenet1/libraries.html', context)

# creating users /////////////////////////
class SignUpView (CreateView):
    form_class = UserCreationForm
    redirects to login when user is created
    success_url = reverse_lazy('login') 
    template_name = 'tenet1/signup.html'

@login_required
def profile_view(request):
    return render(request, 'tenet1/profile.html')"""