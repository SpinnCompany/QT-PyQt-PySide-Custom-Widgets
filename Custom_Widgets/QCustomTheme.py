import os
# FIX: DLL import issues
def set_dll_search_path():
    # Python 3.8 no longer searches for DLLs in PATH, so we have to add
    # everything in PATH manually. Note that unlike PATH add_dll_directory
    # has no defined order, so if there are two cairo DLLs in PATH we
    # might get a random one.
    if os.name != "nt" or not hasattr(os, "add_dll_directory"):
        return
    for p in os.environ.get("PATH", "").split(os.pathsep):
        try:
            os.add_dll_directory(p)
        except OSError:
            pass

set_dll_search_path()

import re
import json
import sys
import shutil
import cairosvg
import codecs
import subprocess
from urllib.parse import urlparse
import __main__

import matplotlib.colors as mc
import colorsys

from qtpy.QtWidgets import QApplication, QPushButton, QLabel, QTabWidget, QCheckBox, QToolBox, QMainWindow, QMenu, QTreeWidgetItem
from qtpy.QtGui import QPalette, QCursor, QFont, QFontDatabase, QIcon, QColor, QPixmap
from qtpy.QtCore import QCoreApplication, QRect, Signal, QObject, QSettings, Property, QDir, QThreadPool

import qtsass

from Custom_Widgets.QCustomCheckBox import QCustomCheckBox
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomSidebarLabel import QCustomSidebarLabel 
from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton 
from Custom_Widgets.WidgetsWorker import Worker, WorkerResponse
from Custom_Widgets.Log import *
from Custom_Widgets.Utils import createQrcFile, is_in_designer
from Custom_Widgets.JSonStyles import loadJsonStyle

script_dir = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"

