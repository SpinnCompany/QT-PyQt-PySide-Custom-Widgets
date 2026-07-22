import logging
import os
import sys
import threading
import traceback
from logging.handlers import RotatingFileHandler
from qtpy.QtCore import QSettings
from Custom_Widgets.Utils import is_in_designer

# Rich for beautiful console output
try:
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.traceback import Traceback
    from rich.panel import Panel
    from rich.text import Text
    from rich.theme import Theme
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Rich not available. Install with: pip install rich")

# Custom theme for rich console
if RICH_AVAILABLE:
    try:
        custom_theme = Theme({
            "info": "cyan",
            "warning": "yellow",
            "error": "red",
            "critical": "bold red",
            "debug": "dim",
            "success": "green",
            "file": "blue",
            "folder": "magenta",
            "monitor": "bold blue"
        })
        console = Console(theme=custom_theme)
    except Exception as e:
        print(f"Failed to initialize Rich theme: {e}")
        RICH_AVAILABLE = False
        console = None

def get_app_data_folder(app_name="CustomWidgets"):
    """
    Get the appropriate application data folder for different platforms
    
    Returns:
        str: Path to the application data folder
    """
    if sys.platform == "win32":
        # Windows: Use APPDATA or LOCALAPPDATA
        base_folder = os.environ.get("LOCALAPPDATA", os.environ.get("APPDATA", ""))
        if not base_folder:
            # Fallback to user's home directory
            base_folder = os.path.expanduser("~")
        app_data_folder = os.path.join(base_folder, app_name)
    elif sys.platform == "darwin":
        # macOS: Use ~/Library/Application Support/
        base_folder = os.path.expanduser("~/Library/Application Support")
        app_data_folder = os.path.join(base_folder, app_name)
    else:
        # Linux/Unix: Use XDG_DATA_HOME or ~/.local/share
        base_folder = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        app_data_folder = os.path.join(base_folder, app_name.lower())
    
    return app_data_folder

def get_log_file_path(app_name="CustomWidgets", designer=False):
    """
    Get the appropriate log file path
    
    Args:
        app_name: Name of the application for folder structure
        designer: Whether this is for designer mode
    
    Returns:
        str: Path to the log file
    """
    # Get the base data folder
    data_folder = get_app_data_folder(app_name)
    
    # Create logs subdirectory
    logs_folder = os.path.join(data_folder, "logs")
    
    # Ensure the logs directory exists
    os.makedirs(logs_folder, exist_ok=True)
    
    # Set log filename based on mode
    if designer:
        log_filename = "custom_widgets_designer.log"
    else:
        log_filename = "custom_widgets.log"
    
    log_file_path = os.path.join(logs_folder, log_filename)
    
    return log_file_path

