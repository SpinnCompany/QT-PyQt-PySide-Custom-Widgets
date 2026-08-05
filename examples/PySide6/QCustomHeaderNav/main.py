"""QCustomHeaderNav showcase — a horizontal top nav. Narrow the window to
watch items collapse into a +N overflow rather than clipping off the edge."""

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
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Name the app BEFORE loadJsonStyle: theme parsing checks QSettings for
        # an existing THEME, and without these names QSettings resolves to the
        # shared "Unknown Organization/main.py.conf" — whose stale THEME would
        # cancel this app's Default-Theme flag on every first run.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomHeaderNav Example")

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

        self._wireControls()

    def _wireControls(self):
        nav = self.ui.headerNav
        status = self.ui.statusLabel
        nav.itemSelected.connect(lambda key: status.setText("selected %s" % key))
        nav.brandClicked.connect(lambda: status.setText("brand clicked"))
        nav.overflowClicked.connect(
            lambda: status.setText("overflow clicked (%d hidden)"
                                   % nav.hiddenCount()))
        self.ui.indicatorCombo.currentTextChanged.connect(
            lambda v: setattr(nav, "indicator", v))
        self.ui.alignCombo.currentTextChanged.connect(
            lambda v: setattr(nav, "alignment", v))
        self.ui.themeButton.clicked.connect(
            lambda: self.themeEngine.toggleTheme(dark="NavMidnight",
                                                 light="NavDaylight"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
