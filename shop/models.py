from django.db import models


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
