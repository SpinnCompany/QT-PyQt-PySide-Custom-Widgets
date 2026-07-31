"""QCustomRadarChart — axes, series, polar geometry, Designer CSV, painting."""
import math

from qtpy.QtCore import QEvent, QPointF, Qt
from qtpy.QtGui import QMouseEvent

AXES = ["Speed", "Power", "Range", "Agility", "Cost"]
ALPHA = [80, 60, 90, 70, 50]
BETA = [60, 90, 50, 80, 70]


def _chart(qapp, axes=AXES, series=(("Alpha", ALPHA),), size=(320, 300)):
    from Custom_Widgets.QCustomRadarChart import QCustomRadarChart
    c = QCustomRadarChart(axes=list(axes), series=list(series))
    c.resize(*size)
    return c


class TestRadarData:
    def test_axes_and_series(self, qapp):
        c = _chart(qapp)
        assert c.axisCount() == 5 and c.seriesCount() == 1
        assert c.series()[0] == ("Alpha", [80.0, 60.0, 90.0, 70.0, 50.0])

    def test_series_padded_to_axis_count(self, qapp):
        """A short series must not desync the polygon from the axes."""
        c = _chart(qapp, series=(("Short", [10, 20]),))
        assert c.series()[0][1] == [10.0, 20.0, 0.0, 0.0, 0.0]

    def test_series_truncated_to_axis_count(self, qapp):
        c = _chart(qapp, series=(("Long", [1, 2, 3, 4, 5, 6, 7]),))
        assert len(c.series()[0][1]) == 5

    def test_shrinking_axes_refits_existing_series(self, qapp):
        c = _chart(qapp)
        c.setAxes(["A", "B"])
        assert c.series()[0][1] == [80.0, 60.0]

    def test_growing_axes_pads_existing_series(self, qapp):
        c = _chart(qapp)
        c.setAxes(AXES + ["Extra"])
        assert c.series()[0][1] == [80.0, 60.0, 90.0, 70.0, 50.0, 0.0]

    def test_add_and_remove_series(self, qapp):
        c = _chart(qapp)
        c.addSeries("Beta", BETA)
        assert c.seriesCount() == 2
        assert c.removeSeries(0) is True and c.seriesCount() == 1
        assert c.series()[0][0] == "Beta"
        assert c.removeSeries(99) is False

    def test_clear_series(self, qapp):
        c = _chart(qapp)
        c.clearSeries()
        assert c.seriesCount() == 0

    def test_set_series_accepts_dicts_and_tuples(self, qapp):
        c = _chart(qapp)
        c.setSeries([{"name": "D", "values": [1, 2, 3, 4, 5]}, ("T", [5, 4, 3, 2, 1])])
        assert [n for n, _ in c.series()] == ["D", "T"]

    def test_maximum_derived_from_data(self, qapp):
        c = _chart(qapp)
        assert c.maximum() == 90.0

    def test_explicit_max_value_wins(self, qapp):
        c = _chart(qapp)
        c.maxValue = 200
        assert c.maximum() == 200.0

    def test_empty_chart_has_safe_maximum(self, qapp):
        """A zero maximum would divide by zero in the polygon mapping."""
        c = _chart(qapp, series=())
        assert c.maximum() == 1.0
        c.grab()                       # must not raise

    def test_all_zero_series_is_safe(self, qapp):
        c = _chart(qapp, series=(("Zero", [0, 0, 0, 0, 0]),))
        assert c.maximum() == 1.0
        c.grab()


class TestRadarGeometry:
    def test_axes_are_evenly_spaced(self, qapp):
        c = _chart(qapp)
        angles = [c._angleFor(i) for i in range(5)]
        steps = [(angles[i] - angles[i + 1]) % (2 * math.pi) for i in range(4)]
        expected = 2 * math.pi / 5
        assert all(abs(s - expected) < 1e-9 for s in steps)

    def test_centre_maps_to_zero_fraction(self, qapp):
        c = _chart(qapp)
        centre = c._plotRect().center()
        point = c._pointAt(0, 0.0)
        assert abs(point.x() - centre.x()) < 1e-6
        assert abs(point.y() - centre.y()) < 1e-6

    def test_full_fraction_reaches_the_radius(self, qapp):
        c = _chart(qapp)
        rect = c._plotRect()
        point = c._pointAt(0, 1.0)
        distance = math.hypot(point.x() - rect.center().x(),
                              point.y() - rect.center().y())
        assert abs(distance - rect.width() / 2.0) < 1e-6

    def test_start_angle_rotates_the_chart(self, qapp):
        c = _chart(qapp)
        before = c._pointAt(0, 1.0)
        c.startAngle = 0
        assert c._pointAt(0, 1.0) != before

    def test_polygon_has_one_point_per_axis(self, qapp):
        c = _chart(qapp)
        assert c._polygonFor(ALPHA).count() == 5

    def test_axis_at_finds_the_nearest_axis(self, qapp):
        c = _chart(qapp)
        c.grab()
        for i in range(5):
            probe = c._pointAt(i, 0.7)
            assert c.axisAt(probe) == i

    def test_axis_at_outside_the_plot(self, qapp):
        c = _chart(qapp)
        assert c.axisAt(QPointF(0, 0)) == -1

    def test_series_at_hits_inside_the_polygon(self, qapp):
        c = _chart(qapp)
        c.grab()
        assert c.seriesAt(c._plotRect().center()) == 0

    def test_series_at_misses_outside(self, qapp):
        c = _chart(qapp)
        c.grab()
        assert c.seriesAt(QPointF(1, 1)) == -1

    def test_topmost_series_wins(self, qapp):
        """The one painted last is the one the user sees under the cursor."""
        c = _chart(qapp)
        c.addSeries("Beta", BETA)
        c.grab()
        assert c.seriesAt(c._plotRect().center()) == 1


