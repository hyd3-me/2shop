from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from shop.models import Role, BusinessElement, AccessRule, Category, Product

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

        self.element_product = BusinessElement.objects.create(
            name="Product", description="Product business model"
        )
        self.category = Category.objects.create(name="Electronics")

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

    def test_read_category_forbidden_for_user_without_permission(self):
        element = BusinessElement.objects.get(name="Category")
        rule = AccessRule.objects.get(role=self.role_user, business_element=element)
        rule.read_permission = False
        rule.save()

        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_forbidden_for_user_without_permission(self):
        element = BusinessElement.objects.get(name="Category")
        rule = AccessRule.objects.get(role=self.role_user, business_element=element)
        rule.update_permission = False
        rule.save()

        self.client.force_authenticate(user=self.normal_user)
        category = Category.objects.create(name="Old Name")
        url = reverse("shop:category-detail", kwargs={"pk": category.pk})
        data = {"name": "New Name"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_forbidden_for_user_without_permission(self):
        element = BusinessElement.objects.get(name="Category")
        rule = AccessRule.objects.get(role=self.role_user, business_element=element)
        rule.delete_permission = False
        rule.save()

        self.client.force_authenticate(user=self.normal_user)
        category = Category.objects.create(name="Test Delete")
        url = reverse("shop:category-detail", kwargs={"pk": category.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_allowed_for_user_with_permission(self):
        element = BusinessElement.objects.get(name="Category")
        rule, created = AccessRule.objects.get_or_create(
            role=self.role_user,
            business_element=element,
            defaults={"update_permission": True},
        )
        if not created:
            rule.update_permission = True
            rule.save()

        self.client.force_authenticate(user=self.normal_user)
        category = Category.objects.create(name="Old Name")
        url = reverse("shop:category-detail", kwargs={"pk": category.pk})
        data = {"name": "Updated Name"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category.refresh_from_db()
        self.assertEqual(category.name, "Updated Name")

    def test_create_product_allowed_for_user_with_permission(self):
        element = BusinessElement.objects.get(name="Product")
        rule, created = AccessRule.objects.get_or_create(
            role=self.role_user,
            business_element=element,
            defaults={"create_permission": True},
        )
        if not created:
            rule.create_permission = True
            rule.save()

        self.client.force_authenticate(user=self.normal_user)
        url = reverse("shop:product-list")
        data = {"name": "New Product", "category": self.category.id, "price": "100.00"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_allowed_for_admin(self):
        element = BusinessElement.objects.get(name="Product")
        AccessRule.objects.update_or_create(
            role=self.role_admin,
            business_element=element,
            defaults={"create_permission": True},
        )

        self.client.force_authenticate(user=self.admin_user)

        url = reverse("shop:product-list")

        data = {
            "name": "New Product",
            "category": self.category.id,
            "price": "100.00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product_allowed_for_admin(self):
        element = BusinessElement.objects.get(name="Product")
        AccessRule.objects.update_or_create(
            role=self.role_admin,
            business_element=element,
            defaults={"update_permission": True},
        )

        self.client.force_authenticate(user=self.admin_user)

        product = Product.objects.create(
            name="Old Name", category=self.category, price="50.00"
        )

        url = reverse("shop:product-detail", kwargs={"pk": product.pk})
        data = {
            "name": "Updated Product Name",
            "category": self.category.id,
            "price": "75.00",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product.refresh_from_db()
        self.assertEqual(product.name, "Updated Product Name")

    def test_delete_product_allowed_for_admin(self):
        element = BusinessElement.objects.get(name="Product")
        AccessRule.objects.update_or_create(
            role=self.role_admin,
            business_element=element,
            defaults={"delete_permission": True},
        )

        self.client.force_authenticate(user=self.admin_user)

        product = Product.objects.create(
            name="Delete Me", category=self.category, price="20.00"
        )
        url = reverse("shop:product-detail", kwargs={"pk": product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

    def test_read_product_allowed_for_admin(self):
        element = BusinessElement.objects.get(name="Product")
        AccessRule.objects.update_or_create(
            role=self.role_admin,
            business_element=element,
            defaults={"read_permission": True},
        )

        self.client.force_authenticate(user=self.admin_user)

        product = Product.objects.create(
            name="Readable Product", category=self.category, price="30.00"
        )

        url = reverse("shop:product-detail", kwargs={"pk": product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["name"], "Readable Product")


class ManagerAccessRulePermissionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.role_manager = Role.objects.create(name="manager")
        self.element_product = BusinessElement.objects.create(name="Product")

        AccessRule.objects.create(
            role=self.role_manager,
            business_element=self.element_product,
            create_permission=True,
            read_permission=True,
            update_permission=True,
            delete_permission=False,
        )

        self.category = Category.objects.create(name="Manager Category")

        self.manager_user = User.objects.create_user(
            email="manager@example.com", password="managerpass"
        )
        self.manager_user.roles.add(self.role_manager)

    def test_create_product_allowed_for_manager(self):
        self.client.force_authenticate(user=self.manager_user)
        url = reverse("shop:product-list")
        data = {
            "name": "Manager Product",
            "category": self.category.id,
            "price": "150.00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_product_allowed_for_manager(self):
        element = BusinessElement.objects.get(name="Product")
        rule = AccessRule.objects.get(role=self.role_manager, business_element=element)
        rule.read_permission = True
        rule.save()

        self.client.force_authenticate(user=self.manager_user)

        product = Product.objects.create(
            name="Readable Product", category=self.category, price="75.00"
        )

        url = reverse("shop:product-detail", kwargs={"pk": product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Readable Product")

    def test_update_product_allowed_for_manager(self):
        self.client.force_authenticate(user=self.manager_user)

        product = Product.objects.create(
            name="Old Manager Product", category=self.category, price="80.00"
        )

        url = reverse("shop:product-detail", kwargs={"pk": product.pk})
        data = {
            "name": "Updated Manager Product",
            "category": self.category.id,
            "price": "100.00",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product.refresh_from_db()
        self.assertEqual(product.name, "Updated Manager Product")
