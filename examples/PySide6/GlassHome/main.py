########################################################################
## GLASSHOME — visionOS-style glass smart-home dashboard.
##
## The maintainable pipeline (not a pure-code app):
##   ui/*.ui  ->  compiled src/ui_*.py       (Custom_Widgets --convert-ui)
##   json-styles/style.json                  (Glass Dusk / Glass Day CustomThemes)
##   Qss/scss/*.scss  ($TOKENS + Other-variables, no hard-coded hex)
##   gui/GuiFunctions.py                     (orchestrator + per-panel managers)
##
## Every floating panel is a QCustomGlassFrame sampling the full-bleed
## wallpaper photo (backdropSource="wallpaper") — real blurred-backdrop
## glassmorphism, not a translucent fill.
########################################################################

import sys

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *                     # QCustomMainWindow, loadJsonStyle, enable_hot_reload
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtWidgets import QApplication

from gui.GuiFunctions import GuiFunctions


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        # build() runs now and re-runs on any compiled Ui_ change (hot reload).
        enable_hot_reload(self, self.build)

    def build(self):
        # Import the compiled Ui_ HERE so hot reload picks up regenerated modules.
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Apply the Glass Dusk / Glass Day themes from the JSON stylesheet.
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()

        # Generate theme icons + compile SCSS + paint the app (run AFTER show()).
        QAppSettings.updateAppSettings(self)

        # Orchestrate the wallpaper + per-panel managers + demo data.
        self.gui = GuiFunctions(self)
        self.gui.initialize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
