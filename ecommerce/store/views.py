from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import Category, Product, Cart, CartItem, Order
from .permissions import IsStaffOrReadOnly,IsOwner
from .serializers import (
    CategorySerializer, ProductSerializer,
    CartSerializer, CartItemSerializer, OrderSerializer,
)
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema



# ---------- Categories ----------

@extend_schema(tags=["Categories"])
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]




class ProductPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50
@extend_schema(tags=["Products"])
class ProductList(generics.ListCreateAPIView):
    """
    Public: anyone can GET the catalog.
    Staff only: POST to add new products.
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "description"]
    pagination_class = ProductPagination


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]


# ---------- Cart (always scoped to the logged-in user) ----------

class CartDetail(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemList(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # A user can only ever touch items inside THEIR OWN cart
        return CartItem.objects.filter(cart__user=self.request.user)


# ---------- Orders ----------

class OrderList(generics.ListCreateAPIView):
    """
    GET: a customer's own order history only (never someone else's).
    POST: checkout — builds an order from the current cart (see serializer).
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'checkout'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")

    def get_serializer_context(self):
        return {"request": self.request}


class OrderDetail(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]

    def get_queryset(self):
        # scoped so customers can't view other customers' orders by guessing IDs
        return Order.objects.filter(user=self.request.user)