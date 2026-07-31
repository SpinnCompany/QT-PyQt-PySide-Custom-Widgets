########################################################################
## QCustomRadarChart example
##
## A product-comparison radar: three candidates across five measures, with
## controls for the grid style, ring count, fill opacity and rotation. Hover a
## polygon to emphasise it; click near an axis to see which measure it is.
## Rendered with QPainter only - no QtCharts.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets, QtCore

from Custom_Widgets.QCustomRadarChart import QCustomRadarChart
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens

AXES = ["Speed", "Power", "Range", "Agility", "Cost"]
SERIES = [("Alpha", [80, 60, 90, 70, 50]),
          ("Beta", [60, 90, 50, 80, 70]),
          ("Gamma", [70, 70, 65, 55, 90])]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRadarChart")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self._theme = "light"

        self.chart = QCustomRadarChart(axes=AXES, series=SERIES)
        self.chart.maxValue = 100
        self.chart.showRingLabels = True
        self.chart.setMinimumHeight(320)
        self.chart.seriesHovered.connect(self._onHover)
        self.chart.axisClicked.connect(self._onAxis)
        layout.addWidget(self.chart, 1)

        self.status = QtWidgets.QLabel("Hover a shape, or click near an axis")
        layout.addWidget(self.status)

        row = QtWidgets.QHBoxLayout()

        self.gridBox = QtWidgets.QComboBox()
        self.gridBox.addItems(["polygon", "circle"])
        self.gridBox.currentTextChanged.connect(self._setGrid)
        row.addWidget(QtWidgets.QLabel("Grid"))
        row.addWidget(self.gridBox)

        rings = QtWidgets.QSpinBox()
        rings.setRange(1, 10)
        rings.setValue(self.chart.rings)
        rings.valueChanged.connect(self._setRings)
        row.addWidget(QtWidgets.QLabel("Rings"))
        row.addWidget(rings)

        opacity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        opacity.setRange(0, 100)
        opacity.setValue(int(self.chart.fillOpacity * 100))
        opacity.valueChanged.connect(self._setOpacity)
        row.addWidget(QtWidgets.QLabel("Fill"))
        row.addWidget(opacity, 1)

        angle = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        angle.setRange(0, 359)
        angle.setValue(self.chart.startAngle)
        angle.valueChanged.connect(self._setAngle)
        row.addWidget(QtWidgets.QLabel("Rotate"))
        row.addWidget(angle, 1)
        layout.addLayout(row)

        buttons = QtWidgets.QHBoxLayout()
        for text, slot in (("Markers", self._toggleMarkers),
                           ("Legend", self._toggleLegend),
                           ("Ring labels", self._toggleRingLabels),
                           ("Drop Gamma", self._dropLast),
                           ("Reset", self._reset),
                           ("Light / dark", self._toggleTheme)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            buttons.addWidget(btn)
        buttons.addStretch(1)
        layout.addLayout(buttons)

        self.resize(620, 620)

    def _onHover(self, index):
        if index < 0:
            self.status.setText("Hover a shape, or click near an axis")
            return
        name, values = self.chart.series()[index]
        pairs = ", ".join("%s %g" % (AXES[i], v) for i, v in enumerate(values))
        self.status.setText("%s — %s" % (name, pairs))

    def _onAxis(self, index):
        self.status.setText("axis %d: %s" % (index, self.chart.axes()[index]))

    def _setGrid(self, value):
        self.chart.gridStyle = value

    def _setRings(self, value):
        self.chart.rings = value

    def _setOpacity(self, value):
        self.chart.fillOpacity = value / 100.0

    def _setAngle(self, value):
        self.chart.startAngle = value

    def _toggleMarkers(self):
        self.chart.showMarkers = not self.chart.showMarkers

    def _toggleLegend(self):
        self.chart.showLegend = not self.chart.showLegend

    def _toggleRingLabels(self):
        self.chart.showRingLabels = not self.chart.showRingLabels

    def _dropLast(self):
        self.chart.removeSeries(self.chart.seriesCount() - 1)

    def _reset(self):
        self.chart.setSeries(SERIES)

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
