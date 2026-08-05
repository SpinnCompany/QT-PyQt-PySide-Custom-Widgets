"""QCustomFeaturedIcon showcase.

Every variant, shape and size of the decorative icon tile.
Full project structure: ui/ + compiled src/ + json-styles themes + Qss scss
tokens (zero inline styling).
"""

import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication

THEME_DARK = "Featured Dark"
THEME_LIGHT = "Featured Light"


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

        self._wire()

    def _tiles(self):
        ui = self.ui
        return [
            (ui.tileTintedRounded, "tinted", "rounded"),
            (ui.tileTintedCircle, "tinted", "circle"),
            (ui.tileTintedSquare, "tinted", "square"),
            (ui.tileFilledRounded, "filled", "rounded"),
            (ui.tileFilledCircle, "filled", "circle"),
            (ui.tileFilledSquare, "filled", "square"),
            (ui.tileOutlineRounded, "outline", "rounded"),
            (ui.tileOutlineCircle, "outline", "circle"),
            (ui.tileOutlineSquare, "outline", "square"),
            (ui.tileGradientRounded, "gradient", "rounded"),
            (ui.tileGradientCircle, "gradient", "circle"),
            (ui.tileGradientSquare, "gradient", "square"),
        ]

    def _wire(self):
        for tile, variant, shape in self._tiles():
            tile.clicked.connect(
                lambda v=variant, sh=shape: self.ui.statusLabel.setText(
                    "clicked %s / %s" % (v, sh)))
        self.ui.sizeCombo.setCurrentText("lg")
        self.ui.sizeCombo.currentTextChanged.connect(self._setSize)
        self.ui.themeBtn.clicked.connect(
            lambda: self.themeEngine.toggleTheme(dark=THEME_DARK,
                                                 light=THEME_LIGHT))

    def _setSize(self, value):
        for tile, _variant, _shape in self._tiles():
            tile.sizeVariant = value


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
