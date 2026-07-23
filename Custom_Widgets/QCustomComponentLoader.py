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

try:
    from Custom_Widgets.Project import projectRoot
except Exception:  # pragma: no cover - defensive, projectRoot is optional here
    projectRoot = None


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

        # In-place hot reload: watch the loaded .py and rebuild just this
        # component's subtree when it changes (no app restart).
        self._hot_reload = True
        self._fs_watcher = None
        self._reload_timer = None

        self.themeEngine = QCustomTheme()
        self.defaultTheme = self.themeEngine.theme
        self.defaultIconsColor = self.themeEngine.iconsColor
        self.themeEngine.onThemeChanged.connect(self.applyThemeIcons)

        self._applying_icon = False
        
        # Set up designer mode immediately if in designer
        if is_in_designer(self):
            self._setup_designer_mode()
        
        self.applyThemeIcons()

    def _normalize_path(self, path):
        """Normalize file path to handle mixed separators and platform differences."""
        if not path:
            return path
        
        # Convert to string if needed
        path = str(path)
        
        # Replace backslashes with forward slashes for consistent processing
        normalized_path = path.replace('\\', '/')
        
        # Remove any duplicate slashes
        while '//' in normalized_path:
            normalized_path = normalized_path.replace('//', '/')
        
        # Get absolute path
        try:
            abs_path = get_absolute_path(normalized_path)
            # Normalize again after get_absolute_path
            if abs_path:
                abs_path = os.path.normpath(abs_path)
        except:
            abs_path = os.path.normpath(normalized_path)
        
        return abs_path

    def _resolve_ui_to_compiled(self, filePath):
        """Given a raw ``.ui`` path, locate the sibling compiled ``.py`` module.

        The loader only accepts compiled Python UI modules (a raw ``.ui`` cannot
        be loaded at runtime any more - see ``_loadComponentImpl``). Older forms
        and user projects may still point ``filePath`` at a ``.ui`` file, so
        rather than rejecting them outright we look for the ``ui_<stem>.py`` that
        ``Custom_Widgets --convert-ui`` would have produced (default output
        directory ``src/``). Returns the resolved ``.py`` path, or ``None`` when
        no compiled module can be found.
        """
        stem = os.path.splitext(os.path.basename(filePath))[0]
        ui_dir = os.path.dirname(filePath)

        candidates = [
            os.path.join(ui_dir, f"ui_{stem}.py"),  # compiled alongside the .ui
            os.path.join(ui_dir, f"{stem}.py"),
        ]
        # Default --convert-ui output is <src_output_dir>=src, relative to the
        # project root / cwd.
        roots = []
        if projectRoot is not None:
            try:
                roots.append(projectRoot())
            except Exception:
                pass
        roots.append(os.getcwd())
        for root in roots:
            if root:
                candidates.append(os.path.join(root, "src", f"ui_{stem}.py"))
        # A src/ sibling of the .ui's directory, e.g. ui/foo.ui -> src/ui_foo.py
        if ui_dir:
            candidates.append(
                os.path.join(os.path.dirname(ui_dir), "src", f"ui_{stem}.py"))

        seen = set()
        for cand in candidates:
            cand = os.path.normpath(cand)
            if cand in seen:
                continue
            seen.add(cand)
            if os.path.isfile(cand):
                return cand
        return None

    def _clear_layout(self):
        """Safely detach and delete the current layout and its child widgets.

        The old ``QWidget().setLayout(self.layout())`` idiom handed the layout
        (and every child widget under it) to a throwaway ``QWidget`` that was
        then garbage-collected, deleting the underlying C++ objects while
        Python still referenced them (e.g. ``self.label``). Re-touching those
        dangling wrappers is what produced the "Internal C++ object already
        deleted" errors and, ultimately, the Designer SIGSEGV.
        """
        layout = self.layout()
        if layout is not None:
            # Detach and schedule deletion of every child widget first, so the
            # throwaway-widget reparent below cannot take ownership of anything
            # we still hold a Python reference to. Recurse into NESTED layouts:
            # a component's real widgets live under nested layouts (e.g. cards
            # inside a row layout), and item.widget() is None for a layout item -
            # skipping those left the old widgets parented to self, rendering as
            # ghosts behind the reloaded component on every hot reload.
            self._delete_layout_items(layout)
            # Reparent the now-empty layout onto a throwaway widget to detach it
            # from self; it is deleted with that widget.
            QWidget().setLayout(layout)
        # Defensive sweep: delete any child widgets that were not under the
        # layout (e.g. widgets parented to self directly by setupUi).
        for child in self.findChildren(QWidget, options=Qt.FindDirectChildrenOnly):
            child.setParent(None)
            child.deleteLater()
        # Drop dangling Python references to child widgets that were just deleted.
        self.label = None
        self._layout = None

    def _delete_layout_items(self, layout):
        """Recursively take out and schedule deletion of every widget in
        ``layout`` and its nested sub-layouts."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
                continue
            child_layout = item.layout()
            if child_layout is not None:
                self._delete_layout_items(child_layout)

    def showEvent(self, event):
        """Handle the show event to ensure designer mode is set up when widget becomes visible."""
        
        # Ensure designer mode is set up when widget is shown in Qt Designer
        if is_in_designer(self) and not self._designer_initialized and not self.previewComponent:
            try:
                self._setup_designer_mode()
            except Exception as e:
                logError(f"Error setting up designer mode: {e}")
        
        else:
            self.applyThemeIcons()

        super().showEvent(event)

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
        """Load the UI class based on the provided parameters.

        This is a guarded wrapper: any unexpected error while loading a .py or
        .ui component is caught, logged and shown as an error label instead of
        propagating into Qt's C++ callchain (which would crash Designer)."""
        try:
            self._loadComponentImpl(formClass, formClassName, filePath)
        except Exception as e:
            logError(f"Component Loader - unexpected error loading component: {e}")
            logException(e)
            try:
                if is_in_designer(self):
                    self._show_error_label(f"Load failed: {e}")
            except Exception:
                pass

    def _loadComponentImpl(self, formClass=None, formClassName=None, filePath=None):
        """Load the UI class based on the provided parameters."""
        # Always show designer label when in designer mode without preview
        if is_in_designer(self) and not self.previewComponent:
            self._update_designer_label()
            return

        # Normalize the file path if provided
        if filePath:
            filePath = self._normalize_path(filePath)
            # Back-compat: forms may still point ``filePath`` at a raw .ui file.
            # The loader only accepts compiled .py modules, so transparently
            # resolve to the sibling ui_<stem>.py produced by --convert-ui.
            if filePath and filePath.lower().endswith(".ui"):
                resolved = self._resolve_ui_to_compiled(filePath)
                if resolved:
                    logInfo("Component Loader - resolved .ui to compiled "
                            f"module: {os.path.basename(filePath)} -> "
                            f"{os.path.basename(resolved)}")
                    filePath = resolved

        # If in designer mode with preview but file path is invalid, show error label
        if is_in_designer(self) and self.previewComponent:
            if filePath and not os.path.isfile(filePath):
                self._show_error_label(f"File not found: {os.path.basename(filePath)}")
                return
            elif formClassName and not self._form_class:
                self._show_error_label(f"Class not found: {formClassName}")
                return

        # Clear any existing UI, layout and labels
        self._clear_layout()

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
            # Store normalized path
            self._file_path = filePath
            
            # Check if file exists
            if not os.path.isfile(filePath):
                logError(f"Component Loader - File not found: {filePath}")
                if is_in_designer(self):
                    self._show_error_label(f"File not found: {os.path.basename(filePath)}")
                return

            # Compiled Python UI module ONLY. The loader accepts a .py file
            # that exposes a Ui_* class; raw .ui files are rejected (compile
            # them first with `Custom_Widgets --convert-ui`). Loading .ui at
            # runtime via QUiLoader was removed - it produced duplicate embeds
            # and a second-class, partially-themed widget tree. One predictable,
            # fully-themed path.
            if not filePath.lower().endswith(".py"):
                msg = (f"No compiled module for {os.path.basename(filePath)}. "
                       "Point filePath at the compiled .py (with a Ui_* class), "
                       "or compile the .ui with `Custom_Widgets --convert-ui` "
                       "(generates src/ui_<name>.py, which is auto-resolved).")
                logError(f"Component Loader - {msg}")
                if is_in_designer(self):
                    self._show_error_label(msg)
                return

            if formClassName is not None:
                self._form_class = self._import_class_from_file(filePath, formClassName)
            else:
                self._form_class = self._import_class_from_file(filePath)

            if not self._form_class:
                logError("Failed to load the UI class from the specified file.")
                if is_in_designer(self):
                    self._show_error_label("No valid Ui_ class found in file")
                return

            try:
                self.ui = self._form_class()  # Instantiate the class
                self.ui.setupUi(self)
            except Exception as e:
                logError(f"Error instantiating UI class: {e}")
                if is_in_designer(self):
                    self._show_error_label(f"Error creating UI: {e}")
                return

        self.applyThemeIcons()

        # Arm hot reload for a file-loaded component.
        if self._file_path:
            self._watchSource()

    def _refresh_component(self):
        self.loadComponent(formClassName=self._form_class_name, filePath=self._file_path)

    ####################################################################
    ## HOT RELOAD - rebuild this component's subtree in place when its
    ## compiled .py source changes (no app / Designer restart).
    ####################################################################
    def _watchSource(self):
        """Watch the loaded .py so edits hot-reload the component in place.

        We watch the compiled .py only (not the .ui): the file monitor /
        dev server regenerates the .py from the .ui on save, so reacting to
        the .py change avoids re-importing a stale module."""
        if not self._hot_reload or not self._file_path:
            return
        try:
            from qtpy.QtCore import QFileSystemWatcher
            if self._fs_watcher is None:
                self._fs_watcher = QFileSystemWatcher(self)
                self._fs_watcher.fileChanged.connect(self._onSourceChanged)
            # Reset to exactly the current source (paths can go stale across
            # reloads / renames).
            watched = self._fs_watcher.files()
            if watched:
                self._fs_watcher.removePaths(watched)
            if os.path.isfile(self._file_path):
                self._fs_watcher.addPath(self._file_path)
        except Exception as e:
            logDebug(f"Component Loader - hot reload watch setup failed: {e}")

    def _onSourceChanged(self, _path):
        # Editors (and the converter) save atomically - write a temp file then
        # rename - which fires one or more change signals and can momentarily
        # drop the watch. Debounce, then reload once things settle.
        try:
            from qtpy.QtCore import QTimer
            if self._reload_timer is None:
                self._reload_timer = QTimer(self)
                self._reload_timer.setSingleShot(True)
                self._reload_timer.timeout.connect(self._doHotReload)
            self._reload_timer.start(150)
        except Exception as e:
            logDebug(f"Component Loader - hot reload debounce failed: {e}")

    def _doHotReload(self):
        if not self._file_path or not os.path.isfile(self._file_path):
            # Source vanished mid-save; re-arm and wait for it to reappear.
            self._watchSource()
            return
        logInfo(f"Component Loader - hot reloading "
                f"{os.path.basename(self._file_path)}")
        # loadComponent clears the old subtree and rebuilds it, then re-arms
        # the watch (atomic saves drop it).
        self.loadComponent(formClassName=self._form_class_name,
                           filePath=self._file_path)

    def _setup_designer_mode(self):
        """Set up the widget for Qt Designer mode."""
        if not is_in_designer(self):
            return

        self._is_designer_mode = True
        self._designer_initialized = True

        # Clear any existing layout and labels
        self._clear_layout()

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
        self._clear_layout()

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
            
        try:
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

        except Exception as e:
            logError(f"Error updating designer label: {e}")

    def _import_class_from_file(self, file_path, class_name=None):
        """Dynamically import a class from a specified Python file."""
        # Normalize the file path first
        file_path = self._normalize_path(file_path)
        
        # Ensure the file exists
        if not os.path.isfile(file_path):
            logError(f"The specified file does not exist: {file_path}")
            return None

        # This loader imports a compiled Python UI module (a file exposing a
        # ``Ui_*`` class). A raw Qt Designer ``.ui`` XML file has no Python
        # loader, so guard against it explicitly rather than crashing on
        # ``spec.loader`` being None.
        if file_path.lower().endswith(".ui"):
            logError(
                "Component Loader expects a compiled Python UI file "
                "(with a Ui_* class), not a raw .ui XML file: "
                f"{os.path.basename(file_path)}. Compile it first, e.g. "
                "`pyside6-uic form.ui -o form.py`."
            )
            return None

        try:
            # Load the module under a UNIQUE, non-dotted name each call. A fixed
            # dotted name ("module.name") makes a second import of the same file
            # (i.e. every hot reload) resolve to an empty module, so the Ui_
            # class isn't found. A fresh name per (file, mtime) forces a clean
            # re-import on every change and never caches in sys.modules.
            try:
                stamp = int(os.path.getmtime(file_path))
            except OSError:
                stamp = 0
            mod_name = f"_cw_ui_{abs(hash(file_path)) & 0xffffffff}_{stamp}"
            spec = importlib.util.spec_from_file_location(mod_name, file_path)
            if spec is None or spec.loader is None:
                logError(f"Cannot import a Python module from file: {file_path}")
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Automatically detect the class from the loaded module
            ui_classes = [cls for name, cls in module.__dict__.items() if isinstance(cls, type)]

            if class_name and class_name.strip():
                # If class_name is provided, attempt to find it
                ui_class = next((cls for cls in ui_classes if cls.__name__ == class_name), None)
                if ui_class:
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
        # Normalize the incoming path
        if value:
            value = self._normalize_path(value)
        
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
    def hotReload(self):
        """When True (default), the component rebuilds itself in place whenever
        its compiled .py source changes - no app/Designer restart."""
        return self._hot_reload

    @hotReload.setter
    def hotReload(self, value: bool):
        self._hot_reload = bool(value)
        if self._hot_reload:
            self._watchSource()
        elif self._fs_watcher is not None:
            watched = self._fs_watcher.files()
            if watched:
                self._fs_watcher.removePaths(watched)

    @Property(bool)
    def previewComponent(self):
        """Property to get or set the preview mode."""
        return self._designer_preview

    @previewComponent.setter
    def previewComponent(self, value: bool):
        if self._designer_preview != value:
            self._designer_preview = value

            # Update the display based on the new preview state. Guarded: this
            # runs inside Designer's property-set callback, so an escaping
            # exception can crash the host.
            if is_in_designer(self):
                try:
                    if value:
                        # Clear designer mode and try to load the component
                        self._is_designer_mode = False
                        self._designer_initialized = False
                        self._clear_layout()
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
                except Exception as e:
                    logError(f"Component Loader - previewComponent update error: {e}")
                    logException(e)

    def paintEvent(self, e):
        """Handle the paint event to customize the appearance of the widget."""
        super().paintEvent(e)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        # Ensure designer mode is set up if needed (fallback). Guard everything:
        # a raise inside paintEvent bubbles into Qt's C++ paint dispatch and can
        # crash the host (Designer).
        try:
            if is_in_designer(self) and not self._designer_initialized and not self.previewComponent:
                self._setup_designer_mode()
            else:
                if self.defaultIconsColor != self.themeEngine.iconsColor:
                    self.defaultIconsColor = self.themeEngine.iconsColor
                    self.applyThemeIcons()
        except Exception as e:
            logError(f"Component Loader - paintEvent fallback error: {e}")