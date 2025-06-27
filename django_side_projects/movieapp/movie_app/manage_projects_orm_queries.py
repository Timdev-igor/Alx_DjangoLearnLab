from .models import Product  

# List of sample products  single& mmultiple creates
Product.objects.create(
    name="Gaming Laptop",
    description="High-end gaming laptop with RTX 3080",
    price=2500.00,
    category="Electronics"
)

products = [
    Product(name="Tablet", description="10-inch display tablet", price=300, category="Electronics"),
    Product(name="Smartwatch", description="Fitness tracking smartwatch", price=250, category="Wearable"),
    Product(name="Desk Chair", description="Ergonomic office chair", price=180, category="Furniture"),
    Product(name="Mechanical Keyboard", description="RGB gaming keyboard", price=120, category="Electronics"),
    Product(name="Noise-Canceling Headphones", description="Over-ear wireless headphones", price=350, category="Audio"),
]
Product.objects.bulk_create(products)  # Bulk insert into the database

#retrieve instances  all & by category
products = list(Product.objects.all().values("name", "price", "category"))
print(products)

electronics = list(Product.objects.filter(category="Electronics").values("name", "price"))
print(electronics)
#delete&update


Product.objects.filter(category="Electronics").update(price=500)

Product.objects.filter(category="Old Electronics").delete()


