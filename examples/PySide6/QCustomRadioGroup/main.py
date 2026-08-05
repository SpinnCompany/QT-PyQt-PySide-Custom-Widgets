########################################################################
## QCustomRadioGroup example
##
## Three groups driven entirely through the group API: a vertical plan picker
## with explicit value=label options, a horizontal group, and one whose options
## are replaced at runtime to show that a surviving selection is kept. Themed
## through the Custom_Widgets pipeline (ui/ + Qss scss + json-styles), with a
## live light/dark toggle so you can watch the colours re-tokenize.
## Run:
##     python main.py
########################################################################
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
            # Default-Theme is ignored by the json parser when ANY QSettings
            # file already holds a THEME, so pin this app's default explicitly.
            if not s.value("INIT-THEME-SET"):
                s.setValue("THEME", "Group-Dark")
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

    def _wireDemo(self):
        ui = self.ui
        ui.planGroup.valueChanged.connect(
            lambda v: ui.statusLabel.setText(
                "plan=%s  billing=%s" % (v, ui.billingGroup.value() or "-")))
        ui.billingGroup.valueChanged.connect(
            lambda v: ui.statusLabel.setText(
                "plan=%s  billing=%s" % (ui.planGroup.value() or "-", v)))
        ui.swapButton.clicked.connect(self._swapSeats)
        ui.themeButton.clicked.connect(self._toggleTheme)

    def _swapSeats(self):
        # "2" survives the swap, so the selection is preserved.
        self.ui.seatsGroup.setOptions(["2", "5", "10"])
        self.ui.statusLabel.setText(
            "seats kept selection: %s" % (self.ui.seatsGroup.value() or "none"))

    def _toggleTheme(self):
        themeEngine = self.themeEngine
        target = "Group-Light" if themeEngine.theme == "Group-Dark" else "Group-Dark"
        QSettings().setValue("THEME", target)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
