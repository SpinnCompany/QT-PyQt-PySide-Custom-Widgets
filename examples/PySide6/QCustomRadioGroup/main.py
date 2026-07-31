########################################################################
## QCustomRadioGroup example
##
## Three groups driven entirely through the group API: a vertical plan picker
## with explicit value=label options, a horizontal group, and one whose options
## are replaced at runtime to show that a surviving selection is kept. Includes
## a live light/dark toggle so you can watch the colours re-tokenize.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRadioGroup")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(22)
        self._theme = "light"

        # -- plan picker: value=label keeps the wire format off the UI text --
        self.plans = QCustomRadioGroup(
            options=["free=Community - free forever",
                     "pro=Pro - $12/month",
                     "studio=Studio - $29/month"],
            value="free",
            title="Choose a plan")
        self.plans.valueChanged.connect(
            lambda v: self.status.setText("plan=%s  billing=%s"
                                          % (v, self.billing.value() or "-")))
        layout.addWidget(self.plans)

        # -- horizontal group ---------------------------------------------
        self.billing = QCustomRadioGroup(
            options=["monthly=Monthly", "yearly=Yearly"],
            value="monthly",
            orientation="horizontal",
            title="Billing period")
        self.billing.valueChanged.connect(
            lambda v: self.status.setText("plan=%s  billing=%s"
                                          % (self.plans.value() or "-", v)))
        layout.addWidget(self.billing)

        # -- options replaced at runtime ------------------------------------
        self.seats = QCustomRadioGroup(options=["1", "2", "5"], value="2",
                                       orientation="horizontal",
                                       title="Seats")
        layout.addWidget(self.seats)

        swap = QtWidgets.QPushButton("Replace seat options with 2, 5, 10")
        swap.clicked.connect(self._swapSeats)
        layout.addWidget(swap)

        layout.addStretch(1)
        self.status = QtWidgets.QLabel("plan=free  billing=monthly")
        layout.addWidget(self.status)

        themeBtn = QtWidgets.QPushButton("Toggle light / dark")
        themeBtn.clicked.connect(self._toggleTheme)
        layout.addWidget(themeBtn)

        self.resize(480, 560)

    def _swapSeats(self):
        # "2" survives the swap, so the selection is preserved.
        self.seats.setOptions(["2", "5", "10"])
        self.status.setText("seats kept selection: %s" % (self.seats.value() or "none"))

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
