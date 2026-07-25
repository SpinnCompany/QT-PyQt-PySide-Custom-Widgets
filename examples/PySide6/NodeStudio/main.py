########################################################################
## NODE STUDIO — a node-based AI creative-tool UI built on Custom_Widgets.
## Showcases the new QCustomNodeGraph + QCustomMediaTimeline widgets in a
## real forms-pipeline app (ui -> src, json themes, scss tokens, GuiFunctions).
## QT GUI BY SPINN TV (YOUTUBE)
########################################################################

import sys

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtWidgets import QApplication

from gui.GuiFunctions import GuiFunctions


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        enable_hot_reload(self, self.build)

    def build(self):
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})
        self.show()
        QAppSettings.updateAppSettings(self)

        self.gui = GuiFunctions(self)
        self.gui.initialize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
