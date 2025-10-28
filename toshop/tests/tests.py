from django.test import TestCase


class RootUrlAccessTest(TestCase):
    def test_root_url_returns_200(self):
        """
        Test that GET request to '/' returns HTTP 200 status.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
