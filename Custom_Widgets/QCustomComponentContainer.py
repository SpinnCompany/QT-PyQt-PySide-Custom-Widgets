import sys
import os
import importlib.util
from qtpy.QtWidgets import QApplication, QMainWindow, QWidget, QStyleOption, QStyle, QLabel, QVBoxLayout, QSizePolicy
from qtpy.QtGui import QPainter
from qtpy.QtCore import Property, Qt

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Utils import is_in_designer
from Custom_Widgets.QCustomComponentLoader import QCustomComponentLoader

class QCustomComponentContainer(QWidget):
    """A custom widget to load and display a UI class defined in an external file."""

    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/loader.png")
    WIDGET_TOOLTIP = "A custom component loader for dynamic UI loading."
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class="QCustomComponentContainer" name="CustomComponentLoader">
        </widget>
    </ui>
    """
    
    WIDGET_MODULE = "Custom_Widgets.QCustomComponentContainer"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        # self.setMinimumSize(0, 0)

        # Initialize UI class and setup
        self._ui_class = None
        self._file_path = None
        self._form_class = None
        self.ui = None

        self._designer_preview = False

        self._is_designer_mode = False

        self.form = QCustomComponentLoader()
    
    def showEvent(self, e):
        super().showEvent(e)
        # Use a single shot timer to avoid recursive layout issues
        if self._form_class and self._file_path and not hasattr(self, "component"):
            from qtpy.QtCore import QTimer
            QTimer.singleShot(0, self._refresh_component)

    def _refresh_component(self):
        # Clear any existing layout and labels
        if self.layout() is not None:
            QWidget().setLayout(self.layout())  # Reset layout
        
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        # self.setMinimumSize(0, 0)
        
        self.form = QCustomComponentLoader()
        self.form.previewComponent = self.previewComponent
        self.form.loadComponent(formClassName=self._form_class, filePath=self._file_path)

        self.layout().addWidget(self.form) 
        # self.setMinimumSize(self.form.sizeHint())

        try:
            #older versions
            self.form.form =  self.form.ui 
            self.shownForm =  self.form.ui  

            # for components
            self.component =  self.form.ui

        except:
            self.shownForm = None

    @Property(str)
    def filePath(self):
        """Property to get or set the file path of the UI class."""
        return self._file_path

    @filePath.setter
    def filePath(self, value: str):
        if self._file_path != value:
            self._file_path = os.path.normpath(value)

            self._refresh_component()

    @Property(str)
    def formClassName(self):
        """Property to get or set the form class name."""
        return self._form_class.__name__ if self._form_class else ""

    @formClassName.setter
    def formClassName(self, value: str):
        if self._form_class != value:
            self._form_class = value

            self._refresh_component()

    @Property(bool)
    def previewComponent(self):
        """Property to get or set the form class name."""
        return self._designer_preview

    @previewComponent.setter
    def previewComponent(self, value: bool):
        if self._designer_preview != value:
            self._designer_preview = value

            self._refresh_component()

    def paintEvent(self, e):
        """Handle the paint event to customize the appearance of the widget."""
        super().paintEvent(e)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

