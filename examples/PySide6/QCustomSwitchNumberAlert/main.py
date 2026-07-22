########################################################################
## QCustomSwitch + QCustomNumberInput + QCustomAlert example
##
## A settings-style panel: toggle switches, a quantity stepper, and inline
## alerts of every variant. Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomSwitch import QCustomSwitch
from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
from Custom_Widgets.QCustomAlert import QCustomAlert
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Switch / Number / Alert")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setSpacing(12)

        # switches
        for label, checked in (("Enable notifications", True),
                               ("Dark mode", False)):
            row = QtWidgets.QHBoxLayout()
            row.addWidget(QtWidgets.QLabel(label))
            row.addStretch(1)
            sw = QCustomSwitch(checked=checked)
            sw.toggled.connect(lambda on, l=label: self.status.setText(
                "%s: %s" % (l, "on" if on else "off")))
            row.addWidget(sw)
            layout.addLayout(row)

        # number stepper
        qrow = QtWidgets.QHBoxLayout()
        qrow.addWidget(QtWidgets.QLabel("Quantity"))
        qrow.addStretch(1)
        qty = QCustomNumberInput(minimum=1, maximum=99, value=3, step=1)
        qty.setMaximumWidth(140)
        qty.valueChanged.connect(lambda v: self.status.setText("Quantity: %s" % v))
        qrow.addWidget(qty)
        layout.addLayout(qrow)

        # price stepper (float)
        prow = QtWidgets.QHBoxLayout()
        prow.addWidget(QtWidgets.QLabel("Unit price"))
        prow.addStretch(1)
        price = QCustomNumberInput(minimum=0, maximum=1000, value=9.99,
                                   step=0.5, decimals=2)
        price.setMaximumWidth(140)
        prow.addWidget(price)
        layout.addLayout(prow)

        # alerts
        layout.addWidget(QCustomAlert(
            title="Heads up", text="Your trial ends in 3 days.", variant="info"))
        layout.addWidget(QCustomAlert(
            title="Saved", text="Settings updated successfully.", variant="success"))
        layout.addWidget(QCustomAlert(
            title="Careful", text="This action can't be undone.",
            variant="warning", dismissible=True))
        layout.addWidget(QCustomAlert(
            title="Error", text="Payment failed. Try another card.",
            variant="destructive", dismissible=True))

        layout.addStretch(1)
        self.status = QtWidgets.QLabel("-")
        layout.addWidget(self.status)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(460, 560)
    window.show()
    sys.exit(app.exec())
