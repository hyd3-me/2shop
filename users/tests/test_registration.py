from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(APITestCase):
    def test_register_user_success(self):
        url = reverse("users:register")
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        user = User.objects.filter(email=data["email"]).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(data["password"]))

    def test_register_password_mismatch(self):
        url = reverse("users:register")
        data = {
            "name": "Test User",
            "email": "testuser2@example.com",
            "password": "StrongPass123!",
            "password_confirm": "DifferentPass123!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("password_confirm", response.data)

    def test_register_missing_required_fields(self):
        url = reverse("users:register")
        data = {
            "name": "Test User",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_register_invalid_email(self):
        url = reverse("users:register")
        data = {
            "name": "Test User",
            "email": "not-an-email",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_register_weak_password(self):
        url = reverse("users:register")
        data = {
            "name": "Test User",
            "email": "testuser3@example.com",
            "password": "123",
            "password_confirm": "123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)
