from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation_email(self, order_id):
    from .models import Order

    try:
        order = Order.objects.select_related("user").prefetch_related("items__product").get(id=order_id)
    except Order.DoesNotExist:
        return

    lines = [
        f"{item.quantity} x {item.product.name if item.product else 'Removed product'}"
        for item in order.items.all()
    ]
    message = (
        f"Hi {order.user.username},\n\n"
        f"Your order #{order.id} has been placed.\n\n"
        + "\n".join(lines)
        + f"\n\nTotal: {order.total_price()}\n\nShipping to: {order.shipping_address}"
    )

    try:
        send_mail(
            subject=f"Order #{order.id} Confirmed",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task
def alert_low_stock(product_id, threshold=5):
    from .models import Product

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return
    if product.stock <= threshold:
        send_mail(
            subject=f"Low stock alert: {product.name}",
            message=f"{product.name} is down to {product.stock} units.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )