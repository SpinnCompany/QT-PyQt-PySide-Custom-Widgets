########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QtLocation backend for QCustomMapView.
##
## Chosen over the plan's MapLibre/QWebEngine suggestion because it ships with
## Qt, needs no Chromium (~100 MB saved) and no API key: QtLocation's `osm`
## plugin talks to OpenStreetMap directly. The facade is engine-agnostic, so
## swapping in a WebEngine backend later changes nothing above this file.
##
## The map itself is a QML `Map` hosted in a QQuickWidget. Everything the
## backend does is push facade state into that QML scene; it holds no state of
## its own, so a reload re-reads from the facade rather than from here.
##
## ATTRIBUTION: OpenStreetMap tiles require attribution and are subject to the
## OSMF tile usage policy. QtLocation's osm plugin renders the attribution
## itself; do not suppress it, and do not point this at a bulk tile scrape.
########################################################################
import os

from qtpy.QtCore import QUrl, QTimer


_QML = """
import QtQuick
import QtQuick.Controls
import QtLocation
import QtPositioning

Item {
    id: root
    property real centerLat: 0
    property real centerLon: 0
    property real zoomLevel: 10
    property string providerName: "osm"
    property bool interactive: true
    // Exposed so callers can see what the provider actually offers and pick a
    // keyless style; the osm plugin's default is Thunderforest, which stamps
    // "API Key Required" on its tiles without one.
    property var mapTypeNames: []
    property int mapTypeIndex: -1

    // Plugin parameters (custom tile host, API keys, cache limits) are
    // rebuilt imperatively: a Plugin's parameters are not assignable after
    // construction, so changing a provider option means a new Plugin.
    property var pluginParameters: ({})

    Plugin {
        id: mapPlugin
        name: root.providerName
    }

    Map {
        id: map
        anchors.fill: parent
        plugin: mapPlugin
        center: QtPositioning.coordinate(root.centerLat, root.centerLon)
        zoomLevel: root.zoomLevel
        // Gestures are opt-out so a dashboard can pin the viewport.
        property bool allowGestures: root.interactive

        onSupportedMapTypesChanged: {
            var names = [];
            for (var i = 0; i < map.supportedMapTypes.length; ++i)
                names.push(map.supportedMapTypes[i].name);
            root.mapTypeNames = names;
        }

        MapItemView {
            id: markerView
            model: ListModel { id: markerModel }
            delegate: MapQuickItem {
                coordinate: QtPositioning.coordinate(model.lat, model.lon)
                anchorPoint.x: bubble.width / 2
                anchorPoint.y: bubble.height / 2
                sourceItem: Item {
                    id: bubble
                    width: model.focused ? 26 : 18
                    height: width
                    Rectangle {
                        anchors.fill: parent
                        radius: width / 2
                        color: model.color
                        border.width: model.focused ? 3 : 1
                        border.color: "#ffffff"
                        opacity: model.focused ? 1.0 : 0.9
                    }
                    Text {
                        visible: model.label !== ""
                        anchors.top: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: model.label
                        color: "#0f172a"
                    }
                }
            }
        }

        MouseArea {
            anchors.fill: parent
            enabled: root.interactive
            onClicked: function (mouse) { mouse.accepted = false }
        }
    }

    function applyCenter(lat, lon) { root.centerLat = lat; root.centerLon = lon }
    function applyPlugin(plugin) { if (plugin) map.plugin = plugin }
    function applyMapType(index) {
        if (index >= 0 && index < map.supportedMapTypes.length) {
            map.activeMapType = map.supportedMapTypes[index];
            root.mapTypeIndex = index;
        }
    }
    function mapTypeCount() { return map.supportedMapTypes.length }
    function applyZoom(z) { root.zoomLevel = z }

    function clearMarkers() { markerModel.clear() }
    function upsertMarker(id, lat, lon, label, color, focused) {
        for (var i = 0; i < markerModel.count; ++i) {
            if (markerModel.get(i).markerId === id) {
                markerModel.set(i, {markerId: id, lat: lat, lon: lon,
                                    label: label, color: color,
                                    focused: focused});
                return;
            }
        }
        markerModel.append({markerId: id, lat: lat, lon: lon, label: label,
                            color: color, focused: focused});
    }
    function removeMarker(id) {
        for (var i = 0; i < markerModel.count; ++i) {
            if (markerModel.get(i).markerId === id) { markerModel.remove(i); return; }
        }
    }
    function setFocused(id) {
        for (var i = 0; i < markerModel.count; ++i) {
            var m = markerModel.get(i);
            markerModel.setProperty(i, "focused", m.markerId === id);
        }
    }

    // Polylines are created imperatively, NOT through a MapItemView/ListModel.
    // MapPolyline.path is QList<QGeoCoordinate>; routed through a ListModel the
    // coordinate list arrives as a QQmlListModel and the binding is rejected
    // with "Unable to assign QQmlListModel to QList<QGeoCoordinate>".
    property var routeItems: ({})

    function clearRoutes() {
        for (var key in root.routeItems) {
            map.removeMapItem(root.routeItems[key]);
            root.routeItems[key].destroy();
        }
        root.routeItems = ({});
    }
    function upsertRoute(id, path, color, width) {
        removeRoute(id);
        var line = Qt.createQmlObject(
            'import QtLocation; MapPolyline {}', map, "route_" + id);
        line.line.width = width;
        line.line.color = color;
        line.path = path;
        map.addMapItem(line);
        root.routeItems[id] = line;
    }
    function removeRoute(id) {
        var item = root.routeItems[id];
        if (item) {
            map.removeMapItem(item);
            item.destroy();
            delete root.routeItems[id];
        }
    }
}
"""


