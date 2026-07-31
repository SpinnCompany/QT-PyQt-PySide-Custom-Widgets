from qtpy.QtWidgets import QWidget, QVBoxLayout, QStyle, QStyleOption
from qtpy.QtCore import Property, Qt
from qtpy.QtGui import QPaintEvent, QPainter, QIcon, QColor
import os

from Custom_Widgets.FileMonitor import QSsFileMonitor
from Custom_Widgets.JSonStyles import updateJson, loadJsonStyle
from Custom_Widgets.Log import logInfo, logError
from Custom_Widgets.Utils import SharedData, is_in_designer
from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets._resources import packageDir

class QCustomComponent(QWidget):
    # Icon path for the widget in Qt Designer
    script_dir = packageDir()
    WIDGET_ICON = os.path.join(script_dir, "components/icons/widgets.png")

    # Tooltip for the widget
    WIDGET_TOOLTIP = "A custom component container for nesting widgets."

    # XML string for Qt Designer integration
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class="QCustomComponent" name="CustomComponent">
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomComponent"

    # Rich editors for the Designer "Custom Properties" dock (see
    # DesignerTools.CustomPropertiesDock).
    DESIGNER_CUSTOM_PROPS = [
        {"name": "jsonStylesheetFilePath", "kind": "file",
         "filter": "JSON (*.json);;All files (*)", "group": "Stylesheet"},
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize file monitor and stylesheet options
        self._json_file = "json-styles/style.json"
        self.qss_watcher = None

        self.showCustomWidgetsLogs = True
        self.themeEngine = QCustomTheme()
        self.shared_data = SharedData()
        self._qss_file_monitor = QSsFileMonitor.instance()

        # Lightweight at design time: no main-window lookup, no file watcher,
        # no JSON loading in Qt Designer. Design-time live compile / painting is
        # handled by the Designer plugin (QSS Editor dock + 'Paint entire
        # Designer'), not per-widget. That runtime work happens below.
        if is_in_designer(self):
            self.win = None
        else:
            self.win = self.themeEngine.getMainWindow()
            self.startFileMonitor()

    # Property for the JSON stylesheet file path
    @Property(str)
    def jsonStylesheetFilePath(self):
        return self._json_file

    @jsonStylesheetFilePath.setter
    def jsonStylesheetFilePath(self, value: str = ""):
        self._json_file = value
        loadJsonStyle(self, self, jsonFiles={self._json_file})

    # Method to start the file monitor
    def startFileMonitor(self):
        try:
            if not self.qss_watcher:
                self._qss_file_monitor.start_qss_file_listener(self.themeEngine)
                logInfo("QSS file monitor started")
        except Exception as e:
            logError(f"Error starting QSS file monitor: {e}")
    
    # Add cleanup method
    def closeEvent(self, event):
        """Clean up file watchers when window is closed"""
        if hasattr(self, '_qss_file_monitor') and self._qss_file_monitor:
            try:
                self._qss_file_monitor.stop_qss_file_listener(self)
            except:
                pass
        super().closeEvent(event)

    # Alternative: use destructor
    def __del__(self):
        if hasattr(self, '_qss_file_monitor') and self._qss_file_monitor:
            try:
                self._qss_file_monitor.stop_qss_file_listener(self)
            except:
                pass

    def resizeEvent(self, e):
        super().resizeEvent(e)

        # Reloading the JSON style on every resize is only useful at runtime -
        # in Qt Designer it needlessly thrashes while resizing (design-time
        # painting is handled by the Designer plugin now).
        if self._json_file and not is_in_designer(self):
            loadJsonStyle(self, self, jsonFiles={self._json_file})

    # Paint event for applying QSS
    def paintEvent(self, event: QPaintEvent):
        """Apply the stylesheet during paint events."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        super().paintEvent(event)

