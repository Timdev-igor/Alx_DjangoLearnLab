from django.urls import path ,include
from .views import LoginCustomView, LogoutCustomview, hello_view  ,get_books ,library_view,SignUpView
from .views import ProfileView 
urlpatterns = [
    path('hello/', hello_view, name='hello'),
    path('login/', LoginCustomView.as_view(), name='login'),
    path("logout/", LogoutCustomview.as_view(), name="logout"),
    path('books/' ,get_books ,name='books'),
    path('library/' ,library_view,name='library'),
    path('signup/',SignUpView.as_view() , name='signup'),
    path('', include("django.contrib.auth.urls")),#django inbuilt auth views
   path('profile/', ProfileView.as_view(), name='profile'),
]
