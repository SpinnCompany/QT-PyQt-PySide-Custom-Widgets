########################################################################
## QCustomCopyButton example
##
## Copy-to-clipboard with confirmation, in all three variants.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomCopyButton import QCustomCopyButton
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomCopyButton")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        self.buttons = []
        for variant in ("outline", "ghost", "solid"):
            widget = QCustomCopyButton(payload="sk-live-%s-abc123" % variant,
                                       text="Copy %s key" % variant)
            widget.variant = variant
            widget.copied.connect(
                lambda text: self.status.setText("copied %d characters" % len(text)))
            layout.addWidget(widget)
            self.buttons.append(widget)
        iconOnly = QCustomCopyButton(payload="short")
        iconOnly.iconOnly = True
        layout.addWidget(iconOnly)
        self.buttons.append(iconOnly)
        self.status = QtWidgets.QLabel("Press a button, then paste somewhere")
        layout.addWidget(self.status)

        row = QtWidgets.QHBoxLayout()
        delay = QtWidgets.QSpinBox()
        delay.setRange(0, 6000)
        delay.setSingleStep(200)
        delay.setValue(1600)
        delay.valueChanged.connect(self._setDelay)
        row.addWidget(QtWidgets.QLabel("Reset ms"))
        row.addWidget(delay)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(560, 260)

    def _setDelay(self, value):
        for widget in self.buttons:
            widget.resetDelay = value


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
