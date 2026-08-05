########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomMapView - engine-agnostic map facade.
##
## The facade owns all the STATE (centre, zoom, markers, routes, focus) and a
## backend renders it. That split is deliberate:
##
##   * the state is plain Python and fully testable headlessly, which is what
##     the project plan said a map could not be - it can, as long as the
##     engine is not tangled into it
##   * the engine can be swapped (QtLocation today, MapLibre/WebEngine later)
##     without touching a line of application code
##
## Every mutation is applied to the state first and then pushed to the backend,
## so a view created before the engine loads still shows the right thing once
## it attaches, and a headless test needs no engine at all.
##
## See docs/design/qcustommapview-project-plan.md for why this is an optional
## extra rather than a core widget.
########################################################################
from qtpy.QtCore import Qt, Signal, Property
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class MapEngineUnavailable(RuntimeError):
    """Raised when no mapping engine can be loaded.

    Carries the reason, because "the map is blank" is otherwise one of the
    least debuggable failures a user can hit.
    """


class Marker(object):
    """A point of interest. `heading` rotates a vehicle icon; None leaves it."""

    __slots__ = ("id", "latitude", "longitude", "label", "color", "heading",
                 "icon")

    def __init__(self, id, latitude, longitude, label="", color="#2563eb",
                 heading=None, icon=""):
        self.id = str(id)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.label = str(label)
        self.color = QColor(color)
        self.heading = None if heading is None else float(heading) % 360.0
        self.icon = str(icon)

    def asTuple(self):
        return (self.id, self.latitude, self.longitude, self.label)

    def __repr__(self):                                  # pragma: no cover
        return "Marker(%r, %g, %g)" % (self.id, self.latitude, self.longitude)


class Route(object):
    """A polyline. `points` is a list of (lat, lon)."""

    __slots__ = ("id", "points", "color", "width")

    def __init__(self, id, points, color="#dc2626", width=4.0):
        self.id = str(id)
        self.points = [(float(a), float(b)) for a, b in (points or [])]
        self.color = QColor(color)
        self.width = max(0.5, float(width))

    def __repr__(self):                                  # pragma: no cover
        return "Route(%r, %d points)" % (self.id, len(self.points))


def _clampLatitude(value):
    """Web-Mercator cannot represent the poles; clamp rather than wrap.

    Wrapping would silently teleport a marker to the other hemisphere.
    """
    return max(-85.05112878, min(85.05112878, float(value)))


def _wrapLongitude(value):
    """Longitude DOES wrap: +181 is -179, and a map crossing the date line is
    ordinary, not an error."""
    value = float(value)
    while value > 180.0:
        value -= 360.0
    while value < -180.0:
        value += 360.0
    return value


