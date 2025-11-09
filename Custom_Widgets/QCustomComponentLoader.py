import sys
import os
import traceback
import importlib.util
from qtpy.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QVBoxLayout
from qtpy.QtGui import QPainter
from qtpy.QtCore import Property, Qt

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Utils import get_absolute_path, is_in_designer

class QCustomComponentLoader(QWidget):
    """A custom widget to load and display a UI class defined in an external file."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self.setMinimumSize(0, 0)

        # Initialize UI class and setup
        self.ui = None

        self._is_designer_mode = False
        self._designer_preview = False

        self._file_path = None

        self.themeEngine = QCustomTheme()
        self.defaultTheme = self.themeEngine.theme
        self.defaultIconsColor = self.themeEngine.iconsColor
        self.themeEngine.onThemeChanged.connect(self.applyThemeIcons)

        self._applying_icon = False

    def applyThemeIcons(self):
        if self._applying_icon:
            return
        
        if self.ui is None:
            return
        
        self._applying_icon = True
        try:
            # Check the module name where ui is loaded from
            self.ui_module_name = self.ui.__module__.split('.')[-1]

            # Replace "ui_" with empty string only at the start
            if self.ui_module_name.startswith("ui_"):
                self.ui_module_name = self.ui_module_name[len("ui_"):]

        except Exception as e:
            self.ui_module_name = ""
            print(f"Error determining UI module name: {e}")
            print(traceback.format_exc())  # Prints the traceback for more context

        try:
            if self._file_path:
                file_name = os.path.basename(self._file_path).split('.')[0][len("ui_"):]
                self.themeEngine.applyIcons(self.ui, ui_file_name=file_name)

            self.themeEngine.applyIcons(self.ui, ui_file_name=self.ui_module_name)
            self.currentTheme = self.themeEngine.theme

        except Exception as e:
            print(f"Error loading theme icons for: {self} (Module: {self.ui_module_name})")
            print(f"Error: {e}")
            print(traceback.format_exc())  # Prints the traceback for more context

        finally:
            self._applying_icon = False


    def loadComponent(self, formClass=None, formClassName=None, filePath=None):
        """Load the UI class based on the provided parameters."""
        if is_in_designer(self) and not self.previewComponent:
            self._update_designer_label()
            return

        # Clear any existing UI
        if self.ui is not None:
            # Remove previous UI widgets and clear layout
            for i in reversed(range(self.layout().count())):
                widget_to_remove = self.layout().itemAt(i).widget()
                if widget_to_remove is not None:
                    widget_to_remove.setParent(None)  # Remove widget from layout

        # Clear any existing layout and labels
        if self.layout() is not None:
            QWidget().setLayout(self.layout())  # Reset layout

        self.themeEngine = QCustomTheme()
        self.defaultTheme = self.themeEngine.theme
        self.defaultIconsColor = self.themeEngine.iconsColor
        # If formClass is provided, use it directly
        if formClass is not None:
            self._form_class = formClass
            try:
                self.ui = self._form_class()  # Instantiate the class
            except:
                self.ui = self._form_class

            self.ui.setupUi(self)
            

        # If filePath is provided, handle accordingly
        elif filePath is not None:
            filePath = get_absolute_path(filePath)
            self._file_path = filePath
            
            if formClassName is not None:
                # Load the specific class
                self._form_class = self._import_class_from_file(filePath, formClassName)
            else:
                # Auto-detect the class name from the file path
                self._form_class = self._import_class_from_file(filePath)
            
            if self._form_class:
                self.ui = self._form_class()  # Instantiate the class
                self.ui.setupUi(self)

            else:
                print("Failed to load the UI class from the specified file.")

        self.applyThemeIcons()
        
    def _refresh_component(self):
        self.loadComponent(formClassName=self._form_class, filePath=self._file_path)

    def _setup_designer_mode(self):
        """Set up the widget for Qt Designer mode."""
        if not is_in_designer(self):
            return

        self._is_designer_mode = True

        # Clear any existing layout and labels
        if self.layout() is not None:
            QWidget().setLayout(self.layout())  # Reset layout

        # Layout to hold the label (for Designer mode)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)  # Set the layout for the widget

        # Create a label
        self.label = QLabel(self)

        self._update_designer_label()
        
        # Add label to the layout
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Optional: Set a border to indicate that it's in designer mode
        self.setStyleSheet("QWidget { border: 1px dotted red; padding: 10px; }QLabel{ border: none }")

    def _update_designer_label(self):
        # Prepare text for label based on class name and file path
        label_text = "<b>Component Loader / Container</b>"  # Default text
        
        if self._form_class is not None or self._file_path:
            # label_text += "<br><i>Details:</i><ul>"

            if self._form_class is not None:
                class_name = self._form_class.__name__
                label_text += f"<li><b>Class:</b> {class_name}</li>"

            if self._file_path:
                file_name = os.path.basename(self._file_path)
                label_text += f"<li><b>File:</b> {file_name}</li>"

            label_text += "</ul>"

        # If nothing is defined, just stick with the default text
        if not self._form_class and not self._file_path:
            label_text = "<b>Component Loader / Container</b><br><i>No Class or File Loaded</i>"

        # Set the label text and styling
        self.label.setText(label_text)
        self.label.setWordWrap(True)

    def _import_class_from_file(self, file_path, class_name=None):
        """Dynamically import a class from a specified Python file."""
        # Ensure the file exists
        if not os.path.isfile(file_path):
            print(f"The specified file does not exist: {file_path}")
            return None

        # Load the module from the file
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Automatically detect the class from the loaded module
        ui_classes = [cls for name, cls in module.__dict__.items() if isinstance(cls, type)]

        if class_name is not None:
            # If class_name is provided, attempt to find it
            ui_class = next((cls for cls in ui_classes if cls.__name__ == class_name), None)
            if ui_class:
                return ui_class
            else:
                print(f"No class named '{class_name}' found in the specified file.")
                
        # If class_name is not provided, check for a class that follows naming conventions (e.g., starts with 'Ui_')
        ui_class = next((cls for cls in ui_classes if cls.__name__.startswith("Ui_")), None)

        if ui_class is None:
            print("No valid UI class found in the specified file.")
            return None

        return ui_class

    @Property(bool)
    def previewComponent(self):
        """Property to get or set the form class name."""
        return self._designer_preview

    @previewComponent.setter
    def previewComponent(self, value: bool):
        if self._designer_preview != value:
            self._designer_preview = value

            self.previewComponent = value

    def paintEvent(self, e):
        """Handle the paint event to customize the appearance of the widget."""
        super().paintEvent(e)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        if is_in_designer(self) and not self._is_designer_mode and not self.previewComponent:
            self._setup_designer_mode()
        else:
            if self.defaultIconsColor != self.themeEngine.iconsColor:
                self.defaultIconsColor = self.themeEngine.iconsColor
                self.applyThemeIcons()

