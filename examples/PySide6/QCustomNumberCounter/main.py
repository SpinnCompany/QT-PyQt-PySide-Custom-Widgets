########################################################################
## QCustomNumberCounter example
##
## Animated count-ups with formatting: separators, decimals, affixes.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomNumberCounter import QCustomNumberCounter
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomNumberCounter")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        self.counters = []
        for label, kwargs in (("Users", dict(suffix="+")),
                              ("Revenue", dict(prefix="$")),
                              ("Uptime", dict(suffix="%"))):
            heading = QtWidgets.QLabel(label)
            font = heading.font(); font.setBold(True); heading.setFont(font)
            layout.addWidget(heading)
            counter = QCustomNumberCounter(**kwargs)
            counter.fontScale = 1.8
            counter.alignment = "left"
            layout.addWidget(counter)
            self.counters.append(counter)
        self.counters[1].decimals = 2
        self.counters[2].decimals = 1

        row = QtWidgets.QHBoxLayout()
        for text, values in (("Count up", (12480, 98432.5, 99.9)),
                             ("Different", (3120, 45210.25, 87.4)),
                             ("Reset", (0, 0, 0))):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(lambda _=False, v=values: self._apply(v))
            row.addWidget(btn)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(560, 300)

    def _apply(self, values):
        for counter, value in zip(self.counters, values):
            counter.setValue(value)


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
