"""QCustomMapView — the optional map extra.

The facade owns all the state and the engine only renders it, so almost
everything here runs with no mapping engine at all. That split is the point:
docs/design/qcustommapview-project-plan.md said a map "can't be verified by an
offscreen grab() pixel probe" — true of the ENGINE, not of the state, and
keeping them apart is what makes the widget testable.
"""
import pytest

from Custom_Widgets.map import (MapEngineUnavailable, Marker, QCustomMapView,
                                Route)

NAIROBI = (-1.286389, 36.817223)


class RecordingEngine(object):
    """A stand-in backend that records the calls the facade pushes."""

    def __init__(self):
        self.calls = []

    def widget(self):
        return None

    def __getattr__(self, name):
        def record(*args):
            self.calls.append((name, args))
        return record

    def names(self):
        return [name for name, _args in self.calls]


class TestCoreIsolation:
    def test_core_never_imports_the_map(self, qapp):
        """The extra must stay optional: if the core imported it, every user
        would pay for the mapping engine whether they wanted a map or not."""
        import ast
        import os
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        package = os.path.join(root, "Custom_Widgets")
        offenders = []
        for dirpath, dirnames, filenames in os.walk(package):
            dirnames[:] = [d for d in dirnames
                           if d not in ("__pycache__", "map")]
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue
                path = os.path.join(dirpath, filename)
                tree = ast.parse(open(path, encoding="utf-8").read())
                for node in ast.walk(tree):
                    mods = []
                    if isinstance(node, ast.Import):
                        mods = [a.name for a in node.names]
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        mods = [node.module]
                    if any(m == "Custom_Widgets.map"
                           or m.startswith("Custom_Widgets.map.") for m in mods):
                        offenders.append(os.path.relpath(path, root))
        assert not offenders, "core imports the optional map extra: %s" % offenders

    def test_map_is_declared_as_an_extra(self, qapp):
        import os
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        text = open(os.path.join(root, "pyproject.toml"), encoding="utf-8").read()
        assert "[project.optional-dependencies]" in text
        assert "map" in text


class TestCoordinateHandling:
    def test_latitude_is_clamped_not_wrapped(self, qapp):
        """Web-Mercator cannot show the poles. Wrapping would teleport a
        marker to the other hemisphere; clamping keeps it near the pole."""
        view = QCustomMapView()
        view.setCenter(95, 0)
        assert view.center()[0] == pytest.approx(85.05112878)
        view.setCenter(-95, 0)
        assert view.center()[0] == pytest.approx(-85.05112878)

    def test_longitude_wraps(self, qapp):
        view = QCustomMapView()
        view.setCenter(0, 200)
        assert view.center()[1] == pytest.approx(-160.0)
        view.setCenter(0, -200)
        assert view.center()[1] == pytest.approx(160.0)

    def test_marker_coordinates_are_normalised_too(self, qapp):
        view = QCustomMapView()
        marker = view.addMarker("m", 95, 200)
        assert marker.latitude == pytest.approx(85.05112878)
        assert marker.longitude == pytest.approx(-160.0)

    def test_route_points_are_normalised(self, qapp):
        view = QCustomMapView()
        route = view.setRoute("r", [(95, 200), (0, 0)])
        assert route.points[0][0] == pytest.approx(85.05112878)
        assert route.points[0][1] == pytest.approx(-160.0)


