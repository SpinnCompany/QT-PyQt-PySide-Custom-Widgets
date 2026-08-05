########################################################################
## Design tokens + variant/size - QCustomQPushButton
##
## Shows every button variant x size, styled entirely from design tokens,
## with a live light/dark theme toggle. The window chrome comes from the
## json-styles / Qss pipeline; the buttons come from applyDesignTokens —
## that pairing (tokens on top of the compiled-sass chrome) is the demo.
########################################################################
import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication

# json-styles theme name per token theme, so both systems flip together
THEME_NAMES = {"light": "Tokens Light", "dark": "Tokens Dark"}


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        self.theme = "light"
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Point QSettings at THIS app BEFORE loadJsonStyle: the loader reads
        # QSettings while parsing CustomThemes, and without an identity it
        # lands on the shared "Unknown Organization/main.py" file whose stale
        # THEME strips our Default-Theme flag (wrong theme wins).
        QCoreApplication.setOrganizationName("Custom Widgets")
        QCoreApplication.setApplicationName("DesignTokensDemo")

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

        # follow whatever theme is active (persisted from a previous run)
        if str(getattr(themeEngine, "theme", "")) == THEME_NAMES["dark"]:
            self.theme = "dark"
        self._syncToggleText()

        # applyCompiledSass REPLACES the app stylesheet, so the token block is
        # (re)applied after it — initially and after every theme switch.
        self._applyTokens()
        themeEngine.onThemeChangeComplete.connect(self._applyTokens)

        self.ui.toggleButton.clicked.connect(self._toggleTheme)

    # -- design tokens ----------------------------------------------------- #
    def _applyTokens(self):
        applyDesignTokens(QApplication.instance(),
                          tokens=DesignTokens(theme=self.theme))

    def _toggleTheme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self._syncToggleText()
        # flip the json-styles chrome, then re-apply the token block on top
        self.themeEngine.setTheme(THEME_NAMES[self.theme])
        self._applyTokens()

    def _syncToggleText(self):
        self.ui.toggleButton.setText(
            "Switch to light" if self.theme == "dark" else "Switch to dark")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
