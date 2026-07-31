########################################################################
## QCustomRainbowButton example
##
## A call-to-action with a rotating conic border. The animation stops\n## while the widget is hidden.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomRainbowButton import QCustomRainbowButton
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRainbowButton")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        self.buttons = []
        for caption, kwargs in (("Get started", {}),
                                ("Upgrade", {"filled": True}),
                                ("Glow", {"glow": True})):
            widget = QCustomRainbowButton(text=caption)
            for key, value in kwargs.items():
                setattr(widget, key, value)
            widget.clicked.connect(
                lambda c=caption: self.status.setText("clicked %s" % c))
            layout.addWidget(widget)
            self.buttons.append(widget)
        self.status = QtWidgets.QLabel("Click a button")
        layout.addWidget(self.status)

        row = QtWidgets.QHBoxLayout()
        speed = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        speed.setRange(16, 200)
        speed.setValue(40)
        speed.valueChanged.connect(self._setSpeed)
        row.addWidget(QtWidgets.QLabel("Speed"))
        row.addWidget(speed, 1)

        stop = QtWidgets.QPushButton("Animate")
        stop.clicked.connect(self._toggle)
        row.addWidget(stop)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(560, 300)

    def _setSpeed(self, value):
        for widget in self.buttons:
            widget.speed = value

    def _toggle(self):
        for widget in self.buttons:
            widget.animated = not widget.animated


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
