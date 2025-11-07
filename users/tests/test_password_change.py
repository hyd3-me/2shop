from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from users.utils.jwt_utils import encode_jwt


User = get_user_model()


class UserPasswordChangeTests(APITestCase):
    def setUp(self):
        self.email = "passworduser@example.com"
        self.old_password = "OldPass123!"
        self.new_password = "NewPass123!"
        self.user = User.objects.create_user(
            email=self.email, password=self.old_password, name="Password User"
        )
        self.token = encode_jwt({"user_id": self.user.id}, settings.SECRET_KEY)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        self.url = reverse("users:password-change")

    def test_password_change_success(self):
        data = {
            "old_password": self.old_password,
            "new_password": self.new_password,
            "new_password_confirm": self.new_password,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))

    def test_password_mismatch(self):
        data = {
            "old_password": self.old_password,
            "new_password": self.new_password,
            "new_password_confirm": "Mismatch123!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_old_password(self):
        data = {
            "old_password": "WrongOldPass!",
            "new_password": self.new_password,
            "new_password_confirm": self.new_password,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
