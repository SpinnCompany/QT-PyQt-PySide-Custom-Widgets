"""Loading indicators demo — all five QCustomLoadingIndicators in one window.

Consolidates the former per-widget mini demos: QCustomArcLoader,
QCustom3CirclesLoader, QCustomSpinner (Bounce + Smooth), QCustomPerlinLoader
and the indeterminate QCustomQProgressBar with its Pause/Play control.
"""

import json
import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomLoadingIndicators import (
    QCustom3CirclesLoader,
    QCustomArcLoader,
    QCustomPerlinLoader,
    QCustomSpinner,
)
from qtpy.QtCore import QCoreApplication, QSettings, QSize, Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        # Set BEFORE loadJsonStyle: the theme engine reads QSettings() while
        # parsing the json — without these names it reads the interpreter-wide
        # settings file and the app's own THEME/default theme never resolve.
        QCoreApplication.setOrganizationName("CustomWidgets")
        QCoreApplication.setApplicationName("LoadingIndicators Demo")

        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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

        self._buildLoaders()
        self._wireDemo()

    def _chartPalette(self):
        """ChartPalette section for the active theme (falls back to the first)."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "json-styles", "style.json")
        with open(path) as fh:
            palettes = json.load(fh)["ChartPalette"]
        theme = str(getattr(self.themeEngine, "theme", "") or "")
        return palettes.get(theme) or next(iter(palettes.values()))

    def _buildLoaders(self):
        """The loaders only take colours in their constructors, so they are
        built here with the active theme's palette and dropped into the .ui
        holder layouts."""
        ui = self.ui
        pal = self._chartPalette()

        self.arcLoader = QCustomArcLoader(color=QColor(pal["arc"]))
        ui.arcHolder.addWidget(self.arcLoader)
        ui.arcHolder.setAlignment(self.arcLoader, Qt.AlignCenter)

        self.circlesLoader = QCustom3CirclesLoader(color=QColor(pal["circles"]))
        ui.circlesHolder.addWidget(self.circlesLoader)
        ui.circlesHolder.setAlignment(self.circlesLoader, Qt.AlignCenter)

        self.spinnerBounce = QCustomSpinner(
            lineWidth=10, lineColor=QColor(pal["spinnerBounce"]), animationType="Bounce")
        self.spinnerSmooth = QCustomSpinner(
            lineColor=QColor(pal["spinnerSmooth"]), animationType="Smooth")
        for spinner in (self.spinnerBounce, self.spinnerSmooth):
            spinner.setMinimumSize(100, 100)
            spinner.setMaximumSize(100, 100)
            ui.spinnerHolder.addWidget(spinner)
            ui.spinnerHolder.setAlignment(spinner, Qt.AlignCenter)

        self.perlinLoader = QCustomPerlinLoader(
            size=QSize(220, 220),
            message="LOADING...",
            color=QColor(pal["perlinMessage"]),
            fontSize=14,
            rayon=70,
            circleColor1=QColor(pal["perlinCircle1"]),
            circleColor2=QColor(pal["perlinCircle2"]),
            circleColor3=QColor(pal["perlinCircle3"]),
        )
        ui.perlinHolder.addWidget(self.perlinLoader)
        ui.perlinHolder.setAlignment(self.perlinLoader, Qt.AlignCenter)

    def _wireDemo(self):
        self.ui.pauseButton.clicked.connect(self.onPauseClicked)

    def onPauseClicked(self):
        bar = self.ui.inProgressBar
        if bar.isStarted():
            bar.pause()
            self.ui.pauseButton.setText("Play")
        else:
            bar.resume()
            self.ui.pauseButton.setText("Pause")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
