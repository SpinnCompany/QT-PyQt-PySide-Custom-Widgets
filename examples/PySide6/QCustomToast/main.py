"""QCustomToast showcase — stacked notifications.

Buttons trigger each toast type; toasts stack in the chosen corner and
reflow as they auto-dismiss. One info toast fires on launch so a toast is
visible immediately. All styling lives in json-styles/ +
Qss/scss/defaultStyle.scss; this file only boots the app and wires signals.
"""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomToast import QCustomToast
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtCore import QCoreApplication, QSettings, QTimer
from qtpy.QtWidgets import QApplication

MESSAGES = {
    "success": "Your changes were saved.",
    "error": "Something went wrong. Please retry.",
    "warning": "Your session expires soon.",
    "info": "A new update is available.",
}


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

        self._wire()
        # Fire one long-lived toast on launch so a toast is visible without
        # a click.
        QTimer.singleShot(
            1500, lambda: self.showToast("info", "Info", duration=20000))

    def _wire(self):
        pairs = [
            (self.ui.successBtn, "success", "Success"),
            (self.ui.errorBtn, "error", "Error"),
            (self.ui.warningBtn, "warning", "Warning"),
            (self.ui.infoBtn, "info", "Info"),
        ]
        for button, variant, title in pairs:
            button.clicked.connect(
                lambda _=False, v=variant, t=title: self.showToast(v, t))

    def showToast(self, variant, title, duration=4000):
        QCustomToast.show_toast(self, MESSAGES[variant], variant=variant,
                                title=title, duration=duration,
                                position=self.ui.pos.currentText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
