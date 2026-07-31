########################################################################
## QCustomSparklesText example
##
## Text with a deterministic sparkle field: same seed, same render, so\n## a screenshot is reproducible.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomSparklesText import QCustomSparklesText
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomSparklesText")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        self.sparkles = QCustomSparklesText(text="Powered by AI")
        self.sparkles.setMinimumHeight(90)
        layout.addWidget(self.sparkles)
        self.second = QCustomSparklesText(text="Magic inside")
        self.second.seed = 42
        self.second.colorsCsv = "#16a34a,#0ea5e9"
        self.second.setMinimumHeight(90)
        layout.addWidget(self.second)

        row = QtWidgets.QHBoxLayout()
        count = QtWidgets.QSpinBox()
        count.setRange(0, 60)
        count.setValue(14)
        count.valueChanged.connect(self._setCount)
        row.addWidget(QtWidgets.QLabel("Sparkles"))
        row.addWidget(count)

        seed = QtWidgets.QSpinBox()
        seed.setRange(0, 999)
        seed.setValue(7)
        seed.valueChanged.connect(lambda v: setattr(self.sparkles, "seed", v))
        row.addWidget(QtWidgets.QLabel("Seed"))
        row.addWidget(seed)

        animate = QtWidgets.QPushButton("Animate")
        animate.clicked.connect(self._toggle)
        row.addWidget(animate)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(560, 300)

    def _setCount(self, value):
        self.sparkles.sparkleCount = value
        self.second.sparkleCount = value

    def _toggle(self):
        for widget in (self.sparkles, self.second):
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
