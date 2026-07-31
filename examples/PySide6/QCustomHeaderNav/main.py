########################################################################
## QCustomHeaderNav example
##
## A horizontal top nav. Narrow the window to watch items collapse into\n## a +N overflow rather than clipping off the edge.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomHeaderNav import QCustomHeaderNav
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomHeaderNav")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        self.nav = QCustomHeaderNav(
            items=["home=Home", "docs=Docs", "pricing=Pricing", "blog=Blog",
                   "changelog=Changelog"],
            brand="Spinn UI")
        self.nav.itemSelected.connect(
            lambda key: self.status.setText("selected %s" % key))
        self.nav.brandClicked.connect(
            lambda: self.status.setText("brand clicked"))
        self.nav.overflowClicked.connect(
            lambda: self.status.setText("overflow clicked (%d hidden)"
                                        % self.nav.hiddenCount()))
        layout.addWidget(self.nav)
        self.status = QtWidgets.QLabel("selected home")
        layout.addWidget(self.status)

        row = QtWidgets.QHBoxLayout()
        indicator = QtWidgets.QComboBox()
        indicator.addItems(["underline", "pill", "none"])
        indicator.currentTextChanged.connect(
            lambda v: setattr(self.nav, "indicator", v))
        row.addWidget(QtWidgets.QLabel("Indicator"))
        row.addWidget(indicator)

        align = QtWidgets.QComboBox()
        align.addItems(["left", "center", "right"])
        align.currentTextChanged.connect(
            lambda v: setattr(self.nav, "alignment", v))
        row.addWidget(QtWidgets.QLabel("Align"))
        row.addWidget(align)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(720, 320)


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
