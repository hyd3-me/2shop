from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from shop.models import Role, BusinessElement, AccessRule

User = get_user_model()


class AccessControlModelsTest(TestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(name="admin")
        self.role_user = Role.objects.create(name="user")
        self.element_product = BusinessElement.objects.create(
            name="Product", description="Product business model"
        )
        self.element_order = BusinessElement.objects.create(
            name="Order", description="Order business model"
        )
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.user.roles.add(self.role_user)

    def test_create_access_rule(self):
        rule = AccessRule.objects.create(
            role=self.role_user,
            business_element=self.element_product,
            read_permission=True,
            read_all_permission=False,
            create_permission=True,
            update_permission=True,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False,
        )
        self.assertEqual(rule.role.name, "user")
        self.assertEqual(rule.business_element.name, "Product")
        self.assertTrue(rule.read_permission)
        self.assertFalse(rule.delete_permission)


class AccessRulePermissionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("shop:category-list")

        self.role_admin = Role.objects.create(name="admin")
        self.role_user = Role.objects.create(name="user")

        self.element_category = BusinessElement.objects.create(
            name="Category", description="Category business model"
        )

        AccessRule.objects.create(
            role=self.role_admin,
            business_element=self.element_category,
            create_permission=True,
        )
        AccessRule.objects.create(
            role=self.role_user,
            business_element=self.element_category,
            create_permission=False,
        )

        self.admin_user = User.objects.create_user(
            email="admin@example.com", password="adminpass"
        )
        self.admin_user.roles.add(self.role_admin)

        self.normal_user = User.objects.create_user(
            email="user@example.com", password="userpass"
        )
        self.normal_user.roles.add(self.role_user)

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.url, {"name": "Books"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_category_authenticated_user(self):
        element = BusinessElement.objects.get(name="Category")
        rule, created = AccessRule.objects.get_or_create(
            role=self.role_user,
            business_element=element,
            defaults={"read_permission": True},
        )
        if not created:
            rule.read_permission = True
            rule.save()

        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
