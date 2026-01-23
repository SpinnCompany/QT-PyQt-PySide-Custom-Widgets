import sys
import os
import traceback
import importlib.util
from qtpy.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QVBoxLayout, QHBoxLayout
from qtpy.QtGui import QPainter
from qtpy.QtCore import Property, Qt

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Utils import get_absolute_path, is_in_designer
from Custom_Widgets.Log import *

class QCustomComponentLoader(QWidget):
    """A custom widget to load and display a UI class defined in an external file."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = None

        # Initialize UI class and setup
        self.ui = None

        self._is_designer_mode = False
        self._designer_preview = False
        self._designer_initialized = False  # Track if designer mode has been initialized

        self._file_path = None
        self._form_class = None  # Add this to track the form class
        self._form_class_name = None  # Track form class name separately

        self.themeEngine = QCustomTheme()
        self.defaultTheme = self.themeEngine.theme
        self.defaultIconsColor = self.themeEngine.iconsColor
        self.themeEngine.onThemeChanged.connect(self.applyThemeIcons)

        self._applying_icon = False
        
        # Set up designer mode immediately if in designer
        if is_in_designer(self):
            self._setup_designer_mode()
        
        self.applyThemeIcons()

    def showEvent(self, event):
        """Handle the show event to ensure designer mode is set up when widget becomes visible."""
        super().showEvent(event)
        
        # Ensure designer mode is set up when widget is shown in Qt Designer
        if is_in_designer(self) and not self._designer_initialized and not self.previewComponent:
            self._setup_designer_mode()
        
        else:
            self.applyThemeIcons()

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
            logError(f"Error determining UI module name: {e}")
            logException(traceback.format_exc())

        try:
            if self._file_path:
                file_name = os.path.basename(self._file_path).split('.')[0][len("ui_"):]
                self.themeEngine.applyIcons(self.ui, ui_file_name=file_name)

            self.themeEngine.applyIcons(self.ui, ui_file_name=self.ui_module_name)
            self.currentTheme = self.themeEngine.theme

        except Exception as e:
            logError(f"Error loading theme icons for: {self} (Module: {self.ui_module_name})")
            logError(f"Error: {e}")
            logException(traceback.format_exc())  

        finally:
            self._applying_icon = False

    def loadComponent(self, formClass=None, formClassName=None, filePath=None):
        """Load the UI class based on the provided parameters."""
        # Always show designer label when in designer mode without preview
        if is_in_designer(self) and not self.previewComponent:
            self._update_designer_label()
            return

        # If in designer mode with preview but file path is invalid, show error label
        if is_in_designer(self) and self.previewComponent:
            if filePath and not os.path.isfile(get_absolute_path(filePath)):
                self._show_error_label(f"File not found: {filePath}")
                return
            elif formClassName and not self._form_class:
                self._show_error_label(f"Class not found: {formClassName}")
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
                self.ui.setupUi(self)
            except Exception as e:
                # maybe formclass has already been instantiated
                try:
                    self.ui = formClass  # Use the provided instance directly
                    self.ui.setupUi(self)
                except Exception as e:
                    logError(f"Error setting up UI: {e}")
                
                    if is_in_designer(self):
                        self._show_error_label(f"Error loading class: {e}")
                    return

        # If filePath is provided, handle accordingly
        elif filePath is not None:
            filePath = get_absolute_path(filePath)
            self._file_path = filePath
            
            # Check if file exists
            if not os.path.isfile(filePath):
                logError(f"File not found: {filePath}")
                if is_in_designer(self):
                    self._show_error_label(f"File not found: {os.path.basename(filePath)}")
                return
            
            if formClassName is not None:
                # Load the specific class
                self._form_class = self._import_class_from_file(filePath, formClassName)
            else:
                # Auto-detect the class name from the file path
                self._form_class = self._import_class_from_file(filePath)
            
            if self._form_class:
                try:
                    self.ui = self._form_class()  # Instantiate the class
                    self.ui.setupUi(self)
                except Exception as e:
                    logError(f"Error instantiating UI class: {e}")
                    if is_in_designer(self):
                        self._show_error_label(f"Error creating UI: {e}")
                    return
            else:
                logError("Failed to load the UI class from the specified file.")
                if is_in_designer(self):
                    self._show_error_label("No valid UI class found in file")
                return
        
        self.applyThemeIcons()
        
    def _refresh_component(self):
        self.loadComponent(formClassName=self._form_class_name, filePath=self._file_path)

    def _setup_designer_mode(self):
        """Set up the widget for Qt Designer mode."""
        if not is_in_designer(self):
            return

        self._is_designer_mode = True
        self._designer_initialized = True

        # Clear any existing layout and labels
        if self.layout() is not None:
            QWidget().setLayout(self.layout())  # Reset layout

        # Layout to hold the label (for Designer mode)
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)  # Set the layout for the widget

        # Create a label
        self.label = QLabel(self)
        self.label.setObjectName("main_label")
        self._update_designer_label()
        
        # Add label to the layout
        self._layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Optional: Set a border to indicate that it's in designer mode
        self.setStyleSheet("QWidget { border: 1px dotted red; } #main_label { border: none; background-color: rgba(0,0,0,.6); }")

    def _ensure_designer_label(self):
        """Ensure the designer label is created and visible."""
        if not is_in_designer(self) or self.previewComponent:
            return
            
        if not hasattr(self, 'label') or self.label is None or not self._designer_initialized:
            self._setup_designer_mode()
        else:
            self._update_designer_label()

    def _show_error_label(self, error_message):
        """Show an error label when component loading fails."""
        if not is_in_designer(self):
            return
            
        # Clear any existing layout and labels
        if self.layout() is not None:
            QWidget().setLayout(self.layout())  # Reset layout

        # Layout to hold the label
        layout = QVBoxLayout(self)
        
        # Create error label
        error_label = QLabel(self)
        error_label.setObjectName("error_label")
        error_label.setText(f"<b>Component Loader - Error</b><br>"
                           f"<font color='red'>{error_message}</font><br>"
                           f"<i>Check file path and class name</i>")
        error_label.setWordWrap(True)
        error_label.setAlignment(Qt.AlignCenter)
        
        # Add label to the layout
        layout.addWidget(error_label)
        
        # Set error styling
        self.setStyleSheet("QWidget { border: 1px dotted red; background-color: #ffeeee; } #error_label { border: none; background-color: rgba(0,0,0,.6)}")

    def _update_designer_label(self):
        """Update the designer label with current configuration."""
        if not hasattr(self, 'label') or not self.label:
            return
            
        # Prepare text for label based on class name and file path
        label_text = "<b>Component Loader / Container</b>"  # Default text
        
        has_config = False
        
        if self._form_class is not None:
            class_name = self._form_class.__name__
            label_text += f"<br><b>Class:</b> {class_name}"
            has_config = True

        if self._file_path:
            file_name = os.path.basename(self._file_path)
            label_text += f"<br><b>File:</b> {file_name}"
            has_config = True
            
        if self._form_class_name and not self._form_class:
            label_text += f"<br><b>Class Name:</b> {self._form_class_name}"
            has_config = True

        if not has_config:
            label_text += "<br><i>No Class or File Loaded</i>"
        else:
            # Add preview status
            preview_status = "Enabled" if self.previewComponent else "Disabled"
            label_text += f"<br><b>Preview:</b> {preview_status}"

        # Set the label text and styling
        self.label.setText(label_text)
        self.label.setWordWrap(True)

    def _import_class_from_file(self, file_path, class_name=None):
        """Dynamically import a class from a specified Python file."""
        # Ensure the file exists
        if not os.path.isfile(file_path):
            logError(f"The specified file does not exist: {file_path}")
            return None

        try:
            # Load the module from the file
            spec = importlib.util.spec_from_file_location("module.name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Automatically detect the class from the loaded module
            ui_classes = [cls for name, cls in module.__dict__.items() if isinstance(cls, type)]

            if class_name and class_name.strip():
                # If class_name is provided, attempt to find it
                ui_class = next((cls for cls in ui_classes if cls.__name__ == class_name), None)
                if ui_class.strip():
                    return ui_class
                else:
                    logError(f"No class named '{class_name}' found in the specified file.")
                    
            # If class_name is not provided, check for a class that follows naming conventions (e.g., starts with 'Ui_')
            ui_class = next((cls for cls in ui_classes if cls.__name__.startswith("Ui_")), None)

            if ui_class is None:
                logError("No valid UI class found in the specified file.")
                return None

            return ui_class
            
        except Exception as e:
            logError(f"Error importing from file {file_path}: {e}")
            return None

    @Property(str)
    def filePath(self):
        """Property to get or set the file path."""
        return self._file_path

    @filePath.setter
    def filePath(self, value: str):
        if self._file_path != value:
            self._file_path = value
            if is_in_designer(self):
                self._ensure_designer_label()
                # Auto-load if preview is enabled
                if self.previewComponent and value:
                    self.loadComponent(filePath=value)

    @Property(str)
    def formClassName(self):
        """Property to get or set the form class name."""
        return self._form_class_name

    @formClassName.setter
    def formClassName(self, value: str):
        if self._form_class_name != value:
            self._form_class_name = value
            if is_in_designer(self):
                self._ensure_designer_label()
                # Auto-load if preview is enabled and we have file path
                if self.previewComponent and self._file_path and value:
                    self.loadComponent(formClassName=value, filePath=self._file_path)

    @Property(bool)
    def previewComponent(self):
        """Property to get or set the preview mode."""
        return self._designer_preview

    @previewComponent.setter
    def previewComponent(self, value: bool):
        if self._designer_preview != value:
            self._designer_preview = value

            # Update the display based on the new preview state
            if is_in_designer(self):
                if value:
                    # Clear designer mode and try to load the component
                    self._is_designer_mode = False
                    self._designer_initialized = False
                    if self.layout() is not None:
                        QWidget().setLayout(self.layout())
                    # Try to load the component if we have the necessary info
                    if self._file_path:
                        if self._form_class_name:
                            self.loadComponent(formClassName=self._form_class_name, filePath=self._file_path)
                        else:
                            self.loadComponent(filePath=self._file_path)
                else:
                    # Switch back to designer mode
                    self._setup_designer_mode()
                    
                self._update_designer_label()

    def paintEvent(self, e):
        """Handle the paint event to customize the appearance of the widget."""
        super().paintEvent(e)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        # Ensure designer mode is set up if needed (fallback)
        if is_in_designer(self) and not self._designer_initialized and not self.previewComponent:
            self._setup_designer_mode()
        else:
            if self.defaultIconsColor != self.themeEngine.iconsColor:
                self.defaultIconsColor = self.themeEngine.iconsColor
                self.applyThemeIcons()
