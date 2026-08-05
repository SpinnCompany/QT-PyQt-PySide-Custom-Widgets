"""QCustomCodeEditor showcase — two editors (live Python pane + a loaded C++
file) with the widget's six named syntax themes switchable from the button row."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from functools import partial

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the app identity BEFORE loadJsonStyle: the theme loader consults
        # QSettings while parsing CustomThemes, and without these names it reads
        # the shared unnamed settings file (polluted by other example apps),
        # which silently cancels this app's Default-Theme flag.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomCodeEditor Showcase")

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
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._seedAndWire()

    def _seedAndWire(self):
        ui = self.ui

        # first editor: an empty, live Python pane
        ui.editor1.setTheme("default")
        ui.editor1.setLang("python")

        # second editor: a C++ file loaded from disk
        ui.editor2.setTheme("default")
        ui.editor2.loadFile(os.path.join(os.path.dirname(__file__), "hello.cpp"))

        # editor syntax-theme switcher (the widget's own named themes)
        buttons = {
            ui.themeDefaultButton: "default",
            ui.themeOneLightButton: "one-light",
            ui.themeOneDarkButton: "one-dark",
            ui.themeMonokaiButton: "monokai",
            ui.themeOceanicButton: "oceanic",
            ui.themeZenburnButton: "zenburn",
        }
        for button, themeName in buttons.items():
            button.clicked.connect(partial(self.applyEditorTheme, themeName))

    def applyEditorTheme(self, themeName):
        self.ui.editor1.setTheme(themeName)
        self.ui.editor2.setTheme(themeName)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
