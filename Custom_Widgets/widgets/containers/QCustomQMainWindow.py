from qtpy.QtWidgets import QMainWindow, QPushButton, QWidget, QFrame, QStyle, QStyleOption, QVBoxLayout
from qtpy.QtCore import Property, Qt, QEvent
from qtpy.QtGui import QIcon, QPaintEvent, QPainter, QColor, QResizeEvent

from Custom_Widgets.JSonStyles import updateJson
from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.FileMonitor import QSsFileMonitor
from Custom_Widgets.Utils import is_in_designer, SharedData
from Custom_Widgets.Log import *
from Custom_Widgets import *

import os
from Custom_Widgets._resources import packageDir

class QCustomQMainWindow(QMainWindow):
    # Icon path for the widget
    script_dir = packageDir()
    WIDGET_ICON = os.path.join(script_dir, "components/icons/dashboard.png")
    
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

    # Rich editors for the Designer "Custom Properties" dock (see
    # DesignerTools.CustomPropertiesDock). Kinds: theme (dropdown of
    # style.json theme names), widget-ref (dropdown of matching widgets in
    # the open form, filtered by `types`), bool / int / str / color.
    # Properties stay visible in the native property editor too - the dock
    # is the friendly editor on top, not a replacement.
    DESIGNER_CUSTOM_PROPS = [
        {"name": "appTheme", "kind": "theme", "group": "Theme"},
        {"name": "jsonStylesheetFilePath", "kind": "str", "group": "Stylesheet"},
        {"name": "frameless", "kind": "bool", "group": "Window"},
        {"name": "translucentBg", "kind": "bool", "group": "Window"},
        {"name": "windowBorderRadius", "kind": "int", "group": "Window"},
        {"name": "sizeGrip", "kind": "widget-ref",
         "types": ("QWidget",), "group": "Window"},
        {"name": "minimizeBtn", "kind": "widget-ref",
         "types": ("QPushButton", "QToolButton"), "group": "Navigation"},
        {"name": "closeBtn", "kind": "widget-ref",
         "types": ("QPushButton", "QToolButton"), "group": "Navigation"},
        {"name": "restoreBtn", "kind": "widget-ref",
         "types": ("QPushButton", "QToolButton"), "group": "Navigation"},
        {"name": "titleBar", "kind": "widget-ref",
         "types": ("QWidget", "QFrame"), "group": "Navigation"},
        {"name": "moveWindow", "kind": "widget-ref",
         "types": ("QWidget", "QFrame"), "group": "Navigation"},
        {"name": "shadowColor", "kind": "color", "group": "Shadow"},
        {"name": "shadowBlurRadius", "kind": "int", "group": "Shadow"},
        {"name": "shadowXOffset", "kind": "int", "group": "Shadow"},
        {"name": "shadowYOffset", "kind": "int", "group": "Shadow"},
        {"name": "customSideDrawers", "kind": "str", "group": "Drawers"},
    ]

    def __init__(self, parent=None, frameless: bool = False, translucentBg: bool = False, minimizeBtn: QPushButton = None, closeBtn: QPushButton = None, restoreBtn: QPushButton = None,
                restoreBtnNormalIcon: QIcon = None, restoreBtnMaximizedIcon: QIcon = None, titleBar: QWidget | QFrame = None, moveWindow: QWidget | QFrame = None, sizeGrip: QWidget | QFrame = None):
        super().__init__(parent)

        self._frameless = frameless
        self._translucent_bg = translucentBg
        self._minimize_btn = minimizeBtn
        self._close_btn = closeBtn
        self._restore_btn = restoreBtn
        self._restore_btn_normal_icon = restoreBtnNormalIcon
        self._restore_btn_maximized_icon = restoreBtnMaximizedIcon
        self._title_bar = titleBar
        self._move_window = moveWindow
        self._size_grip = sizeGrip
        self._designer_prev = True
        self._json_file = "json-styles/style.json"
        self._shadow_color = QColor("")
        self._title = ""
        self._shadow_blur = 0
        self._shadow_x_offset = 0
        self._shadow_y_offset = 0
        self._custom_side_drawers = ""
        
        self.themeEngine = QCustomTheme(self)
        self.shared_data = SharedData()

        self._app_theme = self.themeEngine.theme
        self._window_radius = 0

        self.showCustomWidgetsLogs = True  
        self.checkForMissingicons = True 

        self._qss_file_monitor = QSsFileMonitor.instance()

        loadJsonStyle(
            self,
            jsonFiles={
                self._json_file
            }
        )

    @Property(str)
    def appTheme(self):
        """The active theme, by NAME. Theme names are defined at runtime in
        the project's style.json (built-in "Light"/"Dark" plus any custom
        themes), so this is a string rather than a fixed enum - a static
        enum cannot list values that only exist once style.json is read.
        In Qt Designer, use the "Custom Properties" dock (right-click the
        window -> Custom Properties...) for a dropdown of the current
        style.json themes; an inline property-editor dropdown is not
        reachable from Python (PySide6 6.11 property-sheet extensions can
        neither wrap nor replace Designer's default sheet - see
        DesignerExtensions.py). Use the QCustomThemeList widget for a
        runtime theme dropdown in the app itself.
        The value is validated against the currently-defined themes."""
        return self._app_theme

    @appTheme.setter
    def appTheme(self, value: str):
        if self._app_theme != value and self.isValidTheme(value):
            self._app_theme = value
            self.themeEngine.setTheme(value)

    def isValidTheme(self, value: str):
        """Whether `value` names one of the themes the engine knows about.

        Reads the engine's list, not `self.themes`: this window has no such
        attribute, so the original lookup raised AttributeError on every call
        and the broad `except` below turned that into "invalid theme" — which
        made appTheme silently unsettable. The except is kept narrow now so a
        real failure surfaces instead of being read as a rejected theme.
        """
        try:
            themes = self.themeEngine.themes
        except AttributeError:
            return False
        for theme in themes or []:
            if getattr(theme, "name", None) == value:
                return True
        return False

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

    # Add cleanup method
    def closeEvent(self, event):
        """Clean up file watchers when window is closed"""
        if hasattr(self, '_qss_file_monitor') and self._qss_file_monitor:
            try:
                self._qss_file_monitor.stop_qss_file_listener()
            except Exception:
                pass
        super().closeEvent(event)

    # Alternative: use destructor
    def __del__(self):
        if hasattr(self, '_qss_file_monitor') and self._qss_file_monitor:
            try:
                self._qss_file_monitor.stop_qss_file_listener()
            except Exception:
                pass

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
            "QMainWindow.translucentBg",
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
            "QMainWindow.navigation.titleBar",
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

    @Property(str)
    def customSideDrawers(self):
        return self._custom_side_drawers

    @customSideDrawers.setter
    def customSideDrawers(self, value: str):        
        if self._custom_side_drawers != value:
            self._custom_side_drawers = value

            updateJson(
                self._json_file,
                "QMainWindow.customSideDrawers",
                value,
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
                self.themeEngine.refreshTheme()
        

