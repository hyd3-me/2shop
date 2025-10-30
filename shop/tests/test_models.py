from django.test import TestCase
from shop.models import Product, Category


class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertIsNotNone(category.pk)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_create_product(self):
        product = Product.objects.create(
            name="Laptop", category=self.category, price=1200.00
        )
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.category.name, "Electronics")
        self.assertEqual(product.price, 1200.00)
        self.assertIsNotNone(product.pk)
