from django.urls import path
from .views import  LibraryDetailView, SignUpView 
from .views import CustomLoginView, CustomLogoutView, RegisterView
from .views import book_list
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    path('books/', book_list , name='book-list'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

   
    path("signup/", SignUpView.as_view(), name="signup"),

    # Password Reset Views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Password Change
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]