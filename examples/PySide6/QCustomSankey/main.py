########################################################################
## QCustomSankey example
##
## An acquisition flow: traffic sources into signups, then on to trial,
## paid and churn. Hover a node to light up everything it touches.
## Rendered with QPainter only - no QtCharts.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomSankey import QCustomSankey
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomSankey")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self._theme = "light"

        self.chart = QCustomSankey(links=[
            ("Search", "Signup", 120), ("Social", "Signup", 80),
            ("Referral", "Signup", 45), ("Signup", "Trial", 150),
            ("Signup", "Bounce", 95), ("Trial", "Paid", 70),
            ("Trial", "Churn", 80)])
        self.chart.setMinimumHeight(360)
        self.chart.nodeHovered.connect(self._onNode)
        self.chart.linkHovered.connect(self._onLink)
        self.chart.nodeClicked.connect(
            lambda name: self.status.setText("clicked %s" % name))
        layout.addWidget(self.chart, 1)

        row = QtWidgets.QHBoxLayout()
        curve = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        curve.setRange(0, 100)
        curve.setValue(int(self.chart.curvature * 100))
        curve.valueChanged.connect(
            lambda v: setattr(self.chart, "curvature", v / 100.0))
        row.addWidget(QtWidgets.QLabel("Curve"))
        row.addWidget(curve, 1)

        opacity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        opacity.setRange(5, 100)
        opacity.setValue(int(self.chart.linkOpacity * 100))
        opacity.valueChanged.connect(
            lambda v: setattr(self.chart, "linkOpacity", v / 100.0))
        row.addWidget(QtWidgets.QLabel("Ribbon"))
        row.addWidget(opacity, 1)

        values = QtWidgets.QPushButton("Values")
        values.clicked.connect(
            lambda: setattr(self.chart, "showValues", not self.chart.showValues))
        row.addWidget(values)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("Hover a node or a ribbon")
        layout.addWidget(self.status)
        self.resize(720, 560)

    def _onNode(self, name):
        if not name:
            self.status.setText("Hover a node or a ribbon")
            return
        self.status.setText("%s — throughput %g"
                            % (name, self.chart.nodeValue(name)))

    def _onLink(self, index):
        if index < 0:
            return
        source, target, value = self.chart.links()[index]
        self.status.setText("%s to %s — %g" % (source, target, value))


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
