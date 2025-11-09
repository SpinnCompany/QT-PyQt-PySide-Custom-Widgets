from qtpy.QtWidgets import QMainWindow, QPushButton, QWidget, QFrame, QStyle, QStyleOption, QVBoxLayout
from qtpy.QtCore import Property, Qt, QEvent
from qtpy.QtGui import QIcon, QPaintEvent, QPainter, QColor, QResizeEvent

from Custom_Widgets.QAppSettings import QAppSettings as QCustomAppSettings
from Custom_Widgets.JSonStyles import updateJson
from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.FileMonitor import QSsFileMonitor
from Custom_Widgets.Utils import is_in_designer
from Custom_Widgets.Log import *
from Custom_Widgets import *

import os

class QCustomQMainWindow(QMainWindow):
    # Icon path for the widget
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/airplay.png")
    
    # Tooltip for the widget
    WIDGET_TOOLTIP = "A custom QMainWindow"
    
    # XML string for the widget
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class="QCustomQMainWindow" name="CustomMainWindow">
        <property name="geometry">
        <rect>
            <x>0</x>
            <y>0</y>
            <width>800</width>
            <height>600</height>
        </rect>
        </property>
        <property name="windowTitle">
        <string>Custom MainWindow</string>
        </property>
        <widget class="QWidget" name="centralwidget"/>
        </widget>
    </ui>
    """
    WIDGET_MODULE="Custom_Widgets.QCustomQMainWindow"

    def __init__(self, parent=None, frameless: bool = False, translucentBg: bool = False, minimizeBtn: QPushButton = None, closeBtn: QPushButton = None, restoreBtn: QPushButton = None,
                restoreBtnNormalIcon: QIcon = None, restoreBtnMaximizedIcon: QIcon = None, tittleBar: QWidget | QFrame = None, moveWindow: QWidget | QFrame = None, sizeGrip: QWidget | QFrame = None):
        super().__init__(parent)

        self._frameless = frameless
        self._translucent_bg = translucentBg
        self._minimize_btn = minimizeBtn
        self._close_btn = closeBtn
        self._restore_btn = restoreBtn
        self._restore_btn_normal_icon = restoreBtnNormalIcon
        self._restore_btn_maximized_icon = restoreBtnMaximizedIcon
        self._title_bar = tittleBar
        self._move_window = moveWindow
        self._size_grip = sizeGrip
        self._designer_prev = True
        self._live_compile_style = False
        self._json_file = "json-styles/style.json"
        self._paint_qt_designer = False
        self._shadow_color = QColor("")
        self._title = ""
        self._shadow_blur = 0
        self._shadow_x_offset = 0
        self._shadow_y_offset = 0
        self.themeEngine = QCustomTheme(self)
        # self.themeEngine.onThemeChanged.connect(lambda: print("Theme changed"))
        self._app_theme = self.themeEngine.theme
        self._window_radius = 0

        self.showCustomWidgetsLogs = True  
        self.checkForMissingicons = False 

        loadJsonStyle(
            self, 
            jsonFiles={
                self._json_file
            }        
        )
        
        self.compileStylesheet()

    @Property(str)
    def appTheme(self):
        return self._app_theme
    
    @appTheme.setter
    def appTheme(self, value: str):
        if self._app_theme != value and self.isValidTheme(value):
            self._app_theme = value
            self.themeEngine.setTheme(value)
            self.compileStylesheet()

    def isValidTheme(self, value: str):
        try:
            for theme in self.themes:
                if theme.name == value:
                   return True
            return False
        except:
            return False

    @Property(bool)
    def liveCompileStylesheet(self):
        return self._live_compile_style
    
    @liveCompileStylesheet.setter
    def liveCompileStylesheet(self, value = False):
        if self._live_compile_style == value:
            return

        self._live_compile_style = value

        updateJson(
            self._json_file,
            "LiveCompileQss",
            value
        )

        self.liveCompileQss = value
        
        self.compileStylesheet()
    
    @Property(str)
    def jsonStylesheetFilePath(self):
        return self._json_file
    
    @jsonStylesheetFilePath.setter
    def jsonStylesheetFilePath(self, value:str = ""):
        if self._json_file == value:
            return

        self._json_file = value
        loadJsonStyle(
            self, 
            jsonFiles={
                self._json_file
            }        
        )
        
        self.compileStylesheet()

    def compileStylesheet(self):
        logInfo("Should live compile stylesheet?: "+str(self._live_compile_style))
        logInfo("Should paint Qt Designer UI?: "+str(self._paint_qt_designer))

        if self._live_compile_style and self._json_file:
            try:
                logInfo("JSon stylesheet path: "+self._json_file) 

                QCustomAppSettings.updateAppSettings(self, generateIcons = False, reloadJson = False, paintEntireApp = self._paint_qt_designer, QtDesignerMode = True)
                self.themeEngine = QCustomTheme(self)
                
                self.appTheme = self.themeEngine.theme

                # check file watcher
                if not hasattr(self, 'qss_watcher'):
                    try:
                        QSsFileMonitor.start_qss_file_listener(self)
                    except Exception as e:
                        logError("Failed to start live file listener: "+str(e))

            except Exception as e:
                logError(str(e))

    @Property(bool)
    def paintQtDesignerUI(self):
        return self._paint_qt_designer
    
    @paintQtDesignerUI.setter
    def paintQtDesignerUI(self, value):
        self._paint_qt_designer = value

        self.compileStylesheet()

    @Property(bool)
    def frameless(self):
        return self._frameless
    
    @frameless.setter
    def frameless(self, value):
        if self._frameless == value:
            return
        self._frameless = value

        updateJson(
            self._json_file,
            "QMainWindow.frameless",
            value,
            self = self
        )

    @Property(bool)
    def translucentBg(self):
        return self._translucent_bg
    
    @translucentBg.setter
    def translucentBg(self, value):
        if self._translucent_bg == value:
            return

        self._translucent_bg = value

        updateJson(
            self._json_file,
            "QMainWindow.transluscentBg",
            value,
            self = self
        )

    @Property(str, notify=None)
    def minimizeBtn(self):
        return self._minimize_btn
    
    @minimizeBtn.setter
    def minimizeBtn(self, button: str):
        if self._minimize_btn == button:
            return

        self._minimize_btn = button

        updateJson(
            self._json_file,
            "QMainWindow.navigation.minimize",
            button,
            self = self
        )

    @Property(str, notify=None)
    def closeBtn(self):
        return self._close_btn
    
    @closeBtn.setter
    def closeBtn(self, button: str):
        if self._close_btn == button:
            return

        self._close_btn = button

        updateJson(
            self._json_file,
            "QMainWindow.navigation.close",
            button,
            self = self
        )

    @Property(str, notify=None)
    def restoreBtn(self):
        return self._restore_btn
    
    @restoreBtn.setter
    def restoreBtn(self, button: str):
        if self._restore_btn == button:
            return

        self._restore_btn = button

        updateJson(
            self._json_file,
            "QMainWindow.navigation.restore.buttonName",
            button,
            self = self
        )

    @Property(str, notify=None)
    def restoreBtnNormalIcon(self):
        return self._restore_btn_normal_icon
    
    @restoreBtnNormalIcon.setter
    def restoreBtnNormalIcon(self, icon: QIcon):
        if self._restore_btn_normal_icon == icon:
            return

        self._restore_btn_normal_icon = icon

        updateJson(
            self._json_file,
            "QMainWindow.navigation.restore.normalIcon",
            icon,
            self = self
        )

    @Property(str, notify=None)
    def restoreBtnMaximizedIcon(self):
        return self._restore_btn_maximized_icon
    
    @restoreBtnMaximizedIcon.setter
    def restoreBtnMaximizedIcon(self, icon: QIcon):
        if self._restore_btn_maximized_icon == icon:
            return

        self._restore_btn_maximized_icon = icon

        updateJson(
            self._json_file,
            "QMainWindow.navigation.restore.maximizedIcon",
            icon,
            self = self
        )

    @Property(str, notify=None)
    def titleBar(self):
        return self._title_bar
    
    @titleBar.setter
    def titleBar(self, widget: str):
        if self._title_bar == widget:
            return

        self._title_bar = widget

        updateJson(
            self._json_file,
            "QMainWindow.navigation.tittleBar",
            widget,
            self = self
        )

    @Property(str, notify=None)
    def moveWindow(self):
        return self._move_window
    
    @moveWindow.setter
    def moveWindow(self, widget: str):
        if self._move_window == widget:
            return

        self._move_window = widget

        updateJson(
            self._json_file,
            "QMainWindow.navigation.moveWindow",
            widget,
            self = self
        )

    @Property(str, notify=None)
    def sizeGrip(self):
        return self._size_grip
    
    @sizeGrip.setter
    def sizeGrip(self, widget: str):
        if self._size_grip == widget:
            return

        self._size_grip = widget

        updateJson(
            self._json_file,
            "QMainWindow.sizeGrip",
            widget,
            self = self
        )

    @Property(QColor, notify=None)
    def shadowColor(self):
        return self._shadow_color
    
    @shadowColor.setter
    def shadowColor(self, color: QColor):
        if self._shadow_color == color:
            return

        self._shadow_color = color

        updateJson(
            self._json_file,
            "QMainWindow.shadow.color",
            color.name(),
            self = self
        )

    @Property(int, notify=None)
    def shadowBlurRadius(self):
        return self._shadow_blur
    
    @shadowBlurRadius.setter
    def shadowBlurRadius(self, blur: int):
        if self._shadow_blur == blur:
            return

        self._shadow_blur = blur

        updateJson(
            self._json_file,
            "QMainWindow.shadow.blurRadius",
            blur,
            self = self
        )

    @Property(int, notify=None)
    def shadowXOffset(self):
        return self._shadow_x_offset
    
    @shadowXOffset.setter
    def shadowXOffset(self, x: int):
        if self._shadow_x_offset == x:
            return

        self._shadow_x_offset = x

        updateJson(
            self._json_file,
            "QMainWindow.shadow.xOffset",
            x,
            self = self
        )
    
    @Property(int, notify=None)
    def shadowYOffset(self):
        return self._shadow_y_offset
    
    @shadowYOffset.setter
    def shadowYOffset(self, y: int):
        if self._shadow_y_offset == y:
            return

        self._shadow_y_offset = y

        updateJson(
            self._json_file,
            "QMainWindow.shadow.yOffset",
            y,
            self = self
        )

    @Property(int, notify=None)
    def windowBorderRadius(self):
        return self._window_radius
    
    @windowBorderRadius.setter
    def windowBorderRadius(self, radius: int):
        if self._window_radius == radius:
            return

        self._window_radius = radius

        updateJson(
            self._json_file,
            "QMainWindow.borderRadius",
            radius,
            self = self
        )

    def paintEvent(self, event: QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        # logInfo(str(self._app_theme+" "+self.themeEngine.theme))

        # refresh theme
        if self.themeEngine.theme != "default" and self.themeEngine.theme != "Default-theme" and self._app_theme != self.themeEngine.theme:
            if self.isValidTheme(self._app_theme):
                self.themeEngine.theme = self._app_theme
                self.themeEngine.refreshTheme()
            else:
                self._app_theme = self.themeEngine.theme
                self.compileStylesheet()
                self.themeEngine.refreshTheme()
        

