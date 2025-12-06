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

    # Rich console handler for beautiful output
    if RICH_AVAILABLE:
        rich_handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_level=True,
            show_path=True
        )
        rich_handler.setLevel(logging.INFO)
    else:
        # Fallback to basic console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

# Retrieve QSettings
def get_show_custom_widgets_logs():
    settings = QSettings()
    return settings.value("showCustomWidgetsLogs", True, type=bool)

def set_show_custom_widgets_logs(value: bool):
    settings = QSettings()
    settings.setValue("showCustomWidgetsLogs", value)

# Enhanced logging functions with rich formatting
def logDebug(message, **kwargs):
    logging.debug(message, extra=kwargs)
    if get_show_custom_widgets_logs() and RICH_AVAILABLE:
        console.print(f"🔍 [debug]DEBUG:[/debug] {message}", **kwargs)

def logInfo(message, **kwargs):
    logging.info(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        if RICH_AVAILABLE:
            console.print(f"ℹ️ [info]INFO:[/info] {message}", **kwargs)
        else:
            print(f"INFO: {message}")

def logWarning(message, **kwargs):
    logging.warning(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        if RICH_AVAILABLE:
            console.print(f"⚠️ [warning]WARNING:[/warning] {message}", **kwargs)
        else:
            print(f"WARNING: {message}")

def logError(message, **kwargs):
    logging.error(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        if RICH_AVAILABLE:
            console.print(f"❌ [error]ERROR:[/error] {message}", **kwargs)
        else:
            print(f"ERROR: {message}")

def logCritical(message, **kwargs):
    logging.critical(message, extra=kwargs)
    if get_show_custom_widgets_logs():
        if RICH_AVAILABLE:
            console.print(f"💥 [critical]CRITICAL:[/critical] {message}", **kwargs)
        else:
            print(f"CRITICAL: {message}")

def logSuccess(message, **kwargs):
    logging.info(f"SUCCESS: {message}", extra=kwargs)
    if get_show_custom_widgets_logs() and RICH_AVAILABLE:
        console.print(f"✅ [success]SUCCESS:[/success] {message}", **kwargs)

def logException(exception, message="Exception", **kwargs):
    logging.exception(f"{message}: {exception}", extra=kwargs)
    if get_show_custom_widgets_logs():
        if RICH_AVAILABLE:
            console.print(f"🚨 [error]EXCEPTION:[/error] {message}: {exception}", **kwargs)
            console.print(Traceback.from_exception(type(exception), exception, exception.__traceback__))
        else:
            print(f"EXCEPTION: {message}: {exception}")
            traceback.print_exc()

# File monitoring specific logging functions
def logFileMonitorStart(files_count, folder_path=None):
    message = f"Starting file monitor - Tracking {files_count} files"
    if folder_path:
        message += f" in [folder]{folder_path}[/folder]"
    logInfo(message)
    if RICH_AVAILABLE and get_show_custom_widgets_logs():
        console.print(Panel.fit(
            f"📁 [monitor]FILE MONITOR STARTED[/monitor]\n"
            f"• Files: [file]{files_count}[/file]\n"
            f"• Folder: [folder]{folder_path or 'N/A'}[/folder]",
            border_style="blue"
        ))

def logFileChange(path, action="modified"):
    logInfo(f"File [file]{path}[/file] has been {action}")
    if RICH_AVAILABLE and get_show_custom_widgets_logs():
        console.print(f"📝 [info]File {action}:[/info] [file]{os.path.basename(path)}[/file]")

def logFileListUpdate(new_files, removed_files, total_files):
    changes = []
    if new_files:
        changes.append(f"[success]+{len(new_files)} new[/success]")
    if removed_files:
        changes.append(f"[error]-{len(removed_files)} removed[/error]")
    
    if changes:
        logInfo(f"File list updated: {', '.join(changes)} - Total: {total_files} files")
        if RICH_AVAILABLE and get_show_custom_widgets_logs():
            console.print(f"🔄 [info]File list updated:[/info] {', '.join(changes)} - Total: [file]{total_files}[/file] files")

def logFileConversionStart(file_path):
    logInfo(f"Starting conversion of [file]{file_path}[/file]")
    if RICH_AVAILABLE and get_show_custom_widgets_logs():
        console.print(f"🛠️ [info]Converting:[/info] [file]{os.path.basename(file_path)}[/file]")

def logFileConversionComplete(file_path):
    logSuccess(f"Completed conversion of [file]{file_path}[/file]")
    if RICH_AVAILABLE and get_show_custom_widgets_logs():
        console.print(f"✅ [success]Converted:[/success] [file]{os.path.basename(file_path)}[/file]")

def logWidgetProcessing(widget_class, widget_name, details=""):
    details_text = f" - {details}" if details else ""
    logDebug(f"Processing widget: {widget_class} '{widget_name}'{details_text}")
    if RICH_AVAILABLE and get_show_custom_widgets_logs():
        console.print(f"🎛️ [debug]Widget:[/debug] {widget_class} '[file]{widget_name}[/file]'[dim]{details_text}[/dim]")

def logIconProcessing(widget_name, icon_url, widget_type="Widget"):
    logDebug(f"{widget_type} '{widget_name}' icon: {icon_url}")
    if RICH_AVAILABLE and get_show_custom_widgets_logs():
        console.print(f"🖼️ [debug]{widget_type} icon:[/debug] '[file]{widget_name}[/file]' → [file]{icon_url}[/file]")

def logJSONUpdate(json_file, data_summary):
    logInfo(f"Updated JSON file: {json_file} with {data_summary}")
    if RICH_AVAILABLE and get_show_custom_widgets_logs():
        console.print(f"📊 [info]JSON updated:[/info] [file]{json_file}[/file] - {data_summary}")

# Handle unhandled exceptions with rich formatting
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.critical("Unhandled exception occurred:\n%s", formatted_traceback)
    
    if get_show_custom_widgets_logs():
        if RICH_AVAILABLE:
            console.print(Panel.fit(
                f"[critical]UNHANDLED EXCEPTION[/critical]\n"
                f"[error]{exc_type.__name__}: {exc_value}[/error]",
                border_style="red"
            ))
            console.print(Traceback.from_exception(exc_type, exc_value, exc_traceback))
        else:
            print("UNHANDLED EXCEPTION:")
            print(formatted_traceback)

# Set the exception hook for unhandled exceptions
sys.excepthook = handle_unhandled_exception

# Initialize logger when module is imported
# setupLogger()