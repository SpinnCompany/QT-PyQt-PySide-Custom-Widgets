########################################################################
## QCustomCandlestickChart example
##
## A 30-session price series with a readout driven by hover and click, plus
## toggles for the hollow-up-candle style, the grid and the painted tooltip.
## Rendered with QPainter only - no QtCharts.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


def _series(count=30, start=124.0, seed=7):
    """A deterministic pseudo-random walk, so the demo looks the same daily."""
    candles, labels, price, state = [], [], start, seed
    for i in range(count):
        state = (state * 1103515245 + 12345) % 2147483648
        drift = ((state >> 16) % 1000) / 1000.0 - 0.48
        opening = price
        closing = max(1.0, opening + drift * 4.0)
        state = (state * 1103515245 + 12345) % 2147483648
        wick = ((state >> 16) % 100) / 100.0 * 2.0 + 0.3
        high = max(opening, closing) + wick
        low = min(opening, closing) - wick
        candles.append((opening, high, low, closing))
        labels.append("D%d" % (i + 1))
        price = closing
    return candles, labels


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomCandlestickChart")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        self._theme = "light"

        candles, labels = _series()
        self.chart = QCustomCandlestickChart(data=candles, labels=labels)
        self.chart.setMinimumHeight(300)
        self.chart.candleHovered.connect(self._onHover)
        self.chart.candleClicked.connect(self._onClick)
        layout.addWidget(self.chart, 1)

        self.readout = QtWidgets.QLabel("Hover a candle to inspect its OHLC")
        layout.addWidget(self.readout)

        controls = QtWidgets.QHBoxLayout()
        for text, slot in (("Hollow up candles", self._toggleHollow),
                           ("Grid", self._toggleGrid),
                           ("Tooltip", self._toggleTooltip),
                           ("Light / dark", self._toggleTheme)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            controls.addWidget(btn)
        controls.addStretch(1)
        layout.addLayout(controls)

        self.resize(720, 460)

    def _onHover(self, index):
        if index < 0:
            self.readout.setText("Hover a candle to inspect its OHLC")
            return
        o, h, l, c = self.chart.data()[index]
        direction = "up" if c >= o else "down"
        self.readout.setText(
            "%s  O %.2f  H %.2f  L %.2f  C %.2f  (%s)"
            % (self.chart.labels()[index], o, h, l, c, direction))

    def _onClick(self, index):
        self.readout.setText("clicked candle %d (%s)"
                             % (index, self.chart.labels()[index]))

    def _toggleHollow(self):
        self.chart.hollowUpCandles = not self.chart.hollowUpCandles

    def _toggleGrid(self):
        self.chart.showGrid = not self.chart.showGrid

    def _toggleTooltip(self):
        self.chart.showTooltip = not self.chart.showTooltip

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
