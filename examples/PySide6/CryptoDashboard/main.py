########################################################################
## CRYPTO — Wallet & trading dashboard, built the CORRECT Custom_Widgets way.
##
## The maintainable pipeline (not a pure-code app):
##   ui/*.ui  ->  compiled src/ui_*.py       (Custom_Widgets --convert-ui)
##   json-styles/style.json                  (Crypto Light / Crypto Dark themes)
##   Qss/scss/*.scss  ($TOKENS, no hard-coded hex)
##   gui/GuiFunctions.py                      (orchestrator + managers + workers)
##
## Build the compiled forms first:
##   Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
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

        # Apply the Crypto Light / Dark themes from the JSON stylesheet.
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()

        # Generate theme icons + compile SCSS + paint the app (run AFTER show()).
        QAppSettings.updateAppSettings(self)

        # Orchestrate nav + per-page managers + background workers.
        self.gui = GuiFunctions(self)
        self.gui.initialize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
