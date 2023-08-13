import unittest
from unittest.mock import patch, MagicMock
from unified_logger.unified_logger import UnifiedLogger

class TestUnifiedLogger(unittest.TestCase):

    def setUp(self):
        self.logger = UnifiedLogger(interfaces="cli")

    def test_display(self):
        with patch('unified_logger.logger') as mock_logger:
            self.logger.display("Test message", level="info")
            mock_logger.info.assert_called_once_with("Test message")

    def test_log_exception(self):
        with patch('unified_logger.logger') as mock_logger:
            try:
                raise ValueError("Test exception")
            except Exception as e:
                self.logger.log_exception(e)
                mock_logger.exception.assert_called()

    def test_add_cli_command(self):
        @self.logger.add_cli_command
        def test_command():
            pass
        self.assertIn(test_command, self.logger.app.registered_commands)

    def test_progress_bar(self):
        iterable = range(5)
        progress = self.logger.progress_bar(iterable, label="Processing")
        self.assertEqual(list(progress), list(iterable))

    # Additional tests for other methods can be added here

if __name__ == '__main__':
    unittest.main()
