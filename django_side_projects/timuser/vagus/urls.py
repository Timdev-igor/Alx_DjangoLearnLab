from django.urls import path
from .views import login_view, view_post, create_post, edit_post, delete_post ,home_view,post_list

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),  # Home page at 'tim/'
    path('create/', create_post, name='create_post'),
    path('<int:post_id>/', view_post, name='view_post'),
    path('<int:post_id>/edit/', edit_post, name='edit_post'),
    path('<int:post_id>/delete/', delete_post, name='delete_post'),
    path('posts/', post_list, name='post_list'),  # Add this line
]