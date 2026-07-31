########################################################################
## QCustomRangeBarChart example
##
## Daily temperature ranges as floating bars: each bar spans a low to a
## high rather than sitting on a baseline.
## Rendered with QPainter only - no QtCharts.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomRangeBarChart import QCustomRangeBarChart
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRangeBarChart")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self._theme = "light"

        self.chart = QCustomRangeBarChart(ranges=[
            ("Mon", 4, 12), ("Tue", 6, 15), ("Wed", 3, 9),
            ("Thu", 8, 17), ("Fri", 5, 11), ("Sat", 7, 14), ("Sun", 2, 8)])
        self.chart.showBounds = True
        self.chart.setMinimumHeight(320)
        self.chart.barHovered.connect(self._onHover)
        layout.addWidget(self.chart, 1)

        row = QtWidgets.QHBoxLayout()
        orient = QtWidgets.QComboBox()
        orient.addItems(["vertical", "horizontal"])
        orient.currentTextChanged.connect(
            lambda v: setattr(self.chart, "orientation", v))
        row.addWidget(QtWidgets.QLabel("Orientation"))
        row.addWidget(orient)

        width = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        width.setRange(10, 100)
        width.setValue(int(self.chart.barWidthRatio * 100))
        width.valueChanged.connect(
            lambda v: setattr(self.chart, "barWidthRatio", v / 100.0))
        row.addWidget(QtWidgets.QLabel("Bar width"))
        row.addWidget(width, 1)

        bounds = QtWidgets.QPushButton("Bounds")
        bounds.clicked.connect(
            lambda: setattr(self.chart, "showBounds", not self.chart.showBounds))
        row.addWidget(bounds)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("Hover a bar for its range")
        layout.addWidget(self.status)
        self.resize(640, 520)

    def _onHover(self, index):
        if index < 0:
            self.status.setText("Hover a bar for its range")
            return
        label, low, high = self.chart.ranges()[index]
        self.status.setText("%s — %g to %g (span %g)" % (label, low, high, high - low))


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
