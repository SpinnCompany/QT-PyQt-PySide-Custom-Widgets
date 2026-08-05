########################################################################
## QCustomSankey example
##
## An acquisition flow: traffic sources into signups, then on to trial,
## paid and churn. Hover a node to light up everything it touches.
## Rendered with QPainter only - no QtCharts. Themed through the
## Custom_Widgets pipeline (ui/ + Qss scss + json-styles).
## Run:
##     python main.py
########################################################################
import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
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
            # Default-Theme is ignored by the json parser when ANY QSettings
            # file already holds a THEME, so pin this app's default explicitly.
            if not s.value("INIT-THEME-SET"):
                s.setValue("THEME", "Sankey-Dark")
                s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._wireDemo()

    def _wireDemo(self):
        ui = self.ui
        ui.chart.nodeHovered.connect(self._onNode)
        ui.chart.linkHovered.connect(self._onLink)
        ui.chart.nodeClicked.connect(
            lambda name: ui.statusLabel.setText("clicked %s" % name))
        ui.curveSlider.valueChanged.connect(
            lambda v: setattr(ui.chart, "curvature", v / 100.0))
        ui.ribbonSlider.valueChanged.connect(
            lambda v: setattr(ui.chart, "linkOpacity", v / 100.0))
        ui.valuesButton.clicked.connect(
            lambda: setattr(ui.chart, "showValues", not ui.chart.showValues))
        ui.themeButton.clicked.connect(self._toggleTheme)

    def _onNode(self, name):
        if not name:
            self.ui.statusLabel.setText("Hover a node or a ribbon")
            return
        self.ui.statusLabel.setText(
            "%s — throughput %g" % (name, self.ui.chart.nodeValue(name)))

    def _onLink(self, index):
        if index < 0:
            return
        source, target, value = self.ui.chart.links()[index]
        self.ui.statusLabel.setText("%s to %s — %g" % (source, target, value))

    def _toggleTheme(self):
        themeEngine = self.themeEngine
        target = ("Sankey-Light" if themeEngine.theme == "Sankey-Dark"
                  else "Sankey-Dark")
        QSettings().setValue("THEME", target)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
