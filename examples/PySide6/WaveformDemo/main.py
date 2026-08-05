"""QCustomWaveform showcase — live ECG, equalizer, mirror + neon bars.

Demonstrates a live ECG line ("110 bpm"), a live audio-level equalizer
("Water"), a static voice-message mirror waveform, and a glowing neon bar
chart. The ECG + equalizer self-animate via push(). Structure lives in
ui/MainWindow.ui (Designer-editable); chrome in Qss/scss/defaultStyle.scss;
line / bar hues in the ChartPalette section of json-styles/style.json so they
flip with the theme.
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

THEME_DEFAULT = "Waveform Dark"


def chartPalette(themeName):
    """Waveform line / bar hues live WITH the theme (ChartPalette in style.json)."""
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
        QCoreApplication.setApplicationName("WaveformDemo")
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

        self._seedWaveforms()

    def _seedWaveforms(self):
        """Theme-driven colours + the static voice data (data-driven config
        stays in code — static props live in the .ui)."""
        theme = QSettings().value("THEME") or getattr(self.themeEngine, "theme", "")
        pal = chartPalette(theme)
        ui = self.ui

        # Heart rate — streaming ECG line (animated), red on a faint grid
        ui.ecgWave.lineColor = pal["ecgLine"]
        ui.ecgWave.gridColor = pal["ecgGrid"]

        # Water — audio-level equalizer bars (animated), blue→cyan
        ui.waterWave.barColor = pal["waterBar1"]
        ui.waterWave.barColor2 = pal["waterBar2"]

        # Voice message — static mirror waveform (center-symmetric)
        ui.voiceWave.setValues([0.3, 0.6, 0.4, 0.85, 0.5, 0.7, 0.35, 0.9, 0.55,
                                0.65, 0.45, 0.8, 0.4, 0.7, 0.5, 0.6, 0.3, 0.75,
                                0.5, 0.4])
        ui.voiceWave.barColor = pal["voiceBar1"]
        ui.voiceWave.barColor2 = pal["voiceBar2"]

        # Neon spectrum — glowing bars (the HYPER-CHARTS look)
        ui.neonWave.barColor = pal["neonBar1"]
        ui.neonWave.barColor2 = pal["neonBar2"]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
