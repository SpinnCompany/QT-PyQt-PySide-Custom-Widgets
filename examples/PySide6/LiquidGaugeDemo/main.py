"""QCustomLiquidGauge showcase — fill gauges with token-driven theming.

Demonstrates fuel / battery / tank / humidity fill gauges: the circle +
rounded-rect shapes, gradient waves, centre value+suffix and status badges.
The waves ripple continuously and each level animates in from empty on show.
Structure lives in ui/MainWindow.ui (Designer-editable); chrome in
Qss/scss/defaultStyle.scss; gauge hues in the ChartPalette section of
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

THEME_DEFAULT = "Liquid Dark"


def chartPalette(themeName):
    """Gauge fill / badge hues live WITH the theme (ChartPalette in style.json)."""
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
        QCoreApplication.setApplicationName("LiquidGaugeDemo")
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
        # every level animates in from empty once shown
        QTimer.singleShot(400, self._runIntro)

    def _seedGauges(self):
        """Theme-driven colours + badges (data-driven config stays in code)."""
        theme = QSettings().value("THEME") or getattr(self.themeEngine, "theme", "")
        pal = chartPalette(theme)
        ui = self.ui

        # Fuel — circle, blue→purple, "3.61 gal" + 31% badge
        ui.fuelGauge.setColors(pal["fuelFill1"], pal["fuelFill2"],
                               background=pal["fuelBg"])
        ui.fuelGauge.setBadge("31%", pal["fuelFill1"])

        # Battery — rounded rect (shape set in the .ui), green, 72%
        ui.batteryGauge.setColors(pal["battFill1"], pal["battFill2"],
                                  background=pal["battBg"])

        # Water tank — circle, teal, 88% + badge
        ui.tankGauge.setColors(pal["tankFill1"], pal["tankFill2"],
                               background=pal["tankBg"])
        ui.tankGauge.setBadge("High", pal["tankFill1"])

        # Humidity — circle, blue, 54% + badge
        ui.humidityGauge.setColors(pal["humFill1"], pal["humFill2"],
                                   background=pal["humBg"])
        ui.humidityGauge.setBadge("Indoor", pal["humFill1"])

        self._intro = [(ui.fuelGauge, 31), (ui.batteryGauge, 72),
                       (ui.tankGauge, 88), (ui.humidityGauge, 54)]

    def _runIntro(self):
        for gauge, target in self._intro:
            gauge.setValue(target)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
