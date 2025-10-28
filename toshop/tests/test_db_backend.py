from django.test import TestCase
from django.conf import settings


class DatabaseBackendTest(TestCase):
    def test_database_engine_is_postgresql(self):
        """
        Test that the configured database backend engine is PostgreSQL.
        """
        engine = settings.DATABASES["default"]["ENGINE"]
        self.assertIn("postgresql", engine.lower(), "Database engine is not PostgreSQL")
