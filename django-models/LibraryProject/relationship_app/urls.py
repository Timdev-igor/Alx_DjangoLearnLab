
from django.urls import path
from .views import list_books
from django.contrib.auth.views import LoginView, LogoutView 
from .views import LibraryDetailView, SignUpView
from . import views  
from django.contrib.auth import views as auth_views

from django.urls import path
from .views import LibraryDetailView, list_books, registerView, CustomLoginView, CustomLogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    path('books/', list_books, name='list_books'),
    path("register/", registerView.as_view(), name="register"),
    
    # Use custom login and logout views
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # Password Reset Views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Password Change Views
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
