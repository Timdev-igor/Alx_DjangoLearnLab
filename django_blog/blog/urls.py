from django.urls import path
from .views import user_login, user_logout, register,profile
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
#post views///////////
    path('', PostListView.as_view(), name='post-list'),
    # Home page: List all posts
    # View a single post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # Create a new post
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # Update an existing post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # Delete a post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]