import unittest
from unittest.mock import patch, MagicMock
from unified_logger.unified_logger import UnifiedLogger

class TestUnifiedLogger(unittest.TestCase):

    def setUp(self):
        self.logger = UnifiedLogger(interfaces="cli")

    def test_init(self):
        self.assertEqual(self.logger.log_level, 'DEBUG')
        self.assertEqual(self.logger.log_folder, 'logs')

    def test_set_level(self):
        self.logger.set_level('INFO')
        self.assertEqual(self.logger.log_level, 'INFO')

    def test_display(self):
        with patch('unified_logger.unified_logger.logger') as mock_logger:
            self.logger.display("Test message", level="info")
            mock_logger.info.assert_called_once_with("Test message")

    def test_display_toast(self):
        log = UnifiedLogger()
        log.root = MagicMock()
        log.get_icon_name = MagicMock(return_value="info-circle")
        log.get_boot_style = MagicMock(return_value="info")

        with patch('unified_logger.unified_logger.Toast.show_toast') as mock_toast_show:
            log.display_toast("Test message", "info")
            mock_toast_show.assert_called_once()

    def test_log_exception(self):
        with patch('unified_logger.unified_logger.logger') as mock_logger:
            try:
                raise ValueError("Test exception")
            except Exception as e:
                self.logger.log_exception(e)
                mock_logger.exception.assert_called()

    def test_add_cli_command(self):
        @self.logger.add_cli_command
        def test_command():
            pass
        self.assertIn("test_command", [cmd.callback.__name__ for cmd in self.logger.app.registered_commands])

    def test_progress_bar(self):
        iterable = range(5)
        progress = self.logger.progress_bar(iterable, label="Processing")
        self.assertEqual(list(progress), list(iterable))

    def test_set_format(self):
        format = "{message}"
        self.logger.set_format(format)
        self.assertEqual(self.logger.log_format, format)

    def test_add_stream_handler(self):
        self.logger.add_stream_handler()
        self.assertIsNotNone(self.logger.log_stream_handler)

if __name__ == '__main__':
    unittest.main()
