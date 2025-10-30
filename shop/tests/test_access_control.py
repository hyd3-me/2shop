from django.test import TestCase
from shop.models import Role, BusinessElement, AccessRule
from django.contrib.auth import get_user_model

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
