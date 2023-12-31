# UnifiedLogger

## Description

UnifiedLogger provides a comprehensive and user-friendly logging solution that integrates Command Line Interface (CLI), Graphical User Interface (GUI), and advanced logging functionalities. It leverages popular libraries such as Loguru, Typer, ttkbootstrap, and tkfontawesome to create a versatile and powerful tool suitable for various applications.

## Features

1. **Real-Time Log Viewer:** Displays log messages in real-time, with auto-scrolling to the latest log entry and user-controlled update speeds.
2. **Rich Logging Capabilities:** Utilizes Loguru for advanced logging features, including custom tracebacks, exception handling, and detailed log formatting.
3. **CLI Integration:** Incorporates Typer to enable the creation and execution of CLI commands, seamlessly integrating CLI interactions with the logging system.
4. **GUI Enhancements:** Utilizes ttkbootstrap and tkfontawesome for modern styling and icons, enhancing readability and user experience.
5. **Copy Functionality:** Allows users to copy selected text or all text in the log viewer to the clipboard.
6. **Flexible Initialization:** Supports initialization with either or both CLI and GUI interfaces, providing flexibility for different use cases.
7. **Exception Handling and Debugging:** Offers detailed exception logging with tracebacks and local variables, aiding in debugging and error analysis.

## Usage

The UnifiedLogger class can be easily integrated into various applications, providing a rich and interactive logging experience. Users can view log messages in real-time, control update speeds, copy log messages, and interact with the application through both CLI and GUI interfaces.

```python
log = UnifiedLogger() # Initialize with both CLI and GUI
log.display("This is an informational message.", level="info")
log.run_gui() # Run the GUI event loop if GUI is enabled
```

## Dependencies

- Loguru
- Typer
- ttkbootstrap
- tkfontawesome

## Installation

The package can be installed via pip or by downloading the package files.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.

