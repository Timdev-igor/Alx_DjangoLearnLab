
from django.urls import path
from .views import list_books , add_book, edit_book, delete_book
from django.contrib.auth.views import LoginView, LogoutView 
from .views import LibraryDetailView ,SignUpView
from . import views  
from django.contrib.auth import views as auth_views
 
#python manage.py makemigrations
urlpatterns = [
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    path('books/', list_books, name='list_books'),
    path("login/", LoginView.as_view(template_name="authentication/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="authentication/logout.html"), name="logout"),

   
    path("signup/", SignUpView.as_view(), name="signup"),

    # Password Reset Views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Password Change
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),


    path("add_book/", add_book, name="add_book"),  # ✅ Explicitly matches "add_book/"
    path("edit_book/<int:book_id>/", edit_book, name="edit_book"),  # ✅ Explicitly matches "edit_book/"
    path("books/", list_books, name="list_books"),
    path("delete_book/<int:book_id>/", delete_book, name="delete_book"),#
]