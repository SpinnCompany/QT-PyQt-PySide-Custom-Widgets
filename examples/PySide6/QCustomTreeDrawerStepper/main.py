"""QCustomTreeWidget + QCustomDrawer + QCustomStepper showcase.

A tree, a stepper with Back/Next, and a left drawer (opened by a button;
also opened once on launch so the overlay is visible immediately). All
styling lives in json-styles/ + Qss/scss/defaultStyle.scss; this file only
boots the app, seeds data and wires signals.
"""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomDrawer import QCustomDrawer
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtCore import QCoreApplication, QSettings, QTimer
from qtpy.QtWidgets import QApplication, QLabel


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
            # The Default-Theme flag is dropped by the loader whenever a stale
            # generic-scope THEME setting exists, so fall back to the first
            # app-defined (non-predefined) theme explicitly.
            for t in themeEngine.themes:
                if not getattr(t, "predefined", False):
                    s.setValue("THEME", t.name)
                    s.setValue("INIT-THEME-SET", True)
                    break
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._seedData()
        self._buildDrawer()
        self._wire()
        # Open the drawer once on launch so the overlay is visible without
        # a click.
        QTimer.singleShot(1500, self.openDrawer)

    def _seedData(self):
        self.ui.stepper.setSteps(["Account", "Profile", "Confirm", "Done"])
        self.ui.tree.setItems([
            {"text": "src", "expanded": True, "children": [
                {"text": "widgets", "children": ["button.py", "table.py"]},
                "main.py"]},
            {"text": "tests", "children": ["test_button.py"]},
        ])

    def _buildDrawer(self):
        self.drawer = QCustomDrawer(self, side="left", size=260)
        self.drawer.addWidget(QLabel("<b>Navigation</b>"))
        for name in ("Dashboard", "Projects", "Settings"):
            button = QCustomQPushButton(name)
            button.variant = "ghost"
            self.drawer.addWidget(button)
        self.drawer.contentLayout().addStretch(1)

    def _wire(self):
        self.ui.backBtn.clicked.connect(self.ui.stepper.previous)
        self.ui.nextBtn.clicked.connect(self.ui.stepper.next)
        self.ui.openDrawerBtn.clicked.connect(self.openDrawer)

    def openDrawer(self):
        self.drawer.open()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
