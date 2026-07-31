########################################################################
## QCustomRadialBars example
##
## Activity rings: concentric arcs comparing values that do not sum to a
## whole. Hover a ring to highlight it.
## Rendered with QPainter only - no QtCharts.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomRadialBars import QCustomRadialBars
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomRadialBars")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self._theme = "light"

        self.chart = QCustomRadialBars(bars=[
            ("Move", 82), ("Exercise", 64), ("Stand", 95)])
        self.chart.setMinimumHeight(340)
        self.chart.barHovered.connect(self._onHover)
        layout.addWidget(self.chart, 1)

        row = QtWidgets.QHBoxLayout()
        thickness = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        thickness.setRange(4, 40)
        thickness.setValue(self.chart.thickness)
        thickness.valueChanged.connect(
            lambda v: setattr(self.chart, "thickness", v))
        row.addWidget(QtWidgets.QLabel("Thickness"))
        row.addWidget(thickness, 1)

        angle = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        angle.setRange(0, 359)
        angle.setValue(self.chart.startAngle)
        angle.valueChanged.connect(lambda v: setattr(self.chart, "startAngle", v))
        row.addWidget(QtWidgets.QLabel("Start"))
        row.addWidget(angle, 1)

        for text, attr in (("Rounded", "rounded"), ("Track", "showTrack"),
                           ("Clockwise", "clockwise")):
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

        self.status = QtWidgets.QLabel("Hover a ring")
        layout.addWidget(self.status)
        self.resize(560, 620)

    def _onHover(self, index):
        if index < 0:
            self.status.setText("Hover a ring")
            return
        label, value = self.chart.bars()[index]
        self.status.setText("%s — %g (%.0f%% of max)"
                            % (label, value, self.chart.fractionFor(index) * 100))


    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
