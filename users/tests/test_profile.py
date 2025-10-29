from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status

User = get_user_model()


class UserProfileUpdateTests(APITestCase):
    def setUp(self):
        self.email = "profileuser@example.com"
        self.password = "ProfilePass123!"
        self.user = User.objects.create_user(
            email=self.email, password=self.password, name="Original Name"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.url = reverse("users:profile-update")

    def test_update_user_profile_success(self):
        data = {
            "name": "Updated Name",
            "email": self.email,
        }
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Updated Name")
