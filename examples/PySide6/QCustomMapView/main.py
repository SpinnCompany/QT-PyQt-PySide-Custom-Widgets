########################################################################
## QCustomMapView example — the optional map extra
##
## A small fleet-tracking view: two vehicles, a route between them, focus and
## fit controls, and a live style picker. Requires the map extra:
##     pip install QT-PyQt-PySide-Custom-Widgets[map]
##
## Note the tiles carry an "API Key Required" watermark by default — see
## docs/map-view.md for how to point this at your own tile host.
## Run:
##     python main.py
########################################################################
import sys

from PySide6 import QtCore, QtWidgets

from Custom_Widgets.map import MapEngineUnavailable, QCustomMapView
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens

NAIROBI = (-1.286389, 36.817223)
FLEET = [("truck-1", -1.283, 36.812, "KBZ 123A", "#dc2626"),
         ("truck-2", -1.292, 36.826, "KCA 456B", "#16a34a")]
ROUTE = [(-1.283, 36.812), (-1.287, 36.818), (-1.292, 36.826)]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomMapView")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        self._theme = "light"

        self.map = QCustomMapView()
        self.map.setMinimumHeight(380)
        self.map.centerChanged.connect(self._onCenter)
        self.map.engineFailed.connect(
            lambda why: self.status.setText("map unavailable — %s" % why))
        layout.addWidget(self.map, 1)

        row = QtWidgets.QHBoxLayout()

        self.styleBox = QtWidgets.QComboBox()
        self.styleBox.setPlaceholderText("styles load with the provider")
        self.styleBox.currentIndexChanged.connect(self.map.setMapStyle)
        row.addWidget(QtWidgets.QLabel("Style"))
        row.addWidget(self.styleBox)

        zoom = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        zoom.setRange(int(QCustomMapView.MIN_ZOOM), int(QCustomMapView.MAX_ZOOM))
        zoom.setValue(13)
        zoom.valueChanged.connect(lambda v: self.map.setZoom(float(v)))
        row.addWidget(QtWidgets.QLabel("Zoom"))
        row.addWidget(zoom, 1)

        for text, slot in (("Focus KBZ", lambda: self.map.focusMarker("truck-1")),
                           ("Focus KCA", lambda: self.map.focusMarker("truck-2")),
                           ("Fit fleet", self.map.fitMarkers),
                           ("Move fleet", self._moveFleet),
                           ("Light / dark", self._toggleTheme)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            row.addWidget(btn)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel("starting the map engine...")
        layout.addWidget(self.status)
        self.resize(760, 560)

        # Load the engine after the window exists so a failure can be shown in
        # the widget rather than crashing before anything is on screen.
        QtCore.QTimer.singleShot(0, self._start)

    def _start(self):
        try:
            self.map.loadDefaultEngine()
        except MapEngineUnavailable as exc:
            self.map.showPlaceholder(
                "Map engine unavailable.\n\n%s\n\n"
                "Install the extra:  pip install "
                "QT-PyQt-PySide-Custom-Widgets[map]" % exc)
            return

        self.map.setCenter(*NAIROBI)
        self.map.setZoom(13)
        for id, lat, lon, label, color in FLEET:
            self.map.addMarker(id, lat, lon, label=label, color=color)
        self.map.setRoute("leg-1", ROUTE, color="#2563eb", width=5)
        self.map.focusMarker("truck-1", recenter=False)
        self.status.setText("2 vehicles, 1 route")
        # Styles resolve asynchronously, so ask again once tiles have arrived.
        QtCore.QTimer.singleShot(2500, self._loadStyles)

    def _loadStyles(self):
        styles = self.map.mapStyles()
        if not styles:
            return
        self.styleBox.blockSignals(True)
        self.styleBox.clear()
        self.styleBox.addItems(styles)
        self.styleBox.blockSignals(False)

    def _moveFleet(self):
        """Nudge both vehicles, as a live feed would."""
        for id, _lat, _lon, _label, _colour in FLEET:
            marker = self.map.marker(id)
            if marker is not None:
                self.map.updateMarker(id,
                                      latitude=marker.latitude + 0.002,
                                      longitude=marker.longitude + 0.003)
        self.status.setText("fleet moved")

    def _onCenter(self, lat, lon):
        self.status.setText("centre %.4f, %.4f — zoom %.1f"
                            % (lat, lon, self.map.zoom()))

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
