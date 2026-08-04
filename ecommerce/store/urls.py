from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories-v2", views.CategoryViewSet, basename="category-v2")


urlpatterns = [
    path("categories/", views.CategoryList.as_view(), name="category-list"),
    path("categories/<int:pk>/", views.CategoryDetail.as_view(), name="category-detail"),

    path("products/", views.ProductList.as_view(), name="product-list"),
    path("products/<int:pk>/", views.ProductDetail.as_view(), name="product-detail"),

    path("cart/", views.CartDetail.as_view(), name="cart-detail"),
    path("cart/items/", views.CartItemList.as_view(), name="cart-item-list"),
    path("cart/items/<int:pk>/", views.CartItemDetail.as_view(), name="cart-item-detail"),

    path("orders/", views.OrderList.as_view(), name="order-list"),
    path("orders/<int:pk>/", views.OrderDetail.as_view(), name="order-detail"),
]+ router.urls