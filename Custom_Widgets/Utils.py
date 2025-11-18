import os
import sys
import re
import shutil
import subprocess
import qtpy
from qtpy.QtDesigner import QDesignerFormWindowInterface
from qtpy.QtGui import QIcon
from qtpy.QtCore import QSettings

# Import custom logging module
from Custom_Widgets.Log import *

def get_absolute_path(relative_path):
    """Convert a relative path to an absolute path based on the script's directory."""
    import __main__
    
    # Try multiple methods to find the main script directory
    possible_dirs = []
    
    # Method 1: __main__.__file__
    if hasattr(__main__, '__file__'):
        possible_dirs.append(os.path.dirname(os.path.abspath(__main__.__file__)))
    
    # Method 2: sys.argv[0] (your original approach)
    if sys.argv[0]:
        possible_dirs.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    
    # Method 3: Current working directory
    possible_dirs.append(os.path.abspath(os.getcwd()))
    
    # Use the first valid directory that contains the relative path when joined
    for main_dir in possible_dirs:
        test_path = os.path.join(main_dir, relative_path)
        if os.path.exists(test_path):
            return os.path.normpath(test_path)
    
    # If no existing path found, use the first method and hope for the best
    main_dir = possible_dirs[0] if possible_dirs else os.path.abspath(os.getcwd())
    return os.path.normpath(os.path.join(main_dir, relative_path))

def replace_url_prefix(url, new_prefix):
    pattern = re.compile(r':/[^/]+/')
    return pattern.sub( new_prefix + '/', url, 1)

def get_icon_path(icon: QIcon | str) -> str:
    """Return the correct path for a themed icon. Handle both QIcon and string paths."""
    settings = QSettings()
    # Check if the 'ICONS-COLOR' setting is defined
    if settings.value("ICONS-COLOR") is not None:
        # Get the normal color and derive the icon folder name from it
        normal_color = settings.value("ICONS-COLOR")
        icons_folder = normal_color.replace("#", "")  # Strip the '#' for folder naming

        # Regular expression to remove the old prefix in the icon path
        prefix_to_remove = re.compile(r'^Qss/icons/[^/]+/')

        if isinstance(icon, QIcon):
            # Handle QIcon by converting to the appropriate icon path
            icon_url = icon.name()  # Assuming the QIcon has a name or can be represented
            return icon.addFile(re.sub(prefix_to_remove, f'Qss/icons/{icons_folder}/', replace_url_prefix(icon_url, "Qss/icons")))

        elif isinstance(icon, str):
            # If the input is a string (file path), process it directly
            return re.sub(prefix_to_remove, f'Qss/icons/{icons_folder}/', replace_url_prefix(icon, "Qss/icons"))

    return icon 

def is_in_designer(self):
    """Check if the widget is in Qt Designer."""
    # logInfo(QDesignerFormWindowInterface.findChild(self))
    return QDesignerFormWindowInterface.findFormWindow(self) is not None


def createQrcFile(contents, filePath):
    # Ensure the directory for the filePath exists
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    
    # Save QRC content to a file
    with open(filePath, 'w', encoding='utf-8') as qrc_file:
        qrc_file.write(contents)

    # print(f'QRC file generated: {filePath}')

def qrcToPy(qrcFile, pyFile):
    """
    Convert a Qt Resource Collection (qrc) file to a Python file.

    Parameters:
    - qrc_file (str): Path to the input qrc file.
    - py_file (str): Path to the output py file.
    """
    try:
        if qtpy.API_NAME == "PyQt5":
            rcc_command = 'pyrcc5'
        elif qtpy.API_NAME == "PyQt6":
            rcc_command = 'pyrcc6'
        elif qtpy.API_NAME == "PySide2":
            rcc_command = 'pyside2-rcc'
        elif qtpy.API_NAME == "PySide6":
            rcc_command = 'pyside6-rcc'
        else:
            raise Exception("Error: Unknown QT binding/API Name", qtpy.API_NAME)

        print(f'{rcc_command} "{qrcFile}" -o "{pyFile}"')
        subprocess.run(f'{rcc_command} "{qrcFile}" -o "{pyFile}"')
        
    except Exception as e:
        print("Error converting qrc to py:", e)

def uiToPy(uiFile, pyFile):
    """
    Convert a Qt UI file to a Python file.

    Parameters:
    - uiFile (str): Path to the input UI file.
    - pyFile (str): Path to the output Python file.
    """
    try:
        if qtpy.API_NAME == "PyQt5":
            pyuic_command = 'pyuic5'
        elif qtpy.API_NAME == "PyQt6":
            pyuic_command = 'pyuic6'
        elif qtpy.API_NAME == "PySide2":
            pyuic_command = 'pyside2-uic'
        elif qtpy.API_NAME == "PySide6":
            pyuic_command = 'pyside6-uic'
        else:
            raise Exception("Error: Unknown Qt binding/API Name", qtpy.API_NAME)

        os.system(f'{pyuic_command} "{uiFile}" -o "{pyFile}"')

    except Exception as e:
        print("Error converting ui to py:", e)

def renameFolder(old_name, new_name):
    try:
        # Check if the destination directory exists
        if os.path.exists(new_name):
            # Remove the destination directory if it exists
            shutil.rmtree(new_name)

        # Rename the folder
        os.rename(old_name, new_name)
    except Exception as e:
        pass


class SharedData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedData, cls).__new__(cls)
            cls._instance.file_urls = []  # Initialize an empty list for file URLs
        return cls._instance

    def add_file_url(self, file_url):
        """Add a new file URL to the list."""
        if file_url not in self.file_urls:  # Prevent duplicates
            self.file_urls.append(file_url)

    def get_file_urls(self):
        """Return the list of file URLs."""
        return self.file_urls

    def clear_file_urls(self):
        """Clear the list of file URLs."""
        self.file_urls.clear()

    def url_exists(self, file_url):
        """Check if a file URL exists in the list."""
        return file_url in self.file_urls

