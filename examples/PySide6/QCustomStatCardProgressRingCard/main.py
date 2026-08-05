"""Stat cards / Progress rings / Card showcase — a tiny dashboard.

KPI stat cards, circular progress rings, and a card container wrapping the
rings. The rings animate up to their targets on launch.
"""

import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings, QTimer
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
        QCoreApplication.setApplicationName(
            "QCustomStatCardProgressRingCard Showcase")

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

    def _seedData(self):
        # Deltas carry the trend colouring (up = good, down = bad, flat =
        # muted); the delta TEXT is data, so it is seeded here.
        self.ui.statRevenue.setDelta("12.5%", "up")
        self.ui.statChurn.setDelta("0.4%", "down")
        self.ui.statSignups.setDelta("0%", "flat")

        # The card wraps the rings: move the Designer-authored holder into
        # the card's content area (QCustomCard.addWidget is its public API
        # for exactly this).
        self.ui.goalsCard.addWidget(self.ui.ringsHolder)

        # animate the rings filling up
        self._rings = [
            (self.ui.ringSales, 72),
            (self.ui.ringSupport, 45),
            (self.ui.ringMarketing, 90),
        ]
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)
        self._timer.start(20)

    def _advance(self):
        done = True
        for ring, target in self._rings:
            if ring.value() < target:
                ring.setValue(ring.value() + 1)
                done = False
        if done:
            self._timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
