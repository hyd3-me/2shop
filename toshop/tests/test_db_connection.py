from django.test import TestCase
from django.db import connection


class DatabaseConnectionTest(TestCase):
    def test_database_connection(self):
        """
        Test database connection by executing a raw SQL query.
        """
        try:
            # Выполняем простой SQL-запрос
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
            self.assertEqual(result, (1,))
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
