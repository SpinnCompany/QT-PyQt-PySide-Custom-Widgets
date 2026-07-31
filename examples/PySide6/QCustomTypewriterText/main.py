########################################################################
## QCustomTypewriterText example
##
## A rotating headline that types, holds, erases and moves on.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomTypewriterText import QCustomTypewriterText
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomTypewriterText")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        self.typer = QCustomTypewriterText(
            phrases=["Build faster.", "Ship sooner.", "Sleep better."])
        self.typer.fontScale = 1.4 if hasattr(self.typer, "fontScale") else None
        self.typer.phraseFinished.connect(
            lambda phrase: self.status.setText("finished: %s" % phrase))
        layout.addWidget(self.typer)
        self.status = QtWidgets.QLabel("typing...")
        layout.addWidget(self.status)

        row = QtWidgets.QHBoxLayout()
        speed = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        speed.setRange(10, 200)
        speed.setValue(65)
        speed.valueChanged.connect(lambda v: setattr(self.typer, "typeSpeed", v))
        row.addWidget(QtWidgets.QLabel("Speed"))
        row.addWidget(speed, 1)

        for text, slot in (("Start", lambda: self.typer.start()),
                           ("Stop", lambda: self.typer.stop()),
                           ("Skip", lambda: self.typer.skip()),
                           ("Caret", self._toggleCaret)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            row.addWidget(btn)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(560, 260)

    def _toggleCaret(self):
        self.typer.showCaret = not self.typer.showCaret


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
