"""QCustomCommandPalette example — press Ctrl+K (Cmd+K on macOS).

A fuzzy-searchable command launcher overlay. Type to filter, arrows to
navigate, Enter to run, Esc to close. The palette opens once at startup so
the demo is visible immediately.
"""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomCommandPalette import QCustomCommandPalette
from Custom_Widgets.QCustomToast import QCustomToast
from qtpy.QtCore import QCoreApplication, QSettings, QTimer
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()
        themeEngine = self.themeEngine
        org = getattr(themeEngine, "organizationName", "")
        if org:
            QCoreApplication.setOrganizationName(str(org))
        appn = getattr(themeEngine, "applicationName", "")
        if appn:
            QCoreApplication.setApplicationName(str(appn))
        orgd = getattr(themeEngine, "organizationDomain", "")
        if orgd:
            QCoreApplication.setOrganizationDomain(str(orgd))
        s = QSettings()
        init_set = s.value("INIT-THEME-SET")
        if s.value("THEME") is None or not init_set:
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False) and (init_set is None or not init_set):
                    s.setValue("THEME", t.name)
                    s.setValue("INIT-THEME-SET", True)
        if s.value("THEME") is None:
            # A stray QSettings file (e.g. "Unknown Organization/main.py.conf",
            # written before QApplication got its real names) strips every
            # theme's default flag inside loadJsonStyle — seed explicitly.
            s.setValue("THEME", "Onyx")
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._wire_palette()

    def _wire_palette(self):
        # The palette is a popup-style CHILD OVERLAY (it fills its parent
        # window when opened), so it cannot live in a .ui layout — it is
        # created in code and bound to Ctrl+K, exactly like production use.
        self.commandPalette = QCustomCommandPalette.installShortcut(self, "Ctrl+K", commands=[
            {"id": "new", "title": "New File", "shortcut": "Ctrl+N",
             "callback": lambda: QCustomToast.success(self, "New file created")},
            {"id": "save", "title": "Save File", "shortcut": "Ctrl+S",
             "callback": lambda: QCustomToast.success(self, "Saved")},
            {"id": "open", "title": "Open Folder", "subtitle": "Browse for a folder",
             "callback": lambda: QCustomToast.info(self, "Open folder")},
            {"id": "theme", "title": "Toggle Dark Theme",
             "callback": lambda: QCustomToast.info(self, "Theme toggled")},
            {"id": "close", "title": "Close Window", "shortcut": "Ctrl+W",
             "callback": lambda: QCustomToast.warning(self, "Close requested")},
        ])
        # Open once at startup so the palette is immediately visible.
        QTimer.singleShot(400, self.commandPalette.open)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