class QCustomMapView(QWidget):
    """A slippy map with markers, routes and a focused item.

    Usage mirrors the documented facade API::

        view = QCustomMapView()
        view.setTileProvider("osm")
        view.setCenter(-1.2864, 36.8172)
        view.setZoom(12)
        view.addMarker("truck-1", -1.29, 36.82, label="KBZ 123A", heading=45)
        view.setRoute("leg-1", [(-1.29, 36.82), (-1.31, 36.84)])
        view.focusMarker("truck-1")
    """

    centerChanged = Signal(float, float)
    zoomChanged = Signal(float)
    markerClicked = Signal(str)
    engineFailed = Signal(str)

    MIN_ZOOM = 0.0
    MAX_ZOOM = 20.0

    def __init__(self, parent=None, provider="osm", engine=None):
        super().__init__(parent)
        self.setObjectName("QCustomMapView")
        self._latitude = 0.0
        self._longitude = 0.0
        self._zoom = 10.0
        self._provider = str(provider)
        self._providerOptions = {}
        self._mapStyle = -1
        self._markers = {}          # id -> Marker, insertion ordered
        self._routes = {}           # id -> Route
        self._focused = ""
        self._interactive = True
        self._engine = None
        self._placeholder = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        if engine is not None:
            self.attachEngine(engine)

    # ------------------------------------------------------------------ #
    ## Engine
    # ------------------------------------------------------------------ #
    def attachEngine(self, engine):
        """Attach a backend and replay the current state into it."""
        self._engine = engine
        if hasattr(engine, "widget"):
            widget = engine.widget()
            if widget is not None:
                self._clearPlaceholder()
                self._layout.addWidget(widget)
        self._syncAll()

    def engine(self):
        return self._engine

    def hasEngine(self):
        return self._engine is not None

    def loadDefaultEngine(self):
        """Load the shipped QtLocation backend.

        Raises MapEngineUnavailable with the underlying reason rather than
        letting an ImportError surface from three frames down.
        """
        try:
            from ._qtlocation import QtLocationEngine
        except Exception as exc:
            raise MapEngineUnavailable(
                "QtLocation backend could not be imported: %s. Install the "
                "map extra: pip install QT-PyQt-PySide-Custom-Widgets[map]"
                % exc)
        try:
            engine = QtLocationEngine(self)
        except Exception as exc:
            raise MapEngineUnavailable("QtLocation engine failed to start: %s"
                                       % exc)
        self.attachEngine(engine)
        return engine

    def showPlaceholder(self, message):
        """Show why the map is blank, instead of leaving an empty rectangle."""
        self._clearPlaceholder()
        self._placeholder = QLabel(message, self)
        self._placeholder.setAlignment(Qt.AlignCenter)
        self._placeholder.setWordWrap(True)
        self._layout.addWidget(self._placeholder)
        self.engineFailed.emit(message)

    def _clearPlaceholder(self):
        if self._placeholder is not None:
            self._layout.removeWidget(self._placeholder)
            self._placeholder.deleteLater()
            self._placeholder = None

    def _tell(self, method, *args):
        """Forward to the backend if it implements the call."""
        if self._engine is None:
            return
        handler = getattr(self._engine, method, None)
        if callable(handler):
            handler(*args)

    def _syncAll(self):
        self._tell("setProvider", self._provider, dict(self._providerOptions))
        if self._mapStyle >= 0:
            self._tell("setMapType", self._mapStyle)
        self._tell("setCenter", self._latitude, self._longitude)
        self._tell("setZoom", self._zoom)
        self._tell("setInteractive", self._interactive)
        for marker in self._markers.values():
            self._tell("addMarker", marker)
        for route in self._routes.values():
            self._tell("setRoute", route)
        if self._focused:
            self._tell("focusMarker", self._focused, True)

    # ------------------------------------------------------------------ #
    ## Camera
    # ------------------------------------------------------------------ #
    def setCenter(self, latitude, longitude):
        latitude = _clampLatitude(latitude)
        longitude = _wrapLongitude(longitude)
        if (latitude, longitude) == (self._latitude, self._longitude):
            return
        self._latitude, self._longitude = latitude, longitude
        self._tell("setCenter", latitude, longitude)
        self.centerChanged.emit(latitude, longitude)

    def center(self):
        return (self._latitude, self._longitude)

    def setZoom(self, zoom):
        zoom = max(self.MIN_ZOOM, min(self.MAX_ZOOM, float(zoom)))
        if zoom == self._zoom:
            return
        self._zoom = zoom
        self._tell("setZoom", zoom)
        self.zoomChanged.emit(zoom)

    def zoom(self):
        return self._zoom

    def zoomIn(self, step=1.0):
        self.setZoom(self._zoom + float(step))

    def zoomOut(self, step=1.0):
        self.setZoom(self._zoom - float(step))

    def fitMarkers(self, padding=0.15):
        """Centre on the markers and pick a zoom that contains them all.

        A rough log2 fit rather than a true viewport solve: the backend knows
        the widget size, this does not, and being one zoom level generous is
        better than cropping a marker off the edge.
        """
        if not self._markers:
            return False
        lats = [m.latitude for m in self._markers.values()]
        lons = [m.longitude for m in self._markers.values()]
        self.setCenter((min(lats) + max(lats)) / 2.0,
                       (min(lons) + max(lons)) / 2.0)
        span = max(max(lats) - min(lats), max(lons) - min(lons))
        span *= (1.0 + max(0.0, float(padding)))
        if span <= 1e-9:
            self.setZoom(15.0)
            return True
        import math
        self.setZoom(max(self.MIN_ZOOM,
                         min(self.MAX_ZOOM, math.log2(360.0 / span))))
        return True

    # ------------------------------------------------------------------ #
    ## Provider
    # ------------------------------------------------------------------ #
    def setTileProvider(self, provider, **options):
        """Choose the tile provider. Options are passed to the engine.

        Keys and tokens live in the CALLER's config, never in this library —
        that is one of the reasons the map is an optional extra.
        """
        self._provider = str(provider)
        self._providerOptions = dict(options)
        self._tell("setProvider", self._provider, dict(self._providerOptions))

    def tileProvider(self):
        return self._provider

    def mapStyles(self):
        """Style names the engine reports, or [] before it has resolved them.

        Empty is not an error: providers resolve their styles asynchronously,
        so this is worth re-reading after the map has drawn once.
        """
        engine = self._engine
        if engine is None or not hasattr(engine, "mapTypeNames"):
            return []
        return engine.mapTypeNames()

    def setMapStyle(self, index):
        """Pick one of mapStyles() by index."""
        self._mapStyle = int(index)
        self._tell("setMapType", self._mapStyle)
        return True

    def mapStyle(self):
        return self._mapStyle

    def providerOptions(self):
        return dict(self._providerOptions)

    # ------------------------------------------------------------------ #
    ## Markers
    # ------------------------------------------------------------------ #
    def addMarker(self, id, latitude, longitude, label="", color="#2563eb",
                  heading=None, icon=""):
        marker = Marker(id, _clampLatitude(latitude), _wrapLongitude(longitude),
                        label, color, heading, icon)
        self._markers[marker.id] = marker
        self._tell("addMarker", marker)
        return marker

    def updateMarker(self, id, latitude=None, longitude=None, **kwargs):
        """Move or restyle a marker in place. Returns False if unknown."""
        marker = self._markers.get(str(id))
        if marker is None:
            return False
        if latitude is not None:
            marker.latitude = _clampLatitude(latitude)
        if longitude is not None:
            marker.longitude = _wrapLongitude(longitude)
        for key, value in kwargs.items():
            if key == "color":
                marker.color = QColor(value)
            elif key == "heading":
                marker.heading = None if value is None else float(value) % 360.0
            elif key in Marker.__slots__:
                setattr(marker, key, value)
        self._tell("updateMarker", marker)
        return True

    def removeMarker(self, id):
        id = str(id)
        if id not in self._markers:
            return False
        del self._markers[id]
        if self._focused == id:
            self._focused = ""
        self._tell("removeMarker", id)
        return True

    def clearMarkers(self):
        self._markers = {}
        self._focused = ""
        self._tell("clearMarkers")

    def marker(self, id):
        return self._markers.get(str(id))

    def markers(self):
        return list(self._markers.values())

    def markerCount(self):
        return len(self._markers)

    def focusMarker(self, id, glow=True, recenter=True):
        id = str(id)
        marker = self._markers.get(id)
        if marker is None:
            return False
        self._focused = id
        if recenter:
            self.setCenter(marker.latitude, marker.longitude)
        self._tell("focusMarker", id, bool(glow))
        return True

    def focusedMarker(self):
        return self._focused

    def clearFocus(self):
        self._focused = ""
        self._tell("focusMarker", "", False)

    # ------------------------------------------------------------------ #
    ## Routes
    # ------------------------------------------------------------------ #
    def setRoute(self, id, points, color="#dc2626", width=4.0):
        route = Route(id, points, color, width)
        route.points = [(_clampLatitude(a), _wrapLongitude(b))
                        for a, b in route.points]
        self._routes[route.id] = route
        self._tell("setRoute", route)
        return route

    def removeRoute(self, id):
        id = str(id)
        if id not in self._routes:
            return False
        del self._routes[id]
        self._tell("removeRoute", id)
        return True

    def clearRoutes(self):
        self._routes = {}
        self._tell("clearRoutes")

    def route(self, id):
        return self._routes.get(str(id))

    def routes(self):
        return list(self._routes.values())

    def routeCount(self):
        return len(self._routes)

    # ------------------------------------------------------------------ #
    ## Properties
    # ------------------------------------------------------------------ #
    @Property(float)
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self.setCenter(value, self._longitude)

    @Property(float)
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self.setCenter(self._latitude, value)

    @Property(float)
    def zoomLevel(self):
        return self._zoom

    @zoomLevel.setter
    def zoomLevel(self, value):
        self.setZoom(value)

    @Property(str)
    def tileProviderName(self):
        return self._provider

    @tileProviderName.setter
    def tileProviderName(self, value):
        self.setTileProvider(value, **self._providerOptions)

    @Property(bool)
    def interactive(self):
        return self._interactive

    @interactive.setter
    def interactive(self, value):
        self._interactive = bool(value)
        self._tell("setInteractive", self._interactive)
