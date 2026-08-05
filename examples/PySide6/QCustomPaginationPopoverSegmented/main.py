########################################################################
## QCustomPagination + QCustomPopover + QCustomSegmentedControl example
##
## A segmented view switcher, a click-to-open popover, and pagination.
## Chrome comes from Qss/scss/defaultStyle.scss + json-styles/style.json
## (Pager-Dark default / Pager-Light). Run:
##     python main.py
########################################################################
import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomPopover import QCustomPopover
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication, QLabel


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Name the QSettings scope BEFORE loadJsonStyle: the theme loader
        # checks QSettings("THEME") while registering CustomThemes, and an
        # unnamed app reads a shared fallback file whose stale THEME key
        # strips the Default-Theme flag.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("Pagination Popover Segmented Demo")

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

        self._wireDemo()

    # ------------------------------------------------------------------ #
    ## Wiring + data seeding (no styling here — see Qss/scss)
    # ------------------------------------------------------------------ #
    def _wireDemo(self):
        ui = self.ui

        # segmented control
        ui.segmentedControl.setSegments(
            [("Day", "d"), ("Week", "w"), ("Month", "m"), ("Year", "y")])
        ui.segmentedControl.currentChanged.connect(
            lambda i: ui.statusLabel.setText(
                "View: %s" % ui.segmentedControl.currentData()))

        # popover attached to its trigger button
        self.pop = QCustomPopover.attach(ui.popoverTrigger, placement="bottom")
        self.pop.addWidget(QLabel("<b>Details</b>"))
        self.pop.addWidget(QLabel("Rich content lives in a popover,\n"
                                  "with an arrow to its anchor."))

        # pagination
        ui.pager.setPageCount(20)
        ui.pager.pageChanged.connect(
            lambda p: ui.statusLabel.setText("Page %d" % p))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
