"""QCustomMultiSelect showcase — four fields: a plain multi-select, a
searchable one over a longer list, one capped at 3 choices, and one that
collapses to "+N" past two chips. Click a field to open its popup; click a
chip's x to drop just that one."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication

LANGUAGE_KEYS = ["py", "js", "rs", "go", "cpp", "rb", "kt", "swift", "ts"]


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Name the app BEFORE loadJsonStyle: theme parsing checks QSettings for
        # an existing THEME, and without these names QSettings resolves to the
        # shared "Unknown Organization/main.py.conf" — whose stale THEME would
        # cancel this app's Default-Theme flag on every first run.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomMultiSelect Example")

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

        self._wireControls()

    def _wireControls(self):
        ui = self.ui
        for field in (ui.coloursSelect, ui.languagesSelect, ui.cappedSelect):
            field.selectionChanged.connect(self._report)

        ui.clearButton.clicked.connect(ui.coloursSelect.clearSelection)
        ui.selectAllButton.clicked.connect(
            lambda: ui.languagesSelect.setSelected(list(LANGUAGE_KEYS)))
        ui.themeButton.clicked.connect(
            lambda: self.themeEngine.toggleTheme(dark="MeadowDark",
                                                 light="MeadowLight"))

    def _report(self, _values):
        parts = []
        for name, field in (("colours", self.ui.coloursSelect),
                            ("languages", self.ui.languagesSelect),
                            ("capped", self.ui.cappedSelect)):
            if field.selected():
                parts.append("%s: %s" % (name, ", ".join(field.selectedLabels())))
        self.ui.statusLabel.setText(" | ".join(parts) or "Nothing selected yet")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