class QtLocationEngine(object):
    """Renders QCustomMapView state into a QML Map.

    Holds no state: every method is a push from the facade, so the facade
    stays the single source of truth and a reload replays cleanly.
    """

    def __init__(self, owner=None, qmlPath=None, provider=None):
        from qtpy.QtQuickWidgets import QQuickWidget
        from qtpy.QtPositioning import QGeoCoordinate     # noqa: F401 - probes the module

        self._owner = owner
        # A QML Plugin's `name` (and a Map's `plugin`) are write-once: they
        # cannot be swapped on a live Map without crashing QtQuick. So the
        # provider the facade holds when the engine loads is baked into the
        # QML instead of pushed afterwards.
        if provider is None and owner is not None and hasattr(owner, "tileProvider"):
            provider = owner.tileProvider()
        self._path = qmlPath or self._writeQml(provider)
        self._view = QQuickWidget()
        self._view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self._view.setSource(QUrl.fromLocalFile(self._path))
        if self._view.status() == QQuickWidget.Error:
            errors = "; ".join(str(e.toString()) for e in self._view.errors())
            raise RuntimeError("QML map failed to load: %s" % errors)
        self._root = self._view.rootObject()
        if self._root is None:
            raise RuntimeError("QML map produced no root object")

    @staticmethod
    def _writeQml(provider=None):
        """Materialise the QML next to this module.

        Written to disk rather than loaded from a string because QQuickWidget
        wants a URL, and a real file gives usable line numbers when the QML
        fails to compile. A non-default provider gets its own file with the
        provider baked in, because Plugin.name is write-once (see __init__).
        """
        folder = os.path.dirname(os.path.abspath(__file__))
        qml = _QML
        suffix = ""
        if provider and str(provider) != "osm":
            safe = "".join(c for c in str(provider) if c.isalnum() or c in "-_")
            qml = _QML.replace('property string providerName: "osm"',
                               'property string providerName: "%s"' % safe)
            suffix = "_" + safe
        path = os.path.join(folder, "_map%s.qml" % suffix)
        existing = None
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    existing = fh.read()
            except OSError:
                existing = None
        if existing != qml:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(qml)
        return path

    # -- facade hooks ---------------------------------------------------- #
    def widget(self):
        return self._view

    def _call(self, name, *args):
        handler = getattr(self._root, name, None)
        if handler is not None:
            handler(*args)

    def mapTypeNames(self):
        """Style names the provider offers, once it has resolved them.

        A QML array arrives as a QJSValue, which is not iterable from Python —
        toVariant() is what turns it into a real list.
        """
        names = self._root.property("mapTypeNames")
        if names is None:
            return []
        if hasattr(names, "toVariant"):
            names = names.toVariant()
        try:
            return [str(n) for n in (names or [])]
        except TypeError:
            return []

    def setMapType(self, index):
        self._call("applyMapType", int(index))

    def setProvider(self, name, options=None):
        """Point at a provider, forwarding its options as plugin parameters.

        This is how a caller escapes the default tile host. QtLocation's osm
        plugin stamps "API Key Required" on Thunderforest tiles without a key,
        so production use means either a key or your own tile server:

            view.setTileProvider("osm", **{
                "osm.mapping.custom.host": "https://tiles.example.com/",
                "osm.mapping.copyright": "© Example",
            })

        Keys stay in the caller's config — the library never carries one.
        """
        options = dict(options or {})
        current = self._root.property("providerName")
        if str(name) != str(current):
            # Plugin.name / Map.plugin are write-once in QtLocation: mutating
            # them on a live Map segfaults QtQuick. The provider is baked in
            # at engine construction (see __init__); a later switch needs a
            # new engine, so refuse rather than crash.
            import warnings
            warnings.warn(
                "QtLocationEngine: cannot switch tile provider %r -> %r on a "
                "live map (QML Plugin.name is write-once); reload the engine "
                "to change providers" % (str(current), str(name)),
                RuntimeWarning)
            return
        if options:
            self._applyPluginParameters(options)

    def _applyPluginParameters(self, options):
        """Rebuild the Plugin with parameters.

        A QML Plugin's parameters cannot be reassigned after construction, so
        the whole Plugin is recreated and handed back to the Map.
        """
        from qtpy.QtCore import QUrl                       # noqa: F401
        params = "".join(
            '        PluginParameter { name: "%s"; value: "%s" }\n'
            % (key, str(value).replace('"', '\\"'))
            for key, value in options.items())
        qml = ('import QtLocation\nPlugin {\n    name: "%s"\n%s}\n'
               % (self._root.property("providerName"), params))
        try:
            from qtpy.QtQml import QQmlComponent
            engine = self._view.engine()
            component = QQmlComponent(engine)
            component.setData(qml.encode("utf-8"), QUrl())
            plugin = component.create()
            if plugin is not None:
                self._call("applyPlugin", plugin)
        except Exception:
            # A bad parameter must not take the map down; the default plugin
            # stays in place and the caller sees unstyled tiles rather than a
            # blank widget.
            pass

    def setCenter(self, latitude, longitude):
        self._call("applyCenter", float(latitude), float(longitude))

    def setZoom(self, zoom):
        self._call("applyZoom", float(zoom))

    def setInteractive(self, interactive):
        self._root.setProperty("interactive", bool(interactive))

    def addMarker(self, marker):
        self.updateMarker(marker)

    def updateMarker(self, marker):
        focused = bool(self._owner and self._owner.focusedMarker() == marker.id)
        self._call("upsertMarker", marker.id, marker.latitude, marker.longitude,
                   marker.label, marker.color.name(), focused)

    def removeMarker(self, id):
        self._call("removeMarker", str(id))

    def clearMarkers(self):
        self._call("clearMarkers")

    def focusMarker(self, id, glow=True):
        self._call("setFocused", str(id))

    def setRoute(self, route):
        from qtpy.QtPositioning import QGeoCoordinate
        path = [QGeoCoordinate(lat, lon) for lat, lon in route.points]
        self._call("upsertRoute", route.id, path, route.color.name(),
                   float(route.width))

    def removeRoute(self, id):
        self._call("removeRoute", str(id))

    def clearRoutes(self):
        self._call("clearRoutes")
