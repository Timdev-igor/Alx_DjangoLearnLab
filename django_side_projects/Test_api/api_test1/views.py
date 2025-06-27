from rest_framework import generics , viewsets
from .models import Book ,Product , Comment , Post# Import the Book model
from .serializers import BookSerializer 
from .serializers import ProductSerializer ,CommentSerializer ,PostSerializer
from rest_framework.decorators import action 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

#//auth
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()  # Use the Book model
    serializer_class = BookSerializer  # Use the BookSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=['post'])
    def flag(self, request, pk=None):
        comment = self.get_object()
        comment.flagged = True
        comment.save()
        return Response({'status': 'comment flagged'})
#/////////////////////////////////////////////////////////////////// with_permissions
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create posts

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set the author to the current user

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]