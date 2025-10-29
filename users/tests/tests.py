from django.test import TestCase
from django.contrib.auth import get_user_model
from users import services

User = get_user_model()


class UserModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Тест создание пользователя с email проходит успешно"""
        email = "test@example.com"
        password = "Testpass123"
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Test creating a superuser with correct flags"""
        email = "admin@example.com"
        password = "Adminpass123"
        admin_user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="test1234")

    def test_soft_delete_user_function(self):
        # Create a user
        email = "func_test@example.com"
        password = "FuncTest123"
        user = User.objects.create_user(email=email, password=password)

        # Call the soft delete function
        services.soft_delete_user(user)

        # Reload user and check is_active flag
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_cannot_login_after_soft_delete(self):
        # Create a user
        email = "inactive@example.com"
        password = "InactivePass123"
        user = User.objects.create_user(email=email, password=password)

        # Soft delete the user using the service function
        services.soft_delete_user(user)

        # Attempt to login - should fail because user is not active
        login_success = self.client.login(email=email, password=password)
        self.assertFalse(login_success)