class TestRadarInteraction:
    def test_hover_emits(self, qapp):
        c = _chart(qapp)
        c.grab()
        seen = []
        c.seriesHovered.connect(seen.append)
        centre = c._plotRect().center()
        c.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, centre, Qt.NoButton,
                                     Qt.NoButton, Qt.NoModifier))
        assert seen == [0]
        c.leaveEvent(QEvent(QEvent.Leave))
        assert seen == [0, -1]

    def test_axis_click_emits(self, qapp):
        c = _chart(qapp)
        c.grab()
        seen = []
        c.axisClicked.connect(seen.append)
        probe = c._pointAt(2, 0.6)
        c.mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease, probe,
                                        Qt.LeftButton, Qt.LeftButton,
                                        Qt.NoModifier))
        assert seen == [2]


class TestRadarDesigner:
    def test_axes_csv_roundtrip(self, qapp):
        c = _chart(qapp)
        c.axesCsv = "A, B ,C,"
        assert c.axes() == ["A", "B", "C"] and c.axesCsv == "A,B,C"

    def test_series_csv_roundtrip(self, qapp):
        c = _chart(qapp)
        c.axesCsv = "A,B,C"
        c.seriesCsv = "Alpha=1,2,3;Beta=4,5,6"
        assert c.seriesCsv == "Alpha=1,2,3;Beta=4,5,6"
        assert c.seriesCount() == 2

    def test_series_csv_unnamed_gets_a_name(self, qapp):
        c = _chart(qapp)
        c.axesCsv = "A,B,C"
        c.seriesCsv = "1,2,3"
        assert c.seriesCsv == "Series 1=1,2,3"

    def test_series_csv_skips_junk(self, qapp):
        c = _chart(qapp)
        c.axesCsv = "A,B,C"
        c.seriesCsv = "Alpha=1,x,3;;garbage=;Beta=4,5,6"
        assert [n for n, _ in c.series()] == ["Alpha", "Beta"]

    def test_series_csv_replaces_rather_than_appends(self, qapp):
        c = _chart(qapp)
        c.axesCsv = "A,B,C"
        c.seriesCsv = "Alpha=1,2,3"
        c.seriesCsv = "Alpha=1,2,3"
        assert c.seriesCount() == 1

    def test_series_colors_csv(self, qapp):
        c = _chart(qapp)
        c.addSeries("Beta", BETA)
        c.seriesColorsCsv = "#ff0000,#00ff00"
        assert c.seriesColor(0).name() == "#ff0000"
        assert c.seriesColor(1).name() == "#00ff00"

    def test_series_color_falls_back_to_the_palette(self, qapp):
        c = _chart(qapp)
        assert c.seriesColor(0).isValid()
        assert c.seriesColor(99).isValid()      # wraps rather than raising

    def test_numeric_properties_clamp(self, qapp):
        c = _chart(qapp)
        c.rings = 0
        c.fillOpacity = 5
        c.lineWidth = -3
        c.maxValue = -10
        c.startAngle = 450
        assert c.rings == 1 and c.fillOpacity == 1.0
        assert c.lineWidth == 0.0 and c.maxValue == 0.0 and c.startAngle == 90

    def test_grid_style_falls_back(self, qapp):
        c = _chart(qapp)
        c.gridStyle = "nonsense"
        assert c.gridStyle == "polygon"


class TestRadarPainting:
    def test_paints_something(self, qapp):
        c = _chart(qapp)
        img = c.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) > 2

    def test_no_axes_paints_nothing_but_does_not_raise(self, qapp):
        c = _chart(qapp, axes=[], series=())
        c.grab()

    def test_different_data_renders_differently(self, qapp):
        a = _chart(qapp)
        b = _chart(qapp, series=(("Alpha", BETA),))
        assert a.grab().toImage() != b.grab().toImage()

    def test_circle_and_polygon_grids_differ(self, qapp):
        poly = _chart(qapp)
        circ = _chart(qapp)
        circ.gridStyle = "circle"
        assert poly.grab().toImage() != circ.grab().toImage()

    def test_legend_toggle_changes_render(self, qapp):
        on = _chart(qapp)
        off = _chart(qapp)
        off.showLegend = False
        assert on.grab().toImage() != off.grab().toImage()

    def test_no_qtcharts_import(self, qapp):
        """QtCharts is GPLv3-only, so a Pro wheel cannot link it."""
        import ast
        import Custom_Widgets.QCustomRadarChart as mod
        tree = ast.parse(open(mod.__file__, encoding="utf-8").read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert not any("QtChart" in name for name in imported), imported

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        c = _chart(qapp)
        c.ensurePolished()
        assert c.labelColor.name().lower() == "#0f172a"     # on-surface
        assert c.axisColor.name().lower() == "#cbd5e1"      # outline
        qapp.setStyleSheet("")
