"""QCustomGradientText showcase.

Gradient-filled headlines, optionally sliding. QSS cannot do this: there is
no text-fill gradient, so the text is painted. Full project structure: ui/ +
compiled src/ + json-styles themes + Qss scss tokens (zero inline styling).
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

THEME_DARK = "Headline Dark"
THEME_LIGHT = "Headline Light"


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
            # Prefer the json default; a stale THEME in the pre-boot QSettings
            # scope strips Default-Theme flags, so fall back to the first
            # custom (non-predefined) theme rather than silently keeping the
            # engine's built-in Light palette.
            chosen = None
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False):
                    chosen = t.name
                    break
            if chosen is None:
                for t in themeEngine.themes:
                    if not getattr(t, "predefined", False):
                        chosen = t.name
                        break
            if chosen is not None:
                s.setValue("THEME", chosen)
                s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._seedHeadlines()
        self._wire()

    def _headlines(self):
        return [self.ui.headlineBuild, self.ui.headlineShip,
                self.ui.headlineZero]

    def _seedHeadlines(self):
        """Demo data: the gradient stops for each headline."""
        stops = ("0:#2563eb,1:#a855f7",
                 "0:#f59e0b,0.5:#ef4444,1:#7c3aed",
                 "0:#0ea5e9,1:#065f46")
        for widget, csv in zip(self._headlines(), stops):
            widget.stopsCsv = csv

    def _wire(self):
        self.ui.angleSlider.valueChanged.connect(self._setAngle)
        self.ui.animateBtn.clicked.connect(self._toggleAnimation)
        self.ui.themeBtn.clicked.connect(
            lambda: self.themeEngine.toggleTheme(dark=THEME_DARK,
                                                 light=THEME_LIGHT))

    def _setAngle(self, value):
        for widget in self._headlines():
            widget.angle = value

    def _toggleAnimation(self):
        for widget in self._headlines():
            widget.animated = not widget.animated


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
