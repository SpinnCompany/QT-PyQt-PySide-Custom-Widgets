########################################################################
## QCustomRadialBars example
##
## Activity rings: concentric arcs comparing values that do not sum to a
## whole. Hover a ring to highlight it.
## Rendered with QPainter only - no QtCharts. Chart chrome comes from
## Qss/scss/defaultStyle.scss; ring hues come from the active theme's
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

BARS = [("Move", 82), ("Exercise", 64), ("Stand", 95)]
RING_ROLES = ["RING_1", "RING_2", "RING_3"]


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
        QCoreApplication.setApplicationName("QCustomRadialBars Showcase")

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
        chart = ui.radialBars

        chart.setBars(BARS)
        self._applyRingColors()
        chart.barHovered.connect(self._onHover)

        ui.thicknessSlider.setValue(chart.thickness)
        ui.thicknessSlider.valueChanged.connect(
            lambda v: setattr(chart, "thickness", v))
        ui.startSlider.setValue(chart.startAngle)
        ui.startSlider.valueChanged.connect(
            lambda v: setattr(chart, "startAngle", v))

        ui.roundedBtn.clicked.connect(lambda: self._flip("rounded"))
        ui.trackBtn.clicked.connect(lambda: self._flip("showTrack"))
        ui.clockwiseBtn.clicked.connect(lambda: self._flip("clockwise"))
        ui.themeBtn.clicked.connect(self._toggleTheme)

    def _applyRingColors(self):
        """Ring hues follow the ACTIVE theme's Other-variables."""
        colors = [self.themeEngine.themeColor(role, "") for role in RING_ROLES]
        self.ui.radialBars.colorsCsv = ",".join(colors)

    def _flip(self, attr):
        chart = self.ui.radialBars
        setattr(chart, attr, not getattr(chart, attr))

    def _onHover(self, index):
        if index < 0:
            self.ui.statusLabel.setText("Hover a ring")
            return
        chart = self.ui.radialBars
        label, value = chart.bars()[index]
        self.ui.statusLabel.setText(
            "%s — %g (%.0f%% of max)"
            % (label, value, chart.fractionFor(index) * 100))

    def _toggleTheme(self):
        settings = QSettings()
        current = settings.value("THEME")
        settings.setValue("THEME",
                          "Rings-Light" if current == "Rings-Dark" else "Rings-Dark")
        QAppSettings.updateAppSettings(self, generateIcons=False)
        self._applyRingColors()  # ring hues follow the theme


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
