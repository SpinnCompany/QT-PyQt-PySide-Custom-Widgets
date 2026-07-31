########################################################################
## QCustomRadioButton example
##
## Three single-choice groups: plan selection (auto-exclusive siblings in a
## container), a size row in the three size variants, and a non-exclusive pair
## showing what `autoExclusive = False` is for. Styled from design tokens,
## with a live light/dark switch so you can see the colours re-tokenize.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRadioButton")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)
        self._theme = "light"

        # -- plan picker: exclusivity comes free from sharing a parent -----
        layout.addWidget(self._heading("Choose a plan"))
        plans = QtWidgets.QWidget()
        plansBox = QtWidgets.QVBoxLayout(plans)
        plansBox.setContentsMargins(0, 0, 0, 0)
        plansBox.setSpacing(10)
        for label, value, checked in (("Community - free forever", "free", True),
                                      ("Pro - $12/month", "pro", False),
                                      ("Studio - $29/month", "studio", False)):
            radio = QCustomRadioButton(plans, text=label, value=value, checked=checked)
            radio.selected.connect(self._onPlan)
            plansBox.addWidget(radio)
        layout.addWidget(plans)

        # -- the three size variants --------------------------------------
        layout.addWidget(self._heading("Size variants"))
        sizes = QtWidgets.QWidget()
        sizeRow = QtWidgets.QHBoxLayout(sizes)
        sizeRow.setContentsMargins(0, 0, 0, 0)
        sizeRow.setSpacing(24)
        for variant in ("sm", "md", "lg"):
            radio = QCustomRadioButton(sizes, text=variant, value=variant)
            radio.sizeVariant = variant
            radio.setChecked(variant == "md")
            sizeRow.addWidget(radio)
        sizeRow.addStretch(1)
        layout.addWidget(sizes)

        # -- autoExclusive off: both can be on at once ---------------------
        layout.addWidget(self._heading("autoExclusive = False"))
        loose = QtWidgets.QWidget()
        looseRow = QtWidgets.QHBoxLayout(loose)
        looseRow.setContentsMargins(0, 0, 0, 0)
        looseRow.setSpacing(24)
        for label in ("Independent A", "Independent B"):
            radio = QCustomRadioButton(loose, text=label)
            radio.autoExclusive = False
            looseRow.addWidget(radio)
        looseRow.addStretch(1)
        layout.addWidget(loose)

        layout.addStretch(1)
        self.status = QtWidgets.QLabel("Selected plan: free")
        layout.addWidget(self.status)

        themeBtn = QtWidgets.QPushButton("Toggle light / dark")
        themeBtn.clicked.connect(self._toggleTheme)
        layout.addWidget(themeBtn)

        self.resize(460, 520)

    @staticmethod
    def _heading(text):
        label = QtWidgets.QLabel(text)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        return label

    def _onPlan(self, value):
        self.status.setText("Selected plan: %s" % value)

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
