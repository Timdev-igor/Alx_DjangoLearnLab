# create urls ---------- LOG 6
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('upload/', views.upload_photo, name='upload'),
]