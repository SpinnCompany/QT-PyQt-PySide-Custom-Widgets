"""Switch / Number / Alert showcase — a settings-style panel.

Toggle switches, quantity / price steppers, and inline alerts of every
variant (info / success / warning / destructive).
"""

import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

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
        # QSettings while parsing CustomThemes, and without these names it
        # reads the shared unnamed settings file (polluted by other example
        # apps), which silently cancels this app's Default-Theme flag.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomSwitchNumberAlert Showcase")

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

        self._seedData()
        self._wire()

    def _seedData(self):
        # Stepper values / ranges are data, so they are seeded here.
        self.ui.qtyInput.setRange(1, 99)
        self.ui.qtyInput.setSingleStep(1)
        self.ui.qtyInput.setValue(3)

        self.ui.priceInput.setRange(0, 1000)
        self.ui.priceInput.setDecimals(2)
        self.ui.priceInput.setSingleStep(0.5)
        self.ui.priceInput.setValue(9.99)

    def _wire(self):
        self.ui.notifSwitch.toggled.connect(
            lambda on: self.ui.statusLabel.setText(
                "Enable notifications: %s" % ("on" if on else "off")))
        self.ui.darkSwitch.toggled.connect(
            lambda on: self.ui.statusLabel.setText(
                "Dark mode: %s" % ("on" if on else "off")))
        self.ui.qtyInput.valueChanged.connect(
            lambda v: self.ui.statusLabel.setText("Quantity: %s" % v))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
