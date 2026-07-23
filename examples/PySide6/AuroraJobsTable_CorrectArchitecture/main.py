########################################################################
## AURORA — Work · Jobs, built the CORRECT Custom_Widgets way.
##
## The maintainable pipeline (NOT a pure-code main.py — see
## ../AuroraJobsTable/ARCHITECTURE_REVIEW.md for what that broke):
##   ui/*.ui  ->  compiled src/ui_*.py       (Custom_Widgets --convert-ui)
##   json-styles/style.json                  (Aurora Light / Dark CustomThemes + StatusPalette)
##   Qss/scss/*.scss  ($TOKENS, no hard-coded hex)
##   gui/GuiFunctions.py                      (orchestrator + JobsManager + background loader)
##
## Build the compiled forms first:
##   Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
########################################################################

import os
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

        # Apply the Aurora Light / Dark themes from the JSON stylesheet.
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()

        # Generate theme icons + compile SCSS + paint the app (AFTER show()).
        QAppSettings.updateAppSettings(self)

        # Orchestrate nav + the Jobs manager + background loader.
        self.gui = GuiFunctions(self)
        self.gui.initialize()

        # Opt in to the in-app control server so the Custom_Widgets MCP can
        # OBSERVE and screenshot the REAL rendered window (no-op unless the dev
        # server sets CUSTOM_WIDGETS_APP_CONTROL). Real-display bugs never show
        # in offscreen grabs — see offscreen-grab-verify-gotcha.
        try:
            from Custom_Widgets.AppControl import maybe_start_app_control
            maybe_start_app_control(os.path.dirname(os.path.abspath(__file__)))
        except Exception:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
