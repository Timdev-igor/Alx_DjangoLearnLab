from django.urls import path ,include
from .views import BookListCreateAPIView
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
""" path("books/", BookListCreateAPIView.as_view(), name="book_list_create"),#define url for my api view """
urlpatterns = [
    
    path('', include(router.urls)),
]