class TestCamera:
    def test_center_and_signal(self, qapp):
        view = QCustomMapView()
        seen = []
        view.centerChanged.connect(lambda a, b: seen.append((a, b)))
        view.setCenter(*NAIROBI)
        assert view.center() == pytest.approx(NAIROBI)
        assert len(seen) == 1
        view.setCenter(*NAIROBI)                 # no-op
        assert len(seen) == 1

    def test_zoom_clamped_to_range(self, qapp):
        view = QCustomMapView()
        view.setZoom(99)
        assert view.zoom() == QCustomMapView.MAX_ZOOM
        view.setZoom(-5)
        assert view.zoom() == QCustomMapView.MIN_ZOOM

    def test_zoom_in_out(self, qapp):
        view = QCustomMapView()
        view.setZoom(10)
        view.zoomIn()
        assert view.zoom() == 11.0
        view.zoomOut(3)
        assert view.zoom() == 8.0

    def test_fit_markers_centres_on_them(self, qapp):
        view = QCustomMapView()
        view.addMarker("a", -1.0, 36.0)
        view.addMarker("b", -2.0, 37.0)
        assert view.fitMarkers() is True
        assert view.center() == pytest.approx((-1.5, 36.5))

    def test_fit_markers_with_none(self, qapp):
        assert QCustomMapView().fitMarkers() is False

    def test_fit_a_single_marker_does_not_divide_by_zero(self, qapp):
        view = QCustomMapView()
        view.addMarker("a", -1.0, 36.0)
        assert view.fitMarkers() is True
        assert view.zoom() == 15.0


class TestMarkers:
    def test_add_and_query(self, qapp):
        view = QCustomMapView()
        view.addMarker("t1", *NAIROBI, label="KBZ 123A", heading=45)
        assert view.markerCount() == 1
        marker = view.marker("t1")
        assert marker.label == "KBZ 123A" and marker.heading == 45.0

    def test_adding_the_same_id_replaces(self, qapp):
        view = QCustomMapView()
        view.addMarker("t1", 0, 0)
        view.addMarker("t1", 1, 1)
        assert view.markerCount() == 1
        assert view.marker("t1").latitude == pytest.approx(1.0)

    def test_update_marker(self, qapp):
        view = QCustomMapView()
        view.addMarker("t1", 0, 0, color="#2563eb")
        assert view.updateMarker("t1", latitude=5, color="#ff0000") is True
        marker = view.marker("t1")
        assert marker.latitude == pytest.approx(5.0)
        assert marker.color.name() == "#ff0000"
        assert marker.longitude == pytest.approx(0.0)     # untouched

    def test_update_unknown_marker(self, qapp):
        assert QCustomMapView().updateMarker("nope", latitude=1) is False

    def test_heading_wraps(self, qapp):
        view = QCustomMapView()
        view.addMarker("t1", 0, 0, heading=400)
        assert view.marker("t1").heading == pytest.approx(40.0)

    def test_remove_and_clear(self, qapp):
        view = QCustomMapView()
        view.addMarker("a", 0, 0)
        view.addMarker("b", 1, 1)
        assert view.removeMarker("a") is True
        assert view.removeMarker("a") is False
        view.clearMarkers()
        assert view.markerCount() == 0

    def test_focus(self, qapp):
        view = QCustomMapView()
        view.addMarker("t1", *NAIROBI)
        assert view.focusMarker("t1") is True
        assert view.focusedMarker() == "t1"
        assert view.center() == pytest.approx(NAIROBI)

    def test_focus_without_recentering(self, qapp):
        view = QCustomMapView()
        view.setCenter(10, 10)
        view.addMarker("t1", *NAIROBI)
        view.focusMarker("t1", recenter=False)
        assert view.center() == pytest.approx((10.0, 10.0))

    def test_focus_unknown(self, qapp):
        assert QCustomMapView().focusMarker("nope") is False

    def test_removing_the_focused_marker_clears_focus(self, qapp):
        """A dangling focus id would make the engine highlight nothing."""
        view = QCustomMapView()
        view.addMarker("t1", 0, 0)
        view.focusMarker("t1")
        view.removeMarker("t1")
        assert view.focusedMarker() == ""


class TestRoutes:
    def test_set_and_query(self, qapp):
        view = QCustomMapView()
        route = view.setRoute("leg", [(0, 0), (1, 1)], color="#00ff00", width=6)
        assert view.routeCount() == 1
        assert route.color.name() == "#00ff00" and route.width == 6.0

    def test_same_id_replaces(self, qapp):
        view = QCustomMapView()
        view.setRoute("leg", [(0, 0), (1, 1)])
        view.setRoute("leg", [(0, 0), (2, 2), (3, 3)])
        assert view.routeCount() == 1
        assert len(view.route("leg").points) == 3

    def test_remove_and_clear(self, qapp):
        view = QCustomMapView()
        view.setRoute("a", [(0, 0), (1, 1)])
        assert view.removeRoute("a") is True
        assert view.removeRoute("a") is False
        view.setRoute("b", [(0, 0), (1, 1)])
        view.clearRoutes()
        assert view.routeCount() == 0

    def test_width_has_a_floor(self, qapp):
        view = QCustomMapView()
        assert view.setRoute("a", [(0, 0)], width=0).width >= 0.5


