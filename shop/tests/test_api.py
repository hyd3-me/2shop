from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from shop.models import Product, Category


class CategoryAPITest(APITestCase):
    def test_create_category(self):
        url = reverse("shop:category-list")
        data = {"name": "Books"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "Books")


class ProductAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_create_product(self):
        url = reverse("shop:product-list")
        data = {
            "name": "Laptop",
            "category": self.category.id,
            "price": "1500.00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, "Laptop")
