from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginTests(APITestCase):
    def setUp(self):
        self.email = "loginuser@example.com"
        self.password = "LoginPass123!"
        self.user = User.objects.create_user(
            email=self.email, password=self.password, name="Login User"
        )

    def test_login_success(self):
        url = reverse("users:login")
        data = {"email": self.email, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
