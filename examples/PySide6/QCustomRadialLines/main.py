########################################################################
## QCustomRadialLines example
##
## A polar line chart for cyclical data: weekday against weekend traffic
## wrapped onto a circle, so the series closes back on itself.
## Rendered with QPainter only - no QtCharts. Chart chrome comes from
## Qss/scss/defaultStyle.scss; series hues come from the active theme's
## Other-variables so they flip with the Light / dark toggle.
## Run:
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
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication

SERIES = [("Weekday", [30, 45, 60, 52, 48, 70, 64]),
          ("Weekend", [20, 25, 40, 38, 30, 35, 28])]
LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SERIES_ROLES = ["SERIES_1", "SERIES_2"]


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
        QCoreApplication.setApplicationName("QCustomRadialLines Showcase")

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

        self._wireChart()

    # ------------------------------------------------------------------ #
    ## Wiring + data seeding (no styling here — see Qss/scss)
    # ------------------------------------------------------------------ #
    def _wireChart(self):
        ui = self.ui
        chart = ui.radialLines

        chart.setSeries(SERIES)
        chart.setLabels(LABELS)
        self._applySeriesColors()
        chart.seriesHovered.connect(self._onHover)

        ui.ringsSpin.setValue(chart.rings)
        ui.ringsSpin.valueChanged.connect(
            lambda v: setattr(chart, "rings", v))
        ui.fillSlider.setValue(int(chart.fillOpacity * 100))
        ui.fillSlider.valueChanged.connect(
            lambda v: setattr(chart, "fillOpacity", v / 100.0))

        ui.closedBtn.clicked.connect(lambda: self._flip("closed"))
        ui.markersBtn.clicked.connect(lambda: self._flip("showMarkers"))
        ui.gridBtn.clicked.connect(lambda: self._flip("showGrid"))
        ui.themeBtn.clicked.connect(self._toggleTheme)

    def _applySeriesColors(self):
        """Series hues follow the ACTIVE theme's Other-variables."""
        colors = [self.themeEngine.themeColor(role, "") for role in SERIES_ROLES]
        self.ui.radialLines.colorsCsv = ",".join(colors)

    def _flip(self, attr):
        chart = self.ui.radialLines
        setattr(chart, attr, not getattr(chart, attr))

    def _onHover(self, index):
        if index < 0:
            self.ui.statusLabel.setText("Hover a shape")
            return
        name, values = self.ui.radialLines.series()[index]
        self.ui.statusLabel.setText("%s — peak %g" % (name, max(values)))

    def _toggleTheme(self):
        settings = QSettings()
        current = settings.value("THEME")
        settings.setValue("THEME",
                          "Polar-Light" if current == "Polar-Dark" else "Polar-Dark")
        QAppSettings.updateAppSettings(self, generateIcons=False)
        self._applySeriesColors()  # series hues follow the theme


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
