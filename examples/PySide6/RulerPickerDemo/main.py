"""QCustomRulerPicker showcase — fixed / centered / vertical rulers, token-driven.

Demonstrates a weight ruler (fixed span, value in the card header), a height
ruler with a big readout (centered scrolling picker), a fine-step body-fat
ruler and a vertical thermostat ruler — fixed vs centered, horizontal vs
vertical, snap, units and the live value readout. Structure lives in
ui/MainWindow.ui (Designer-editable); chrome in Qss/scss/defaultStyle.scss;
indicator hues in the ChartPalette section of json-styles/style.json so they
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

THEME_DEFAULT = "Ruler Dark"


def chartPalette(themeName):
    """Ruler indicator hues live WITH the theme (ChartPalette in style.json)."""
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
        QCoreApplication.setApplicationName("RulerPickerDemo")
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

        self._seedRulers()

    def _seedRulers(self):
        """Theme-driven indicator colours + live readout wiring (static ruler
        config — spans, steps, units, orientation — lives in the .ui)."""
        theme = QSettings().value("THEME") or getattr(self.themeEngine, "theme", "")
        pal = chartPalette(theme)
        ui = self.ui

        ui.weightRuler.indicatorColor = pal["weightIndicator"]
        ui.heightRuler.indicatorColor = pal["heightIndicator"]
        ui.bodyFatRuler.indicatorColor = pal["bodyFatIndicator"]
        ui.thermoRuler.indicatorColor = pal["thermoIndicator"]

        # Weight — value shown live in the card header
        ui.weightRuler.valueChanged.connect(
            lambda v: ui.weightValue.setText("%g" % v))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
