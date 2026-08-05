"""QCustomCopyButton example — copy-to-clipboard with confirmation, in all
three variants plus icon-only, with a reset-delay control and a live
light/dark theme toggle."""

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
        if s.value("THEME") is None:
            # A stray QSettings file (written before QApplication got its real
            # names) strips every theme's default flag — seed explicitly.
            s.setValue("THEME", "Slate")
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._wire()

    def _wire(self):
        ui = self.ui
        self.copyButtons = [ui.copyOutline, ui.copyGhost, ui.copySolid,
                            ui.copyIconOnly]
        for widget in self.copyButtons:
            widget.copied.connect(
                lambda text: ui.statusLabel.setText("copied %d characters" % len(text)))
        ui.delaySpin.valueChanged.connect(self._setDelay)
        ui.themeButton.clicked.connect(self._toggleTheme)

    def _setDelay(self, value):
        for widget in self.copyButtons:
            widget.resetDelay = value

    def _toggleTheme(self):
        s = QSettings()
        new = "Ivory" if s.value("THEME") == "Slate" else "Slate"
        s.setValue("THEME", new)
        self.themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
