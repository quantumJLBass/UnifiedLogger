from loguru import logger
import traceback
import typer
import inspect
import tkinter as tk
from tkinter import Canvas, Scrollbar, Label
from ttkbootstrap import Style
from tkfontawesome import icon_to_image
from ttkbootstrap import Style, Toast
from tkinter import Text
from tkinter import Listbox

class UnifiedLogger:
    def __init__(self, interfaces: str = "cli,GUI"):
        self.app = typer.Typer()
        self.interfaces = interfaces.lower().split(',')

        if "gui" in self.interfaces:
            self.root = tk.Tk()
            self.style = Style(self.root)
            self.toast = Toast(self.root)
            self.create_log_viewer() # Initialize the GUI log viewer
            self.run_gui()

        if "cli" in self.interfaces:
            self.run_cli() # Start the CLI interface


    def display(self, message: str, level: str = "info", gui: bool = False):
        log_func = getattr(logger, level, logger.info)
        log_func(message)
        if gui:
            self.toast.show(message, icon=level)

    def log_exception(self, e: Exception, gui: bool = False):
        local_vars = self.get_local_vars()
        message = f"Exception: {e} | Local variables: {local_vars}"
        logger.exception(message)
        if gui:
            self.toast.show(message, icon="error")

    def get_local_vars(self):
        frame = inspect.currentframe().f_back.f_back
        local_vars = inspect.getargvalues(frame).locals
        return local_vars

    def add_cli_command(self, func):
        self.app.command()(func)

    def run_cli(self):
        self.app()

    def run_gui(self):
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
            self.toast.show(custom_tb, icon="error")

    def switch_theme(self, theme_name: str):
        self.style.theme_use(theme_name)

    def configure_cli_command(self, command_name, *args, **kwargs):
        # GUI elements to configure CLI command parameters
        # ...

    def execute_cli_command(self, command_name):
        command_func = self.app.get_command(command_name)
        command_func(*args, **kwargs)

    def create_log_viewer(self):
        self.log_viewer = Listbox(self.root)
        self.log_viewer.pack()
        logger.add(self.update_log_viewer)

    def update_log_viewer(self, message):
        self.log_viewer.insert(tk.END, message)


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
        self.speed_button_slow = Button(self.log_viewer_frame, text="Slow", command=lambda: self.set_update_speed(1000))
        self.speed_button_slow.pack(side=tk.LEFT)
        self.speed_button_medium = Button(self.log_viewer_frame, text="Medium", command=lambda: self.set_update_speed(500))
        self.speed_button_medium.pack(side=tk.LEFT)
        self.speed_button_fast = Button(self.log_viewer_frame, text="Fast", command=lambda: self.set_update_speed(100))
        self.speed_button_fast.pack(side=tk.LEFT)

        self.update_speed = 500 # Default update speed in milliseconds


    def update_log_viewer(self, message):
        icon_name = self.get_icon_name(message)
        icon_image = icon_to_image(icon_name, fill="#177255", scale_to_width=30)
        icon_label = Label(self.log_viewer_content, image=icon_image)
        icon_label.image = icon_image # Keep a reference to the image
        icon_label.pack(side=tk.LEFT)

        text_label = tk.Label(self.log_viewer_content, text=message, wraplength=800)
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.log_viewer_content.update_idletasks()
        self.log_viewer_canvas.config(scrollregion=self.log_viewer_canvas.bbox("all"))
        # Auto-scroll to the latest log entry if the user is at the latest row
        if self.log_viewer_canvas.yview()[1] == 1.0:
            self.log_viewer_canvas.yview_moveto(1.0)

        # Schedule the next update based on the selected speed
        self.log_viewer_content.after(self.update_speed, self.update_log_viewer, message)


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
        self.log_viewer_canvas.config(scrollregion=self.log_viewer_canvas.bbox("all"))

    def get_icon_name(self, message):
        # Define logic to determine the appropriate icon based on the message or log level
        if "error" in message:
            return "times-circle" # Icon for error messages
        elif "warning" in message:
            return "exclamation-triangle" # Icon for warning messages
        elif "info" in message:
            return "info-circle" # Icon for informational messages
        elif "success" in message:
            return "check-circle" # Icon for success messages
        elif "system" in message:
            return "cogs" # Icon for system-related messages
        elif "user" in message:
            return "user" # Icon for user-related messages
        elif "debug" in message:
            return "bug" # Icon for debug messages
        elif "network" in message:
            return "sitemap" # Icon for network-related messages
        elif "security" in message:
            return "shield-alt" # Icon for security-related messages
        else:
            return "comment" # Default icon for other messages




# Example Usage
log = UnifiedLogger()

@log.add_cli_command
def divide(x: int, y: int, gui: bool = False):
    try:
        result = x / y
        log.display(f"The result is: {result}", gui=gui)
    except Exception as e:
        log.log_exception(e, gui=gui)
        log.custom_traceback(e, gui=gui)

if __name__ == "__main__":
    log.run_cli()
