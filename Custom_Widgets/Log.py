import logging
import os
import sys
import traceback
from logging.handlers import RotatingFileHandler
from qtpy.QtCore import QSettings
from Custom_Widgets.Utils import is_in_designer

# Setup logger
def setupLogger(self = None, designer = False):
    logFilePath = os.path.join(os.getcwd(), "logs/custom_widgets.log")
    if designer or (self is not None and is_in_designer(self)):
        logFilePath = os.path.join(os.getcwd(), "logs/custom_widgets_designer.log")
    # Ensure the log directory exists
    logDirectory = os.path.dirname(logFilePath)
    if logDirectory != "" and not os.path.exists(logDirectory):
        os.makedirs(logDirectory)

    # Set up the rotating file handler
    logFileMaxSize = 5 * 1024 * 1024  # 1 MB
    backupCount = 3  # Keep up to 3 backup log files
    
    # Set up the RotatingFileHandler
    handler = RotatingFileHandler(logFilePath, maxBytes=logFileMaxSize, backupCount=backupCount)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Get the root logger and configure it
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    # Optionally, also log to the console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

# Retrieve QSettings
def get_show_custom_widgets_logs():
    settings = QSettings()
    return settings.value("showCustomWidgetsLogs", False, type=bool)

# Example of how to set QSettings value
def set_show_custom_widgets_logs(value: bool):
    settings = QSettings()
    settings.setValue("showCustomWidgetsLogs", value)

# Log info with QSettings
def logInfo(message):
    logging.info(message)
    if get_show_custom_widgets_logs():
        print(message)

def logWarning(message):
    logging.warning(message)
    if get_show_custom_widgets_logs():
        print(message)

def logError(message):
    logging.error(message)
    if get_show_custom_widgets_logs():
        print(message)

def logException(exception, message="Exception"):
    logging.exception(f"{message}: {exception}")
    if get_show_custom_widgets_logs():
        print(f"{message}: {exception}")

def logCritical(message):
    logging.critical(message)
    if get_show_custom_widgets_logs():
        print(message)

# Handle unhandled exceptions
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow keyboard interrupts to exit the program
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    # Log the unhandled exception
    # Format the traceback
    formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    # Log the unhandled exception with detailed traceback
    logging.error("Unhandled exception occurred:\n%s", formatted_traceback)
    
    # Print the detailed exception information to the console
    print("Unhandled exception occurred:")
    print(formatted_traceback)

# Set the exception hook for unhandled exceptions
sys.excepthook = handle_unhandled_exception

# Call the logger setup
# setupLogger()
