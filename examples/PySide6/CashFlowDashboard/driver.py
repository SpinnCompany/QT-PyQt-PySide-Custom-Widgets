"""Headless screenshot driver — verify rendering in both themes.

    QT_QPA_PLATFORM=offscreen .venv/bin/python driver.py --shots shots

Grabs the whole window to shots/light.png then flips the theme and grabs
shots/dark.png, then quits. (Offscreen bare grab is fine here because we drive
it through the real app event loop with QTimers, per the verify gotcha.)
"""

import os
import sys

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *                       # noqa: F401,F403
from Custom_Widgets.QAppSettings import QAppSettings
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QTimer

from gui.GuiFunctions import GuiFunctions


class MainWindow(QCustomMainWindow):               # noqa: F405
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        enable_hot_reload(self, self.build)         # noqa: F405

    def build(self):
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})  # noqa: F405
        self.show()
        QAppSettings.updateAppSettings(self)
        self.gui = GuiFunctions(self)
        self.gui.initialize()


def main():
    out = "shots"
    if "--shots" in sys.argv:
        out = sys.argv[sys.argv.index("--shots") + 1]
    os.makedirs(out, exist_ok=True)

    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1380, 880)
    win.show()

    def grab(name):
        win.grab().save(os.path.join(out, name))
        print("saved", os.path.join(out, name))

    eng = getattr(win.gui, "themeEngine", None)

    def set_theme(name):
        try:
            eng.setTheme(name)
        except Exception as e:
            print("setTheme failed:", e)

    # Deterministic sequence with generous settle windows (QSettings persists the
    # last theme across runs, and icon regen is async — so FORCE each theme rather
    # than trust the persisted default).
    QTimer.singleShot(600,  lambda: set_theme("Cashflow Light"))
    QTimer.singleShot(2600, lambda: grab("light.png"))
    QTimer.singleShot(3000, lambda: set_theme("Cashflow Dark"))
    QTimer.singleShot(5200, lambda: grab("dark.png"))
    QTimer.singleShot(5600, app.quit)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
