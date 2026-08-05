"""QCustomRadialGauge showcase — needles, zones, dials + countdown, token-driven.

Exercises the gauge's flexibility: the Threat-Level semicircles (needle + zones
+ status badge + dashed guide), a wide speedometer with a numeric scale, a
full-circle dial, and the "17 Sec" radial-tick countdown (dotted scale ring +
labels + emphasised leading tick). Everything animates in on show. Structure
lives in ui/MainWindow.ui (Designer-editable); chrome in
Qss/scss/defaultStyle.scss; zone / gradient hues in the ChartPalette section of
json-styles/style.json so they flip with the theme.
"""

import json
import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings, QTimer
from qtpy.QtWidgets import QApplication

THEME_DEFAULT = "Gauge Dark"


def chartPalette(themeName):
    """Zone / gradient hues live WITH the theme (ChartPalette in style.json)."""
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root, "json-styles", "style.json"), encoding="utf-8") as f:
        data = json.load(f)
    pal = data.get("ChartPalette", {})
    return pal.get(str(themeName)) or pal.get(THEME_DEFAULT) or {}


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Point QSettings at THIS app BEFORE loadJsonStyle: the loader reads
        # THEME during parse, and a stale value in the shared pre-identity
        # store strips every Default-Theme flag (wrong theme wins).
        QCoreApplication.setOrganizationName("Custom Widgets")
        QCoreApplication.setApplicationName("RadialGaugeDemo")
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
            # Prefer the theme flagged default; a stale shared QSettings file can
            # clear every defaultTheme flag at load time, so fall back to this
            # app's own default theme name explicitly.
            names = [t.name for t in themeEngine.themes]
            default = next((t.name for t in themeEngine.themes
                            if getattr(t, "defaultTheme", False)), None)
            if default is None and THEME_DEFAULT in names:
                default = THEME_DEFAULT
            if default:
                s.setValue("THEME", default)
                s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._seedGauges()
        # animate every gauge in from 0, and start the countdown, once shown
        QTimer.singleShot(350, self._runIntro)

    def _seedGauges(self):
        """Theme-driven zones/gradients + animation targets (data-driven config
        stays in code — static props live in the .ui)."""
        theme = QSettings().value("THEME") or getattr(self.themeEngine, "theme", "")
        pal = chartPalette(theme)
        ui = self.ui

        threatZones = [(0, 33, pal["zoneLow"]), (33, 66, pal["zoneMid"]),
                       (66, 100, pal["zoneHigh"])]

        # Row 1 — the three Threat-Level semicircle gauges (needle + zones + guide)
        self._animateIn = []
        for gauge, target in ((ui.threatGauge1, 24), (ui.threatGauge2, 55),
                              (ui.threatGauge3, 75)):
            gauge.setZones(threatZones)
            gauge._target = target
            self._animateIn.append(gauge)

        # Row 2a — a wide speedometer (gradient arc + numeric scale, no zones)
        ui.speedGauge.zonesCsv = ""
        ui.speedGauge.setGradient(pal["speedStart"], pal["speedEnd"])
        ui.speedGauge.statusText = ""
        ui.speedGauge._target = 92
        self._animateIn.append(ui.speedGauge)

        # Row 2b — a FULL-CIRCLE dial (any start/span; numeric scale; no needle)
        ui.usageGauge.zonesCsv = ""
        ui.usageGauge.setGradient(pal["usageStart"], pal["usageEnd"])
        ui.usageGauge.statusText = ""
        ui.usageGauge._target = 68
        self._animateIn.append(ui.usageGauge)

        # Row 2c — a FULL-360 radial-tick countdown (dotted scale ring + labels
        # + outward-emphasised leading tick)
        ui.timerGauge.zonesCsv = ""
        ui.timerGauge.setGradient(pal["timerStart"], pal["timerEnd"])
        ui.timerGauge.statusText = ""
        ui.timerGauge.valueChanged.connect(
            lambda v: ui.timerGauge.setCenterText("%g" % v))
        ui.timerGauge.finished.connect(
            lambda: ui.timerGauge.start(seconds=20))  # loop the demo

    def _runIntro(self):
        for gauge in self._animateIn:
            gauge.setValue(gauge._target)
        self.ui.timerGauge.start(seconds=20)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
