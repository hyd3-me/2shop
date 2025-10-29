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
        self.assertIn("non_field_errors", response.data)  # Validation error key
