########################################################################
## QCustomSocialButton example
##
## Brand-coloured sign-in buttons; the foreground contrast is chosen\n## automatically from the brand colour.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomSocialButton import QCustomSocialButton
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomSocialButton")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        ICON = "Custom_Widgets/components/icons/rocket_launch.png"
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        self.buttons = []
        brands = ["github", "google", "x", "facebook", "linkedin", "discord",
                  "slack", "apple", "whatsapp"]
        for index, brand in enumerate(brands):
            widget = QCustomSocialButton(brand=brand, icon=ICON)
            widget.clicked.connect(
                lambda b=brand: self.status.setText("clicked %s" % b))
            grid.addWidget(widget, index // 3, index % 3)
            self.buttons.append(widget)
        layout.addLayout(grid)
        self.status = QtWidgets.QLabel("Click a brand")
        layout.addWidget(self.status)

        row = QtWidgets.QHBoxLayout()
        variant = QtWidgets.QComboBox()
        variant.addItems(["solid", "outline", "soft"])
        variant.currentTextChanged.connect(self._setVariant)
        row.addWidget(QtWidgets.QLabel("Variant"))
        row.addWidget(variant)

        shape = QtWidgets.QComboBox()
        shape.addItems(["rounded", "pill", "square"])
        shape.currentTextChanged.connect(self._setShape)
        row.addWidget(QtWidgets.QLabel("Shape"))
        row.addWidget(shape)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addStretch(1)
        self.resize(620, 520)

    def _setVariant(self, value):
        for widget in self.buttons:
            widget.variant = value

    def _setShape(self, value):
        for widget in self.buttons:
            widget.shape = value


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
