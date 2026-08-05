"""QCustomAgendaList — live preview.

A day-plan schedule card (Running / Cycling / Gym / Swimming) with the connector
rail + done/active/pending status markers, and a second "meetings" agenda — inside
scroll areas so it flexes. Full project structure: ui/ + compiled src/ +
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

_STYLE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "json-styles", "style.json")


def chartPalette(themeName):
    """Per-item hues from style.json's ChartPalette — they live WITH the theme."""
    with open(_STYLE, "r", encoding="utf-8") as f:
        pal = json.load(f).get("ChartPalette", {})
    return pal.get(str(themeName)) or pal.get("Agenda Dark") or {}


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
        QCoreApplication.setApplicationName("AgendaDemo")

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

        self._seedAgendas()

    def _seedAgendas(self):
        pal = chartPalette(getattr(self.themeEngine, "theme", ""))
        # Today's plan — the widget's reference seed (Running/Cycling/Gym/Swimming)
        # stays as-is; the meetings agenda gets its own data, hued by the theme.
        self.ui.meetAgenda.setItems([
            {"time": "09:30", "endTime": "10:00", "title": "Standup",
             "subtitle": "Zoom · Product", "status": "done", "color": pal.get("green")},
            {"time": "11:00", "endTime": "11:45", "title": "Design review",
             "subtitle": "Figma · Aurora", "status": "done", "color": pal.get("purple")},
            {"time": "13:00", "endTime": "14:00", "title": "1:1 with Sam",
             "subtitle": "Room “Nebula”", "status": "active", "color": pal.get("blue")},
            {"time": "15:30", "endTime": "16:00", "title": "Roadmap sync",
             "subtitle": "Room “Orbit”", "status": "pending", "color": pal.get("amber")},
            {"time": "17:00", "endTime": "17:30", "title": "Retro",
             "subtitle": "Zoom · Team", "status": "pending", "color": pal.get("red")},
        ])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
