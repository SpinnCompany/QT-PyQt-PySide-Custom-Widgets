"""QCustomTipOverlay showcase — every tail position, one button each.

Click a button to anchor a closable tip overlay to it. One tip is opened
automatically on launch so the overlay is visible immediately. All styling
lives in json-styles/ + Qss/scss/defaultStyle.scss; this file only boots
the app and wires signals.
"""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomTipOverlay import QCustomTipOverlay
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtCore import QCoreApplication, QSettings, QTimer
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

        self._wire()
        # Open one tip on launch so the overlay shows without a click.
        QTimer.singleShot(1500, lambda: self.showTip(self.ui.btnAuto2, "auto"))

    def _wire(self):
        pairs = [
            (self.ui.btnAuto1, "auto"),
            (self.ui.btnTopLeft, "top-left"),
            (self.ui.btnTopCenter, "top-center"),
            (self.ui.btnTopRight, "top-right"),
            (self.ui.btnBottomLeft, "bottom-left"),
            (self.ui.btnBottomCenter, "bottom-center"),
            (self.ui.btnBottomRight, "bottom-right"),
            (self.ui.btnAuto2, "auto"),
            (self.ui.btnLeftTop, "left-top"),
            (self.ui.btnLeftBottom, "left-bottom"),
            (self.ui.btnRightTop, "right-top"),
            (self.ui.btnRightBottom, "right-bottom"),
            (self.ui.btnLeftCenter, "left-center"),
            (self.ui.btnRightCenter, "right-center"),
            (self.ui.btnAuto3, "auto"),
        ]
        for button, tailPosition in pairs:
            button.clicked.connect(
                lambda _=False, b=button, t=tailPosition: self.showTip(b, t))

    def showTip(self, button, tailPosition):
        tip = QCustomTipOverlay(
            target=button,
            title="Test Tip",
            description="This is a test tip",
            isClosable=True,
            tailPosition=tailPosition,
            parent=self,
            duration=-1,
        )
        tip.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
