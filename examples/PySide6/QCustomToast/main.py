########################################################################
## QCustomToast - stacked notifications example
##
## Buttons trigger each toast type; toasts stack in the chosen corner and
## reflow as they auto-dismiss. Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomToast import QCustomToast
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens

POSITIONS = ["top-right", "top-left", "bottom-right", "bottom-left",
             "top-center", "bottom-center"]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomToast Example")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        self.pos = QtWidgets.QComboBox()
        self.pos.addItems(POSITIONS)
        form = QtWidgets.QHBoxLayout()
        form.addWidget(QtWidgets.QLabel("Corner:"))
        form.addWidget(self.pos)
        form.addStretch(1)
        layout.addLayout(form)

        grid = QtWidgets.QGridLayout()
        specs = [("Success", "success"), ("Error", "error"),
                 ("Warning", "warning"), ("Info", "info")]
        for i, (label, variant) in enumerate(specs):
            btn = QCustomQPushButton(label)
            btn.variant = "primary" if variant == "info" else variant if variant in (
                "success", "destructive") else "secondary"
            btn.clicked.connect(lambda _=False, v=variant, t=label: self._toast(v, t))
            grid.addWidget(btn, i // 2, i % 2)
        layout.addLayout(grid)
        layout.addStretch(1)

    def _toast(self, variant, title):
        messages = {
            "success": "Your changes were saved.",
            "error": "Something went wrong. Please retry.",
            "warning": "Your session expires soon.",
            "info": "A new update is available.",
        }
        QCustomToast.show_toast(self, messages[variant], variant=variant,
                                title=title, duration=4000,
                                position=self.pos.currentText())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(560, 360)
    window.show()
    sys.exit(app.exec())
