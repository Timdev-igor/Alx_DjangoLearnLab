from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product

User = get_user_model()


class ProductAPITests(APITestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="admin", email="admin@example.com", password="pass123", is_staff=True
        )
        self.customer = User.objects.create_user(
            username="sarah", email="sarah@example.com", password="pass123"
        )
        self.category = Category.objects.create(name="Electronics", slug="electronics")

    def test_anyone_can_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_create_product(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.post("/api/products/", {
            "name": "Mouse", "slug": "mouse", "price": 10,
            "stock": 5, "category": "electronics",
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create_product(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post("/api/products/", {
            "name": "Mouse", "slug": "mouse", "price": 10,
            "stock": 5, "category": "electronics",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_checkout_decrements_stock(self):
        product = Product.objects.create(
            name="Keyboard", slug="keyboard", price=50, stock=5, category=self.category
        )
        self.client.force_authenticate(user=self.customer)
        self.client.post("/api/cart/items/", {"product": product.id, "quantity": 2})
        self.client.post("/api/orders/", {"shipping_address": "Nairobi"})
        product.refresh_from_db()
        self.assertEqual(product.stock, 3)

    def test_category_list_caches(self):
        cache.delete("category_list")
        self.client.get("/api/categories/")
        self.assertIsNotNone(cache.get("category_list"))

    def test_category_cache_invalidates_on_create(self):
        self.client.get("/api/categories/")
        Category.objects.create(name="New", slug="new")
        self.assertIsNone(cache.get("category_list"))