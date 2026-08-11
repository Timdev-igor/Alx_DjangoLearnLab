from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from store.models import Category, Product, Cart, CartItem

User = get_user_model()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class CheckoutTaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
    username="tester", password="pass1234", email="tester@example.com"
)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        category = Category.objects.create(name="Clothing", slug="clothing")
        self.product = Product.objects.create(
            category=category, name="Denim Jeans", slug="denim-jeans",
            price="49.99", stock=10,
        )
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=3)

    def test_checkout_sends_confirmation_email(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                "/api/orders/", {"shipping_address": "123 Test St"}, format="json"
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Order", mail.outbox[0].subject)

    def test_checkout_decrements_stock(self):
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post("/api/orders/", {"shipping_address": "123 Test St"}, format="json")
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

    def test_low_stock_alert_fires_when_threshold_crossed(self):
        self.product.stock = 6
        self.product.save()

        with self.captureOnCommitCallbacks(execute=True):
            self.client.post("/api/orders/", {"shipping_address": "123 Test St"}, format="json")

        subjects = [m.subject for m in mail.outbox]
        self.assertTrue(any("Low stock" in s for s in subjects))