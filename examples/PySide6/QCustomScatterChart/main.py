"""QCustomScatterChart showcase — two correlated samples plus a bubble plot.

Hover a marker for its coordinates, click one to pin it to the status line,
and use the controls to change marker shape, size and tick density.
"""

import math
import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication


def _sample(count=28, phase=0.0, spread=12.0, seed=11):
    """A deterministic scatter, so the demo looks the same every run."""
    points, state = [], seed
    for i in range(count):
        state = (state * 1103515245 + 12345) % 2147483648
        jitter = ((state >> 16) % 1000) / 1000.0 - 0.5
        points.append((i, 30 + spread * math.sin(i / 3.0 + phase) + jitter * 6))
    return points


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the app identity BEFORE loadJsonStyle: the theme loader consults
        # QSettings while parsing CustomThemes, and without these names it
        # reads the shared unnamed settings file (polluted by other example
        # apps), which silently cancels this app's Default-Theme flag.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("QCustomScatterChart Showcase")

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

        self._seedData()
        self._wire()

    def _seedData(self):
        self.ui.chart.setSeries([
            ("Control", _sample()),
            ("Treatment", _sample(phase=1.4, spread=16.0, seed=29)),
        ])
        self.ui.bubbles.setSeries([
            ("Segments", [(1, 12, 10), (2, 26, 26), (3, 18, 16),
                          (4, 33, 34), (5, 22, 12), (6, 29, 20)]),
        ])
        # controls reflect the charts' current (data-dependent) state
        self.ui.sizeSlider.setValue(int(self.ui.chart.markerSize))
        self.ui.tickSpin.setValue(self.ui.chart.tickCount)

    def _wire(self):
        self.ui.chart.pointHovered.connect(self._onHover)
        self.ui.chart.pointClicked.connect(self._onClick)
        self.ui.shapeCombo.currentTextChanged.connect(self._setShape)
        self.ui.sizeSlider.valueChanged.connect(self._setSize)
        self.ui.tickSpin.valueChanged.connect(self._setTicks)
        self.ui.gridBtn.clicked.connect(self._toggleGrid)
        self.ui.legendBtn.clicked.connect(self._toggleLegend)
        self.ui.themeBtn.clicked.connect(self._toggleTheme)

    def _onHover(self, si, pi):
        if si < 0:
            self.ui.statusLabel.setText("Hover a marker for its coordinates")
            return
        name, points = self.ui.chart.series()[si]
        x, y, _size = points[pi]
        self.ui.statusLabel.setText("%s — x %g, y %.2f" % (name, x, y))

    def _onClick(self, si, pi):
        name, points = self.ui.chart.series()[si]
        x, y, _size = points[pi]
        self.ui.statusLabel.setText(
            "pinned %s point %d — x %g, y %.2f" % (name, pi, x, y))

    def _setShape(self, value):
        self.ui.chart.markerShape = value
        self.ui.bubbles.markerShape = value

    def _setSize(self, value):
        self.ui.chart.markerSize = float(value)

    def _setTicks(self, value):
        self.ui.chart.tickCount = value
        self.ui.bubbles.tickCount = value

    def _toggleGrid(self):
        self.ui.chart.showGrid = not self.ui.chart.showGrid
        self.ui.bubbles.showGrid = self.ui.chart.showGrid

    def _toggleLegend(self):
        self.ui.chart.showLegend = not self.ui.chart.showLegend

    def _toggleTheme(self):
        self.themeEngine.toggleTheme(dark="Scatter Night", light="Scatter Day")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
