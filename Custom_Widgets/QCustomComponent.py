from qtpy.QtWidgets import QWidget, QVBoxLayout, QStyle, QStyleOption
from qtpy.QtCore import Property, Qt
from qtpy.QtGui import QPaintEvent, QPainter, QIcon, QColor
import os

from Custom_Widgets.FileMonitor import QSsFileMonitor
from Custom_Widgets.JSonStyles import updateJson, loadJsonStyle
from Custom_Widgets.Log import logInfo, logError
from Custom_Widgets.Utils import SharedData, is_in_designer
from Custom_Widgets.QAppSettings import QAppSettings as QCustomAppSettings
from Custom_Widgets.QCustomTheme import QCustomTheme

class Object(object):
    pass

class QCustomComponent(QWidget):
    # Icon path for the widget in Qt Designer
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/container.png")

    # Tooltip for the widget
    WIDGET_TOOLTIP = "A custom component container for nesting widgets."

    # XML string for Qt Designer integration
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class="QCustomComponent" name="CustomComponentContainer">
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomComponent"

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize file monitor and stylesheet options
        self._json_file = "json-styles/style.json"
        self.liveCompileQss = False
        self._paint_qt_designer = False
        self.qss_watcher = None

        self.showCustomWidgetsLogs = True
        self.themeEngine = QCustomTheme()   
        self.win = self.themeEngine.getMainWindow()  
        self.shared_data = SharedData()

        # Start the file monitor
        self.startFileMonitor()

    # Property for the JSON stylesheet file path
    @Property(str)
    def jsonStylesheetFilePath(self):
        return self._json_file

    @jsonStylesheetFilePath.setter
    def jsonStylesheetFilePath(self, value: str = ""):
        self._json_file = value
        loadJsonStyle(self, self, jsonFiles={self._json_file})
        self.compileStylesheet()

    # Property for enabling or disabling live compilation of the stylesheet
    @Property(bool)
    def liveCompileStylesheet(self):
        return self.liveCompileQss

    @liveCompileStylesheet.setter
    def liveCompileStylesheet(self, value: bool):
        self.liveCompileQss = value
        self.compileStylesheet()

    @Property(bool)
    def paintQtDesignerUI(self):
        return self._paint_qt_designer
    
    @paintQtDesignerUI.setter
    def paintQtDesignerUI(self, value):
        self._paint_qt_designer = value

        self.compileStylesheet()

    # Method to compile the stylesheet
    def compileStylesheet(self):
        if self.liveCompileQss and self._json_file:
            QCustomAppSettings.updateAppSettings(self, generateIcons = False, reloadJson = False, paintEntireApp = self._paint_qt_designer, QtDesignerMode = True)
            if not self.qss_watcher:
                self.startFileMonitor()
   

    # Method to start the file monitor
    def startFileMonitor(self):
        try:
            if not self.qss_watcher:
                QSsFileMonitor.start_qss_file_listener(self)
                logInfo("QSS file monitor started")
        except Exception as e:
            logError(f"Error starting QSS file monitor: {e}")

    def showEvent(self, e):
        # self.adjustSize()
        super().showEvent(e)
        # self.update()

    def resizeEvent(self, e):
        # self.adjustSize()
        super().resizeEvent(e)

        if self._json_file:
            loadJsonStyle(self, self, jsonFiles={self._json_file})

    # Paint event for applying QSS
    def paintEvent(self, event: QPaintEvent):
        """Apply the stylesheet during paint events."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        super().paintEvent(event)

