########################################################################
## DESIGNER EXTENSIONS - appTheme dropdown for QCustomQMainWindow
##
## Goal: let designers pick QCustomQMainWindow.appTheme from a DROPDOWN of
## the theme names defined at runtime in the project's json-styles/style.json
## (built-in Light/Dark plus custom themes), instead of typing a string.
##
## Mechanism: a QDesignerTaskMenuExtension. Right-clicking the window in
## Qt Designer adds "Custom Properties..." to the context menu, which
## raises the selection-following Custom Properties dock (see
## DesignerTools.CustomPropertiesDock) - dropdowns for themes and widget
## references, pickers for colors - applied through the form cursor
## (undo-aware, marks the form dirty, saved to the .ui like any manual
## property edit). When the dock is unavailable the action falls back to
## a theme-only dropdown dialog.
##
## Why not an inline property-editor dropdown (property-sheet extension)?
## Empirically dead under PySide6 6.11:
##   * QExtensionManager.extension() returns Designer's default property
##     sheet as a bare QObject; the QDesignerPropertySheetExtension interface
##     cannot be recovered (shiboken returns the already-registered QObject
##     wrapper), so wrapping/delegation is impossible; and
##   * replacing the sheet with a complete QMetaObject-built Python sheet
##     segfaults Designer during form load (even when returning plain
##     strings) - its core requires the internal QDesignerPropertySheet.
## A native inline dropdown therefore needs a compiled C++ Designer plugin.
## appTheme stays a validated @Property(str) as the base representation.
##
## This module fails silently when the PySide6 Designer extension APIs are
## unavailable (e.g. under PyQt / PySide2).
########################################################################
import glob
import json
import os

from Custom_Widgets.Log import *

# Designer's IID for the task-menu extension (the string declared by
# Q_DECLARE_EXTENSION_INTERFACE in C++; PySide6 does not expose Q_TYPEID).
TASKMENU_IID = "org.qt-project.Qt.Designer.TaskMenu"

# Built-in theme names always offered, on top of whatever style.json defines.
_BUILTIN_THEMES = ["Light", "Dark"]


def _find_style_json(project_dir=None):
    """Locate the project's style.json under the Designer cwd / project dir.
    Designer runs with cwd = the folder the app was launched from
    (Custom_Widgets --start-designer), and QCustomTheme uses that same cwd."""
    project_dir = os.path.abspath(project_dir or os.getcwd())
    candidates = [
        os.path.join(project_dir, "json-styles", "style.json"),
        os.path.join(project_dir, "style.json"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # Fall back to a shallow search under the project dir.
    for depth in ("*/style.json", "*/*/style.json"):
        hits = glob.glob(os.path.join(project_dir, depth))
        # Skip virtualenvs / build dirs / hidden folders.
        hits = [h for h in hits
                if not any(part.startswith(".") or part in ("build", "dist")
                           for part in os.path.relpath(h, project_dir).split(os.sep))]
        if hits:
            return sorted(hits, key=len)[0]
    return None


def readThemeNames(project_dir=None):
    """Theme names for the appTheme dropdown: every
    ThemeSettings.CustomThemes[].Theme-name in the project's style.json,
    then the built-in Light/Dark. Re-read on every call, so themes added to
    style.json show up the next time the dropdown opens. Always returns at
    least the built-ins, so the dropdown is never empty."""
    names = []
    path = _find_style_json(project_dir)
    if path:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            custom = (data.get("QSettings", {})
                          .get("ThemeSettings", {})
                          .get("CustomThemes", []))
            for theme in custom:
                name = theme.get("Theme-name")
                if name and name not in names:
                    names.append(name)
        except Exception as e:
            logDebug(f"DesignerExtensions: failed to read themes from {path}: {e}")
    for builtin in _BUILTIN_THEMES:
        if builtin not in names:
            names.append(builtin)
    return names


def _make_task_menu_classes():
    """Build (factory, extension) classes, or None when the PySide6 Designer
    extension APIs are unavailable."""
    try:
        from PySide6.QtDesigner import (QDesignerFormWindowInterface,
                                        QExtensionFactory,
                                        QPyDesignerTaskMenuExtension)
        from PySide6.QtGui import QAction
        from PySide6.QtWidgets import QInputDialog
    except Exception:
        return None

    class AppThemeTaskMenu(QPyDesignerTaskMenuExtension):
        """Adds 'Custom Properties...' to the Designer context menu of a
        QCustomQMainWindow - raises the Custom Properties dock focused on
        the widget (falls back to a theme-only dropdown dialog when the
        dock is unavailable). Structure follows Qt's PySide6
        taskmenuextension example (tictactoe)."""

        def __init__(self, widget, parent=None):
            super().__init__(parent)
            self._widget = widget
            self._action = QAction("Custom Properties...", self)
            self._action.triggered.connect(self._openEditor)

        def taskActions(self):
            return [self._action]

        def preferredEditAction(self):
            # Not the double-click default: designers double-click the window
            # background while laying out, and a surprise modal would annoy.
            return None

        def _openEditor(self):
            try:
                from Custom_Widgets.DesignerTools import raiseCustomProperties
                if raiseCustomProperties(self._widget):
                    return
            except Exception as e:
                logDebug(f"DesignerExtensions: dock unavailable: {e}")
            self._chooseTheme()

        def _chooseTheme(self):
            try:
                names = readThemeNames()
                current = self._widget.property("appTheme") or ""
                index = names.index(current) if current in names else 0
                name, ok = QInputDialog.getItem(
                    self._widget.window(), "App Theme",
                    "Theme name (from style.json):", names, index, False)
                if not ok or not name:
                    return
                fw = QDesignerFormWindowInterface.findFormWindow(self._widget)
                if fw is not None:
                    # Through the form cursor: undo-aware, marks the form
                    # dirty, persisted to the .ui on save.
                    fw.cursor().setWidgetProperty(self._widget, "appTheme", name)
                else:
                    self._widget.setProperty("appTheme", name)
                logInfo(f"DesignerExtensions: appTheme set to '{name}'")
            except Exception as e:
                logException(e, message="DesignerExtensions: theme choice failed")

    class AppThemeTaskMenuFactory(QExtensionFactory):
        def createExtension(self, obj, iid, parent):
            if iid != TASKMENU_IID:
                return None
            try:
                if not obj.inherits("QCustomQMainWindow"):
                    return None
            except Exception:
                return None
            return AppThemeTaskMenu(obj, parent)

    return AppThemeTaskMenuFactory, AppThemeTaskMenu


_registered_factory = None


def registerDesignerExtensions(core):
    """Register the appTheme task-menu factory with the given Designer
    form-editor core. Called from the plugin registrars once the core has
    been captured (see DesignerBridge.addCoreListener). Fails silently if
    the extension APIs are unavailable."""
    global _registered_factory
    try:
        classes = _make_task_menu_classes()
        if classes is None:
            logDebug("DesignerExtensions: PySide6 Designer extension APIs "
                     "unavailable; appTheme task menu not installed")
            return False
        if core is None:
            logDebug("DesignerExtensions: no form-editor core; deferring")
            return False
        manager = core.extensionManager()
        if manager is None:
            logDebug("DesignerExtensions: core has no extension manager")
            return False
        AppThemeTaskMenuFactory, _ = classes
        factory = AppThemeTaskMenuFactory(manager)
        manager.registerExtensions(factory, TASKMENU_IID)
        _registered_factory = factory
        logInfo("DesignerExtensions: appTheme task-menu factory registered")
        return True
    except Exception as e:
        logException(e, message="DesignerExtensions: registration failed")
        return False
