"""Prism Showcase — the colourful display widgets in one window.

QCustomGradientText, QCustomSparklesText, QCustomRainbowButton and a
QCustomProgressRing + QCustomNumberCounter pair driven by a slider.
"""

import os, sys

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
        # Set BEFORE loadJsonStyle: the theme engine reads QSettings() while
        # parsing the json — without these names it reads the interpreter-wide
        # settings file and the app's own THEME/default theme never resolve.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("PrismShowcase")

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
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._launches = 0
        self._wireDemo()

    def _wireDemo(self):
        ui = self.ui
        # Seed the ring/counter pair, then let the slider drive both.
        ui.driveSlider.valueChanged.connect(self._onSliderMoved)
        self._onSliderMoved(ui.driveSlider.value())

        ui.rainbowButton.clicked.connect(self._onLaunch)
        ui.sparklesText.clicked.connect(self._reseedSparkles)
        ui.themeButton.clicked.connect(self._toggleTheme)

    def _onSliderMoved(self, value):
        self.ui.progressRing.setValue(value)
        self.ui.numberCounter.setValue(value)

    def _onLaunch(self):
        self._launches += 1
        noun = "time" if self._launches == 1 else "times"
        self.ui.launchLabel.setText("Launched %d %s" % (self._launches, noun))

    def _reseedSparkles(self):
        self.ui.sparklesText.seed = self.ui.sparklesText.seed + 1

    def _toggleTheme(self):
        current = str(getattr(self.themeEngine, "theme", "") or "")
        target = "Prism-Day" if current == "Prism-Night" else "Prism-Night"
        self.themeEngine.setTheme(target)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
