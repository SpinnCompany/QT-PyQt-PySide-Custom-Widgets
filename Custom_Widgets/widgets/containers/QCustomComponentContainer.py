import sys
import os
import importlib.util
from PySide6.QtGui import QResizeEvent
from qtpy.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QVBoxLayout, QSizePolicy
from qtpy.QtGui import QPainter
from qtpy.QtCore import Property, Qt

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Utils import is_in_designer
from Custom_Widgets.QCustomComponentLoader import QCustomComponentLoader
from Custom_Widgets.Log import logError, logException
from Custom_Widgets._resources import packageDir

class QCustomComponentContainer(QWidget):
    """A custom widget to load and display a UI class defined in an external file."""

    script_dir = packageDir()
    WIDGET_ICON = os.path.join(script_dir, "components/icons/view_quilt.png")
    WIDGET_TOOLTIP = "A custom component loader for dynamic UI loading."
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class="QCustomComponentContainer" name="QCustomComponentContainer">
        </widget>
    </ui>
    """
    
    WIDGET_MODULE = "Custom_Widgets.QCustomComponentContainer"

    # Rich editors for the Designer "Custom Properties" dock (see
    # DesignerTools.CustomPropertiesDock).
    DESIGNER_CUSTOM_PROPS = [
        {"name": "filePath", "kind": "file",
         "filter": "Compiled Python UI (*.py);;All files (*)", "group": "Component"},
        {"name": "formClassName", "kind": "str", "group": "Component"},
        {"name": "previewComponent", "kind": "bool", "group": "Component"},
        {"name": "hotReload", "kind": "bool", "group": "Component"},
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = None

        # Initialize UI class and setup
        self._ui_class = None
        self._file_path = None
        self._form_class = None
        self.ui = None

        self._designer_preview = False
        self._is_designer_mode = False
        self._hot_reload = True
        self.form = QCustomComponentLoader()
    
    def showEvent(self, e):
        super().showEvent(e)
        # Use a single shot timer to avoid recursive layout issues
        if self._form_class and self._file_path and not hasattr(self, "component"):
            from qtpy.QtCore import QTimer
            QTimer.singleShot(0, self._refresh_component)

    def _refresh_component(self):
        """(Re)load the embedded component. Guarded end-to-end: this runs from
        Designer property-set callbacks, so an escaping exception would crash
        the host.

        A single QCustomComponentLoader is created once and reused across
        refreshes. Recreating it on every property change (the old behaviour)
        left each discarded loader's ``onThemeChanged`` connection dangling on
        a deleted C++ object; the next theme signal then fired into freed
        memory, crashing Qt Designer."""
        try:
            # Create the loader once and keep it; never tear it down mid-edit.
            if getattr(self, "form", None) is None:
                self.form = QCustomComponentLoader()

            # Ensure our own layout exists exactly once and hosts the loader.
            if self.layout() is None:
                self._layout = QVBoxLayout(self)
                self._layout.setContentsMargins(0, 0, 0, 0)
                self._layout.setSpacing(0)
                self.setLayout(self._layout)
            if self.form.parent() is not self:
                self.layout().addWidget(self.form)

            # Push the current config into the reused loader. The loader clears
            # and rebuilds its own content safely (see QCustomComponentLoader).
            self.form.hotReload = self._hot_reload
            self.form.previewComponent = self.previewComponent
            self.form.loadComponent(formClassName=self._form_class,
                                    filePath=self._file_path)

            try:
                # Back-compat aliases used by older example code.
                self.form.form = self.form.ui
                self.shownForm = self.form.ui
                self.component = self.form.ui
            except Exception:
                self.shownForm = None

            # A container is a pure composition shell — it must NEVER paint the
            # palette (a rounded/glass component otherwise shows dark squares
            # at its corners). Re-applied on every refresh so hot reloads can't
            # bring the background back. Explicit QSS backgrounds still paint.
            try:
                from qtpy.QtCore import Qt as _Qt
                from qtpy.QtWidgets import QWidget as _QW
                for w in (self, self.form):
                    w.setAutoFillBackground(False)
                    w.setAttribute(_Qt.WA_TranslucentBackground, True)
                for child in self.form.children():
                    if isinstance(child, _QW):
                        child.setAutoFillBackground(False)
                        child.setAttribute(_Qt.WA_TranslucentBackground, True)
            except Exception:
                pass
        except Exception as e:
            logError(f"QCustomComponentContainer: refresh failed: {e}")
            logException(e)

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

    @Property(bool)
    def hotReload(self):
        """When True (default), the embedded component rebuilds itself in place
        whenever its compiled .py source changes - no app/Designer restart."""
        return self._hot_reload

    @hotReload.setter
    def hotReload(self, value: bool):
        value = bool(value)
        if self._hot_reload != value:
            self._hot_reload = value
            if getattr(self, "form", None) is not None:
                self.form.hotReload = value

    def paintEvent(self, e):
        """Handle the paint event to customize the appearance of the widget."""
        super().paintEvent(e)
        try:
            opt = QStyleOption()
            opt.initFrom(self)
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        except Exception as ex:
            logError(f"QCustomComponentContainer: paintEvent error: {ex}")
    
    def resizeEvent(self, event: QResizeEvent) -> None:  
        # self.adjustSize()

        return super().resizeEvent(event)
    

