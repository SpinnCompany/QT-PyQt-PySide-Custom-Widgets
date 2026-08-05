########################################################################
## QCustomRadarChart example
##
## A product-comparison radar: three candidates across five measures, with
## controls for the grid style, ring count, fill opacity and rotation. Hover a
## polygon to emphasise it; click near an axis to see which measure it is.
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

AXES = ["Speed", "Power", "Range", "Agility", "Cost"]
SERIES = [("Alpha", [80, 60, 90, 70, 50]),
          ("Beta", [60, 90, 50, 80, 70]),
          ("Gamma", [70, 70, 65, 55, 90])]
SERIES_ROLES = ["SERIES_1", "SERIES_2", "SERIES_3"]


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
        QCoreApplication.setApplicationName("QCustomRadarChart Showcase")

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
        chart = ui.radarChart

        chart.setAxes(AXES)
        chart.setSeries(SERIES)
        chart.maxValue = 100
        self._applySeriesColors()
        chart.seriesHovered.connect(self._onHover)
        chart.axisClicked.connect(self._onAxis)

        ui.gridBox.currentTextChanged.connect(self._setGrid)
        ui.ringsSpin.setValue(chart.rings)
        ui.ringsSpin.valueChanged.connect(self._setRings)
        ui.fillSlider.setValue(int(chart.fillOpacity * 100))
        ui.fillSlider.valueChanged.connect(self._setOpacity)
        ui.rotateSlider.setValue(chart.startAngle)
        ui.rotateSlider.valueChanged.connect(self._setAngle)

        ui.markersBtn.clicked.connect(self._toggleMarkers)
        ui.legendBtn.clicked.connect(self._toggleLegend)
        ui.ringLabelsBtn.clicked.connect(self._toggleRingLabels)
        ui.dropSeriesBtn.clicked.connect(self._dropLast)
        ui.resetBtn.clicked.connect(self._reset)
        ui.themeBtn.clicked.connect(self._toggleTheme)

    def _applySeriesColors(self):
        """Series hues follow the ACTIVE theme's Other-variables."""
        chart = self.ui.radarChart
        colors = [self.themeEngine.themeColor(role, "") for role in SERIES_ROLES]
        chart.seriesColorsCsv = ",".join(colors[:chart.seriesCount()])

    def _onHover(self, index):
        if index < 0:
            self.ui.statusLabel.setText("Hover a shape, or click near an axis")
            return
        name, values = self.ui.radarChart.series()[index]
        pairs = ", ".join("%s %g" % (AXES[i], v) for i, v in enumerate(values))
        self.ui.statusLabel.setText("%s — %s" % (name, pairs))

    def _onAxis(self, index):
        self.ui.statusLabel.setText(
            "axis %d: %s" % (index, self.ui.radarChart.axes()[index]))

    def _setGrid(self, value):
        self.ui.radarChart.gridStyle = value

    def _setRings(self, value):
        self.ui.radarChart.rings = value

    def _setOpacity(self, value):
        self.ui.radarChart.fillOpacity = value / 100.0

    def _setAngle(self, value):
        self.ui.radarChart.startAngle = value

    def _toggleMarkers(self):
        chart = self.ui.radarChart
        chart.showMarkers = not chart.showMarkers

    def _toggleLegend(self):
        chart = self.ui.radarChart
        chart.showLegend = not chart.showLegend

    def _toggleRingLabels(self):
        chart = self.ui.radarChart
        chart.showRingLabels = not chart.showRingLabels

    def _dropLast(self):
        chart = self.ui.radarChart
        chart.removeSeries(chart.seriesCount() - 1)

    def _reset(self):
        self.ui.radarChart.setSeries(SERIES)
        self._applySeriesColors()

    def _toggleTheme(self):
        settings = QSettings()
        current = settings.value("THEME")
        settings.setValue("THEME",
                          "Radar-Light" if current == "Radar-Dark" else "Radar-Dark")
        QAppSettings.updateAppSettings(self, generateIcons=False)
        self._applySeriesColors()  # series hues follow the theme


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
