"""QCustomFunnelChart showcase.

A conversion funnel with drop-off percentages, plus the same data as a
pyramid and rotated horizontal. Hover a stage to highlight it. Rendered with
QPainter only - no QtCharts. Full project structure: ui/ + compiled src/ +
json-styles themes + Qss scss tokens (zero inline styling).
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

THEME_DARK = "Funnel Dark"
THEME_LIGHT = "Funnel Light"

_STYLE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "json-styles", "style.json")


def stagePalette(themeName):
    """Per-stage hues from style.json's ChartPalette — they live WITH the theme."""
    with open(_STYLE, "r", encoding="utf-8") as f:
        pal = json.load(f).get("ChartPalette", {})
    entry = pal.get(str(themeName)) or pal.get(THEME_DARK) or {}
    return entry.get("stages", [])


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
            # Prefer the json default; a stale THEME in the pre-boot QSettings
            # scope strips Default-Theme flags, so fall back to the first
            # custom (non-predefined) theme rather than silently keeping the
            # engine's built-in Light palette.
            chosen = None
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False):
                    chosen = t.name
                    break
            if chosen is None:
                for t in themeEngine.themes:
                    if not getattr(t, "predefined", False):
                        chosen = t.name
                        break
            if chosen is not None:
                s.setValue("THEME", chosen)
                s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._seedFunnel()
        self._wire()

    def _seedFunnel(self):
        chart = self.ui.funnelChart
        chart.setStages([("Visits", 1000), ("Signups", 420),
                         ("Trials", 180), ("Paid", 64)])
        self._applyStageColors()

    def _applyStageColors(self):
        colors = stagePalette(getattr(self.themeEngine, "theme", ""))
        if colors:
            self.ui.funnelChart.colorsCsv = ",".join(colors)

    def _wire(self):
        chart = self.ui.funnelChart
        chart.stageHovered.connect(self._onHover)
        chart.stageClicked.connect(self._onClick)
        self.ui.shapeCombo.currentTextChanged.connect(
            lambda v: setattr(chart, "shape", v))
        self.ui.orientCombo.currentTextChanged.connect(
            lambda v: setattr(chart, "orientation", v))
        self.ui.basisCombo.currentTextChanged.connect(
            lambda v: setattr(chart, "percentOf", v))
        self.ui.neckSlider.valueChanged.connect(
            lambda v: setattr(chart, "neckRatio", v / 100.0))
        self.ui.themeBtn.clicked.connect(self._toggleTheme)

    def _toggleTheme(self):
        self.themeEngine.toggleTheme(dark=THEME_DARK, light=THEME_LIGHT)
        self._applyStageColors()

    def _onHover(self, index):
        if index < 0:
            self.ui.statusLabel.setText("Hover a stage for its conversion")
            return
        label, value = self.ui.funnelChart.stages()[index]
        self.ui.statusLabel.setText(
            "%s — %g (%.1f%% of the first stage)"
            % (label, value, self.ui.funnelChart.percentFor(index)))

    def _onClick(self, index):
        self.ui.statusLabel.setText("clicked stage %d" % index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
