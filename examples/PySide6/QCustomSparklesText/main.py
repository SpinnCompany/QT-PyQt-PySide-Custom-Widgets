"""QCustomSparklesText showcase — text with a deterministic sparkle field.

Same seed, same render, so a screenshot is reproducible. The second banner's
sparkle hues come from the theme (Other-variables → SPARKLE_COLORS).
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
        QCoreApplication.setApplicationName("QCustomSparklesText Showcase")

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

        self._applyThemeColors()
        self._wire()

    def _applyThemeColors(self):
        # The second banner's sparkle hues are theme data (Other-variables),
        # applied through the widget's colorsCsv property so they flip with
        # the theme.
        colors = self.themeEngine.themeColor("SPARKLE_COLORS", "")
        if colors:
            self.ui.sparklesSecond.colorsCsv = colors

    def _wire(self):
        self.ui.countSpin.valueChanged.connect(self._setCount)
        self.ui.seedSpin.valueChanged.connect(
            lambda v: setattr(self.ui.sparklesMain, "seed", v))
        self.ui.animateBtn.clicked.connect(self._toggleAnimation)
        self.ui.themeBtn.clicked.connect(self._toggleTheme)
        self.themeEngine.onThemeChanged.connect(self._applyThemeColors)

    def _setCount(self, value):
        self.ui.sparklesMain.sparkleCount = value
        self.ui.sparklesSecond.sparkleCount = value

    def _toggleAnimation(self):
        for widget in (self.ui.sparklesMain, self.ui.sparklesSecond):
            widget.animated = not widget.animated

    def _toggleTheme(self):
        self.themeEngine.toggleTheme(dark="Sparkle Night", light="Sparkle Day")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
