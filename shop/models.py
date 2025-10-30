from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


User = get_user_model()
User.add_to_class("roles", models.ManyToManyField(Role, related_name="users"))
