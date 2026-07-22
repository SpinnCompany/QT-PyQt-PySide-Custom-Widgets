########################################################################
## QCustomPagination + QCustomPopover + QCustomSegmentedControl example
##
## A segmented view switcher, a click-to-open popover, and pagination.
## Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomPagination import QCustomPagination
from Custom_Widgets.QCustomPopover import QCustomPopover
from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pagination / Popover / Segmented")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # segmented control
        layout.addWidget(QtWidgets.QLabel("View:"))
        seg = QCustomSegmentedControl()
        seg.setSegments([("Day", "d"), ("Week", "w"), ("Month", "m"), ("Year", "y")])
        seg.currentChanged.connect(lambda i: self.status.setText("View: %s" % seg.currentData()))
        srow = QtWidgets.QHBoxLayout(); srow.addWidget(seg); srow.addStretch(1)
        layout.addLayout(srow)

        # popover
        layout.addWidget(QtWidgets.QLabel("Popover:"))
        trigger = QCustomQPushButton("Show details")
        trigger.variant = "outline"
        self.pop = QCustomPopover.attach(trigger, placement="bottom")
        self.pop.addWidget(QtWidgets.QLabel("<b>Details</b>"))
        self.pop.addWidget(QtWidgets.QLabel("Rich content lives in a popover,\nwith an arrow to its anchor."))
        prow = QtWidgets.QHBoxLayout(); prow.addWidget(trigger); prow.addStretch(1)
        layout.addLayout(prow)

        layout.addStretch(1)

        # pagination
        self.pager = QCustomPagination(pageCount=20)
        self.pager.pageChanged.connect(lambda p: self.status.setText("Page %d" % p))
        layout.addWidget(self.pager)

        self.status = QtWidgets.QLabel("-")
        layout.addWidget(self.status)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(480, 340)
    window.show()
    sys.exit(app.exec())
