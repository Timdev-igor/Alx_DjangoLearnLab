from django.urls import path , include
from .views import BookListCreateAPIView, ProductListCreateAPIView , CommentViewSet ,PostListCreateView, PostDetailView,BookViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'books',BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    

]