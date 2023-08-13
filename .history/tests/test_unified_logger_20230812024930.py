import unittest
from unittest.mock import patch, MagicMock
from unified_logger.unified_logger import UnifiedLogger

class TestUnifiedLogger(unittest.TestCase):

    def setUp(self):
        self.logger = UnifiedLogger(interfaces="cli")

    def test_display(self):
        with patch('unified_logger.unified_logger.logger') as mock_logger:
            self.logger.display("Test message", level="info")
            mock_logger.info.assert_called_once_with("Test message")

    def test_log_exception(self):
        with patch('unified_logger.unified_logger.logger') as mock_logger:
            try:
                raise ValueError("Test exception")
            except Exception as e:
                self.logger.log_exception(e)
                mock_logger.exception.assert_called()

    def test_toast_notification(self):
        toaster = ToastNotifier()
        toaster.show_toast("Test Notification", "This is a test notification", duration=5)
        input("Press Enter to continue...")
        self.assertTrue(True)

    def test_add_cli_command(self):
        @self.logger.add_cli_command
        def test_command():
            pass
        self.assertIn(test_command, self.logger.app.registered_commands)

    def test_progress_bar(self):
        iterable = range(5)
        progress = self.logger.progress_bar(iterable, label="Processing")
        self.assertEqual(list(progress), list(iterable))


    def test_log_file(self):
        self.logger.set_log_file("test.log")
        self.logger.log("Test message")
        with open("test.log", "r") as f:
            self.assertIn("Test message", f.read())

    def test_set_level(self):
        self.logger.set_level("debug")
        self.assertEqual(self.logger.level, "debug")

    def test_set_format(self):
        self.logger.set_format("{message}")
        self.assertEqual(self.logger.format, "{message}")

    def test_set_output(self):
        self.logger.set_output("test_output.txt")
        self.logger.log("Test message")
        with open("test_output.txt", "r") as f:
            self.assertIn("Test message", f.read())

    def test_add_file_handler(self):
        self.logger.add_file_handler("test.log")
        self.assertIn("test.log", [h.baseFilename for h in self.logger.handlers])

    def test_add_stream_handler(self):
        self.logger.add_stream_handler()
        self.assertIn("StreamHandler", [h.__class__.__name__ for h in self.logger.handlers])

if __name__ == '__main__':
    unittest.main()
