import logging
import os
import sys
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

# Setup logger
def setupLogger(self=None, designer=False):
    logFilePath = os.path.join(os.getcwd(), "logs/custom_widgets.log")
    if designer or (self is not None and is_in_designer(self)):
        logFilePath = os.path.join(os.getcwd(), "logs/custom_widgets_designer.log")
    
    # Ensure the log directory exists
    logDirectory = os.path.dirname(logFilePath)
    if logDirectory != "" and not os.path.exists(logDirectory):
        os.makedirs(logDirectory)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Set up the rotating file handler
    logFileMaxSize = 10 * 1024 * 1024  # 10 MB
    backupCount = 5  # Keep up to 5 backup log files
    
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

# Retrieve QSettings
def get_show_custom_widgets_logs():
    try:
        settings = QSettings()
        return settings.value("showCustomWidgetsLogs", True, type=bool)
    except Exception:
        return True

def set_show_custom_widgets_logs(value: bool):
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
        safe_console_print(f"🔍 DEBUG: {message}", **kwargs)

def logInfo(message, **kwargs):
    logging.info(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f"ℹ️ INFO: {message}", **kwargs)

def logWarning(message, **kwargs):
    logging.warning(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f"⚠️ WARNING: {message}", **kwargs)

def logError(message, **kwargs):
    logging.error(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f"❌ ERROR: {message}", **kwargs)

def logCritical(message, **kwargs):
    logging.critical(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f"💥 CRITICAL: {message}", **kwargs)

def logSuccess(message, **kwargs):
    logging.info(f"SUCCESS: {message}", extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f"✅ SUCCESS: {message}", **kwargs)

def logException(exception, message="Exception", **kwargs):
    logging.exception(f"{message}: {exception}", extra=kwargs)
    if get_show_custom_widgets_logs():
        safe_console_print(f"🚨 EXCEPTION: {message}: {exception}")
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
                f"📁 FILE MONITOR STARTED\n"
                f"• Files: {files_count}\n"
                f"• Folder: {folder_path or 'N/A'}",
                border_style="blue"
            ))
        except Exception:
            print(f"📁 FILE MONITOR STARTED - Files: {files_count}, Folder: {folder_path or 'N/A'}")

def logFileChange(path, action="modified"):
    filename = os.path.basename(path)
    logInfo(f"File {filename} has been {action}")
    if get_show_custom_widgets_logs():
        safe_console_print(f"📝 File {action}: {filename}")

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
            safe_console_print(f"🔄 File list updated: {changes_text} - Total: {total_files} files")

def logFileConversionStart(file_path):
    filename = os.path.basename(file_path)
    logInfo(f"Starting conversion of {filename}")
    if get_show_custom_widgets_logs():
        safe_console_print(f"🛠️ Converting: {filename}")

def logFileConversionComplete(file_path):
    filename = os.path.basename(file_path)
    logSuccess(f"Completed conversion of {filename}")
    if get_show_custom_widgets_logs():
        safe_console_print(f"✅ Converted: {filename}")

def logWidgetProcessing(widget_class, widget_name, details=""):
    details_text = f" - {details}" if details else ""
    logDebug(f"Processing widget: {widget_class} '{widget_name}'{details_text}")
    if get_show_custom_widgets_logs():
        safe_console_print(f"🎛️ Widget: {widget_class} '{widget_name}'{details_text}")

def logIconProcessing(widget_name, icon_url, widget_type="Widget"):
    logDebug(f"{widget_type} '{widget_name}' icon: {icon_url}")
    if get_show_custom_widgets_logs():
        safe_console_print(f"🖼️ {widget_type} icon: '{widget_name}' → {icon_url}")

def logJSONUpdate(json_file, data_summary):
    logInfo(f"Updated JSON file: {json_file} with {data_summary}")
    if get_show_custom_widgets_logs():
        safe_console_print(f"📊 JSON updated: {json_file} - {data_summary}")

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
# setupLogger()