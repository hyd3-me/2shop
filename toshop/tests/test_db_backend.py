import unittest
from pathlib import Path


class SettingsFileTest(unittest.TestCase):
    def test_default_database_engine_in_settings_file(self):
        # Найти файл settings.py
        settings_path = Path(__file__).resolve().parent.parent / "settings.py"
        content = settings_path.read_text()

        # Проверяем, что в файле есть строка с engine postgresql
        self.assertIn('ENGINE": "django.db.backends.postgresql', content)
