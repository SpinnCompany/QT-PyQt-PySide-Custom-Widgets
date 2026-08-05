########################################################################
## QCustomRangeBarChart example
##
## Daily temperature ranges as floating bars: each bar spans a low to a
## high rather than sitting on a baseline.
## Rendered with QPainter only - no QtCharts. Themed through the
## Custom_Widgets pipeline (ui/ + Qss scss + json-styles).
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
                s.setValue("THEME", "RangeBar-Dark")
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
        ui.chart.barHovered.connect(self._onHover)
        ui.orientationCombo.currentTextChanged.connect(
            lambda v: setattr(ui.chart, "orientation", v))
        ui.widthSlider.valueChanged.connect(
            lambda v: setattr(ui.chart, "barWidthRatio", v / 100.0))
        ui.boundsButton.clicked.connect(
            lambda: setattr(ui.chart, "showBounds", not ui.chart.showBounds))
        ui.themeButton.clicked.connect(self._toggleTheme)

    def _onHover(self, index):
        if index < 0:
            self.ui.statusLabel.setText("Hover a bar for its range")
            return
        label, low, high = self.ui.chart.ranges()[index]
        self.ui.statusLabel.setText(
            "%s — %g to %g (span %g)" % (label, low, high, high - low))

    def _toggleTheme(self):
        themeEngine = self.themeEngine
        target = ("RangeBar-Light" if themeEngine.theme == "RangeBar-Dark"
                  else "RangeBar-Dark")
        QSettings().setValue("THEME", target)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
