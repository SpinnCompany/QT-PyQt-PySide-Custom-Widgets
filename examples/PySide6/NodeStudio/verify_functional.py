"""Headless proof the SETTINGS rows are FUNCTIONAL: cycle Voice + Mode via the
same rowClicked path the UI uses, and confirm the node value + 3D preview
actually change. QT_QPA_PLATFORM=offscreen python verify_functional.py OUTDIR"""
import sys
import os

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QTimer

from gui.GuiFunctions import GuiFunctions

OUT = sys.argv[1] if len(sys.argv) > 1 else "."


class MainWindow(QCustomMainWindow):
    def __init__(self):
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


app = QApplication(sys.argv)
win = MainWindow()
win.resize(1280, 820)
win.show()


def go():
    g = win.gui
    # rows: 0 Mode, 1 Trim, 2 Think, 3 Voice, 4 Music
    before = g._nodeGraph.nodeRows("settings")[3]["value"]
    g._on_row_clicked("settings", 3)   # Voice: Happy -> Calm (blue shirt)
    g._on_row_clicked("settings", 0)   # Mode:  Fun -> Serious (glow)
    after = g._nodeGraph.nodeRows("settings")[3]["value"]
    print("VOICE %s -> %s" % (before, after))
    print("SHIRT set:", g._shirt_color is not None, "GLOW set:", g._glow_color is not None)
    win.grab().save(os.path.join(OUT, "nodestudio_functional.png"))
    print("saved")
    app.quit()


QTimer.singleShot(1400, go)
app.exec_() if hasattr(app, "exec_") else app.exec()
