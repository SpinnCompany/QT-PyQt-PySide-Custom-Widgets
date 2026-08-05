"""QCustomDateEdit / QCustomTimeEdit / QCustomDateRangeEdit example.

Date field with a calendar popup, a time field, and a start/end range picker
that keeps end >= start. All chrome comes from Qss/scss + json-styles."""

import os, sys

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
            # A stray QSettings file (written before QApplication got its real
            # names) strips every theme's default flag — seed explicitly.
            s.setValue("THEME", "Midnight")
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._wire()

    def _wire(self):
        ui = self.ui
        # Seed the range (data, so set in code after load)
        ui.rangeEdit.setDateRange(QDate.currentDate(),
                                  QDate.currentDate().addDays(7))
        ui.dateEdit.dateChanged.connect(
            lambda d: ui.resultLabel.setText("Date: %s" % d.toString("yyyy-MM-dd")))
        ui.rangeEdit.rangeChanged.connect(
            lambda s, e: ui.resultLabel.setText(
                "Range: %s -> %s" % (s.toString("MMM d"), e.toString("MMM d"))))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
