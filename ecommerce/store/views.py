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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import flag_abandoned_carts
from rest_framework.response import Response
from django.http import JsonResponse
import httpx
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import sync_to_async



async def convert_price(request, order_id):
    from .models import Order

    is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
    if not is_authenticated:
        return JsonResponse({"detail": "Authentication required"}, status=401)

    user = await sync_to_async(lambda: request.user)()
    target_currency = request.GET.get("currency", "KES")

    get_order = sync_to_async(Order.objects.get)
    try:
        order = await get_order(id=order_id, user=user)
    except Order.DoesNotExist:
        return JsonResponse({"detail": "Order not found"}, status=404)

    get_total = sync_to_async(order.total_price)
    total_usd = await get_total()

    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = resp.json()
        rate = data["rates"].get(target_currency, 1)

    converted = round(float(total_usd) * rate, 2)

    return JsonResponse({
        "order_id": order.id,
        "total_usd": str(total_usd),
        "currency": target_currency,
        "converted_total": converted,
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def trigger_abandoned_cart_check(request):
    result = flag_abandoned_carts.delay(hours=0)
    return Response({"task_id": result.id, "status": "queued"})

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