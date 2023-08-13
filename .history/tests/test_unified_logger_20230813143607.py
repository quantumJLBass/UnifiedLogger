import unittest
from unittest.mock import patch, MagicMock
from unified_logger.unified_logger import UnifiedLogger
import tkinter as tk
from tkinter import Canvas, Scrollbar, Label, Button, Listbox, Text

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



    def test_get_icon_name(self):
        self.assertEqual(self.logger.get_icon_name("error"), "times-circle")
        self.assertEqual(self.logger.get_icon_name("invalid_level"), "comment")

    def test_get_boot_style(self):
        self.assertEqual(self.logger.get_boot_style("error"), "danger")
        self.assertEqual(self.logger.get_boot_style("invalid_level"), "primary")


    def test_display_toast(self):
        log = UnifiedLogger()
        log.root = MagicMock()
        log.get_icon_name = MagicMock(return_value="info-circle")
        log.get_boot_style = MagicMock(return_value="info")

        with patch('unified_logger.unified_logger.Toast.show_toast') as mock_toast_show:
            log.display_toast("Test message", "info")
            mock_toast_show.assert_called_once()



    # def test_get_line_height(self):
    #     log = UnifiedLogger()
    #     text_label = Label(log.root,text="test")
    #     line_height = self.logger.get_line_height(text_label)
    #     self.assertIsInstance(line_height, int, "Value is not an integer")
    #     self.assertGreater(line_height, 0, "Value is not greater than 0")


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



    def test_init_loguru(self):
        with patch('loguru.logger.add') as mock_logger_add:
            self.logger.init_loguru(log_level='INFO', log_folder='logs_test')
            mock_logger_add.assert_called_once()
            self.assertEqual(self.logger.log_level, 'INFO')
            self.assertEqual(self.logger.log_folder, 'logs_test')

    def test_run_gui(self):
        with patch('tkinter.Tk.mainloop') as mock_mainloop:
            log = UnifiedLogger(interfaces="gui")
            mock_mainloop.assert_called_once()

    def test_run_cli(self):
        log = UnifiedLogger(interfaces="cli")
        self.assertEqual(log.run_cli(), None)  # No commands registered, so it returns None

    def test_custom_traceback(self):
        with patch('loguru.logger.error') as mock_logger_error:
            try:
                raise ValueError("Test exception")
            except Exception as e:
                self.logger.custom_traceback(e)
                mock_logger_error.assert_called()


    # def test_copy_to_clipboard(self):
    #     with patch('tkinter.Tk') as mock_tk:
    #         log = UnifiedLogger(interfaces="gui")
    #         log.create_log_viewer()
    #         log.log_viewer_content.insert(tk.END, "Test text")
    #         log.copy_to_clipboard()
    #         mock_tk.return_value.clipboard_get.assert_called_once_with()



if __name__ == '__main__':
    unittest.main()
