########################################################################
## QCustomGradientText example
##
## Gradient-filled headlines, optionally sliding. QSS cannot do this:\n## there is no text-fill gradient, so the text is painted.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomGradientText import QCustomGradientText
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomGradientText")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        self.texts = []
        for caption, stops in (("Build something great", "0:#2563eb,1:#a855f7"),
                               ("Ship it today", "0:#f59e0b,0.5:#ef4444,1:#7c3aed"),
                               ("Zero to one", "0:#0ea5e9,1:#065f46")):
            widget = QCustomGradientText(text=caption)
            widget.stopsCsv = stops
            layout.addWidget(widget)
            self.texts.append(widget)

        row = QtWidgets.QHBoxLayout()
        angle = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        angle.setRange(0, 359)
        angle.valueChanged.connect(self._setAngle)
        row.addWidget(QtWidgets.QLabel("Angle"))
        row.addWidget(angle, 1)

        animate = QtWidgets.QPushButton("Animate")
        animate.clicked.connect(self._toggleAnimation)
        row.addWidget(animate)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(620, 320)

    def _setAngle(self, value):
        for widget in self.texts:
            widget.angle = value

    def _toggleAnimation(self):
        for widget in self.texts:
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
