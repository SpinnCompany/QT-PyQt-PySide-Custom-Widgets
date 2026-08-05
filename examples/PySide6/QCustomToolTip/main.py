"""QCustomQToolTip showcase — auto-positioned custom tooltips.

Four buttons carry plain Qt toolTips; the app-wide QCustomQToolTipFilter
replaces the native tooltip with the custom bubble (tail position auto).
All styling lives in json-styles/ + Qss/scss/defaultStyle.scss; this file
only boots the app and installs the filter.
"""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomQToolTip import QCustomQToolTipFilter
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtCore import QCoreApplication, QSettings
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
            # The Default-Theme flag is dropped by the loader whenever a stale
            # generic-scope THEME setting exists, so fall back to the first
            # app-defined (non-predefined) theme explicitly.
            for t in themeEngine.themes:
                if not getattr(t, "predefined", False):
                    s.setValue("THEME", t.name)
                    s.setValue("INIT-THEME-SET", True)
                    break
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Install the QCustomQToolTipFilter on the app to use the custom tooltip
    appToolTipFilter = QCustomQToolTipFilter(tailPosition="auto")
    app.installEventFilter(appToolTipFilter)
    window = MainWindow()
    sys.exit(app.exec())
