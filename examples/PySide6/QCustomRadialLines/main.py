########################################################################
## QCustomRadialLines example
##
## A polar line chart for cyclical data: weekday against weekend traffic
## wrapped onto a circle, so the series closes back on itself.
## Rendered with QPainter only - no QtCharts.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomRadialLines import QCustomRadialLines
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRadialLines")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self._theme = "light"

        self.chart = QCustomRadialLines(
            series=[("Weekday", [30, 45, 60, 52, 48, 70, 64]),
                    ("Weekend", [20, 25, 40, 38, 30, 35, 28])],
            labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        self.chart.showMarkers = True
        self.chart.setMinimumHeight(360)
        self.chart.seriesHovered.connect(self._onHover)
        layout.addWidget(self.chart, 1)

        row = QtWidgets.QHBoxLayout()
        rings = QtWidgets.QSpinBox()
        rings.setRange(1, 10)
        rings.setValue(self.chart.rings)
        rings.valueChanged.connect(lambda v: setattr(self.chart, "rings", v))
        row.addWidget(QtWidgets.QLabel("Rings"))
        row.addWidget(rings)

        fill = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        fill.setRange(0, 100)
        fill.setValue(int(self.chart.fillOpacity * 100))
        fill.valueChanged.connect(
            lambda v: setattr(self.chart, "fillOpacity", v / 100.0))
        row.addWidget(QtWidgets.QLabel("Fill"))
        row.addWidget(fill, 1)

        for text, attr in (("Closed", "closed"), ("Markers", "showMarkers"),
                           ("Grid", "showGrid")):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(
                lambda _=False, a=attr: setattr(self.chart, a,
                                                not getattr(self.chart, a)))
            row.addWidget(btn)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("Hover a shape")
        layout.addWidget(self.status)
        self.resize(580, 620)

    def _onHover(self, index):
        if index < 0:
            self.status.setText("Hover a shape")
            return
        name, values = self.chart.series()[index]
        self.status.setText("%s — peak %g" % (name, max(values)))


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
