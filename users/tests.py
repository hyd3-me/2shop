from django.test import TestCase
from django.contrib.auth import get_user_model

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

    def test_soft_delete_user(self):
        # Create a user with active status
        email = "testuser@example.com"
        password = "Testpass123"
        user = User.objects.create_user(email=email, password=password)

        # Perform soft delete by setting is_active to False
        user.is_active = False
        user.save()

        # Reload user from the database and check is_active flag
        user.refresh_from_db()
        self.assertFalse(user.is_active)

        # Attempt to login with the soft-deleted user should fail
        login_success = self.client.login(email=email, password=password)
        self.assertFalse(login_success)
