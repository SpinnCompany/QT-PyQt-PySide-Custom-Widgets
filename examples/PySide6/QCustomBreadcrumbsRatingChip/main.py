"""Breadcrumbs / Rating / Chips showcase — a breadcrumb trail, a star rating,
and removable + filter chips, themed from json-styles design tokens."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the app identity BEFORE loadJsonStyle: the theme loader consults
        # QSettings while parsing CustomThemes, and without these names it reads
        # the shared unnamed settings file (polluted by other example apps),
        # which silently cancels this app's Default-Theme flag.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("Breadcrumbs Rating Chips Showcase")

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

        self._seedAndWire()

    def _seedAndWire(self):
        ui = self.ui

        # breadcrumb trail (data-driven, so seeded here rather than in the .ui)
        ui.breadcrumbs.setItems([("Home", "/"), ("Library", "/lib"),
                                 ("Widgets", "/lib/widgets"), "Rating"])
        ui.breadcrumbs.itemClicked.connect(
            lambda i, d: ui.statusLabel.setText("Go to: %s" % d))

        # star rating (initial value comes from the .ui)
        ui.rating.valueChanged.connect(
            lambda v: ui.statusLabel.setText("Rated %d/5" % v))

        # removable tags
        for tag in ("python", "pyside6", "qt", "widgets", "tokens"):
            ui.tagsGroup.addChip(tag, closable=True)

        # multi-select filter chips
        for name in ("All", "Free", "Pro", "New"):
            ui.filtersGroup.addChip(name, selectable=True)
        ui.filtersGroup.selectionChanged.connect(
            lambda sel: ui.statusLabel.setText(
                "Filters: %s" % (", ".join(map(str, sel)) or "none")))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
