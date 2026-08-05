########################################################################
## QCustomMapView example — the optional map extra
##
## A small fleet-tracking view: two vehicles, a route between them, focus and
## fit controls, a live style picker and a theme toggle. Requires the map
## extra:
##     pip install QT-PyQt-PySide-Custom-Widgets[map]
##
## OFFLINE BY DEFAULT: the demo uses the keyless `itemsoverlay` engine (an
## empty base map, zero tile traffic) so it runs deterministically without a
## network. Set CW_MAPVIEW_ONLINE=1 to use OpenStreetMap tiles instead — note
## the default tiles then carry an "API Key Required" watermark; see
## docs/map-view.md for pointing this at your own tile host.
## Run:
##     python main.py
########################################################################
import os
import sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.map import MapEngineUnavailable
from qtpy.QtCore import QCoreApplication, QSettings, QTimer
from qtpy.QtWidgets import QApplication

NAIROBI = (-1.286389, 36.817223)
# (id, lat, lon, label, theme-colour role) — colours come from the active
# theme's Other-variables so they flip with the light/dark toggle.
FLEET = [("truck-1", -1.283, 36.812, "KBZ 123A", "MARKER_A"),
         ("truck-2", -1.292, 36.826, "KCA 456B", "MARKER_B")]
ROUTE = [(-1.283, 36.812), (-1.287, 36.818), (-1.292, 36.826)]


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
            # Name the app's default theme explicitly: a stale THEME key in the
            # pre-appName fallback QSettings file makes the json loader drop
            # every Default-Theme flag, so relying on the flag alone can leave
            # the app with no theme selected at all.
            target = "Atlas-Dark"
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False):
                    target = t.name
                    break
            s.setValue("THEME", target)
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._wireMap()

    # ------------------------------------------------------------------ #
    ## Wiring
    # ------------------------------------------------------------------ #
    def _wireMap(self):
        ui = self.ui
        ui.mapView.centerChanged.connect(self._onCenter)
        ui.mapView.engineFailed.connect(
            lambda why: ui.statusLabel.setText("map unavailable — %s" % why))
        ui.styleBox.currentIndexChanged.connect(ui.mapView.setMapStyle)
        ui.zoomSlider.valueChanged.connect(lambda v: ui.mapView.setZoom(float(v)))
        ui.focusKbzBtn.clicked.connect(lambda: ui.mapView.focusMarker("truck-1"))
        ui.focusKcaBtn.clicked.connect(lambda: ui.mapView.focusMarker("truck-2"))
        ui.fitFleetBtn.clicked.connect(ui.mapView.fitMarkers)
        ui.moveFleetBtn.clicked.connect(self._moveFleet)
        ui.themeToggleBtn.clicked.connect(self._toggleTheme)

        self._online = os.environ.get("CW_MAPVIEW_ONLINE", "") == "1"
        if self._online:
            ui.offlineBadge.hide()
        else:
            # The itemsoverlay engine is an empty base map: markers, routes
            # and focus all work, and NOTHING is fetched over the network, so
            # the demo behaves the same on every machine.
            ui.mapView.setTileProvider("itemsoverlay")

        # Load the engine after the window exists so a failure can be shown in
        # the widget rather than crashing before anything is on screen.
        QTimer.singleShot(0, self._start)

    def _start(self):
        try:
            self.ui.mapView.loadDefaultEngine()
        except MapEngineUnavailable as exc:
            self.ui.mapView.showPlaceholder(
                "Map engine unavailable.\n\n%s\n\n"
                "Install the extra:  pip install "
                "QT-PyQt-PySide-Custom-Widgets[map]" % exc)
            return

        self.ui.mapView.setCenter(*NAIROBI)
        self.ui.mapView.setZoom(13)
        self._applyFleet()
        self.ui.mapView.focusMarker("truck-1", recenter=False)
        mode = "online (OSM tiles)" if self._online else \
            "offline demo — set CW_MAPVIEW_ONLINE=1 for OSM tiles"
        self.ui.statusLabel.setText("2 vehicles, 1 route — %s" % mode)
        # Styles resolve asynchronously, so ask again once the engine settled.
        QTimer.singleShot(2500, self._loadStyles)

    # ------------------------------------------------------------------ #
    ## Fleet data (colours come from the ACTIVE theme, not hard-coded)
    # ------------------------------------------------------------------ #
    def _applyFleet(self):
        view = self.ui.mapView
        accent = self.themeEngine.COLOR_ACCENT_1   # token fallback, theme-driven
        for id, lat, lon, label, role in FLEET:
            color = self.themeEngine.themeColor(role, accent)
            if view.marker(id) is None:
                view.addMarker(id, lat, lon, label=label, color=color)
            else:
                view.updateMarker(id, color=color)
        view.setRoute("leg-1", ROUTE,
                      color=self.themeEngine.themeColor("ROUTE", accent),
                      width=5)

    def _loadStyles(self):
        styles = self.ui.mapView.mapStyles()
        if not styles:
            return
        self.ui.styleBox.blockSignals(True)
        self.ui.styleBox.clear()
        self.ui.styleBox.addItems(styles)
        self.ui.styleBox.blockSignals(False)

    def _moveFleet(self):
        """Nudge both vehicles, as a live feed would."""
        for id, _lat, _lon, _label, _role in FLEET:
            marker = self.ui.mapView.marker(id)
            if marker is not None:
                self.ui.mapView.updateMarker(id,
                                             latitude=marker.latitude + 0.002,
                                             longitude=marker.longitude + 0.003)
        self.ui.statusLabel.setText("fleet moved")

    def _onCenter(self, lat, lon):
        self.ui.statusLabel.setText("centre %.4f, %.4f — zoom %.1f"
                                    % (lat, lon, self.ui.mapView.zoom()))

    def _toggleTheme(self):
        settings = QSettings()
        current = settings.value("THEME")
        settings.setValue("THEME",
                          "Atlas-Light" if current == "Atlas-Dark" else "Atlas-Dark")
        QAppSettings.updateAppSettings(self, generateIcons=False)
        self._applyFleet()   # marker/route colours follow the theme


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
