from django.urls import path
from .views import register, user_login, user_logout,BookListCreateAPIView
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    #api
    path("books/",BookListCreateAPIView.as_view(), name="book_list_create"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # New token endpoint
]
