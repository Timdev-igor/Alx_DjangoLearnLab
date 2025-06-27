
from rest_framework import generics ,viewsets
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm
from rest_framework.permissions import IsAuthenticated
from .models import Author, Book, Review
from .serializers import AuthorSerializer, BookSerializer, ReviewSerializer

# ✅ User Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user automatically after registration
            return redirect('home')  # Redirect to home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'useraccount/register.html', {'form': form})

# ✅ User Login View
def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'useraccount/login.html', {'form': form})

# ✅ User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

#api-project

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all().select_related('author').prefetch_related('reviews')
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict to logged-in users

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication
