
from django.urls import path
from .views import book_list , add_book, edit_book, delete_book
from django.contrib.auth.views import LoginView, LogoutView 
from .views import LibraryDetailView ,SignUpView
from . import views  
from django.contrib.auth import views as auth_views

 
#python manage.py makemigrations
urlpatterns = [
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    path('books/', views.book_list, name='book_list'),
    path("login/", LoginView.as_view(template_name="bookshelf/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="bookshelf/logout.html"), name="logout"),
    path('register/', views.register, name='register'),
    path('search/', views.search_books, name='search_books'),

   
    path("signup/", SignUpView.as_view(), name="signup"),
    path('admin-dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian-dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member-dashboard/', views.member_view, name='member_dashboard'),
    path('profile/', views.profile_view, name='profile'),

    path('success/', views.success_page, name='success_page'),

    # Password Reset Views
path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name='bookshelf/password_reset_form.html',
    email_template_name='bookshelf/password_reset_email.html',
    subject_template_name='bookshelf/password_reset_subject.txt',
), name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    template_name='bookshelf/password_reset_done.html'
), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='bookshelf/password_reset_confirm.html'
), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    template_name='bookshelf/password_reset_complete.html'
), name='password_reset_complete'),

    path("add_book/", add_book, name="add_book"),  # ✅ Explicitly matches "add_book/"
    path("edit_book/<int:book_id>/", edit_book, name="edit_book"),  # ✅ Explicitly matches "edit_book/"
    path("books/", views.book_list, name="book_list"),
    path("delete_book/<int:book_id>/", delete_book, name="delete_book"),#
    path('example-form/', views.example_form_view, name='example_form'),


path('add_library/', views.add_library, name='add_library'),
path('libraries/', views.library_list, name='library_list'),
path('authors/', views.author_list, name='author_list'),
path('add_author/', views.add_author, name='add_author'),
path('users/', views.user_list, name='user_list'),
path('select_book/<int:book_id>/', views.select_book, name='select_book'),
path('my-selections/', views.my_selections, name='my_selections'),

]