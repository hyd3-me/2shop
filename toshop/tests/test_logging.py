import logging
from django.test import TestCase
from django.conf import settings

# Import logger that должен быть инициализирован в settings.py
logger = logging.getLogger("django")


class LoggerFunctionalityTest(TestCase):
    def test_logger_logs_message(self):
        """
        Test that the imported logger from settings actually logs messages.
        """
        with self.assertLogs(logger, level="INFO") as cm:
            logger.info("Test log message")
        # Проверяем, что наше сообщение появилось в логах
        self.assertTrue(any("Test log message" in message for message in cm.output))
