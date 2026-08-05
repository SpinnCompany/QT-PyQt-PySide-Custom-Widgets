"""QCustomCompass — live preview.

A heading rose (needle rotates), an aircraft-style rotating-card compass, a
compact map-corner compass and the premium beveled instrument dial. The top-left
rose drifts its heading so you can watch it ease; drag any of them to set the
heading. Full project structure: ui/ + compiled src/ + json-styles themes +
Qss scss tokens (zero inline styling).
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

        # Point QSettings at THIS app BEFORE loadJsonStyle: the loader reads
        # QSettings while parsing CustomThemes, and without an identity it
        # lands on the shared "Unknown Organization/main.py" file whose stale
        # THEME strips our Default-Theme flag (wrong theme wins).
        QCoreApplication.setOrganizationName("Custom Widgets")
        QCoreApplication.setApplicationName("CompassDemo")

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

        self._startDrift()

    def _startDrift(self):
        # drift the heading rose (and the dial, offset 90°) so the ease
        # animation is visible
        self._steps = [30, 75, 130, 210, 300, 350, 20, 315]
        self._i = 0
        self._drift = QTimer(self)
        self._drift.setInterval(2200)
        self._drift.timeout.connect(self._next)
        self._drift.start()

    def _next(self):
        h = self._steps[self._i % len(self._steps)]
        self.ui.roseCompass.setHeading(h)
        self.ui.dialCompass.setHeading((h + 90) % 360)
        self._i += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
