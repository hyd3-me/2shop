from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from shop.models import (
    User,
    Role,
    BusinessElement,
    AccessRule,
    Order,
    OrderItem,
    Category,
    Product,
)


class UserOrderAccessRulePermissionTest(APITestCase):
    def setUp(self):
        self.role_user = Role.objects.create(name="user")
        self.element_order = BusinessElement.objects.create(name="Order")

        self.user = User.objects.create_user(
            email="user_order@example.com", password="userpass"
        )
        self.user.roles.add(self.role_user)

        self.other_user = User.objects.create_user(
            email="other_user@example.com", password="otherpass"
        )
        self.other_user.roles.add(self.role_user)

        AccessRule.objects.create(
            role=self.role_user,
            business_element=self.element_order,
            create_permission=True,
            read_permission=True,
            update_permission=False,
            delete_permission=False,
        )

        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            name="Django Guide", category=self.category, price=30.00
        )

        self.client.force_authenticate(user=self.user)

    def test_user_can_read_own_order(self):
        order = Order.objects.create(user=self.user, status="pending")
        url = reverse("shop:order-detail", kwargs={"pk": order.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], order.id)

    def test_user_cannot_read_other_order(self):
        other_order = Order.objects.create(user=self.other_user, status="pending")
        url = reverse("shop:order-detail", kwargs={"pk": other_order.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_create_order_for_self(self):
        url = reverse("shop:order-list")
        data = {
            "user": self.user.id,
            "status": "pending",
            "items": [{"product": self.product.id, "quantity": 1}],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_create_order_for_other(self):
        url = reverse("shop:order-list")
        data = {
            "user": self.other_user.id,
            "status": "pending",
            "items": [{"product": self.product.id, "quantity": 1}],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_any_order(self):
        order = Order.objects.create(user=self.user, status="pending")
        url = reverse("shop:order-detail", kwargs={"pk": order.pk})
        data = {"status": "processing"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_any_order(self):
        order = Order.objects.create(user=self.user, status="pending")
        url = reverse("shop:order-detail", kwargs={"pk": order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
