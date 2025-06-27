from django.http import HttpResponse 
from django.shortcuts import render 

# Create your views here.
def index(request):
    return HttpResponse("Hello, this is the index page!")

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')