########################################################################
## QCustomTreeWidget + QCustomDrawer + QCustomStepper example
##
## A tree, a stepper with Back/Next, and a left drawer (opened by a button).
## Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomTreeWidget import QCustomTreeWidget
from Custom_Widgets.QCustomDrawer import QCustomDrawer
from Custom_Widgets.QCustomStepper import QCustomStepper
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tree / Drawer / Stepper")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # stepper + nav
        self.stepper = QCustomStepper()
        self.stepper.setSteps(["Account", "Profile", "Confirm", "Done"])
        layout.addWidget(self.stepper)
        nav = QtWidgets.QHBoxLayout()
        back = QCustomQPushButton("Back"); back.variant = "outline"
        nxt = QCustomQPushButton("Next"); nxt.variant = "primary"
        back.clicked.connect(self.stepper.previous)
        nxt.clicked.connect(self.stepper.next)
        nav.addWidget(back); nav.addStretch(1); nav.addWidget(nxt)
        layout.addLayout(nav)

        # tree
        self.tree = QCustomTreeWidget()
        self.tree.setItems([
            {"text": "src", "expanded": True, "children": [
                {"text": "widgets", "children": ["button.py", "table.py"]},
                "main.py"]},
            {"text": "tests", "children": ["test_button.py"]},
        ])
        layout.addWidget(self.tree, 1)

        # drawer trigger
        openBtn = QCustomQPushButton("Open drawer")
        openBtn.variant = "secondary"
        openBtn.clicked.connect(self._openDrawer)
        layout.addWidget(openBtn)

        self.drawer = QCustomDrawer(self, side="left", size=260)
        self.drawer.addWidget(QtWidgets.QLabel("<b>Navigation</b>"))
        for name in ("Dashboard", "Projects", "Settings"):
            b = QCustomQPushButton(name); b.variant = "ghost"
            self.drawer.addWidget(b)
        self.drawer.contentLayout().addStretch(1)

    def _openDrawer(self):
        self.drawer.open()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(560, 520)
    window.show()
    sys.exit(app.exec())
