import os
from pathlib import Path
import re
import json
import sys
import shutil
import codecs
import subprocess
from urllib.parse import urlparse
import __main__

import colorsys

from qtpy.QtWidgets import QApplication, QPushButton, QLabel, QTabWidget, QCheckBox, QToolBox, QMainWindow, QMenu, QTreeWidgetItem
from qtpy.QtGui import QPalette, QCursor, QFont, QFontDatabase, QIcon, QColor, QPixmap, QPixmapCache
from qtpy.QtCore import QCoreApplication, QRect, Signal, QObject, QSettings, Property, QDir, QThreadPool

import qtsass


def _qcolor_rgbf(color):
    """Any color spec (CSS/SVG name, hex string, float rgb(a) tuple) ->
    (r, g, b) floats in 0-1, via QColor. Replaces matplotlib.colors."""
    if isinstance(color, (tuple, list)):
        qc = QColor.fromRgbF(*[float(v) for v in color[:3]])
    else:
        qc = QColor(str(color))
    if not qc.isValid():
        raise ValueError(f"Invalid color: {color!r}")
    return qc.redF(), qc.greenF(), qc.blueF()

# Icons are shipped and themed as SVG. Importing QtSvg makes sure the Qt SVG
# image-format plugin is bundled by deployment tools (PyInstaller, cx_Freeze).
try:
    from qtpy import QtSvg  # noqa: F401
except Exception:
    QtSvg = None

from Custom_Widgets.QCustomCheckBox import QCustomCheckBox
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomSidebarLabel import QCustomSidebarLabel 
from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton 
from Custom_Widgets.WidgetsWorker import Worker, WorkerResponse
from Custom_Widgets.Project import projectRoot
from Custom_Widgets.Log import *
from Custom_Widgets.Utils import createQrcFile, is_in_designer
from Custom_Widgets.JSonStyles import loadJsonStyle

