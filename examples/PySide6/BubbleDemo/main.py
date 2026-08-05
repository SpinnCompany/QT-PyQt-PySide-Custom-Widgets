"""QCustomBubbleChart — live preview.

Interactive sentiment bubble cloud + market-share chart: hover for a CUSTOM
tooltip card, wheel/±/drag to zoom & pan, double-click to reset, type in the
search box (or click the painted search icon) to highlight matches. Full
project structure: ui/ + compiled src/ + json-styles themes + Qss scss tokens.
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

_STYLE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "json-styles", "style.json")


def chartPalette(themeName):
    """Bubble hues from style.json's ChartPalette — they live WITH the theme."""
    with open(_STYLE, "r", encoding="utf-8") as f:
        pal = json.load(f).get("ChartPalette", {})
    return pal.get(str(themeName)) or pal.get("Bubble Dark") or {}


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Point QSettings at THIS app BEFORE loadJsonStyle: the loader reads
        # QSettings while parsing CustomThemes, and without an identity it
        # lands on the shared "Unknown Organization/main.py" file whose stale
        # THEME strips our Default-Theme flag (wrong theme wins).
        QCoreApplication.setOrganizationName("Custom Widgets")
        QCoreApplication.setApplicationName("BubbleDemo")

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

        self._seedCharts()

    def _seedCharts(self):
        pal = chartPalette(getattr(self.themeEngine, "theme", ""))

        # Sentiment cloud — grouped by category (positive / negative / neutral
        # lobes); the widget's reference seed data stays as-is.
        self.ui.sentChart.setCategoryColors({
            "positive": pal.get("positive"),
            "negative": pal.get("negative"),
            "neutral": pal.get("neutral"),
        })

        # Market share — single-blob, different data
        self.ui.shareChart.setItems([
            {"label": "Chrome", "value": 64, "category": "a"},
            {"label": "Safari", "value": 19, "category": "b"},
            {"label": "Edge", "value": 5, "category": "c"},
            {"label": "Firefox", "value": 3, "category": "c"},
            {"label": "Opera", "value": 2, "category": "c"},
            {"label": "Samsung", "value": 3, "category": "b"},
            {"label": "UC", "value": 1, "category": "c"},
            {"label": "Other", "value": 3, "category": "c"},
        ])
        self.ui.shareChart.setCategoryColors({
            "a": pal.get("catA"), "b": pal.get("catB"), "c": pal.get("catC"),
        })

        # search boxes drive each chart's highlight query
        for search, chart in ((self.ui.sentSearch, self.ui.sentChart),
                              (self.ui.shareSearch, self.ui.shareChart)):
            search.textChanged.connect(chart.setSearchQuery)
            chart.searchRequested.connect(search.setFocus)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
