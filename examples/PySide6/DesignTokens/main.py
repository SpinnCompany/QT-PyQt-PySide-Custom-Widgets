########################################################################
## Design tokens + variant/size - QCustomQPushButton
##
## Shows every button variant x size, styled entirely from design tokens,
## with a live light/dark theme toggle. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens

VARIANTS = ["primary", "secondary", "outline", "ghost", "destructive"]
SIZES = ["sm", "md", "lg"]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Design Tokens - variant / size")
        self.theme = "light"

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        outer = QtWidgets.QVBoxLayout(central)

        # theme toggle
        top = QtWidgets.QHBoxLayout()
        self.toggle = QCustomQPushButton("Switch to dark")
        self.toggle.variant = "outline"
        self.toggle.clicked.connect(self._toggleTheme)
        top.addWidget(QtWidgets.QLabel("Theme:"))
        top.addWidget(self.toggle)
        top.addStretch(1)
        outer.addLayout(top)

        # grid: one row per variant, one column per size
        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel(""), 0, 0)
        for c, size in enumerate(SIZES):
            grid.addWidget(QtWidgets.QLabel("<b>%s</b>" % size), 0, c + 1)
        for row, variant in enumerate(VARIANTS):
            grid.addWidget(QtWidgets.QLabel("<b>%s</b>" % variant), row + 1, 0)
            for col, size in enumerate(SIZES):
                btn = QCustomQPushButton(variant.capitalize())
                btn.variant = variant
                btn.sizeVariant = size
                grid.addWidget(btn, row + 1, col + 1)
        outer.addLayout(grid)
        outer.addStretch(1)

    def _toggleTheme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.toggle.setText("Switch to light" if self.theme == "dark"
                            else "Switch to dark")
        apply_theme(self.theme)


def apply_theme(theme):
    app = QtWidgets.QApplication.instance()
    tokens = DesignTokens(theme=theme)
    # reset to just the window chrome each time, then let applyDesignTokens
    # append its (marker-delimited) component block -> no accumulation
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_theme("light")
    window = MainWindow()
    window.resize(520, 420)
    window.show()
    sys.exit(app.exec())
