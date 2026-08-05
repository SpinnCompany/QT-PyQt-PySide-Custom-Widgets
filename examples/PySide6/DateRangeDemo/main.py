"""QCustomDateRangePicker — live preview.

The inline dual-month travel-dates range picker (the reference), with live
Start/End readouts + a Save button. Full project structure: ui/ + compiled
src/ + json-styles themes + Qss scss tokens (zero inline styling).
"""

import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QDate, QSettings
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
        QCoreApplication.setApplicationName("DateRangeDemo")

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

        self._wirePicker()

    def _wirePicker(self):
        # seed the travel dates, then keep the Start/End readouts live
        self.ui.picker.setRange(QDate(2025, 6, 23), QDate(2025, 7, 9))
        self.ui.picker.rangeChanged.connect(self._onRange)
        self._onRange(self.ui.picker.startDate(), self.ui.picker.endDate())

    def _onRange(self, s, e):
        self.ui.startVal.setText(s.toString("dd.MM.yyyy") if s.isValid() else "—")
        self.ui.endVal.setText(e.toString("dd.MM.yyyy") if e.isValid() else "—")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
