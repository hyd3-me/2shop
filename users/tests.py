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
