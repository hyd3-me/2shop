from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Role

User = get_user_model()


class RoleModelTest(TestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(name="admin")
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )

    def test_assign_role_to_user(self):
        self.user.roles.add(self.role_admin)
        self.assertTrue(self.user.roles.filter(name="admin").exists())
