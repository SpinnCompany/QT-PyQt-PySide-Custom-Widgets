########################################################################
## QCustomFeaturedIcon example
##
## Every variant, shape and size of the decorative icon tile.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomFeaturedIcon import QCustomFeaturedIcon
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomFeaturedIcon")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        ICON = "Custom_Widgets/components/icons/rocket_launch.png"
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(14)
        self.icons = []
        for col, variant in enumerate(("tinted", "filled", "outline", "gradient")):
            for rowIndex, shape in enumerate(("rounded", "circle", "square")):
                widget = QCustomFeaturedIcon(icon=ICON, variant=variant, shape=shape)
                widget.sizeVariant = "lg"
                widget.clicked.connect(
                    lambda v=variant, s=shape: self.status.setText(
                        "clicked %s / %s" % (v, s)))
                grid.addWidget(widget, rowIndex, col)
                self.icons.append(widget)
        layout.addLayout(grid)
        self.status = QtWidgets.QLabel("Click a tile")
        layout.addWidget(self.status)

        row = QtWidgets.QHBoxLayout()
        sizes = QtWidgets.QComboBox()
        sizes.addItems(["sm", "md", "lg", "xl"])
        sizes.setCurrentText("lg")
        sizes.currentTextChanged.connect(self._setSize)
        row.addWidget(QtWidgets.QLabel("Size"))
        row.addWidget(sizes)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(560, 320)

    def _setSize(self, value):
        for widget in self.icons:
            widget.sizeVariant = value


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