class QCustomTheme(QObject):
    _instance = None  # Class-level variable to hold the singleton instance
    onThemeChanged = Signal()  # Define a class-level signal

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create a new instance if not already created
            cls._instance = super(QCustomTheme, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parent=None):
        if not hasattr(self, "_initialized"):  # To prevent reinitialization
            super().__init__(parent)
            self._theme = "default"
            self._themes = []
            self._initialized = True  # Mark as initialized to avoid multiple init calls
            self.checkForMissingicons = False

            self.initializeThemeVars()
            self.defineThemeVarMapping()
            self.loadProductSansFont()

            QCoreApplication.instance().aboutToQuit.connect(self.stopWorkers)

            # START THREAD
            self.customWidgetsThreadpool = QThreadPool()

            self._themes.append(Light())
            self._themes.append(Dark())

            self.jsonStyleSheets = [] 
            self.jsonStyleData = {}

            self.designerIconsColor = "#000"
            self.themesRead = False

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
            '$SIZE_BORDER_RADIUS': '4px',
            '$BORDER_1': '1px solid ' + self.COLOR_BACKGROUND_1,
            '$BORDER_2': '1px solid ' + self.COLOR_BACKGROUND_4,
            '$BORDER_3': '1px solid ' + self.COLOR_BACKGROUND_6,
            '$BORDER_SELECTION_3': '1px solid ' + self.COLOR_ACCENT_3,
            '$BORDER_SELECTION_2': '1px solid ' + self.COLOR_ACCENT_2,
            '$BORDER_SELECTION_1': '1px solid ' + self.COLOR_ACCENT_1,
            '$PATH_RESOURCES': f"'{self.PATH_RESOURCES}'",
            '$RELATIVE_FOLDER': f"{script_dir}",
            
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
            'THEME.SIZE_BORDER_RADIUS': '4px',
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
        settings.setValue("THEME", value)
        # if settings.value("INIT-THEME-SET") is None:
        #     settings.setValue("INIT-THEME-SET", True)
        
        self.onThemeChanged.emit()  # Emit the signal when theme is modified
        self.applyCompiledSass()

    def refreshTheme(self):
        QAppSettings.updateAppSettings(self, reloadJson = False)

    def themeChanged(self):
        # Emit the signal from the instance
        self.onThemeChanged.emit()

    @staticmethod
    def isAppDarkThemed():
        app = QApplication.instance()
        if app is None:
            raise RuntimeError("QApplication instance is required.")
        
        palette = app.palette()
        
        # Extract the background color of the application palette
        background_color = palette.color(QPalette.Window)
        
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
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

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

    def applyIcons(self, widget_container, folder=None, ui_file_name=None):
        try:
            icons_color = self.iconsColor

            settings = QSettings()
            settings.setValue("ICONS-COLOR", icons_color)

            if icons_color is None:
                logging.warning("Icons color is not set. Skipping icon application.")
                return
            if not folder:
                folder = icons_color.replace("#", "")

            current_script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
            jsonFilesFolder = os.path.abspath(os.path.join(current_script_folder, "generated-files/json"))
            if not os.path.exists(jsonFilesFolder):
                os.makedirs(jsonFilesFolder)
                logInfo(f"Created JSON files folder: {jsonFilesFolder}")
            
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

                                    if not os.path.exists(abs_icon_url):
                                        logError(f"Failed to process widget '{widget_name}' in JSON file '{jsonFile}': Error: Missing file - {abs_icon_url}")

                                    if widget_class == "QCustomThemeDarkLightToggle":
                                        light_icon_url = widget_info.get("lightThemeIcon", "")
                                        dark_icon_url = widget_info.get("darkThemeIcon", "")

                                        if light_icon_url is None:
                                            light_icon_url = ""
                                        if dark_icon_url is None:
                                            dark_icon_url = ""
                                            
                                        light_icon_url = re.sub(prefix_to_remove, f'icons/{folder}', light_icon_url).replace("../", "")
                                        abs_l_icon_url = os.path.abspath(os.path.join(current_script_folder, light_icon_url))

                                        dark_icon_url = re.sub(prefix_to_remove, f'icons/{folder}', dark_icon_url).replace("../", "")
                                        abs_d_icon_url = os.path.abspath(os.path.join(current_script_folder, dark_icon_url))

                                        if hasattr(widget_container, str(widget_name)):
                                            btn = getattr(widget_container, str(widget_name))
                                            if abs_l_icon_url != "default_icon_url":
                                                btn.lightThemeIcon = QIcon(abs_l_icon_url)
                                            if abs_d_icon_url != "default_icon_url":
                                                btn.darkThemeIcon = QIcon(abs_d_icon_url)
                                            btn.update()

                                    elif abs_icon_url != "default_icon_url" and hasattr(widget_container, str(widget_name)):
                                        widget = getattr(widget_container, str(widget_name))
                                        if setter_method is not None and isinstance(widget, globals()[widget_class]):
                                            getattr(widget, setter_method)(abs_icon_url)
                                        elif widget_class == "QWidget" and "QTabWidget" in widget_info:
                                            parent_name = widget_info.get("QTabWidget", "")
                                            parent = getattr(widget_container, str(parent_name))
                                            if isinstance(parent, QTabWidget):
                                                parent.setNewTabIcon(widget_name, abs_icon_url)
                                        elif widget_class == "QWidget" and "QToolBox" in widget_info:
                                            parent_name = widget_info.get("QToolBox", "")
                                            parent = getattr(widget_container, str(parent_name))
                                            if isinstance(parent, QToolBox):
                                                parent.setNewItemIcon(widget_name, abs_icon_url)
                                        elif widget_class == "QTreeWidget":
                                            tree_item = getattr(widget_container, str(widget_name))
                                            tree_item.setNewItemIcon(tree_item, abs_icon_url)

                                except Exception as e:
                                    logError(f"Failed to process widget '{widget_name}' in JSON file '{jsonFile}': {e}")
                                    logging.debug(traceback.format_exc())
                    except Exception as e:
                        logError(f"Error processing JSON file '{jsonFile}': {e}")
                        logging.debug(traceback.format_exc())
        except Exception as e:
            logCritical(f"Critical error in applyIcons: {e}")
            logging.debug(traceback.format_exc())
                                                
    
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
        try:
            c = mc.cnames[color]
        except KeyError:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))

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
            if color in mc.CSS4_COLORS:
                return mc.CSS4_COLORS[color]
            else:
                try:
                    rgba = mc.to_rgba(color)
                    return mc.to_hex(rgba)
                except ValueError:
                    raise ValueError(f"Invalid color name: {color}")

        elif isinstance(color, tuple) and len(color) == 3:
            rgba = color + (1.0,)
            return mc.to_hex(rgba)

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
        rgb = mc.to_rgba(color)[:3]
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
                rgb = mc.to_rgb(color)
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
        settings.setValue("ICONS-COLOR", iconsColor)
        
        return currentThemeInfo
        
    def createVariables(self):
        theme = self.currentTheme
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

        if theme.icons_color is not None and theme.icons_color != "":
            folder = theme.icons_color.replace("#", "")
        else:
            folder = theme.accent_color.replace("#", "")
        
        QDir.addSearchPath('theme-icons', os.path.join(os.getcwd(), 'Qss/icons/'))
        theme.ICONS = "theme-icons:"+folder+"/"

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

         # Add other variables from the theme
        other_vars_scss = ""
        if hasattr(theme, 'other_variables') and theme.other_variables:
            for var_name, var_value in theme.other_variables.items():
                # Convert to SCSS variable format
                other_vars_scss += f"${var_name}: {var_value};\n"

        scss_folder = os.path.abspath(os.path.join(os.getcwd(), 'Qss/scss'))
        if not os.path.exists(scss_folder):
            os.makedirs(scss_folder)

        scss_path = os.path.abspath(os.path.join(scss_folder, '_variables.scss'))
        with open(scss_path, 'w') as f:
            f.write(f"""
            //===================================================//
            // FILE AUTO-GENERATED, ANY CHANGES MADE WILL BE LOST //
            //====================================================//
            $COLOR_BACKGROUND_1: {theme.BG_1};
            $COLOR_BACKGROUND_2: {theme.BG_2};
            $COLOR_BACKGROUND_3: {theme.BG_3};
            $COLOR_BACKGROUND_4: {theme.BG_4};
            $COLOR_BACKGROUND_5: {theme.BG_5};
            $COLOR_BACKGROUND_6: {theme.BG_6};
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
            $COLOR_TEXT_1: {theme.CT_1};
            $COLOR_TEXT_2: {theme.CT_2};
            $COLOR_TEXT_3: {theme.CT_3};
            $COLOR_TEXT_4: {theme.CT_4};
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
            $COLOR_ACCENT_1: {theme.CA_1};
            $COLOR_ACCENT_2: {theme.CA_2};
            $COLOR_ACCENT_3: {theme.CA_3};
            $COLOR_ACCENT_4: {theme.CA_4};
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
            $OPACITY_TOOLTIP: 230;
            $SIZE_BORDER_RADIUS: 4px;
            $BORDER_1: 1px solid $COLOR_BACKGROUND_1;
            $BORDER_2: 1px solid $COLOR_BACKGROUND_4;
            $BORDER_3: 1px solid $COLOR_BACKGROUND_6;
            $BORDER_SELECTION_3: 1px solid $COLOR_ACCENT_3;
            $BORDER_SELECTION_2: 1px solid $COLOR_ACCENT_2;
            $BORDER_SELECTION_1: 1px solid $COLOR_ACCENT_1;
            $PATH_RESOURCES: '{theme.ICONS}';
            $RELATIVE_FOLDER: "{script_dir}";
            """)
            
            # Add the other variables section
            if other_vars_scss:
                f.write("\n        // Additional theme variables\n")
                f.write(other_vars_scss)
            
            f.write("""
            //===================================================//
            // END //
            //====================================================//
            """)

        f.close()

    def compileSassTheme(self, progress_callback):
        ## GENERATE NEW ICONS FOR CURRENT THEME
        self.generateNewIcons(progress_callback)

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
        except:
            pass

    def styleVariablesFromTheme(self, stylesheet):
        self.defineThemeVarMapping()
        # Replace variables in the stylesheet string
        for var, value in self._variable_mapping.items():
            # Escape special characters in the variable name
            var_pattern = re.escape(var)
            # Replace the variable with its corresponding value
            stylesheet = re.sub(var_pattern, value, stylesheet)
        return stylesheet
    
    def getThemeVariableValue(self, color_variable):
        self.createVariables()
        return self._variable_mapping.get(color_variable, color_variable)
    
    def reloadJsonStyles(self, update = False):
        loadJsonStyle(self, jsonFiles = self.jsonStyleSheets, update = update)

    # apply custom font
    def loadProductSansFont(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        """Load and apply product sans font"""
        font_id = QFontDatabase.addApplicationFont(os.path.join(script_dir, "Qss/fonts/Rosario/Rosario-VariableFont_wght.ttf"))
        # if font loaded
        if font_id == -1:
            print("Failed to load Product Sans font")
            return

    def applyCompiledSass(self, generateIcons: bool = True, paintEntireApp: bool = True):
        if not self.themesRead:
            return
        qcss_folder = os.path.abspath(os.path.join(os.getcwd(), 'Qss/scss'))
        if not os.path.exists(qcss_folder):
            os.makedirs(qcss_folder)
        
        css_folder = os.path.abspath(os.path.join(os.getcwd(), 'generated-files/css/'))
        if not os.path.exists(css_folder):
            os.makedirs(css_folder)

        main_sass_path = os.path.abspath(os.path.join(os.getcwd(), 'Qss/scss/main.scss'))
        styles_sass_path = os.path.abspath(os.path.join(os.getcwd(), 'Qss/scss/_styles.scss'))
        css_path = os.path.abspath(os.path.join(os.getcwd(), 'generated-files/css/main.css'))

        self.createVariables()

        if not os.path.exists(main_sass_path):   
            shutil.copy(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Qss/scss/main.scss')), qcss_folder)  

        if not os.path.exists(styles_sass_path):   
            shutil.copy(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Qss/scss/_styles.scss')), qcss_folder)  

        default_scss_path = os.path.abspath(os.path.join(os.getcwd(), 'Qss/scss/defaultStyle.scss'))
        if not os.path.exists(default_scss_path):   
            f = open(default_scss_path, 'w')
            print(f"""
            //===================================================//
            // FILE AUTO-GENERATED. PUT YOUR DEFAULT STYLES HERE. 
            // THESE STYLES WILL OVERIDE THE THEME STYLES
            //====================================================//
            
            //===================================================//
            // END //
            //====================================================//
            """, file=f)

            f.close()

        qtsass.compile_filename(main_sass_path, css_path)
        
        with open(css_path,"r") as css:
            stylesheet = css.read()

        # Create QApplication instance if it doesn't exist
        app = QApplication.instance() if QApplication.instance() else QApplication([])
        mainWindow = self.getMainWindow()

        if not paintEntireApp:
            mainWindow.setStyleSheet(stylesheet)
            palette = mainWindow.palette()

            app.setStyleSheet("")
            # app.setPalette(app.style().standardPalette())

        else:
            mainWindow.setStyleSheet("")
            mainWindow.setPalette(mainWindow.style().standardPalette())

            app.setStyleSheet(stylesheet)
            # newly created menus may need re-styling
            for obj in QApplication.instance().allWidgets():
                if isinstance(obj, QMenu):
                    obj.setStyleSheet(stylesheet)
        
            # palette = QPalette()
            palette = app.palette()

            # Set the background color
            try:
                # pyside2
                palette.setColor(QPalette.Background, QColor(self.COLOR_BACKGROUND_1))
            except AttributeError as e:
                pass
            try:
                # pyside6
                palette.setColor(QPalette.Window, QColor(self.COLOR_BACKGROUND_1))
            except AttributeError as e:
                pass
            

            # Set the text color
            palette.setColor(QPalette.Text, QColor(self.COLOR_TEXT_1))

            # Set the button color
            palette.setColor(QPalette.Button, QColor(self.COLOR_BACKGROUND_3))

            # Set the button text color
            palette.setColor(QPalette.ButtonText, QColor(self.COLOR_TEXT_1))

            # Set the highlight color
            palette.setColor(QPalette.Highlight, QColor(self.COLOR_BACKGROUND_6))

            # Set the highlight text color
            palette.setColor(QPalette.HighlightedText, QColor(self.COLOR_ACCENT_1))

            # Apply the palette to the main window
            mainWindow.setPalette(palette)

            app.setPalette(palette)

        try:
            mainWindow.update()
            app.update()
        except:
            pass

        background_color = palette.color(QPalette.Window)
        
        # Calculate luminance using the YIQ color space formula
        luminance = (0.299 * background_color.red() + 0.587 * background_color.green() + 0.114 * background_color.blue()) / 255
        
        if luminance < 0.5:
            self.isThemeDark =  True  # Dark theme
        else:
            self.isThemeDark = False  # Light theme
            
        
        if generateIcons:
            ########################################################################
            ## GENERATE NEW ICONS
            # START WORKER
            # CURRENT THEME ICONS
            color = self.getCurrentThemeInfo()
            normal_color = str(color["icons-color"])
            icons_folder = normal_color.replace("#", "")

            self.iconsWorker = Worker(self.compileSassTheme)
            self.iconsWorker.signals.result.connect(WorkerResponse.print_output)
            # self.iconsWorker.signals.finished.connect(lambda: self.applyIcons(folder=icons_folder))
            self.iconsWorker.signals.progress.connect(self.sassCompilationProgress)

            # ALL THEME ICONS
            self.allIconsWorker = Worker(self.makeAllIcons)
            self.allIconsWorker.signals.result.connect(WorkerResponse.print_output)
            self.allIconsWorker.signals.finished.connect(lambda: logInfo("all icons have been checked and missing icons generated!"))
            self.allIconsWorker.signals.progress.connect(self.sassCompilationProgress)

            
            if not self.iconsColor == normal_color and color["icons-color"] is not None:     
                # Execute
                self.customWidgetsThreadpool.start(self.iconsWorker)
            else:
                self.customWidgetsThreadpool.start(self.allIconsWorker)

    def getAllFolders(self, base_folder):
        all_folders = []
        for root, dirs, files in os.walk(base_folder):
            for dir_name in dirs:
                folder_path = os.path.relpath(os.path.join(root, dir_name), base_folder)
                all_folders.append(folder_path)
        return all_folders

    def getAllSvgFiles(self, base_folder):
        svg_files = []
        for file_name in os.listdir(base_folder):
            if file_name.lower().endswith('.svg'):
                file_path = os.path.join(base_folder, file_name)
                svg_files.append(file_path)
        return svg_files
    
    def generateIcons(self, progress_callback, iconsColor, suffix, iconsFolder="", createQrc=False, output_width=None, output_height=None):
        # Base folder
        base_folder = os.path.dirname(__file__)
        icons_folder_base = os.path.join(base_folder, 'Qss/icons')

        svg_color = "#ffffff"

        # Get a list of all folders inside 'icons'
        try:
            folders = self.getAllFolders(icons_folder_base)
        except:
            folders = QCustomTheme.getAllFolders(None, icons_folder_base)

        new_icon_made = False
        qrc_content = f'<RCC>\n'

        qrc_folder_path = os.path.abspath(os.path.join(os.getcwd(), f'Qss/icons'))
        
        for folder in folders:
            qrc_prefix = (folder+suffix).replace("/", "_")
            qrc_prefix = (folder+suffix).replace("\\", "_")
            qrc_content += f'  <qresource prefix="{qrc_prefix}">\n'
            
            icons_folder_path = os.path.abspath(os.path.join(os.getcwd(), f'Qss/icons/{iconsFolder}/{folder}'))

            try:
                if not os.path.exists(icons_folder_path):
                    os.makedirs(icons_folder_path)
            except:
                pass

            folder_path = os.path.join(icons_folder_base, folder)
            list_of_files = self.getAllSvgFiles(folder_path)
            total_icons = len(list_of_files)

            for index, file_path in enumerate(list_of_files):
                file_name = os.path.basename(urlparse(file_path).path).replace(".svg", f"{suffix}.png")
                output_path = os.path.abspath(os.path.join(icons_folder_path, file_name))

                qrc_content += f'    <file>icons/{folder}/{file_name}</file>\n'
                if progress_callback is not None:
                    progress_callback.emit(int((index / total_icons) * 100))

                if os.path.exists(output_path):
                    continue

                try:
                    with codecs.open(file_path, encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                        new_svg = content.replace(svg_color, iconsColor)
                        new_bytes = str.encode(new_svg)

                        if output_height is not None and output_width is not None:
                            cairosvg.svg2png(bytestring=new_bytes, write_to=output_path, output_width=output_width, output_height=output_height)
                        
                        else:
                            cairosvg.svg2png(bytestring=new_bytes, write_to=output_path)

                        new_icon_made = True

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

            qrc_content += f'  </qresource>\n'

        qrc_content += f'</RCC>\n'
        qrc_file_path = os.path.abspath(os.path.join(qrc_folder_path, f'{suffix}_icons.qrc'))

        if (createQrc and new_icon_made) or not os.path.exists(qrc_file_path):
            createQrcFile(qrc_content, qrc_file_path)
            # Convert qrc to py 
            # qrc_output_path = qrc_file_path.replace(".qrc", "_rc.py")
            # qrc_output_path = qrc_output_path.replace("Qss/", "") #linux
            # qrc_output_path = qrc_output_path.replace("Qss\\", "") #windows
            # NewIconsGenerator.qrcToPy(qrc_file_path, qrc_output_path)

    def generateNewIcons(self, progress_callback = None, force = False): 
        if not self.checkForMissingicons and progress_callback is not None:
                # emit 100% progress
                progress_callback.emit(100)
                return 

        # Icons color
        color = self.getCurrentThemeInfo()
        normal_color = str(color["icons-color"])
        
        settings = QSettings()
        if color["icons-color"] is not None or force:
            logInfo(("Current icons color ", settings.value("ICONS-COLOR"), "New icons color", normal_color))
            logInfo("Generating icons for your theme, please wait. This may take long")
            
            settings.setValue("ICONS-COLOR", normal_color)
            iconsFolderName = normal_color.replace("#", "")

            # Create normal icons
            self.generateIcons(progress_callback, normal_color, "", iconsFolderName, createQrc = False)

            settings = QSettings()

            logInfo(("DONE: Current icons color ", settings.value("ICONS-COLOR")))        

    def generateAllIcons(self, progress_callback = None):
        if is_in_designer(self):
            return
        
        settings = QSettings()
        if not self.checkForMissingicons and progress_callback is not None:
            # emit 100% progress
            progress_callback.emit(100)
            return
        
        # Local list to hold all theme names that have been checked
        checked_themes = []

        def get_theme_color(theme):
            if hasattr(theme, "iconsColor") and theme.iconsColor != "":
                return theme.iconsColor
            if hasattr(theme, "accentColor") and theme.accentColor != "":
                return theme.accentColor
            return ""
        
        def make_theme_icons(theme):
            # Skip if the theme has already been checked
            if theme.name in checked_themes:
                return
        
            color = get_theme_color(theme)
            try:
                if color == "":
                    return
            except:
                pass

            logInfo(f"Checking icons for {theme.name} theme. Icons color: {color}")

            iconsFolderName = color.replace("#", "")
            self.generateIcons(progress_callback, color, "", iconsFolderName)

            # Add the theme name to the checked list
            checked_themes.append(theme.name)

        current_theme = self.currentTheme
        make_theme_icons(current_theme)

        themes = self.themes
        
        for theme in themes:
            if theme.name == current_theme.name:
                continue
            make_theme_icons(theme)
            
        # then make icons for qt designer
        logInfo(f"Checking icons for qt designer app.")
        if settings.value("DESIGNER-ICONS-COLOR") is not None:
            self.generateIcons(progress_callback, settings.value("DESIGNER-ICONS-COLOR"), "", "icons", createQrc=True, output_width=24, output_height=24)
        else:
            self.generateIcons(progress_callback, self.designerIconsColor, "", "icons", createQrc=True, output_width=24, output_height=24)

    # Method to create a new theme dynamically
    def createNewTheme(self, name, bg_color, txt_color, accent_color, icons_color, createNewIcons=True, defaultTheme=False, other_variables={}):
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
            
            # Update dynamic properties as well
            existing_theme.backgroundColor = bg_color
            existing_theme.textColor = txt_color
            existing_theme.accentColor = accent_color
            existing_theme.iconsColor = icons_color
            
        else:
            # Create a new theme
            new_theme = Theme(name, bg_color, txt_color, accent_color, icons_color, createNewIcons, defaultTheme, other_variables)
            new_theme.other_variables = other_variables
            self._themes.append(new_theme)


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
    def __init__(self, name, bg_color, txt_color, accent_color, icons_color="", createNewIcons=True, defaultTheme=False, other_variables={}):
        self.name = name
        self.bg_color = bg_color
        self.txt_color = txt_color
        self.accent_color = accent_color
        self.icons_color = icons_color
        self.defaultTheme = defaultTheme
        self.other_variables = other_variables

        # Properties for dynamic access
        self.backgroundColor = bg_color
        self.textColor = txt_color
        self.accentColor = accent_color
        self.iconsColor = icons_color

        self.createNewIcons = createNewIcons

class Dark(Theme):
    def __init__(self, defaultTheme=False, other_variables={}):
        super().__init__("Dark", "#0d1117", "white", "#238636", "white", defaultTheme, other_variables)

class Light(Theme):
    def __init__(self, defaultTheme=False, other_variables={}):
        super().__init__("Light", "white", "black", "#00bcff", "black", defaultTheme, other_variables)

class NewTheme(Theme):
    def __init__(self, name, bg_color, txt_color, accent_color, icons_color, defaultTheme=False, other_variables={}):
        super().__init__(name, bg_color, txt_color, accent_color, icons_color, defaultTheme, other_variables)
