########################################################################
## QCustomDateEdit / QCustomTimeEdit / QCustomDateRangeEdit example
##
## Date field with a calendar popup, a time field, and a start/end range
## picker that keeps end >= start. Styled from design tokens. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QDate

from Custom_Widgets.QCustomDateTimeEdit import (QCustomDateEdit, QCustomTimeEdit,
                                                QCustomDateRangeEdit)
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomDateTimeEdit Example")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        form = QtWidgets.QFormLayout(central)

        self.date = QCustomDateEdit()
        self.time = QCustomTimeEdit()
        self.range = QCustomDateRangeEdit()
        self.range.setDateRange(QDate.currentDate(), QDate.currentDate().addDays(7))

        self.result = QtWidgets.QLabel("-")
        self.date.dateChanged.connect(
            lambda d: self.result.setText("Date: %s" % d.toString("yyyy-MM-dd")))
        self.range.rangeChanged.connect(
            lambda s, e: self.result.setText("Range: %s -> %s"
                                             % (s.toString("MMM d"), e.toString("MMM d"))))

        form.addRow("Date:", self.date)
        form.addRow("Time:", self.time)
        form.addRow("Range:", self.range)
        form.addRow("Result:", self.result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tokens = DesignTokens(theme="light")
    app.setStyleSheet("QMainWindow, QWidget { background-color: %s; color: %s; }"
                      % (tokens.role("surface"), tokens.role("on-surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(460, 220)
    window.show()
    sys.exit(app.exec())
