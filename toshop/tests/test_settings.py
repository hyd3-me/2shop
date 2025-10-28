from django.test import SimpleTestCase
from django.conf import settings
from pathlib import Path


class BaseDirTest(SimpleTestCase):
    def test_base_dir_path(self):
        expected_path = Path(__file__).resolve().parent.parent.parent
        self.assertEqual(settings.BASE_DIR, expected_path)


class SettingsTest(SimpleTestCase):
    def test_secret_key(self):
        default_key = "your_default_insecure_secret_key"
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(
            settings.SECRET_KEY, default_key, "SECRET_KEY must be changed from default!"
        )
