########################################################################
## QCustomFunnelChart example
##
## A conversion funnel with drop-off percentages, plus the same data
## as a pyramid and rotated horizontal. Hover a stage to highlight it.
## Rendered with QPainter only - no QtCharts.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomFunnelChart import QCustomFunnelChart
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomFunnelChart")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self._theme = "light"

        self.chart = QCustomFunnelChart(stages=[
            ("Visits", 1000), ("Signups", 420), ("Trials", 180), ("Paid", 64)])
        self.chart.showPercent = True
        self.chart.setMinimumHeight(300)
        self.chart.stageHovered.connect(self._onHover)
        self.chart.stageClicked.connect(self._onClick)
        layout.addWidget(self.chart, 1)

        row = QtWidgets.QHBoxLayout()
        shape = QtWidgets.QComboBox()
        shape.addItems(["funnel", "pyramid"])
        shape.currentTextChanged.connect(lambda v: setattr(self.chart, "shape", v))
        row.addWidget(QtWidgets.QLabel("Shape"))
        row.addWidget(shape)

        orient = QtWidgets.QComboBox()
        orient.addItems(["vertical", "horizontal"])
        orient.currentTextChanged.connect(
            lambda v: setattr(self.chart, "orientation", v))
        row.addWidget(QtWidgets.QLabel("Orientation"))
        row.addWidget(orient)

        basis = QtWidgets.QComboBox()
        basis.addItems(["first", "previous"])
        basis.currentTextChanged.connect(
            lambda v: setattr(self.chart, "percentOf", v))
        row.addWidget(QtWidgets.QLabel("% of"))
        row.addWidget(basis)

        neck = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        neck.setRange(0, 80)
        neck.valueChanged.connect(
            lambda v: setattr(self.chart, "neckRatio", v / 100.0))
        row.addWidget(QtWidgets.QLabel("Neck"))
        row.addWidget(neck, 1)

        theme = QtWidgets.QPushButton("Light / dark")
        theme.clicked.connect(self._toggleTheme)
        row.addWidget(theme)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("Hover a stage for its conversion")
        layout.addWidget(self.status)
        self.resize(620, 560)

    def _onHover(self, index):
        if index < 0:
            self.status.setText("Hover a stage for its conversion")
            return
        label, value = self.chart.stages()[index]
        self.status.setText("%s — %g (%.1f%% of the first stage)"
                            % (label, value, self.chart.percentFor(index)))

    def _onClick(self, index):
        self.status.setText("clicked stage %d" % index)


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
