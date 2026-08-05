
import QtQuick
import QtQuick.Controls
import QtLocation
import QtPositioning

Item {
    id: root
    property real centerLat: 0
    property real centerLon: 0
    property real zoomLevel: 10
    property string providerName: "itemsoverlay"
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
