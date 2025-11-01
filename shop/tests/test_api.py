from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from shop.models import (
    Cart,
    CartItem,
    Order,
    OrderItem,
    Product,
    Category,
    Role,
    BusinessElement,
    AccessRule,
)
from users.models import User


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("shop:category-list")

        self.role_admin = Role.objects.create(name="admin")
        self.element_category = BusinessElement.objects.create(
            name="Category", description="Category business model"
        )

        AccessRule.objects.create(
            role=self.role_admin,
            business_element=self.element_category,
            create_permission=True,
        )

        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        self.user.roles.add(self.role_admin)

        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        data = {"name": "Books"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "Books")


class ProductAPITest(APITestCase):
    def setUp(self):
        self.element_product = BusinessElement.objects.create(
            name="Product", description="Product business model"
        )
        role = Role.objects.create(name="manager")
        AccessRule.objects.create(
            role=role, business_element=self.element_product, create_permission=True
        )
        self.user = User.objects.create_user(
            email="creator@example.com", password="pass1234"
        )
        self.user.roles.add(role)
        self.category = Category.objects.create(name="Electronics")

    def test_create_product(self):
        self.client.force_authenticate(user=self.user)
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


class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="customer@example.com", password="pass1234"
        )
        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            name="Django Guide", category=self.category, price=30.00
        )

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("shop:order-list")
        data = {
            "user": self.user.id,
            "items": [{"product": self.product.id, "quantity": 2}],
            "status": "pending",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
        self.assertEqual(order.items.first().quantity, 2)


class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.category = Category.objects.create(name="Gadgets")
        self.product = Product.objects.create(
            name="Smartphone", category=self.category, price=500.00
        )

    def test_create_cart(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("shop:cart-list")
        data = {
            "user": self.user.id,
            "items": [{"product": self.product.id, "quantity": 1}],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_update_cart(self):
        self.client.force_authenticate(user=self.user)
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)

        url = reverse("shop:cart-detail", kwargs={"pk": cart.pk})
        data = {"items": [{"product": self.product.id, "quantity": 3}]}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart.items.first().quantity, 3)
