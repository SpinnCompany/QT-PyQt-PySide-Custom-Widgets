"""Headless screenshot driver: boot the real app, grab the dark theme, flip to
light, grab again. Usage: QT_QPA_PLATFORM=offscreen python driver.py OUTDIR"""
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
os.makedirs(OUT, exist_ok=True)


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


def shot(name):
    win.grab().save(os.path.join(OUT, name))
    print("saved", name)


def force_dark():
    win.gui.themeEngine.setTheme("Studio Dark")
    QTimer.singleShot(1500, step_dark)


def step_dark():
    shot("nodestudio_dark.png")
    win.gui.themeEngine.setTheme("Studio Light")
    QTimer.singleShot(1500, step_light)


def step_light():
    shot("nodestudio_light.png")
    app.quit()


QTimer.singleShot(1200, force_dark)
app.exec_() if hasattr(app, "exec_") else app.exec()
print("DONE")
