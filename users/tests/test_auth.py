from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from users.utils.jwt_utils import encode_jwt


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

    def test_login_failure_wrong_password(self):
        url = reverse("users:login")
        data = {"email": self.email, "password": "WrongPassword123!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)


class UserLogoutTests(APITestCase):
    def setUp(self):
        self.email = "logoutuser@example.com"
        self.password = "LogoutPass123!"
        self.user = User.objects.create_user(
            email=self.email, password=self.password, name="Logout User"
        )
        self.token = encode_jwt({"user_id": self.user.id}, settings.SECRET_KEY)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_logout_success(self):
        url = reverse("users:logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "Successfully logged out.")
