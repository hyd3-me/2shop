from django.test import SimpleTestCase
from django.conf import settings
from pathlib import Path


class BaseDirTest(SimpleTestCase):
    def test_base_dir_path(self):
        expected_path = Path(__file__).resolve().parent.parent.parent
        self.assertEqual(settings.BASE_DIR, expected_path)
