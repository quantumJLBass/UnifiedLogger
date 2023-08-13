from loguru import logger
import traceback
import typer
import inspect
import tkinter as tk
import tkinter.font as tkf
from tkinter import Canvas, Scrollbar, Label, Button, Listbox, Text
from ttkbootstrap import Style
from ttkbootstrap.toast import ToastNotification as Toast
from tkfontawesome import icon_to_image
import os
import sys  # Import sys module
from datetime import datetime


class UnifiedLogger:
    def __init__(self, app_name: str = "UnifiedLogger", interfaces: str = "cli,gui", log_level: str = 'DEBUG', log_folder: str = 'logs'):
        self.app = typer.Typer()
        self.interfaces = interfaces.lower().split(',')
        self.app_name = app_name
        self.theme_name = "darkly"
        self.log_level = log_level
        self.log_folder = log_folder
        self.log_format = "{time} [{level}] {message}"
        self.init_loguru(log_level, log_folder)

        if "gui" in self.interfaces:
            self.run_gui()

        if "cli" in self.interfaces:
            self.run_cli()

    def init_loguru(self, log_level: str = 'DEBUG', log_folder: str = 'logs', log_file: str = None):
        if log_level.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError(f"Invalid log level: {log_level}")

        os.makedirs(log_folder, exist_ok=True)
        if log_file is None:
            log_file = os.path.join(log_folder, f'gui-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log')
        self.log_file = log_file  # Define log_file attribute
        self.log_folder = log_folder  # Define log_folder attribute
        self.log_level = log_level  # Define log_level attribute.log_level
        logger.add(log_file, level=log_level.upper(), format="{time} [{level}] {message}", rotation="1 day")  # Use uppercase log level

    def set_level(self, level):
        logger.remove() # Remove existing handlers
        self.log_level = level
        self.init_loguru(log_level=level, log_folder=self.log_folder)

    def display_toast(self, message: str, level: str = "info"):
        icon_name = self.get_icon_name(level)
        boot_style = self.get_boot_style(level)
        Toast(title="ttkbootstrap toast message",  message=message,duration=3000, bootstyle=boot_style,alert=True, icon=icon_name, iconfont=None, position= (100, 100, 'se')).show_toast()


    def set_format(self, format):
        self.log_format = format
        logger.remove() # Remove existing handlers
        self.init_loguru(log_level=self.log_level, log_folder=self.log_folder)

    def display(self, message: str, level: str = "info", gui: bool = False):
        log_func = getattr(logger, level, logger.info)
        log_func(message)
        if gui and hasattr(self, 'root'):
            self.display_toast(message, level)

    def log_exception(self, e: Exception, gui: bool = False):
        local_vars = self.get_local_vars()
        message = f"Exception: {e} | Local variables: {local_vars}"
        logger.exception(message)
        if gui:
            self.display_toast(message, "error")

    def get_local_vars(self):
        frame = inspect.currentframe().f_back.f_back
        local_vars = inspect.getargvalues(frame).locals
        return local_vars

    def add_cli_command(self, func):
        self.app.command()(func)
        return func

    def run_cli(self):
        if self.app.registered_commands: # Check if there are registered commands
            self.app()

    def run_gui(self):
        self.root = tk.Tk()
        self.style = Style(self.theme_name)
        #self.toast = Toast(self.root) #this doesn't seem right, it should be a notice that is shown as a toast when the error or message is called for
        #self.create_log_viewer() # Initialize the GUI log viewer # only do that when wanted though
        self.root.mainloop()

    def progress_bar(self, iterable, label: str = "Processing"):
        with typer.progressbar(iterable, label=label) as progress:
            for item in progress:
                yield item

    def add_logging_sink(self, sink, level="INFO"):
        logger.add(sink, level=level)

    def custom_traceback(self, e: Exception, gui: bool = False):
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        custom_tb = "Custom Traceback:\n" + "".join(tb)
        logger.error(custom_tb)
        if gui:
            self.display_toast(custom_tb, "error")

    def switch_theme(self, theme_name: str):
        self.style.theme_use(theme_name)

    def configure_cli_command(self, command_name, *args, **kwargs):
        # Create a new window for configuring the CLI command
        config_window = tk.Toplevel(self.root)
        config_window.title(f"Configure {command_name}")

        # Add labels and input fields for each argument and keyword argument
        row = 0
        for arg in args:
            label = tk.Label(config_window, text=arg)
            label.grid(row=row, column=0)
            entry = tk.Entry(config_window)
            entry.grid(row=row, column=1)
            row += 1

        for key, value in kwargs.items():
            label = tk.Label(config_window, text=key)
            label.grid(row=row, column=0)
            entry = tk.Entry(config_window, text=value)
            entry.grid(row=row, column=1)
            entry.insert(0, value) # Insert default value if provided
            row += 1

        # Add a button to execute the CLI command with the configured parameters
        execute_button = tk.Button(config_window, text="Execute", command=lambda: self.execute_cli_command(command_name, *args, **kwargs))
        execute_button.grid(row=row, column=0, columnspan=2)

    def execute_cli_command(self, command_name, *args, **kwargs):
        command_func = self.app.get_command(command_name)
        command_func(*args, **kwargs)

    def create_debug_console(self):
        self.console = Text(self.root)
        self.console.pack()
        # Add more functionalities to support interactive debugging

    def create_log_viewer(self):
        self.log_viewer_frame = tk.Frame(self.root)
        self.log_viewer_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.log_viewer_canvas = Canvas(self.log_viewer_frame, bg=self.style.colors.bg)
        self.log_viewer_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        self.log_viewer_scrollbar = Scrollbar(self.log_viewer_frame, command=self.log_viewer_canvas.yview)
        self.log_viewer_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_viewer_canvas.configure(yscrollcommand=self.log_viewer_scrollbar.set)
        self.log_viewer_canvas.bind('<Configure>', self.on_canvas_configure)

        self.log_viewer_content = tk.Frame(self.log_viewer_canvas)
        self.log_viewer_canvas.create_window((0, 0), window=self.log_viewer_content, anchor=tk.NW)

        logger.add(self.update_log_viewer)
        # Add a copy button
        self.copy_button = Button(self.log_viewer_frame, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.pack()

        # Add speed control buttons
        self.speed_button_slow = Button(self.log_viewer_frame, text="Slow", command=lambda: self.set_speed("slow"))
        self.speed_button_slow.pack(side=tk.LEFT)

        self.speed_button_normal = Button(self.log_viewer_frame, text="Normal", command=lambda: self.set_speed("normal"))
        self.speed_button_normal.pack(side=tk.LEFT)

        self.speed_button_fast = Button(self.log_viewer_frame, text="Fast", command=lambda: self.set_speed("fast"))
        self.speed_button_fast.pack(side=tk.LEFT)

    def update_log_viewer(self, message):
        icon_name = self.get_icon_name(message)
        text_label = tk.Label(self.log_viewer_content, text=message, wraplength=800)
        icon_image = self.get_icon_with_matching_height(icon_name, text_label)
        icon_label = Label(self.log_viewer_content, image=icon_image)
        icon_label.image = icon_image # Keep a reference to the image
        icon_label.pack(side=tk.LEFT)

        text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.log_viewer_content.update_idletasks()
        self.log_viewer_canvas.config(scrollregion=self.log_viewer_canvas.bbox("all"))
        # Auto-scroll to the latest log entry if the user is at the latest row
        if self.log_viewer_canvas.yview()[1] == 1.0:
            self.log_viewer_canvas.yview_moveto(1.0)

        # Schedule the next update based on the selected speed
        self.log_viewer_content.after(self.update_speed, self.update_log_viewer, message)

    def add_stream_handler(self):
        self.log_stream_handler = logger.add(sys.stderr, level=self.log_level.upper(), format=self.log_format)  # Use uppercase log level

    def set_update_speed(self, speed):
        self.update_speed = speed

    def copy_to_clipboard(self):
        # Get the selected text or all the text in the log viewer
        try:
            selected_text = self.log_viewer_content.selection_get()
        except:
            selected_text = self.log_viewer_content.get("1.0", tk.END)

        # Copy the text to the clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
        self.root.update() # Required to finalize the clipboard update

    def on_canvas_configure(self, event):
        self.log_viewer_canvas.itemconfig(self.log_viewer_content, width=event.width)

    def set_speed(self, speed):
        if speed == "slow":
            self.log_viewer_scrollbar.config(jump=0)
        elif speed == "normal":
            self.log_viewer_scrollbar.config(jump=0.5)
        elif speed == "fast":
            self.log_viewer_scrollbar.config(jump=1)

    def get_icon_name(self, level):
        icons = {
            "error": "times-circle",
            "warning": "exclamation-triangle",
            "info": "info-circle",
            "success": "check-circle",
            "system": "cogs",
            "user": "user",
            "debug": "bug",
            "network": "sitemap",
            "security": "shield-alt"
        }
        return icons.get(level, "comment")

    def get_boot_style(self, level):
        styles = {
            "error": "danger",
            "warning": "warning",
            "info": "info",
            "success": "success"
        }
        return styles.get(level, "primary")

    def get_line_height(self, text_label):
        # Get the font size of the text label
        #font_size = text_label.cget("font")[-1]
        font_size = tkf.Font(font=text_label['font']).metrics('linespace')

        return font_size



# # Example Usage
# log = UnifiedLogger()

# @log.add_cli_command
# def divide(x: int, y: int, gui: bool = False):
#     try:
#         result = x / y
#         log.display(f"The result is: {result}", gui=gui)
#     except Exception as e:
#         log.log_exception(e, gui=gui)
#         log.custom_traceback(e, gui=gui)

# if __name__ == "__main__":
#     log.run_cli()