# Setup logger
def setupLogger(self=None, designer=False):
    """
    Setup logger with proper file handling
    
    Args:
        self: Widget instance (optional)
        designer: Whether running in designer mode
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get the log file path
    logFilePath = get_log_file_path(designer=designer or (self is not None and is_in_designer(self)))
    
    # Get the log directory (already created in get_log_file_path, but just in case)
    logDirectory = os.path.dirname(logFilePath)
    if logDirectory and not os.path.exists(logDirectory):
        os.makedirs(logDirectory, exist_ok=True)
    
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Set up the rotating file handler
    logFileMaxSize = 10 * 1024 * 1024  # 10 MB
    backupCount = 5  # Keep up to 5 backup log files
    
    try:
        file_handler = RotatingFileHandler(
            logFilePath, 
            maxBytes=logFileMaxSize, 
            backupCount=backupCount,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Log the log file location on startup
        print(f"Log file location: {logFilePath}")
        
    except Exception as e:
        print(f"Failed to create log file handler for {logFilePath}: {e}")
        # Try fallback to temp folder if permission denied
        if "Permission denied" in str(e) or "Access is denied" in str(e):
            import tempfile
            fallback_path = os.path.join(tempfile.gettempdir(), "custom_widgets.log")
            print(f"Permission denied. Falling back to temp folder: {fallback_path}")
            try:
                file_handler = RotatingFileHandler(
                    fallback_path,
                    maxBytes=logFileMaxSize,
                    backupCount=backupCount,
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            except Exception as fallback_error:
                print(f"Also failed to create log in temp folder: {fallback_error}")
    
    # Console handler
    if RICH_AVAILABLE:
        try:
            rich_handler = RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                show_time=True,
                show_level=True,
                show_path=True
            )
            rich_handler.setLevel(logging.INFO)
            logger.addHandler(rich_handler)
        except Exception as e:
            print(f"Failed to create Rich handler: {e}")
            # Fallback to basic console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
    else:
        # Basic console handler when Rich is not available
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

# Optional: Function to clean up old logs
def cleanup_old_logs(app_name="CustomWidgets", max_log_files=10):
    """
    Clean up old log files, keeping only the most recent ones
    
    Args:
        app_name: Name of the application
        max_log_files: Maximum number of log files to keep
    """
    try:
        logs_folder = os.path.join(get_app_data_folder(app_name), "logs")
        if not os.path.exists(logs_folder):
            return
        
        # Get all log files
        log_files = []
        for file in os.listdir(logs_folder):
            if file.startswith("custom_widgets") and file.endswith(".log"):
                file_path = os.path.join(logs_folder, file)
                log_files.append((file_path, os.path.getmtime(file_path)))
        
        # Sort by modification time (oldest first)
        log_files.sort(key=lambda x: x[1])
        
        # Remove old files if we have too many
        while len(log_files) > max_log_files:
            old_file = log_files.pop(0)[0]
            try:
                os.remove(old_file)
                print(f"Removed old log file: {old_file}")
            except Exception as e:
                print(f"Failed to remove old log file {old_file}: {e}")
                
    except Exception as e:
        print(f"Error during log cleanup: {e}")

# The flag is cached: logging happens on worker threads too, and QSettings
# must never be constructed off the main thread (concurrent main-thread use
# can deadlock both threads on the settings lock file).
_show_logs_cache = None

def get_show_custom_widgets_logs():
    global _show_logs_cache
    if _show_logs_cache is None:
        if threading.current_thread() is not threading.main_thread():
            # Never touch QSettings from a worker; use the default until the
            # main thread primes the cache
            return True
        try:
            settings = QSettings()
            _show_logs_cache = settings.value("showCustomWidgetsLogs", True, type=bool)
        except Exception:
            return True
    return _show_logs_cache

def set_show_custom_widgets_logs(value: bool):
    global _show_logs_cache
    _show_logs_cache = bool(value)
    try:
        settings = QSettings()
        settings.setValue("showCustomWidgetsLogs", value)
    except Exception:
        pass

# Helper function to safely print with rich or fallback to normal print
def safe_console_print(*args, **kwargs):
    """Safely print using rich if available, otherwise use normal print"""
    if RICH_AVAILABLE:
        try:
            console.print(*args, **kwargs)
            return True
        except Exception:
            # If rich fails, fall back to normal print
            pass
    
    # Fallback to normal print
    # Remove any rich formatting tags for cleaner output
    message = args[0] if args else ""
    if isinstance(message, str):
        # Simple stripping of rich tags [tag]text[/tag] -> text
        import re
        message = re.sub(r'\[/?[^\]]+\]', '', message)
    print(message)
    return False

# Enhanced logging functions with rich formatting
def logDebug(message, **kwargs):
    logging.debug(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f" DEBUG: {message}", **kwargs)

def logInfo(message, **kwargs):
    logging.info(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f" INFO: {message}", **kwargs)

def logWarning(message, **kwargs):
    logging.warning(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f" WARNING: {message}", **kwargs)

def logError(message, **kwargs):
    logging.error(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f" ERROR: {message}", **kwargs)

def logCritical(message, **kwargs):
    logging.critical(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f" CRITICAL: {message}", **kwargs)

def logSuccess(message, **kwargs):
    logging.info(f"SUCCESS: {message}", extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f" SUCCESS: {message}", **kwargs)

def logException(exception, message="Exception", **kwargs):
    logging.exception(f"{message}: {exception}", extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f" EXCEPTION: {message}: {exception}")
        if RICH_AVAILABLE:
            try:
                console.print(Traceback.from_exception(type(exception), exception, exception.__traceback__))
            except Exception:
                traceback.print_exc()
        else:
            traceback.print_exc()

# File monitoring specific logging functions
def logFileMonitorStart(files_count, folder_path=None):
    folder_text = f" in {folder_path}" if folder_path else ""
    message = f"Starting file monitor - Tracking {files_count} files{folder_text}"
    logInfo(message)
    
    if get_show_custom_widgets_logs() and RICH_AVAILABLE:
        try:
            console.print(Panel.fit(
                f" FILE MONITOR STARTED\n"
                f"• Files: {files_count}\n"
                f"• Folder: {folder_path or 'N/A'}",
                border_style="blue"
            ))
        except Exception:
            print(f" FILE MONITOR STARTED - Files: {files_count}, Folder: {folder_path or 'N/A'}")

def logFileChange(path, action="modified"):
    filename = os.path.basename(path)
    logInfo(f"File {filename} has been {action}")
    if get_show_custom_widgets_logs():
        safe_console_print(f" File {action}: {filename}")

def logFileListUpdate(new_files, removed_files, total_files):
    changes = []
    if new_files:
        changes.append(f"+{len(new_files)} new")
    if removed_files:
        changes.append(f"-{len(removed_files)} removed")
    
    if changes:
        changes_text = ', '.join(changes)
        logInfo(f"File list updated: {changes_text} - Total: {total_files} files")
        if get_show_custom_widgets_logs():
            safe_console_print(f" File list updated: {changes_text} - Total: {total_files} files")

def logFileConversionStart(file_path):
    filename = os.path.basename(file_path)
    logInfo(f"Starting conversion of {filename}")
    if get_show_custom_widgets_logs():
        safe_console_print(f" Converting: {filename}")

def logFileConversionComplete(file_path):
    filename = os.path.basename(file_path)
    logSuccess(f"Completed conversion of {filename}")
    if get_show_custom_widgets_logs():
        safe_console_print(f" Converted: {filename}")

def logWidgetProcessing(widget_class, widget_name, details=""):
    details_text = f" - {details}" if details else ""
    logDebug(f"Processing widget: {widget_class} '{widget_name}'{details_text}")
    if get_show_custom_widgets_logs():
        safe_console_print(f" Widget: {widget_class} '{widget_name}'{details_text}")

def logIconProcessing(widget_name, icon_url, widget_type="Widget"):
    logDebug(f"{widget_type} '{widget_name}' icon: {icon_url}")
    if get_show_custom_widgets_logs():
        safe_console_print(f" {widget_type} icon: '{widget_name}'  {icon_url}")

def logJSONUpdate(json_file, data_summary):
    logInfo(f"Updated JSON file: {json_file} with {data_summary}")
    if get_show_custom_widgets_logs():
        safe_console_print(f" JSON updated: {json_file} - {data_summary}")

# Handle unhandled exceptions with rich formatting
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.critical("Unhandled exception occurred:\n%s", formatted_traceback)
    
    if get_show_custom_widgets_logs():
        if RICH_AVAILABLE:
            try:
                console.print(Panel.fit(
                    f"UNHANDLED EXCEPTION\n"
                    f"{exc_type.__name__}: {exc_value}",
                    border_style="red"
                ))
                console.print(Traceback.from_exception(exc_type, exc_value, exc_traceback))
            except Exception:
                print("UNHANDLED EXCEPTION:")
                print(formatted_traceback)
        else:
            print("UNHANDLED EXCEPTION:")
            print(formatted_traceback)

# Set the exception hook for unhandled exceptions
sys.excepthook = handle_unhandled_exception

# Initialize logger when module is imported
# Note: You may want to call this explicitly in your main application
# logger = setupLogger()