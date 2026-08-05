"""QCustomCandlestickChart showcase — a 30-session price series with a hover /
click readout, style toggles, and a JSON-theme light/dark switch."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication

THEME_DARK = "Candle Night"
THEME_LIGHT = "Candle Day"


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


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the app identity BEFORE loadJsonStyle: the theme loader consults
        # QSettings while parsing CustomThemes, and without these names it reads
        # the shared unnamed settings file (polluted by other example apps),
        # which silently cancels this app's Default-Theme flag.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomCandlestickChart Showcase")

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()
        themeEngine = self.themeEngine
        org = getattr(themeEngine, "organizationName", "")
        if org:
            QCoreApplication.setOrganizationName(str(org))
        appn = getattr(themeEngine, "applicationName", "")
        if appn:
            QCoreApplication.setApplicationName(str(appn))
        orgd = getattr(themeEngine, "organizationDomain", "")
        if orgd:
            QCoreApplication.setOrganizationDomain(str(orgd))
        s = QSettings()
        init_set = s.value("INIT-THEME-SET")
        if s.value("THEME") is None or not init_set:
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False) and (init_set is None or not init_set):
                    s.setValue("THEME", t.name)
                    s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._seedAndWire()

    def _seedAndWire(self):
        ui = self.ui

        # seed the price series AFTER the chart exists (data-driven config)
        candles, labels = _series()
        ui.chart.setData(candles, labels)
        ui.chart.candleHovered.connect(self._onHover)
        ui.chart.candleClicked.connect(self._onClick)

        ui.hollowButton.clicked.connect(self._toggleHollow)
        ui.gridButton.clicked.connect(self._toggleGrid)
        ui.tooltipButton.clicked.connect(self._toggleTooltip)
        ui.themeButton.clicked.connect(self._toggleTheme)

    def _onHover(self, index):
        if index < 0:
            self.ui.readoutLabel.setText("Hover a candle to inspect its OHLC")
            return
        o, h, l, c = self.ui.chart.data()[index]
        direction = "up" if c >= o else "down"
        self.ui.readoutLabel.setText(
            "%s  O %.2f  H %.2f  L %.2f  C %.2f  (%s)"
            % (self.ui.chart.labels()[index], o, h, l, c, direction))

    def _onClick(self, index):
        self.ui.readoutLabel.setText(
            "clicked candle %d (%s)" % (index, self.ui.chart.labels()[index]))

    def _toggleHollow(self):
        self.ui.chart.hollowUpCandles = not self.ui.chart.hollowUpCandles

    def _toggleGrid(self):
        self.ui.chart.showGrid = not self.ui.chart.showGrid

    def _toggleTooltip(self):
        self.ui.chart.showTooltip = not self.ui.chart.showTooltip

    def _toggleTheme(self):
        current = str(getattr(self.themeEngine, "theme", "") or THEME_DARK)
        target = THEME_LIGHT if current == THEME_DARK else THEME_DARK
        self.themeEngine.setTheme(target)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
