import os
from django.test import SimpleTestCase


class EnvVariablesTest(SimpleTestCase):
    def test_env_vars_loaded(self):
        """
        Test that essential environment variables are loaded.
        """
        db_name = os.getenv("POSTGRES_DB")
        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")

        self.assertIsNotNone(db_name, "POSTGRES_DB should be set in environment")
        self.assertIsNotNone(db_user, "POSTGRES_USER should be set in environment")
        self.assertIsNotNone(
            db_password, "POSTGRES_PASSWORD should be set in environment"
        )