class QCustomTheme(QObject):
    _instance = None  # Class-level variable to hold the singleton instance
    onThemeChanged = Signal()  # Define a class-level signal
    onThemeChangeComplete = Signal()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create a new instance if not already created
            cls._instance = super(QCustomTheme, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parent=None):
        if not hasattr(self, "_initialized"):  # To prevent reinitialization
            # NEVER adopt a QObject parent: the theme engine is a process
            # singleton and a parent (e.g. the first QCustomQMainWindow)
            # would let Qt destroy it with that widget, leaving every later
            # QCustomTheme() caller a dead C++ wrapper.
            super().__init__(None)
            self._theme = "default"
            self._themes = []
            self._last_variables_scss = None
            self._initialized = True  # Mark as initialized to avoid multiple init calls
            self.checkForMissingicons = True
            self.script_dir = projectRoot().replace("\\", "/") + "/"

            self.initializeThemeVars()
            self.defineThemeVarMapping()
            self.loadAppFont()

            QCoreApplication.instance().aboutToQuit.connect(self.stopWorkers)

            # START THREAD
            self.customWidgetsThreadpool = QThreadPool()

            self._themes.append(Light())
            self._themes.append(Dark())

            self.jsonStyleSheets = [] 
            self.jsonStyleData = {}

            self.designerIconsColor = ""  # empty = follow theme / $ICONS_COLOR
            self.themesRead = False

            self._isThemeDark = False 
            # Theme indicator variables 
            self.THEME_MODE = ""      # Will be "DARK" or "LIGHT"
            self.THEME_ICON = ""      # Will be "moon" or "sun"
            self.THEME_STATUS = ""    # Will be "Dark Mode Active" or "Light Mode Active"

    def updateThemeIndicators(self):
        """Update theme indicator variables based on current theme"""
        is_dark = self.isAppDarkThemed()
        
        if is_dark:
            self.THEME_MODE = "DARK"
            self.THEME_ICON = "moon"
            self.THEME_STATUS = "Dark Mode Active"
            self._isThemeDark = True
        else:
            self.THEME_MODE = "LIGHT"
            self.THEME_ICON = "sun"
            self.THEME_STATUS = "Light Mode Active"
            self._isThemeDark = False
        
        return self.THEME_MODE

    def initializeThemeVars(self):
        """Initialize all theme variables"""

        # Initialize background colors
        self.COLOR_BACKGROUND_1 = ""
        self.COLOR_BACKGROUND_2 = ""
        self.COLOR_BACKGROUND_3 = ""
        self.COLOR_BACKGROUND_4 = ""
        self.COLOR_BACKGROUND_5 = ""
        self.COLOR_BACKGROUND_6 = ""
        
        # Initialize text colors
        self.COLOR_TEXT_1 = ""
        self.COLOR_TEXT_2 = ""
        self.COLOR_TEXT_3 = ""
        self.COLOR_TEXT_4 = ""
        
        # Initialize accent colors
        self.COLOR_ACCENT_1 = ""
        self.COLOR_ACCENT_2 = ""
        self.COLOR_ACCENT_3 = ""
        self.COLOR_ACCENT_4 = ""
        
        # Initialize other theme-specific variables
        self.PATH_RESOURCES = ""

    def defineThemeVarMapping(self):
        # Define the mapping of variables to their corresponding values in self
        mapping = {
            '$COLOR_BACKGROUND_1': self.COLOR_BACKGROUND_1,
            '$COLOR_BACKGROUND_2': self.COLOR_BACKGROUND_2,
            '$COLOR_BACKGROUND_3': self.COLOR_BACKGROUND_3,
            '$COLOR_BACKGROUND_4': self.COLOR_BACKGROUND_4,
            '$COLOR_BACKGROUND_5': self.COLOR_BACKGROUND_5,
            '$COLOR_BACKGROUND_6': self.COLOR_BACKGROUND_6,
            '$COLOR_TEXT_1': self.COLOR_TEXT_1,
            '$COLOR_TEXT_2': self.COLOR_TEXT_2,
            '$COLOR_TEXT_3': self.COLOR_TEXT_3,
            '$COLOR_TEXT_4': self.COLOR_TEXT_4,
            '$COLOR_ACCENT_1': self.COLOR_ACCENT_1,
            '$COLOR_ACCENT_2': self.COLOR_ACCENT_2,
            '$COLOR_ACCENT_3': self.COLOR_ACCENT_3,
            '$COLOR_ACCENT_4': self.COLOR_ACCENT_4,
            '$OPACITY_TOOLTIP': '230',
            '$SIZE_BORDER_RADIUS': '8px',
            '$BORDER_1': '1px solid ' + self.COLOR_BACKGROUND_1,
            '$BORDER_2': '1px solid ' + self.COLOR_BACKGROUND_4,
            '$BORDER_3': '1px solid ' + self.COLOR_BACKGROUND_6,
            '$BORDER_SELECTION_3': '1px solid ' + self.COLOR_ACCENT_3,
            '$BORDER_SELECTION_2': '1px solid ' + self.COLOR_ACCENT_2,
            '$BORDER_SELECTION_1': '1px solid ' + self.COLOR_ACCENT_1,
            '$PATH_RESOURCES': f"'{self.PATH_RESOURCES}'",
            '$RELATIVE_FOLDER': f"{self.script_dir}",
            '$BASE_DIR': f"{self.script_dir}",
            
            'THEME.COLOR_BACKGROUND_1': self.COLOR_BACKGROUND_1,
            'THEME.COLOR_BACKGROUND_2': self.COLOR_BACKGROUND_2,
            'THEME.COLOR_BACKGROUND_3': self.COLOR_BACKGROUND_3,
            'THEME.COLOR_BACKGROUND_4': self.COLOR_BACKGROUND_4,
            'THEME.COLOR_BACKGROUND_5': self.COLOR_BACKGROUND_5,
            'THEME.COLOR_BACKGROUND_6': self.COLOR_BACKGROUND_6,
            'THEME.COLOR_TEXT_1': self.COLOR_TEXT_1,
            'THEME.COLOR_TEXT_2': self.COLOR_TEXT_2,
            'THEME.COLOR_TEXT_3': self.COLOR_TEXT_3,
            'THEME.COLOR_TEXT_4': self.COLOR_TEXT_4,
            'THEME.COLOR_ACCENT_1': self.COLOR_ACCENT_1,
            'THEME.COLOR_ACCENT_2': self.COLOR_ACCENT_2,
            'THEME.COLOR_ACCENT_3': self.COLOR_ACCENT_3,
            'THEME.COLOR_ACCENT_4': self.COLOR_ACCENT_4,
            'THEME.OPACITY_TOOLTIP': '230',
            'THEME.SIZE_BORDER_RADIUS': '8px',
            'THEME.BORDER_1': '1px solid ' + self.COLOR_BACKGROUND_1,
            'THEME.BORDER_2': '1px solid ' + self.COLOR_BACKGROUND_4,
            'THEME.BORDER_3': '1px solid ' + self.COLOR_BACKGROUND_6,
            'THEME.BORDER_SELECTION_3': '1px solid ' + self.COLOR_ACCENT_3,
            'THEME.BORDER_SELECTION_2': '1px solid ' + self.COLOR_ACCENT_2,
            'THEME.BORDER_SELECTION_1': '1px solid ' + self.COLOR_ACCENT_1,
            'THEME.PATH_RESOURCES': f"'{self.PATH_RESOURCES}'"
        }
        
        # Add other variables from the current theme
        if hasattr(self.currentTheme, 'other_variables'):
            for var_name, var_value in self.currentTheme.other_variables.items():
                mapping[f'${var_name}'] = var_value
                mapping[f'THEME.{var_name}'] = var_value
        
        self._variable_mapping = mapping
        return self._variable_mapping

    @Property(object)
    def themes(self):
        return self._themes
    
    @Property(str)
    def theme(self):
        settings = QSettings()
        theme = settings.value("THEME")
        if theme:
            self._theme = theme
        return self._theme
    
    @theme.setter
    def theme(self, value: str):
        self._theme = value

        self.setTheme(value)
    
    def setTheme(self, value):
        self._theme = value
        settings = QSettings()
        try:
            settings.setValue("THEME", value)
        except Exception as e:
            logError(f"Failed to write theme to QSettings: {e}")
        # if settings.value("INIT-THEME-SET") is None:
        #     settings.setValue("INIT-THEME-SET", True)
        
        self.onThemeChanged.emit()  # Emit the signal when theme is modified
        self.applyCompiledSass()

    def refreshTheme(self):
        QAppSettings.updateAppSettings(self, reloadJson = False)

    def themeChanged(self):
        # Emit the signal from the instance
        self.onThemeChanged.emit()

    def isAppDarkThemed(self):
        app = QApplication.instance()
        # if app is None:
        #     raise RuntimeError("QApplication instance is required.")
        
        palette = app.palette()
        
        # Extract the background color of the application palette
        background_color = QColor(self.COLOR_BACKGROUND_1)
        
        # Calculate luminance using the YIQ color space formula
        luminance = (0.299 * background_color.red() + 0.587 * background_color.green() + 0.114 * background_color.blue()) / 255
        # Determine if the background color is considered dark or light
        if luminance < 0.5:
            return True  # Dark theme
        else:
            return False  # Light theme
        
    @staticmethod
    def getCurrentScreen():
        """ get current screen """
        cursorPos = QCursor.pos()

        for s in QApplication.screens():
            if s.geometry().contains(cursorPos):
                return s

        return None
    
    @staticmethod
    def readJsonFile(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except Exception as e:
            logError(f"Failed to read JSON file {file_path}: {e}")
            return {}

    @Property(object)
    def currentTheme(self):
        settings = QSettings()
        _theme = settings.value("THEME")
        for theme in self.themes:
            if theme.name == _theme:
               return theme 
            
            if theme.name == self.theme:
               return theme 
            
        for theme in self.themes:
            if theme.name == "Light":
               return theme 

    @Property(str)
    def iconsColor(self):
        return self.currentTheme.iconsColor
    
    @Property(bool)
    def isThemeDark(self):
        # Create QApplication instance if it doesn't exist
        app = QApplication.instance() if QApplication.instance() else QApplication([])
        palette = app.palette()

        background_color = palette.color(QPalette.Window)
        
        # Calculate luminance using the YIQ color space formula
        luminance = (0.299 * background_color.red() + 0.587 * background_color.green() + 0.114 * background_color.blue()) / 255

        if luminance < 0.5:
            self._isThemeDark =  True  
        else:
            self._isThemeDark = False 
        
        return self._isThemeDark
    
    def getPalette(self):
        app = QApplication.instance() if QApplication.instance() else QApplication([])
        return app.palette()

    def _resolveThemedIconPath(self, abs_icon_url):
        """Themed icons are SVG. UI files designed against the old rasterized
        set may still name .png files - map them to the .svg equivalent."""
        root, ext = os.path.splitext(abs_icon_url)
        if ext.lower() == ".png":
            return root + ".svg"
        return abs_icon_url

    def applyIcons(self, widget_container, folder=None, ui_file_name=None):
        try:
            icons_color = self.iconsColor

            settings = QSettings()
            try:
                settings.setValue("ICONS-COLOR", icons_color)
            except Exception as e:
                logError(f"Failed to write ICONS-COLOR to QSettings: {e}")

            if not folder:
                # Single shared icon set
                folder = "icons"

            current_script_folder = projectRoot()
            jsonFilesFolder = os.path.abspath(os.path.join(current_script_folder, "generated-files/json"))
            if not os.path.exists(jsonFilesFolder):
                try:
                    os.makedirs(jsonFilesFolder)
                    logInfo(f"Created JSON files folder: {jsonFilesFolder}")
                except Exception as e:
                    logError(f"Failed to create JSON files folder {jsonFilesFolder}: {e}")
            
            prefix_to_remove = re.compile(r'icons(.*?)icons', re.IGNORECASE)

            widget_classes = {
                "QPushButton": "setNewIcon",
                "QCheckBox": "setNewIcon",
                "QCustomCheckBox": "setNewIcon",
                "QWidget": None,
                "QCustomSidebarLabel": "setNewIcon",
                "QCustomSidebarButton": "setNewIcon",
                "QCustomThemeDarkLightToggle": None,
                "QTreeWidget": None,
                "QLabel": "setNewPixmap"
            }

            for jsonFile in os.listdir(jsonFilesFolder):
                if jsonFile.endswith(".json"):
                    try:
                        if ui_file_name:
                            json_filename_without_extension = os.path.splitext(jsonFile)[0]
                            if json_filename_without_extension != ui_file_name:
                                continue
                        jsonFilePath = os.path.join(jsonFilesFolder, jsonFile)

                        widget_data = self.readJsonFile(jsonFilePath)
                        logInfo(f"Processing JSON file: {jsonFilePath}")

                        for widget_class, setter_method in widget_classes.items():
                            widgets_info = widget_data.get(widget_class, [])
                            for widget_info in widgets_info:
                                try:
                                    widget_name = widget_info.get("name", "")
                                    icon_url = widget_info.get("icon", "") or widget_info.get("pixmap", "")

                                    icon_url = re.sub(prefix_to_remove, f'icons/{folder}', icon_url).replace("../", "")
                                    abs_icon_url = os.path.abspath(os.path.join(current_script_folder, icon_url))
                                    abs_icon_url = self._resolveThemedIconPath(abs_icon_url)

                                    if not os.path.exists(abs_icon_url):
                                        logError(f"Failed to process widget '{widget_name}' in JSON file '{jsonFile}': Error: Missing file - {abs_icon_url}")
                                        continue

                                    # Safety check: ensure widget_container still has the attribute
                                    if not hasattr(widget_container, str(widget_name)):
                                        continue
                                    
                                    # Safety check: try to get widget and verify it's not deleted
                                    try:
                                        widget = getattr(widget_container, str(widget_name))
                                        # Test if widget is still valid by calling a simple method
                                        _ = widget.objectName()
                                    except (RuntimeError, AttributeError) as e:
                                        if "already deleted" in str(e) or "C++ object" in str(e):
                                            logDebug(f"Widget '{widget_name}' already deleted, skipping")
                                        continue

                                    if widget_class == "QCustomThemeDarkLightToggle":
                                        light_icon_url = widget_info.get("lightThemeIcon", "")
                                        dark_icon_url = widget_info.get("darkThemeIcon", "")

                                        if light_icon_url is None:
                                            light_icon_url = ""
                                        if dark_icon_url is None:
                                            dark_icon_url = ""
                                            
                                        light_icon_url = re.sub(prefix_to_remove, f'icons/{folder}', light_icon_url).replace("../", "")
                                        abs_l_icon_url = os.path.abspath(os.path.join(current_script_folder, light_icon_url))
                                        abs_l_icon_url = self._resolveThemedIconPath(abs_l_icon_url)

                                        dark_icon_url = re.sub(prefix_to_remove, f'icons/{folder}', dark_icon_url).replace("../", "")
                                        abs_d_icon_url = os.path.abspath(os.path.join(current_script_folder, dark_icon_url))
                                        abs_d_icon_url = self._resolveThemedIconPath(abs_d_icon_url)

                                        if hasattr(widget_container, str(widget_name)):
                                            try:
                                                btn = getattr(widget_container, str(widget_name))
                                                _ = btn.objectName()  # Check if valid
                                                if abs_l_icon_url != "default_icon_url" and os.path.exists(abs_l_icon_url):
                                                    btn.lightThemeIcon = QIcon(abs_l_icon_url)
                                                if abs_d_icon_url != "default_icon_url" and os.path.exists(abs_d_icon_url):
                                                    btn.darkThemeIcon = QIcon(abs_d_icon_url)
                                                btn.update()
                                            except (RuntimeError, AttributeError):
                                                continue

                                    elif abs_icon_url != "default_icon_url":
                                        try:
                                            if setter_method is not None and isinstance(widget, globals().get(widget_class, object())):
                                                if hasattr(widget, setter_method):
                                                    getattr(widget, setter_method)(abs_icon_url)
                                            elif widget_class == "QWidget" and "QTabWidget" in widget_info:
                                                parent_name = widget_info.get("QTabWidget", "")
                                                if hasattr(widget_container, parent_name):
                                                    parent = getattr(widget_container, parent_name)
                                                    try:
                                                        _ = parent.objectName()  # Check if valid
                                                        if isinstance(parent, QTabWidget) and hasattr(parent, 'setNewTabIcon'):
                                                            parent.setNewTabIcon(widget_name, abs_icon_url)
                                                    except (RuntimeError, AttributeError):
                                                        pass
                                            elif widget_class == "QWidget" and "QToolBox" in widget_info:
                                                parent_name = widget_info.get("QToolBox", "")
                                                if hasattr(widget_container, parent_name):
                                                    parent = getattr(widget_container, parent_name)
                                                    try:
                                                        _ = parent.objectName()  # Check if valid
                                                        if isinstance(parent, QToolBox) and hasattr(parent, 'setNewItemIcon'):
                                                            parent.setNewItemIcon(widget_name, abs_icon_url)
                                                    except (RuntimeError, AttributeError):
                                                        pass
                                            elif widget_class == "QTreeWidget":
                                                if hasattr(widget, 'setNewItemIcon'):
                                                    try:
                                                        widget.setNewItemIcon(widget, abs_icon_url)
                                                    except (RuntimeError, AttributeError):
                                                        pass
                                        except (RuntimeError, AttributeError) as e:
                                            if "already deleted" in str(e) or "C++ object" in str(e):
                                                logDebug(f"Widget '{widget_name}' deleted during icon application")
                                            continue

                                except (RuntimeError, AttributeError) as e:
                                    if "already deleted" in str(e) or "C++ object" in str(e):
                                        logDebug(f"Widget '{widget_info.get('name', 'unknown')}' already deleted, skipping")
                                    else:
                                        logError(f"Failed to process widget '{widget_info.get('name', 'unknown')}' in JSON file '{jsonFile}': {e}")
                                except Exception as e:
                                    logError(f"Failed to process widget '{widget_info.get('name', 'unknown')}' in JSON file '{jsonFile}': {e}")

                    except Exception as e:
                        logError(f"Error processing JSON file '{jsonFile}': {e}")
        except Exception as e:
            logCritical(f"Critical error in applyIcons: {e}")
                                                
    
    def getMainWindow(self):
        # Start with the immediate parent of the current widget
        parent = self.parent()

        # Traverse the parent hierarchy
        while parent is not None:
            # Check if the parent is a QMainWindow
            if isinstance(parent, QMainWindow):
                return parent
            # Move to the next parent
            parent = parent.parent()

        # If no QMainWindow is found, return the QApplication instance
        return QApplication.instance()  # This returns the QApplication instance if no main window is found

    def adjustLightness(self, color, amount=0.5):
        c = colorsys.rgb_to_hls(*_qcolor_rgbf(color))

        if c[1] > 0:
            adjusted_lightness = c[1] * amount * amount 
        else:
            adjusted_lightness = 1 - (amount * amount)

        adjusted_hue = c[0]
        adjusted_saturation = c[2] 

        rgb = colorsys.hls_to_rgb(adjusted_hue, adjusted_lightness, adjusted_saturation)
        new_color = self.rgbToHex((int(rgb[0] * 250), int(rgb[1] * 250), int(rgb[2] * 250)))

        return new_color

    def rgbToHex(self, rgb):
        hex_color = '%02x%02x%02x' % rgb
        return "#" + hex_color

    def hexToRgb(self, hex_color):
        hex_color = self.colorToHex(hex_color)
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        # Convert hexadecimal to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return r, g, b

    def colorToHex(self, color):
        if isinstance(color, str):
            qc = QColor(color)
            if not qc.isValid():
                raise ValueError(f"Invalid color name: {color}")
            return qc.name()

        elif isinstance(color, tuple) and len(color) == 3:
            return QColor.fromRgbF(*[float(v) for v in color]).name()

        else:
            raise ValueError("Invalid color representation")

    def lightenColor(self, hex_color, factor=0.35):
        hex_color = self.colorToHex(hex_color)
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)

        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)

        lightened_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        
        return lightened_color

    def darkenColor(self, hex_color, factor=0.35):
        hex_color = self.colorToHex(hex_color)
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)

        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))

        darkened_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        return darkened_color

    def isColorDarkOrLight(self, color):
        rgb = _qcolor_rgbf(color)
        luminance = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
        threshold = 0.5
        return "dark" if luminance < threshold else "light"

    def convertToSixDigitHex(self, color):
        if color.startswith("#"):
            if len(color) == 4:
                color = "#" + color[1]*2 + color[2]*2 + color[3]*2
            elif len(color) == 7:
                pass
            else:
                raise ValueError("Invalid hex color format")
        else:
            try:
                rgb = _qcolor_rgbf(color)
                color = "#{:02X}{:02X}{:02X}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            except ValueError:
                raise ValueError("Invalid color name")

        return color

    def getCurrentThemeInfo(self):
        THEME = self.theme    
        currentThemeInfo = {}

        if THEME == "LIGHT":
            theme = Light()
            if theme.icons_color == "":
                iconsColor = theme.accent_color
                theme.icons_color = theme.accent_color
            else:
                iconsColor = theme.icons_color

            currentThemeInfo = {"background-color": theme.bg_color, "text-color": theme.txt_color, "accent-color": theme.accent_color, "icons-color": iconsColor}

        elif THEME == "DARK":
            theme = Dark()
            if theme.icons_color == "":
                iconsColor = theme.accent_color
                theme.icons_color = theme.accent_color
            else:
                iconsColor = theme.icons_color

            currentThemeInfo = {"background-color": self.convertToSixDigitHex(theme.bg_color), "text-color": self.convertToSixDigitHex(theme.txt_color), "accent-color": self.convertToSixDigitHex(theme.accent_color), "icons-color": self.convertToSixDigitHex(iconsColor)}

        else:
            for theme in self.themes:
                if theme.defaultTheme or theme.name == THEME:
                    bg_color = theme.backgroundColor
                    txt_color = theme.textColor
                    accent_color = theme.accentColor

                    if theme.createNewIcons:
                        if theme.iconsColor == "":
                            iconsColor = accent_color
                        else:
                            iconsColor = theme.iconsColor
                    else:
                        iconsColor = None

                    currentThemeInfo = {"background-color": bg_color, "text-color": txt_color, "accent-color": accent_color, "icons-color": iconsColor}

        if len(currentThemeInfo) == 0:
            theme = Light()
            if theme.icons_color == "":
                iconsColor = theme.accent_color
            else:
                iconsColor = theme.icons_color

            currentThemeInfo = {"background-color": theme.bg_color, "text-color": theme.txt_color, "accent-color": theme.accent_color, "icons-color": iconsColor}

        settings = QSettings()
        try:
            settings.setValue("ICONS-COLOR", iconsColor)
        except Exception as e:
            logError(f"Failed to write ICONS-COLOR to QSettings: {e}")
        
        return currentThemeInfo
        
    def createVariables(self):
        theme = self.currentTheme
        
        # ============ EXISTING COLOR CALCULATIONS (PRESERVED) ============
        if self.isColorDarkOrLight(theme.bg_color) == "light":
            theme.BG_1 = theme.bg_color
            theme.BG_2 = self.darkenColor(theme.bg_color, 0.05)
            theme.BG_3 = self.darkenColor(theme.bg_color, 0.1)
            theme.BG_4 = self.darkenColor(theme.bg_color, 0.15)
            theme.BG_5 = self.darkenColor(theme.bg_color, 0.2)
            theme.BG_6 = self.darkenColor(theme.bg_color, 0.25)
        else:
            theme.BG_1 = theme.bg_color
            theme.BG_2 = self.adjustLightness(theme.bg_color, 0.90)
            theme.BG_3 = self.adjustLightness(theme.bg_color, 0.80)
            theme.BG_4 = self.adjustLightness(theme.bg_color, 0.70)
            theme.BG_5 = self.adjustLightness(theme.bg_color, 0.60)
            theme.BG_6 = self.adjustLightness(theme.bg_color, 0.50)

        if self.isColorDarkOrLight(theme.txt_color) == "light":
            theme.CT_1 = theme.txt_color
            theme.CT_2 = self.darkenColor(theme.txt_color, 0.2)
            theme.CT_3 = self.darkenColor(theme.txt_color, 0.4)
            theme.CT_4 = self.darkenColor(theme.txt_color, 0.6)
        else:
            theme.CT_1 = theme.txt_color
            theme.CT_2 = self.lightenColor(theme.txt_color, 0.2)
            theme.CT_3 = self.lightenColor(theme.txt_color, 0.4)
            theme.CT_4 = self.lightenColor(theme.txt_color, 0.6)

        if self.isColorDarkOrLight(theme.txt_color) == "light":
            theme.CA_1 = theme.accent_color
            theme.CA_2 = self.darkenColor(theme.accent_color, .2)
            theme.CA_3 = self.darkenColor(theme.accent_color, .4)
            theme.CA_4 = self.darkenColor(theme.accent_color, .6)
        else:
            theme.CA_1 = theme.accent_color
            theme.CA_2 = self.lightenColor(theme.accent_color, .2)
            theme.CA_3 = self.lightenColor(theme.accent_color, .4)
            theme.CA_4 = self.lightenColor(theme.accent_color, .6)

        QDir.addSearchPath('theme-icons', os.path.join(projectRoot(), 'Qss/icons/'))
        # Single shared icon set: the app stylesheet, ui files and Qt Designer
        # all read Qss/icons/icons. The set is recolored in place whenever the
        # resolved icon color changes (theme switch, QtDesignerIconsColor or
        # a $ICONS_COLOR override in defaultStyle.scss).
        theme.ICONS = "theme-icons:icons/"

        if theme.icons_color is not None and theme.icons_color != "":
            self.ICONS_COLOR = theme.icons_color
        else:
            self.ICONS_COLOR = theme.accent_color
        # Apply overrides so $ICONS_COLOR matches the generated set
        self.ICONS_COLOR = self.resolvedIconsColor()

        self.COLOR_BACKGROUND_1 = theme.BG_1
        self.COLOR_BACKGROUND_2 = theme.BG_2
        self.COLOR_BACKGROUND_3 = theme.BG_3
        self.COLOR_BACKGROUND_4 = theme.BG_4
        self.COLOR_BACKGROUND_5 = theme.BG_5
        self.COLOR_BACKGROUND_6 = theme.BG_6

        self.COLOR_TEXT_1 = theme.CT_1
        self.COLOR_TEXT_2 = theme.CT_2
        self.COLOR_TEXT_3 = theme.CT_3
        self.COLOR_TEXT_4 = theme.CT_4

        self.COLOR_ACCENT_1 = theme.CA_1
        self.COLOR_ACCENT_2 = theme.CA_2
        self.COLOR_ACCENT_3 = theme.CA_3
        self.COLOR_ACCENT_4 = theme.CA_4

        # ============ MODERN CSS VARIABLES (DERIVED FROM YOUR CALCULATIONS) ============
        self.COLOR_PRIMARY = theme.CA_1
        self.COLOR_PRIMARY_DARK = theme.CA_2
        self.COLOR_PRIMARY_LIGHT = self.COLOR_ACCENT_2
        self.COLOR_ON_PRIMARY = theme.CT_1
        
        self.COLOR_SURFACE = theme.BG_1
        self.COLOR_SURFACE_VARIANT = theme.BG_3
        self.COLOR_ON_SURFACE = theme.CT_1
        
        self.COLOR_BORDER = theme.BG_4
        self.COLOR_BORDER_FOCUS = theme.CA_1

        # Spacing variables
        self.SPACING_XS = "4px"
        self.SPACING_SM = "8px"
        self.SPACING_MD = "12px"
        self.SPACING_LG = "16px"
        self.SPACING_XL = "20px"
        self.SPACING_XXL = "24px"
        self.SPACING_3XL = "32px"
        
        # Border radius
        self.BORDER_RADIUS_NONE = "0px"
        self.BORDER_RADIUS_SM = "4px"
        self.BORDER_RADIUS_MD = "6px"
        self.BORDER_RADIUS_LG = "8px"
        self.BORDER_RADIUS_XL = "12px"
        self.BORDER_RADIUS_2XL = "16px"
        self.BORDER_RADIUS_3XL = "24px"
        self.BORDER_RADIUS_FULL = "9999px"

        # ============ RGB CONVERSIONS (PRESERVED) ============
        bg_rgb_1 = self.hexToRgb(theme.BG_1)
        bg_rgb_2 = self.hexToRgb(theme.BG_2)
        bg_rgb_3 = self.hexToRgb(theme.BG_3)
        bg_rgb_4 = self.hexToRgb(theme.BG_4)
        bg_rgb_5 = self.hexToRgb(theme.BG_5)
        bg_rgb_6 = self.hexToRgb(theme.BG_6)

        txt_rgb_1 = self.hexToRgb(theme.CT_1)
        txt_rgb_2 = self.hexToRgb(theme.CT_2)
        txt_rgb_3 = self.hexToRgb(theme.CT_3)
        txt_rgb_4 = self.hexToRgb(theme.CT_4)

        accent_rgb_1 = self.hexToRgb(theme.CA_1)
        accent_rgb_2 = self.hexToRgb(theme.CA_2)
        accent_rgb_3 = self.hexToRgb(theme.CA_3)
        accent_rgb_4 = self.hexToRgb(theme.CA_4)

        theme.CB1_R, theme.CB1_G, theme.CB1_B = bg_rgb_1[0], bg_rgb_1[1], bg_rgb_1[2]
        theme.CB2_R, theme.CB2_G, theme.CB2_B = bg_rgb_2[0], bg_rgb_2[1], bg_rgb_2[2]
        theme.CB3_R, theme.CB3_G, theme.CB3_B = bg_rgb_3[0], bg_rgb_3[1], bg_rgb_3[2]
        theme.CB4_R, theme.CB4_G, theme.CB4_B = bg_rgb_4[0], bg_rgb_4[1], bg_rgb_4[2]
        theme.CB5_R, theme.CB5_G, theme.CB5_B = bg_rgb_5[0], bg_rgb_5[1], bg_rgb_5[2]
        theme.CB6_R, theme.CB6_G, theme.CB6_B = bg_rgb_6[0], bg_rgb_6[1], bg_rgb_6[2]

        theme.CT1_R, theme.CT1_G, theme.CT1_B = txt_rgb_1[0], txt_rgb_1[1], txt_rgb_1[2]
        theme.CT2_R, theme.CT2_G, theme.CT2_B = txt_rgb_2[0], txt_rgb_2[1], txt_rgb_2[2]
        theme.CT3_R, theme.CT3_G, theme.CT3_B = txt_rgb_3[0], txt_rgb_3[1], txt_rgb_3[2]
        theme.CT4_R, theme.CT4_G, theme.CT4_B = txt_rgb_4[0], txt_rgb_4[1], txt_rgb_4[2]

        theme.CA1_R, theme.CA1_G, theme.CA1_B = accent_rgb_1[0], accent_rgb_1[1], accent_rgb_1[2]
        theme.CA2_R, theme.CA2_G, theme.CA2_B = accent_rgb_2[0], accent_rgb_2[1], accent_rgb_2[2]
        theme.CA3_R, theme.CA3_G, theme.CA3_B = accent_rgb_3[0], accent_rgb_3[1], accent_rgb_3[2]
        theme.CA4_R, theme.CA4_G, theme.CA4_B = accent_rgb_4[0], accent_rgb_4[1], accent_rgb_4[2]

        self.PATH_RESOURCES = theme.ICONS
        self.RELATIVE_FOLDER = self.script_dir
        self.BASE_DIR = self.script_dir

        self.updateThemeIndicators()

        # ============ ADD OTHER VARIABLES FROM THEME ============
        other_vars_scss = ""
        if hasattr(theme, 'other_variables') and theme.other_variables:
            for var_name, var_value in theme.other_variables.items():
                other_vars_scss += f"${var_name}: {var_value};\n"

        scss_folder = os.path.abspath(os.path.join(projectRoot(), 'Qss/scss'))
        if not os.path.exists(scss_folder):
            try:
                os.makedirs(scss_folder)
                logInfo(f"Created SCSS folder: {scss_folder}")
            except Exception as e:
                logError(f"Failed to create SCSS folder {scss_folder}: {e}")

        scss_path = os.path.abspath(os.path.join(scss_folder, '_variables.scss'))
        try:
            content = f"""//===================================================//
    // FILE AUTO-GENERATED, ANY CHANGES MADE WILL BE LOST //
    //====================================================//

    // Background Colors
    $COLOR_BACKGROUND_1: {theme.BG_1};
    $COLOR_BACKGROUND_2: {theme.BG_2};
    $COLOR_BACKGROUND_3: {theme.BG_3};
    $COLOR_BACKGROUND_4: {theme.BG_4};
    $COLOR_BACKGROUND_5: {theme.BG_5};
    $COLOR_BACKGROUND_6: {theme.BG_6};

    // Background RGB Values
    $CB1_R: {theme.CB1_R};
    $CB1_G: {theme.CB1_G};
    $CB1_B: {theme.CB1_B};
    $CB2_R: {theme.CB2_R};
    $CB2_G: {theme.CB2_G};
    $CB2_B: {theme.CB2_B};
    $CB3_R: {theme.CB3_R};
    $CB3_G: {theme.CB3_G};
    $CB3_B: {theme.CB3_B};
    $CB4_R: {theme.CB4_R};
    $CB4_G: {theme.CB4_G};
    $CB4_B: {theme.CB4_B};
    $CB5_R: {theme.CB5_R};
    $CB5_G: {theme.CB5_G};
    $CB5_B: {theme.CB5_B};
    $CB6_R: {theme.CB6_R};
    $CB6_G: {theme.CB6_G};
    $CB6_B: {theme.CB6_B};

    // Text Colors
    $COLOR_TEXT_1: {theme.CT_1};
    $COLOR_TEXT_2: {theme.CT_2};
    $COLOR_TEXT_3: {theme.CT_3};
    $COLOR_TEXT_4: {theme.CT_4};

    // Text RGB Values
    $CT1_R: {theme.CT1_R};
    $CT1_G: {theme.CT1_G};
    $CT1_B: {theme.CT1_B};
    $CT2_R: {theme.CT2_R};
    $CT2_G: {theme.CT2_G};
    $CT2_B: {theme.CT2_B};
    $CT3_R: {theme.CT3_R};
    $CT3_G: {theme.CT3_G};
    $CT3_B: {theme.CT3_B};
    $CT4_R: {theme.CT4_R};
    $CT4_G: {theme.CT4_G};
    $CT4_B: {theme.CT4_B};

    // Accent Colors
    $COLOR_ACCENT_1: {theme.CA_1};
    $COLOR_ACCENT_2: {theme.CA_2};
    $COLOR_ACCENT_3: {theme.CA_3};
    $COLOR_ACCENT_4: {theme.CA_4};

    // Accent RGB Values
    $CA1_R: {theme.CA1_R};
    $CA1_G: {theme.CA1_G};
    $CA1_B: {theme.CA1_B};
    $CA2_R: {theme.CA2_R};
    $CA2_G: {theme.CA2_G};
    $CA2_B: {theme.CA2_B};
    $CA3_R: {theme.CA3_R};
    $CA3_G: {theme.CA3_G};
    $CA3_B: {theme.CA3_B};
    $CA4_R: {theme.CA4_R};
    $CA4_G: {theme.CA4_G};
    $CA4_B: {theme.CA4_B};

    // Modern CSS Variables (Derived)
    $COLOR_PRIMARY: {self.COLOR_PRIMARY};
    $COLOR_PRIMARY_DARK: {self.COLOR_PRIMARY_DARK};
    $COLOR_PRIMARY_LIGHT: {self.COLOR_PRIMARY_LIGHT};
    $COLOR_ON_PRIMARY: {self.COLOR_ON_PRIMARY};
    $COLOR_SURFACE: {self.COLOR_SURFACE};
    $COLOR_SURFACE_VARIANT: {self.COLOR_SURFACE_VARIANT};
    $COLOR_ON_SURFACE: {self.COLOR_ON_SURFACE};
    $COLOR_BORDER: {self.COLOR_BORDER};
    $COLOR_BORDER_FOCUS: {self.COLOR_BORDER_FOCUS};

    // Theme Mode Variables
    $THEME_MODE: "{self.THEME_MODE}";
    $THEME_ICON: "{self.THEME_ICON}";
    $THEME_STATUS: "{self.THEME_STATUS}";
    $IS_THEME_DARK: {str(self._isThemeDark).lower()};

    // Spacing
    $SPACING_XS: {self.SPACING_XS};
    $SPACING_SM: {self.SPACING_SM};
    $SPACING_MD: {self.SPACING_MD};
    $SPACING_LG: {self.SPACING_LG};
    $SPACING_XL: {self.SPACING_XL};
    $SPACING_XXL: {self.SPACING_XXL};
    $SPACING_3XL: {self.SPACING_3XL};

    // Border Radius
    $BORDER_RADIUS_NONE: {self.BORDER_RADIUS_NONE};
    $BORDER_RADIUS_SM: {self.BORDER_RADIUS_SM};
    $BORDER_RADIUS_MD: {self.BORDER_RADIUS_MD};
    $BORDER_RADIUS_LG: {self.BORDER_RADIUS_LG};
    $BORDER_RADIUS_XL: {self.BORDER_RADIUS_XL};
    $BORDER_RADIUS_2XL: {self.BORDER_RADIUS_2XL};
    $BORDER_RADIUS_3XL: {self.BORDER_RADIUS_3XL};
    $BORDER_RADIUS_FULL: {self.BORDER_RADIUS_FULL};

    // Legacy Variables (Keep for backward compatibility)
    $OPACITY_TOOLTIP: 230;
    $SIZE_BORDER_RADIUS: {self.SPACING_SM};
    $BORDER_1: 1px solid $COLOR_BACKGROUND_1;
    $BORDER_2: 1px solid $COLOR_BACKGROUND_4;
    $BORDER_3: 1px solid $COLOR_BACKGROUND_6;
    $BORDER_SELECTION_3: 1px solid $COLOR_ACCENT_3;
    $BORDER_SELECTION_2: 1px solid $COLOR_ACCENT_2;
    $BORDER_SELECTION_1: 1px solid $COLOR_ACCENT_1;

    // Paths
    $PATH_RESOURCES: '{theme.ICONS}';
    $ICONS_COLOR: {self.ICONS_COLOR};
    $RELATIVE_FOLDER: "{self.script_dir}";
    $BASE_DIR: "{self.script_dir}";

    """
            if other_vars_scss:
                content += "\n// Additional theme variables\n" + other_vars_scss
            content += """
    //===================================================//
    // END //
    //====================================================//
    """
            # Only touch the disk when the variables actually changed -
            # getThemeVariableValue used to rewrite this file on EVERY
            # variable lookup, dozens of times per style pass.
            if content != self._last_variables_scss or not os.path.exists(scss_path):
                with open(scss_path, 'w') as f:
                    f.write(content)
                self._last_variables_scss = content
        except Exception as e:
            logError(f"Failed to write SCSS variables file {scss_path}: {e}")

        # Keep the $VAR -> value mapping in sync with what was just computed
        # (getThemeVariableValue reads it).
        self.defineThemeVarMapping()

    def compileSassTheme(self, progress_callback, themeInfo, iconsColor, iconsForce):
        ## Runs on a worker thread: every QSettings-derived value is resolved
        ## by the caller on the main thread, so nothing below touches QSettings.
        ## GENERATE THE SHARED ICON SET (app stylesheet + ui files + Designer)
        self.generateNewIcons(progress_callback, force=iconsForce, themeInfo=themeInfo, iconsColor=iconsColor)

    def makeAllIcons(self, progress_callback):
        ## GENERATE ALL ICONS FOR ALL THEMES
        self.generateAllIcons(progress_callback)

    def sassCompilationProgress(self, n):
        pass
        # self.ui.activityProgress.setValue(n)

    def stopWorkers(self):
        try:
            if self.iconsWorker is not None:
                self.iconsWorker.stop()

            if self.allIconsWorker is not None:
                self.allIconsWorker.stop()
        except Exception:
            pass

    def styleVariablesFromTheme(self, stylesheet):
        self.defineThemeVarMapping()
        # Replace variables in the stylesheet string. The trailing
        # (?![A-Za-z0-9_]) guard stops $COLOR_ACCENT_1 from eating the
        # front of $COLOR_ACCENT_10 and similar prefix collisions.
        for var, value in self._variable_mapping.items():
            var_pattern = re.escape(var) + r"(?![A-Za-z0-9_])"
            stylesheet = re.sub(var_pattern, str(value), stylesheet)
        return stylesheet
    
    def getThemeVariableValue(self, color_variable):
        self.createVariables()
        return self._variable_mapping.get(color_variable, color_variable)
    
    def reloadJsonStyles(self, update = False):
        loadJsonStyle(self, jsonFiles = self.jsonStyleSheets, update = update)

    # apply custom font
    def loadAppFont(self):
        """Load and register the bundled app font (Rosario, SIL OFL 1.1)."""
        try:
            font_id = QFontDatabase.addApplicationFont(os.path.join(self.script_dir, "Qss/fonts/Rosario/Rosario-VariableFont_wght.ttf"))
            # if font loaded
            if font_id == -1:
                logDebug("Failed to load the bundled Rosario font")
        except Exception as e:
            logError(f"Error loading font: {e}")

    def applyCompiledSass(self, generateIcons: bool = True, paintEntireApp: bool = True):
        if not self.themesRead:
            return
        qcss_folder = os.path.abspath(os.path.join(projectRoot(), 'Qss/scss'))
        if not os.path.exists(qcss_folder):
            try:
                os.makedirs(qcss_folder)
            except Exception as e:
                logError(f"Failed to create QSS folder {qcss_folder}: {e}")
        
        css_folder = os.path.abspath(os.path.join(projectRoot(), 'generated-files/css/'))
        if not os.path.exists(css_folder):
            try:
                os.makedirs(css_folder)
            except Exception as e:
                logError(f"Failed to create CSS folder {css_folder}: {e}")

        main_sass_path = os.path.abspath(os.path.join(projectRoot(), 'Qss/scss/main.scss'))
        styles_sass_path = os.path.abspath(os.path.join(projectRoot(), 'Qss/scss/_styles.scss'))
        css_path = os.path.abspath(os.path.join(projectRoot(), 'generated-files/css/main.css'))

        if not os.path.exists(main_sass_path):   
            try:
                shutil.copy(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Qss/scss/main.scss')), qcss_folder)
            except Exception as e:
                logError(f"Failed to copy main.scss: {e}")  

        if not os.path.exists(styles_sass_path):   
            try:
                shutil.copy(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Qss/scss/_styles.scss')), qcss_folder)
            except Exception as e:
                logError(f"Failed to copy _styles.scss: {e}")  

        default_scss_path = os.path.abspath(os.path.join(projectRoot(), 'Qss/scss/defaultStyle.scss'))
        if not os.path.exists(default_scss_path):   
            try:
                with open(default_scss_path, 'w') as f:
                    f.write("""
                    //===================================================//
                    // FILE AUTO-GENERATED. PUT YOUR DEFAULT STYLES HERE. 
                    // THESE STYLES WILL OVERIDE THE THEME STYLES
                    //====================================================//
                    
                    //===================================================//
                    // END //
                    //====================================================//
                    """)
            except Exception as e:
                logError(f"Failed to create defaultStyle.scss: {e}")

        # Create QApplication instance if it doesn't exist
        app = QApplication.instance() if QApplication.instance() else QApplication([])
        mainWindow = self.getMainWindow()
        
        # palette = QPalette()
        palette = app.palette()

        # Set the background color
        palette.setColor(QPalette.Window, QColor(self.COLOR_BACKGROUND_1))


        # Set the text color
        try:
            palette.setColor(QPalette.Text, QColor(self.COLOR_TEXT_1))
        except Exception as e:
            logError(f"Failed to set text color: {e}")

        # Set the button color
        try:
            palette.setColor(QPalette.Button, QColor(self.COLOR_BACKGROUND_3))
        except Exception as e:
            logError(f"Failed to set button color: {e}")

        # Set the button text color
        try:
            palette.setColor(QPalette.ButtonText, QColor(self.COLOR_TEXT_1))
        except Exception as e:
            logError(f"Failed to set button text color: {e}")

        # Set the highlight color
        try:
            palette.setColor(QPalette.Highlight, QColor(self.COLOR_BACKGROUND_6))
        except Exception as e:
            logError(f"Failed to set highlight color: {e}")

        # Set the highlight text color
        try:
            palette.setColor(QPalette.HighlightedText, QColor(self.COLOR_ACCENT_1))
        except Exception as e:
            logError(f"Failed to set highlight text color: {e}")

        # Apply the palette to the main window
        try:
            mainWindow.setPalette(palette)
        except Exception as e:
            logError(f"Failed to set palette on main window: {e}")

        try:
            app.setPalette(palette)
        except Exception as e:
            logError(f"Failed to set palette on app: {e}")
        
        self.createVariables()

        background_color = QColor(self.COLOR_BACKGROUND_1)

        # Calculate luminance using the YIQ color space formula
        luminance = (0.299 * background_color.red() + 0.587 * background_color.green() + 0.114 * background_color.blue()) / 255
        
        if luminance < 0.5:
            self._isThemeDark = True  # Dark theme
        else:
            self._isThemeDark = False  # Light theme

        # Skip the (slow, UI-thread) sass compile when none of the scss
        # inputs changed since the last compile.
        try:
            scss_dir = os.path.dirname(main_sass_path)
            mtimes = []
            for name in sorted(os.listdir(scss_dir)):
                if name.endswith('.scss'):
                    fp = os.path.join(scss_dir, name)
                    mtimes.append((name, os.path.getmtime(fp)))
            # include the light/dark state: token() values change with the
            # theme even when no .scss file changed, so a flip must recompile.
            compile_key = (tuple(mtimes), bool(getattr(self, "_isThemeDark", False)))
        except Exception:
            compile_key = None

        stylesheet = ""
        if compile_key is not None and \
                compile_key == getattr(self, '_last_compile_key', None) and \
                os.path.exists(css_path):
            try:
                with open(css_path, "r") as css:
                    stylesheet = css.read()
                logDebug("SASS unchanged - reusing compiled stylesheet")
            except Exception:
                stylesheet = ""
        if not stylesheet:
            # Expose design tokens to SCSS as token('role'). Bridge the active
            # theme's colours onto the core semantic roles so token() reflects
            # the current theme; other roles fall back to the light/dark
            # defaults. This must never break theme compilation, so any failure
            # degrades to a plain compile (token() simply unavailable).
            token_fns = []
            try:
                from Custom_Widgets.JSonStyles.tokens import DesignTokens, sass_functions
                _tname = "dark" if getattr(self, "_isThemeDark", False) else "light"
                _roles = {"surface": self.COLOR_BACKGROUND_1,
                          "on-surface": self.COLOR_TEXT_1,
                          "primary": self.COLOR_ACCENT_1,
                          "accent": self.COLOR_ACCENT_1}
                _overrides = {_tname: {k: str(v) for k, v in _roles.items() if v}}
                token_fns = sass_functions(DesignTokens(theme=_tname, semantic=_overrides))
            except Exception as e:
                logError(f"Failed to build design-token SCSS functions: {e}")
            try:
                qtsass.compile_filename(main_sass_path, css_path,
                                        custom_functions=token_fns)
                self._last_compile_key = compile_key
            except Exception as e:
                # qtsass errors on a dangling @import are opaque
                # (CompileError/"expected str ... not NoneType"). Translate to
                # an actionable message naming the file + missing partial; the
                # app then keeps the last-good CSS (read below) so it stays
                # usable, but the real cause is no longer buried.
                detail = None
                try:
                    from Custom_Widgets.JSonStyles.tokens import \
                        describe_scss_compile_error
                    detail = describe_scss_compile_error(
                        main_sass_path, [os.path.dirname(main_sass_path)], e)
                except Exception:
                    pass
                if detail:
                    logError(detail)
                    logError("Keeping the previously compiled stylesheet - fix "
                             "the SCSS above and re-save to apply new styles.")
                else:
                    logError(f"Failed to compile SASS: {e}")
            try:
                with open(css_path, "r") as css:
                    stylesheet = css.read()
            except Exception as e:
                logError(f"Failed to read compiled CSS {css_path}: {e}")

        try:
            mainWindow.setStyleSheet("")
            mainWindow.setPalette(mainWindow.style().standardPalette())

            app.setStyleSheet(stylesheet)
            # newly created menus may need re-styling
            for obj in QApplication.instance().allWidgets():
                if isinstance(obj, QMenu):
                    obj.setStyleSheet(stylesheet)
        except Exception as e:
            logError(f"Failed to set application stylesheet: {e}")

        if generateIcons:
            ########################################################################
            ## GENERATE NEW ICONS (SVG)
            # Icons are recolored SVG copies - generation is a fast text
            # substitution, so only the active theme and the Qt Designer set
            # are generated here. Other themes generate when activated.
            #
            # Every QSettings-derived value is resolved here on the main thread
            # and passed to the worker as plain values: QSettings is not safe
            # to use from a worker thread while the main thread also uses it
            # (both block on the settings lock file and deadlock).
            themeInfo = self.getCurrentThemeInfo()  # also persists ICONS-COLOR
            iconsColor, iconsForce = self._resolveIconsColor(themeInfo)
            settings = QSettings()
            try:
                settings.setValue("GENERATED-ICONS-COLOR", iconsColor)
            except Exception as e:
                logError(f"Failed to write GENERATED-ICONS-COLOR to QSettings: {e}")

            self.iconsWorker = Worker(self.compileSassTheme, themeInfo=themeInfo,
                                      iconsColor=iconsColor, iconsForce=iconsForce)
            self.iconsWorker.signals.result.connect(WorkerResponse.print_output)
            self.iconsWorker.signals.finished.connect(lambda: self._themeChangeComplete())
            self.iconsWorker.signals.progress.connect(self.sassCompilationProgress)

            self.customWidgetsThreadpool.start(self.iconsWorker)

    def _themeChangeComplete(self):
        # The shared icon set may have been rewritten in place - drop cached
        # pixmaps and re-apply the stylesheet so QSS urls re-read the files.
        app = QApplication.instance()
        try:
            QPixmapCache.clear()
            if app is not None and app.styleSheet():
                app.setStyleSheet(app.styleSheet())
        except Exception as e:
            logError(f"Failed to refresh pixmap cache after icon generation: {e}")

        # Tell a running Qt Designer about the change so open forms recolor
        # live (no-op when Designer or the bridge is not running)
        if not is_in_designer(self):
            try:
                from Custom_Widgets.DesignerBridge import DesignerBridgeClient
                DesignerBridgeClient().notifyThemeChanged(
                    color=getattr(self, "ICONS_COLOR", None),
                    qss=app.styleSheet() if app is not None else "")
            except Exception as e:
                logDebug(f"Designer bridge notify skipped: {e}")

        self.onThemeChangeComplete.emit()
        logInfo("all icons have been checked and missing icons generated!")

    def getAllFolders(self, base_folder):
        all_folders = []
        try:
            for root, dirs, files in os.walk(base_folder):
                for dir_name in dirs:
                    folder_path = os.path.relpath(os.path.join(root, dir_name), base_folder)
                    all_folders.append(folder_path)
        except Exception as e:
            logError(f"Failed to walk folder {base_folder}: {e}")
        return all_folders

    def getAllSvgFiles(self, base_folder):
        svg_files = []
        try:
            for file_name in os.listdir(base_folder):
                if file_name.lower().endswith('.svg'):
                    file_path = os.path.join(base_folder, file_name)
                    svg_files.append(file_path)
        except Exception as e:
            logError(f"Failed to list SVG files in {base_folder}: {e}")
        return svg_files

    def _normalizeSvgNamespace(self, svg_text):
        """Rewrite namespace-prefixed svg documents (<ns0:svg ...>) to the
        default-namespace form. Qt's SVG image-format plugin (QPixmap /
        QImageReader - the path Qt Designer previews use) does not recognize
        prefixed root tags and yields empty pixmaps, while QIcon renders
        them. Normalizing keeps every consumer working."""
        match = re.search(r'<([A-Za-z_][\w.-]*):svg\b', svg_text)
        if not match:
            return svg_text
        prefix = match.group(1)
        svg_text = svg_text.replace(f'xmlns:{prefix}=', 'xmlns=')
        svg_text = svg_text.replace(f'<{prefix}:', '<').replace(f'</{prefix}:', '</')
        return svg_text

    def _setSvgSize(self, svg_text, width, height):
        """Force width/height attributes on the root <svg> tag (viewBox is kept).
        Handles namespaced roots such as <ns0:svg> (material_design pack)."""
        def fix_root(match):
            tag = match.group(0)
            closing = '/>' if tag.rstrip().endswith('/>') else '>'
            tag = tag[:-len(closing)]
            tag = re.sub(r'\s(width|height)="[^"]*"', '', tag)
            return f'{tag} width="{width}" height="{height}"{closing}'
        return re.sub(r'<(?:[A-Za-z_][\w.-]*:)?svg\b[^>]*?/?>', fix_root, svg_text, count=1)

    def generateIcons(self, progress_callback, iconsColor, suffix, iconsFolder="", createQrc=False, output_width=None, output_height=None, force=False):
        # Base folder
        base_folder = os.path.dirname(__file__)
        icons_folder_base = os.path.join(base_folder, 'Qss/icons')

        svg_color = "#ffffff"

        # Get a list of all folders inside 'icons'
        try:
            folders = self.getAllFolders(icons_folder_base)
        except Exception:
            folders = QCustomTheme.getAllFolders(None, icons_folder_base)

        new_icon_made = False
        qrc_content = f'<RCC>\n'

        qrc_folder_path = os.path.abspath(os.path.join(projectRoot(), f'Qss/icons'))
        
        for folder in folders:
            # Prefix must be identical on every platform - ui files reference it
            qrc_prefix = (folder + suffix).replace("/", "_").replace("\\", "_")
            qrc_content += f'  <qresource prefix="{qrc_prefix}">\n'
            
            icons_folder_path = os.path.abspath(os.path.join(projectRoot(), f'Qss/icons/{iconsFolder}/{folder}'))

            try:
                if not os.path.exists(icons_folder_path):
                    os.makedirs(icons_folder_path)
                    logInfo(f"Created icons folder: {icons_folder_path}")
            except Exception as e:
                logError(f"Failed to create icons folder {icons_folder_path}: {e}")

            folder_path = os.path.join(icons_folder_base, folder)
            list_of_files = self.getAllSvgFiles(folder_path)
            total_icons = len(list_of_files)
            last_pct = -1

            for index, file_path in enumerate(list_of_files):
                file_name = os.path.basename(urlparse(file_path).path).replace(".svg", f"{suffix}.svg")
                output_path = os.path.abspath(os.path.join(icons_folder_path, file_name))

                qrc_content += f'    <file>icons/{folder}/{file_name}</file>\n'
                if progress_callback is not None:
                    pct = int((index / total_icons) * 100)
                    if pct != last_pct:
                        progress_callback.emit(pct)
                        last_pct = pct

                if not force and os.path.exists(output_path):
                    continue

                try:
                    with open(file_path, encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    new_svg = content.replace(svg_color, iconsColor)
                    new_svg = self._normalizeSvgNamespace(new_svg)

                    if output_height is not None and output_width is not None:
                        new_svg = self._setSvgSize(new_svg, output_width, output_height)

                    with open(output_path, 'w', encoding='utf-8') as out:
                        out.write(new_svg)

                    new_icon_made = True

                except Exception as e:
                    logError(f"Error processing {file_path}: {e}")

            qrc_content += f'  </qresource>\n'

        qrc_content += f'</RCC>\n'
        qrc_file_path = os.path.abspath(os.path.join(qrc_folder_path, f'{suffix}_icons.qrc'))

        if (createQrc and new_icon_made) or not os.path.exists(qrc_file_path):
            try:
                createQrcFile(qrc_content, qrc_file_path)
                logInfo(f"Created QRC file: {qrc_file_path}")
            except Exception as e:
                logError(f"Failed to create QRC file {qrc_file_path}: {e}")

    def generateNewIcons(self, progress_callback = None, force = False, themeInfo = None, iconsColor = None):
        if not self.checkForMissingicons and progress_callback is not None:
                # emit 100% progress
                progress_callback.emit(100)
                return

        # Color of the shared icon set. When run on a worker thread the
        # caller resolves themeInfo/iconsColor on the main thread and passes
        # them in - QSettings must not be touched off the main thread.
        if iconsColor is None:
            iconsColor, resolved_force = self._resolveIconsColor(themeInfo)
            force = force or resolved_force
            try:
                QSettings().setValue("GENERATED-ICONS-COLOR", iconsColor)
            except Exception as e:
                logError(f"Failed to write GENERATED-ICONS-COLOR to QSettings: {e}")

        if iconsColor:
            if force:
                logInfo(f"Icons color changed to {iconsColor}, regenerating the shared icon set")
            logInfo("Generating SVG icons for your theme")

            # One shared set (Qss/icons/icons): app stylesheet urls, ui files
            # and Qt Designer all read these, like a web app's single assets
            # folder. Regenerated in place when the color changes.
            self.generateIcons(progress_callback, iconsColor, "", "icons", createQrc=True, output_width=24, output_height=24, force=force)

            logInfo(("DONE: Current icons color ", iconsColor))


    def generateAllIcons(self, progress_callback = None):
        if is_in_designer(self):
            return
        if not self.checkForMissingicons and progress_callback is not None:
            # emit 100% progress
            progress_callback.emit(100)
            return
        
        # Icons are a single shared set colored for the active theme, so
        # this simply ensures that set exists (kept for backward compat).
        self.generateNewIcons(progress_callback)

    def iconsColorFromQss(self):
        """Optional stylesheet override for the icon color: put e.g.
        `$ICONS_COLOR: #ff5722;` in Qss/scss/defaultStyle.scss and the whole
        shared icon set is generated in that color."""
        path = os.path.abspath(os.path.join(projectRoot(), 'Qss/scss/defaultStyle.scss'))
        try:
            if os.path.exists(path):
                with open(path, encoding='utf-8', errors='ignore') as f:
                    match = re.search(r'^\s*\$ICONS_COLOR\s*:\s*([^;\n]+);', f.read(), re.MULTILINE)
                if match:
                    return match.group(1).strip()
        except Exception as e:
            logError(f"Failed to read $ICONS_COLOR from {path}: {e}")
        return None

    def resolvedIconsColor(self, themeInfo=None):
        """The color of the shared icon set. Precedence:
        1. `$ICONS_COLOR` in Qss/scss/defaultStyle.scss (stylesheet override)
        2. "QtDesignerIconsColor" in the json style - an explicit color
           applies to ALL icons; "theme"/"auto"/empty falls through
        3. the active theme's icons color"""
        color = self.iconsColorFromQss()
        if not color:
            designer_color = str(self.designerIconsColor or "")
            if designer_color and designer_color.lower() not in ("theme", "auto"):
                color = designer_color
        if not color:
            if themeInfo is not None:
                color = themeInfo.get("icons-color")
            else:
                color = getattr(self, "ICONS_COLOR", None) or self.iconsColor
        return color

    def _resolveIconsColor(self, themeInfo=None):
        """Resolve the shared icon set color and whether the set must be
        regenerated. Reads QSettings, so it must run on the main thread."""
        if themeInfo is None:
            themeInfo = self.getCurrentThemeInfo()
        color = self.resolvedIconsColor(themeInfo)
        force = QSettings().value("GENERATED-ICONS-COLOR") != color
        return color, force

    def generateDesignerIcons(self, progress_callback=None, designerIconsColor=None, force=False):
        """Backward-compatible wrapper: the app and Qt Designer share one icon
        set (Qss/icons/icons). An explicit designerIconsColor recolors the
        whole shared set."""
        if designerIconsColor is not None:
            self.designerIconsColor = designerIconsColor
        self.generateNewIcons(progress_callback, force=force)

    # Method to create a new theme dynamically
    def createNewTheme(self, name, bg_color, txt_color, accent_color, icons_color, createNewIcons=True, defaultTheme=False, other_variables={}, predefined=False):
        # Check if the theme already exists
        existing_theme = next((theme for theme in self._themes if theme.name == name), None)
        
        if existing_theme:
            # Update the existing theme
            existing_theme.bg_color = bg_color
            existing_theme.txt_color = txt_color
            existing_theme.accent_color = accent_color
            existing_theme.icons_color = icons_color
            existing_theme.createNewIcons = createNewIcons
            existing_theme.defaultTheme = defaultTheme
            existing_theme.other_variables = other_variables
            existing_theme.predefined = predefined
            
            # Update dynamic properties as well
            existing_theme.backgroundColor = bg_color
            existing_theme.textColor = txt_color
            existing_theme.accentColor = accent_color
            existing_theme.iconsColor = icons_color
        
            
        else:
            # Create a new theme
            new_theme = Theme(name, bg_color, txt_color, accent_color, icons_color, createNewIcons, defaultTheme, other_variables)
            new_theme.other_variables = other_variables
            new_theme.predefined = predefined
            self._themes.append(new_theme)

            # NEW: Ensure theme variable consistency
            self.ensureThemeVariableConsistency()
    
    def copyMissingVariablesFromOtherThemes(self):
        """Copy missing variables from other themes to ensure all themes have the same variable structure"""
        if not self._themes:
            return
        
        # Collect all unique variable names from all themes
        all_variable_names = set()
        for theme in self._themes:
            if hasattr(theme, 'other_variables') and theme.other_variables:
                all_variable_names.update(theme.other_variables.keys())
        
        # For each theme, check for missing variables and copy from other themes
        for target_theme in self._themes:
            if not hasattr(target_theme, 'other_variables'):
                target_theme.other_variables = {}
            
            # Find missing variables in this theme
            missing_vars = all_variable_names - set(target_theme.other_variables.keys())
            
            if missing_vars:
                # Try to find values for missing variables from other themes
                for var_name in missing_vars:
                    for source_theme in self._themes:
                        if (source_theme != target_theme and 
                            hasattr(source_theme, 'other_variables') and 
                            source_theme.other_variables and 
                            var_name in source_theme.other_variables):
                            
                            # Copy the variable value from source theme
                            target_theme.other_variables[var_name] = source_theme.other_variables[var_name]
                            logInfo(f"Copied variable '{var_name}' from theme '{source_theme.name}' to theme '{target_theme.name}'")
                            break

    def ensureThemeVariableConsistency(self):
        """Ensure all themes have consistent variable structure by copying missing ones"""
        self.copyMissingVariablesFromOtherThemes()

def setNewIcon(self, url):
    icon = QIcon(url)
    self.setIcon(icon)

    self.iconUrl = url

def setNewPixmap(self, url):
    piximap = QPixmap(url)
    self.setPixmap(piximap)

    self.piximapUrl = url

def setNewTabIcon(self, tabName, url):
    icon = QIcon(url)

    # Find the index of the tab with the name "Tab 2"
    tab_index = -1
    for index in range(self.count()):
        tab_object_name = self.widget(index).objectName()
        if tab_object_name == tabName:
            tab_index = index
            break
    # Change icon of the tab with the name "Tab 2"
    if tab_index != -1:
        self.setTabIcon(tab_index, icon)

    self.iconUrl = url

def setNewToolBoxIcon(self, itemName, url):
    icon = QIcon(url)

    # Find the index of the item with the specified name
    item_index = -1
    for index in range(self.count()):
        item_text = self.widget(index).objectName()
        if item_text == itemName:
            item_index = index
            break

    # Change icon of the item with the specified name
    if item_index != -1:
        self.setItemIcon(item_index, icon)

    self.iconUrl = url

def setNewTreeWidgetItemIcon(self, itemName, url, column=0):
    icon = QIcon(url)
    self.setIcon(column, icon)
    self.iconUrl = url

# Monkey patching QPushButton class to add setNewIcon method
QPushButton.iconUrl = None
QPushButton.setNewIcon = setNewIcon

QCheckBox.iconUrl = None
QCheckBox.setNewIcon = setNewIcon

QCustomCheckBox.iconUrl = None
QCustomCheckBox.setNewIcon = setNewIcon

QLabel.piximapUrl = None
QLabel.setNewPixmap = setNewPixmap

QTabWidget.setNewTabIcon = setNewTabIcon
QToolBox.setNewItemIcon = setNewToolBoxIcon
QTreeWidgetItem.setNewItemIcon = setNewTreeWidgetItemIcon

QCustomSidebarLabel.iconUrl = None
QCustomSidebarLabel.setNewIcon = setNewIcon

QCustomSidebarButton.iconUrl = None
QCustomSidebarButton.setNewIcon = setNewIcon

class Theme:
    def __init__(self, name, bg_color, txt_color, accent_color, icons_color="", createNewIcons=True, defaultTheme=False, other_variables={}, predefined=False):
        self.name = name
        self.bg_color = bg_color
        self.txt_color = txt_color
        self.accent_color = accent_color
        self.icons_color = icons_color
        self.defaultTheme = defaultTheme
        self.other_variables = other_variables
        self.predefined = predefined

        # Properties for dynamic access
        self.backgroundColor = bg_color
        self.textColor = txt_color
        self.accentColor = accent_color
        self.iconsColor = icons_color

        self.createNewIcons = createNewIcons

class Dark(Theme):
    def __init__(self, defaultTheme=False, other_variables={}):
        super().__init__("Dark", "#0d1117", "white", "#238636", "white", defaultTheme, other_variables = other_variables, predefined=True)

class Light(Theme):
    def __init__(self, defaultTheme=False, other_variables={}):
        super().__init__("Light", "white", "black", "#00bcff", "black", defaultTheme, other_variables = other_variables, predefined=True)

class NewTheme(Theme):
    def __init__(self, name, bg_color, txt_color, accent_color, icons_color, defaultTheme=False, other_variables={}):
        super().__init__(name, bg_color, txt_color, accent_color, icons_color, defaultTheme, other_variables)