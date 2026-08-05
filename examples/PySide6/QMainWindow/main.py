"""QCustomQMainWindow starter — a minimal frameless window with a custom
title bar.

Everything window-related (frameless flag, translucent background, drop
shadow, minimize / restore / close buttons, drag-to-move title bar and the
size grip) is declared under the "QMainWindow" key of
json-styles/style.json; the look lives in Qss/scss/defaultStyle.scss.
"""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtCore import QCoreApplication, QDir, QSettings
from qtpy.QtWidgets import QApplication

# Register the themed-icon search path BEFORE setupUi runs: the compiled ui
# references icons as "theme-icons:icons/..." and a QIcon/QPixmap created
# before the search path exists stays null forever.
QDir.addSearchPath("theme-icons",
                   os.path.join(os.path.dirname(os.path.abspath(__file__)), "Qss", "icons"))


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the QSettings identity BEFORE loadJsonStyle: while the json is
        # parsed the engine consults QSettings(), and without these names it
        # falls back to "Unknown Organization/main.py.conf" whose stale THEME
        # key strips the Default-Theme flag from the json themes.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomQMainWindow Starter")

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()
        themeEngine = self.themeEngine
        s = QSettings()
        init_set = s.value("INIT-THEME-SET")
        if s.value("THEME") is None or not init_set:
            default = None
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False):
                    default = t.name
                    break
            if default is None:
                # Fall back to the first custom (non-predefined) theme
                for t in themeEngine.themes:
                    if not getattr(t, "predefined", False):
                        default = t.name
                        break
            if default:
                s.setValue("THEME", default)
                s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
