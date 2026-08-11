from django.db import transaction
from rest_framework import serializers

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .tasks import send_order_confirmation_email, alert_low_stock

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "price",
            "stock", "image", "is_active", "category",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.CharField(source="product.name", read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "quantity", "subtotal"]

    def get_subtotal(self, obj):
        return obj.subtotal()

    def validate(self, data):
        product = data.get("product") or getattr(self.instance, "product", None)
        quantity = data.get("quantity") or getattr(self.instance, "quantity", None)
        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if product and quantity and quantity > product.stock:
            raise serializers.ValidationError(
                f"Only {product.stock} unit(s) of '{product.name}' available."
            )
        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "price_at_purchase", "subtotal"]
        read_only_fields = ["price_at_purchase"]

    def get_subtotal(self, obj):
        return obj.subtotal()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "status", "shipping_address", "items", "total_price", "created_at"]
        read_only_fields = ["status", "created_at"]

    def get_total_price(self, obj):
        return obj.total_price()

    @transaction.atomic
    def create(self, validated_data):
        """
        Builds an Order from the requesting user's current cart:
        - locks stock rows to avoid race conditions on checkout
        - snapshots price_at_purchase (price changes later shouldn't rewrite history)
        - decrements stock
        - empties the cart
        """
        user = self.context["request"].user
        cart = getattr(user, "cart", None)
        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")

        order = Order.objects.create(user=user, **validated_data)

        for item in cart.items.select_related("product").select_for_update():
            product = item.product
            if item.quantity > product.stock:
                raise serializers.ValidationError(
                    f"Only {product.stock} unit(s) of '{product.name}' left in stock."
                )
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price_at_purchase=product.price,
            )
            product.stock -= item.quantity
            product.save(update_fields=["stock"])

        cart.items.all().delete()

        transaction.on_commit(lambda: send_order_confirmation_email.delay(order.id))
        for item in order.items.all():
            if item.product and item.product.stock <= 5:
                pid = item.product.id
                transaction.on_commit(lambda pid=pid: alert_low_stock.delay(pid))

        return order