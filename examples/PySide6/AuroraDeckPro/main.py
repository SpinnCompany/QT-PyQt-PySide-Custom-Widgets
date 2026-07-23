########################################################################
## AURORA DECK PRO — application entry point
## QT GUI BY SPINN TV (YOUTUBE)
########################################################################

import os
import sys

# Make the app location-independent: the project root is THIS file's folder.
from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

# Custom widgets framework (exposes QCustomMainWindow, loadJsonStyle,
# enable_hot_reload, QApplication, ...). The compiled Ui_ modules are imported
# INSIDE build() so hot reload picks up freshly regenerated modules.
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtWidgets import QApplication

from gui.GuiFunctions import GuiFunctions


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        # enable_hot_reload runs build() once now, then re-runs it whenever a
        # compiled Ui_ module changes — no restart needed.
        enable_hot_reload(self, self.build)

    def build(self):
        """(Re)construct the UI, apply the theme, and wire the app.

        Imports the Ui_ class HERE (not at module top) so a hot-reloaded module
        is picked up. Re-runs safely on every rebuild.
        """
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Apply the Aurora Dark / Aurora Light themes from the JSON stylesheet.
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()

        # Generate theme icons + apply settings (run AFTER show()).
        QAppSettings.updateAppSettings(self)

        # Orchestrate the pages (nav + per-page managers).
        self.gui = GuiFunctions(self)
        self.gui.initialize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
