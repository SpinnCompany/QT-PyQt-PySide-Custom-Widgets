########################################################################
## QCustomScatterChart example
##
## Two correlated samples plus a bubble plot sized by a third value. Hover a
## marker for its coordinates, click one to pin it to the status line, and use
## the controls to change marker shape, size and tick density.
## Rendered with QPainter only - no QtCharts.
## Run:
##     python main.py
########################################################################
import math
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomScatterChart import QCustomScatterChart
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


def _sample(count=28, phase=0.0, spread=12.0, seed=11):
    """A deterministic scatter, so the demo looks the same every run."""
    points, state = [], seed
    for i in range(count):
        state = (state * 1103515245 + 12345) % 2147483648
        jitter = ((state >> 16) % 1000) / 1000.0 - 0.5
        points.append((i, 30 + spread * math.sin(i / 3.0 + phase) + jitter * 6))
    return points


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomScatterChart")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self._theme = "light"

        self.chart = QCustomScatterChart(
            series=[("Control", _sample()),
                    ("Treatment", _sample(phase=1.4, spread=16.0, seed=29))])
        self.chart.xAxisTitle = "Session"
        self.chart.yAxisTitle = "Score"
        self.chart.setMinimumHeight(280)
        self.chart.pointHovered.connect(self._onHover)
        self.chart.pointClicked.connect(self._onClick)
        layout.addWidget(self.chart, 2)

        self.bubbles = QCustomScatterChart(
            series=[("Segments", [(1, 12, 10), (2, 26, 26), (3, 18, 16),
                                  (4, 33, 34), (5, 22, 12), (6, 29, 20)])])
        self.bubbles.xAxisTitle = "Quarter"
        self.bubbles.yAxisTitle = "Revenue"
        self.bubbles.markerOpacity = 0.55
        self.bubbles.setMinimumHeight(200)
        layout.addWidget(self.bubbles, 1)

        row = QtWidgets.QHBoxLayout()

        shape = QtWidgets.QComboBox()
        shape.addItems(["circle", "square", "diamond", "triangle"])
        shape.currentTextChanged.connect(self._setShape)
        row.addWidget(QtWidgets.QLabel("Marker"))
        row.addWidget(shape)

        size = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        size.setRange(3, 24)
        size.setValue(int(self.chart.markerSize))
        size.valueChanged.connect(self._setSize)
        row.addWidget(QtWidgets.QLabel("Size"))
        row.addWidget(size, 1)

        ticks = QtWidgets.QSpinBox()
        ticks.setRange(2, 12)
        ticks.setValue(self.chart.tickCount)
        ticks.valueChanged.connect(self._setTicks)
        row.addWidget(QtWidgets.QLabel("Ticks"))
        row.addWidget(ticks)

        for text, slot in (("Grid", self._toggleGrid),
                           ("Legend", self._toggleLegend),
                           ("Light / dark", self._toggleTheme)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            row.addWidget(btn)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("Hover a marker for its coordinates")
        layout.addWidget(self.status)
        self.resize(720, 640)

    def _onHover(self, si, pi):
        if si < 0:
            self.status.setText("Hover a marker for its coordinates")
            return
        name, points = self.chart.series()[si]
        x, y, _size = points[pi]
        self.status.setText("%s — x %g, y %.2f" % (name, x, y))

    def _onClick(self, si, pi):
        name, points = self.chart.series()[si]
        x, y, _size = points[pi]
        self.status.setText("pinned %s point %d — x %g, y %.2f" % (name, pi, x, y))

    def _setShape(self, value):
        self.chart.markerShape = value
        self.bubbles.markerShape = value

    def _setSize(self, value):
        self.chart.markerSize = float(value)

    def _setTicks(self, value):
        self.chart.tickCount = value
        self.bubbles.tickCount = value

    def _toggleGrid(self):
        self.chart.showGrid = not self.chart.showGrid
        self.bubbles.showGrid = self.chart.showGrid

    def _toggleLegend(self):
        self.chart.showLegend = not self.chart.showLegend

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
