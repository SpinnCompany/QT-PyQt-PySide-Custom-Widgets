"""QCustomPieChart showcase — % callout labels + hatch fills, token-driven.

The QtCharts pie already renders labels; this demo shows the convenience
%-inside toggle + the per-slice HATCH fills (indices via setHatchIndices),
next to a default pie (enhancements off). Structure lives in ui/MainWindow.ui
(Designer-editable); chrome in Qss/scss/defaultStyle.scss; slice hues in the
ChartPalette section of json-styles/style.json so they flip with the theme.
"""

import json
import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication

THEME_DEFAULT = "Pie Dark"


def chartPalette(themeName):
    """Slice hues live WITH the theme (ChartPalette in style.json)."""
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
        QCoreApplication.setApplicationName("PieEnhanceDemo")
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

        self._seedCharts()

    @staticmethod
    def _configurePie(chart, data, colors, hatch=None, pattern="bdiag",
                      pct=False, hole=0.0):
        """Series/data-driven config stays in code — Designer cannot set series."""
        if hasattr(chart, "setChartTitle"):
            chart.setChartTitle("")
        chart._chart.setTitle("")
        chart.addSeries("S", data, colors=colors)
        try:
            chart.holeSize = hole
        except Exception:
            pass
        if pct:
            chart.setShowPercentLabels(True)
        if hatch:
            chart.setHatchIndices(hatch)
            chart.setHatchPattern(pattern)

    def _seedCharts(self):
        theme = QSettings().value("THEME") or getattr(self.themeEngine, "theme", "")
        pal = chartPalette(theme)

        data = [("Product", 30), ("Restaurants", 23), ("Media", 18),
                ("Pay", 17), ("Other", 12)]

        # 1) % labels inside + hatched Pay/Other (bdiag), donut hole
        self._configurePie(self.ui.transferPie, data, pal["transferColors"],
                           hatch=[3, 4], pattern="bdiag", pct=True, hole=0.45)

        # 2) cross-hatch on one slice, full pie
        self._configurePie(self.ui.storagePie,
                           [("Photos", 44), ("Apps", 26), ("Media", 16), ("Free", 14)],
                           pal["storageColors"],
                           hatch=[3], pattern="cross", pct=True, hole=0.0)

        # 3) default pie — enhancements OFF
        self._configurePie(self.ui.defaultPie, data, pal["transferColors"],
                           hole=0.0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
