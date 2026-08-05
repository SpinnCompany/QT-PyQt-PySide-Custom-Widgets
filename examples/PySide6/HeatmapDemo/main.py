"""QCustomHeatmap showcase — grid + calendar heatmaps with token-driven theming.

Demonstrates the grid "Activity by time" heatmap, a GitHub-style contributions
calendar, and a second grid with a different ramp/labels — grid + calendar
modes, the colour ramp, labels, legend and flex sizing. Structure lives in
ui/MainWindow.ui (Designer-editable); chrome in Qss/scss/defaultStyle.scss;
ramp hues in the ChartPalette section of json-styles/style.json so they flip
with the theme.
"""

import itertools
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


THEME_DEFAULT = "Heatmap Dark"


def _cycle(seq, n):
    it = itertools.cycle(seq)
    return [float(next(it)) for _ in range(n)]


def chartPalette(themeName):
    """Heatmap ramp hues live WITH the theme (ChartPalette in style.json)."""
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
        QCoreApplication.setApplicationName("HeatmapDemo")
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

        self._seedHeatmaps()

    def _seedHeatmaps(self):
        """Seed the demo data + theme-driven ramp colours (data-driven config
        stays in code — Designer cannot author series/values)."""
        theme = QSettings().value("THEME") or getattr(self.themeEngine, "theme", "")
        pal = chartPalette(theme)

        # 1) Activity by time — grid mode, purple ramp
        activity = self.ui.activityHeatmap
        activity.setValues([_cycle([3, 8, 2, 6, 9, 1, 4, 7, 5][i % 9:] +
                                   [3, 8, 2, 6, 9, 1, 4, 7, 5][:i % 9], 7)
                            for i in range(6)])
        activity.setColors(pal["activityLow"], pal["activityHigh"],
                           empty=pal["activityEmpty"])
        activity.setLabels(row_labels=["1pm", "2pm", "3pm", "4pm", "5pm", "6pm"],
                           col_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

        # 2) Contributions — calendar mode (set in the .ui), green ramp
        cal = self.ui.contributionsHeatmap
        cal.setValues(_cycle([0, 1, 0, 2, 4, 1, 3, 0, 5, 2, 6, 1,
                              0, 3, 4, 2, 0, 1, 5, 3], 7 * 20))
        cal.setColors(pal["calLow"], pal["calHigh"], empty=pal["calEmpty"])

        # 3) Server load by hour — grid mode, teal ramp, different labels
        load = self.ui.loadHeatmap
        load.setValues([_cycle([2, 5, 9, 7, 3, 6, 8, 4][i % 8:] +
                               [2, 5, 9, 7, 3, 6, 8, 4][:i % 8], 7) for i in range(8)])
        load.setColors(pal["loadLow"], pal["loadHigh"], empty=pal["loadEmpty"])
        load.setLabels(row_labels=["00h", "03h", "06h", "09h", "12h", "15h", "18h", "21h"],
                       col_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
