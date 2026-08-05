"""QCustomDonut % callouts + hatch fills — live preview.

Shows the opt-in enhancements (segments mode): on-arc % pills + hatched slices
(the "Transfer history" reference), a variant with a cross hatch, and the classic
rings mode untouched (proof the enhancements default OFF). Full project
structure: ui/ + compiled src/ + json-styles themes + Qss scss tokens.
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

        # Point QSettings at THIS app BEFORE loadJsonStyle: the loader reads
        # QSettings while parsing CustomThemes, and without an identity it
        # lands on the shared "Unknown Organization/main.py" file whose stale
        # THEME strips our Default-Theme flag (wrong theme wins).
        QCoreApplication.setOrganizationName("Custom Widgets")
        QCoreApplication.setApplicationName("DonutEnhanceDemo")

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

        self._seedDonuts()

    def _seedDonuts(self):
        # Slice hues come from the ACTIVE theme's Other-variables — the same
        # values the scss uses for the legend dots, so they always match.
        color = self.themeEngine.themeColor

        # 1) Transfer history — % pills + hatched Pay/Other slices (the reference)
        self.ui.transferDonut.setData(
            [30, 23, 18, 17, 12],
            [color("DONUT_T%d" % i) for i in range(1, 6)])
        self.ui.transferDonut.setHatchIndices([3, 4])   # Pay-for-workplace + Other

        # 2) Storage — % pills + a cross-hatch on the Free slice
        self.ui.storageDonut.setData(
            [44, 26, 16, 14],
            [color("DONUT_S%d" % i) for i in range(1, 5)])
        self.ui.storageDonut.setHatchIndices([3])       # Free

        # 3) Classic rings mode — UNCHANGED (enhancements default OFF)
        self.ui.classicDonut.setData(
            [82, 55, 30],
            [color("DONUT_C%d" % i) for i in range(1, 4)])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