class TestEngineContract:
    def test_state_is_replayed_when_an_engine_attaches_late(self, qapp):
        """A view built before the engine loads must not come up blank."""
        view = QCustomMapView()
        view.setCenter(*NAIROBI)
        view.setZoom(12)
        view.addMarker("t1", *NAIROBI)
        view.setRoute("leg", [(0, 0), (1, 1)])
        view.focusMarker("t1")

        engine = RecordingEngine()
        view.attachEngine(engine)
        names = engine.names()
        for expected in ("setProvider", "setCenter", "setZoom", "addMarker",
                         "setRoute", "focusMarker"):
            assert expected in names, expected

    def test_mutations_reach_the_engine(self, qapp):
        engine = RecordingEngine()
        view = QCustomMapView(engine=engine)
        engine.calls = []
        view.setZoom(7)
        view.addMarker("t1", 1, 2)
        view.removeMarker("t1")
        view.clearRoutes()
        assert engine.names() == ["setZoom", "addMarker", "removeMarker",
                                  "clearRoutes"]

    def test_engine_absent_is_not_an_error(self, qapp):
        """Every mutation must be safe with no backend attached."""
        view = QCustomMapView()
        assert view.hasEngine() is False
        view.setCenter(1, 2)
        view.addMarker("a", 0, 0)
        view.setRoute("r", [(0, 0), (1, 1)])
        view.focusMarker("a")
        view.clearMarkers()

    def test_provider_options_are_not_invented(self, qapp):
        view = QCustomMapView()
        view.setTileProvider("maptiler", apiKey="secret", style="dark")
        assert view.tileProvider() == "maptiler"
        assert view.providerOptions() == {"apiKey": "secret", "style": "dark"}

    def test_placeholder_explains_a_blank_map(self, qapp):
        view = QCustomMapView()
        seen = []
        view.engineFailed.connect(seen.append)
        view.showPlaceholder("no engine")
        assert seen == ["no engine"]


class TestDesignerProperties:
    def test_properties_roundtrip(self, qapp):
        view = QCustomMapView()
        view.latitude = -1.5
        view.longitude = 36.5
        view.zoomLevel = 9
        view.tileProviderName = "osm"
        view.interactive = False
        assert view.latitude == pytest.approx(-1.5)
        assert view.longitude == pytest.approx(36.5)
        assert view.zoomLevel == 9.0
        assert view.tileProviderName == "osm"
        assert view.interactive is False


class TestQtLocationEngine:
    def test_loads_or_reports_why(self, qapp):
        """Either the engine starts, or the failure names its own cause.

        A map that silently renders nothing is the worst outcome, so the
        facade converts any backend failure into MapEngineUnavailable with the
        underlying reason attached.
        """
        view = QCustomMapView()
        try:
            engine = view.loadDefaultEngine()
        except MapEngineUnavailable as exc:
            assert str(exc)
            return
        assert view.hasEngine() is True
        assert engine.widget() is not None

    def test_engine_renders_state_without_qml_errors(self, qapp):
        view = QCustomMapView()
        try:
            view.loadDefaultEngine()
        except MapEngineUnavailable:
            pytest.skip("QtLocation not available in this environment")
        view.setCenter(*NAIROBI)
        view.setZoom(12)
        view.addMarker("t1", -1.29, 36.82, label="KBZ 123A")
        view.setRoute("leg", [(-1.29, 36.82), (-1.31, 36.84)])
        view.focusMarker("t1")
        view.removeRoute("leg")
        view.clearMarkers()
