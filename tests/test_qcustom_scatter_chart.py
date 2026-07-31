"""QCustomScatterChart — x/y data, mapping, hit-testing, Designer CSV."""
from qtpy.QtCore import QEvent, QPointF, Qt
from qtpy.QtGui import QMouseEvent

ALPHA = [(1, 2), (2, 4), (3, 9), (4, 7)]
BETA = [(1, 5), (2, 3), (3, 4)]


def _chart(series=(("Alpha", ALPHA),), size=(420, 300)):
    from Custom_Widgets.QCustomScatterChart import QCustomScatterChart
    c = QCustomScatterChart(series=[(n, list(p)) for n, p in series])
    c.resize(*size)
    return c


class TestScatterData:
    def test_series_and_points(self, qapp):
        c = _chart((("Alpha", ALPHA), ("Beta", BETA)))
        assert c.seriesCount() == 2 and c.pointCount() == 7

    def test_point_accepts_tuple_dict_and_size(self, qapp):
        c = _chart(())
        c.addSeries("S", [(1, 2), {"x": 3, "y": 4}, (5, 6, 20)])
        points = c.series()[0][1]
        assert points[0] == (1.0, 2.0, None)
        assert points[1] == (3.0, 4.0, None)
        assert points[2] == (5.0, 6.0, 20.0)

    def test_malformed_points_dropped(self, qapp):
        c = _chart(())
        c.addSeries("S", [(1, 2), (3,), None, "junk", (4, "x"), {"x": 1}])
        assert len(c.series()[0][1]) == 1

    def test_data_bounds(self, qapp):
        c = _chart((("Alpha", ALPHA),))
        assert c.dataBounds() == (1.0, 4.0, 2.0, 9.0)

    def test_empty_bounds_are_safe(self, qapp):
        c = _chart(())
        assert c.dataBounds() == (0.0, 1.0, 0.0, 1.0)
        c.grab()

    def test_ranges_snap_to_nice_numbers(self, qapp):
        c = _chart((("Alpha", ALPHA),))
        xlo, xhi = c.xRange()
        ylo, yhi = c.yRange()
        assert xlo <= 1 and xhi >= 4
        assert ylo <= 2 and yhi >= 9

    def test_remove_and_clear(self, qapp):
        c = _chart((("Alpha", ALPHA), ("Beta", BETA)))
        assert c.removeSeries(0) is True and c.seriesCount() == 1
        assert c.removeSeries(9) is False
        c.clearSeries()
        assert c.seriesCount() == 0


class TestScatterMapping:
    def test_maps_into_the_plot_rect(self, qapp):
        c = _chart()
        c.grab()
        rect = c._plotRect()
        for x, y in ALPHA:
            point = c.mapPoint(x, y)
            assert rect.left() - 1 <= point.x() <= rect.right() + 1
            assert rect.top() - 1 <= point.y() <= rect.bottom() + 1

    def test_y_axis_points_up(self, qapp):
        """Screen y grows downward; a larger data y must map higher."""
        c = _chart()
        c.grab()
        assert c.mapPoint(1, 9).y() < c.mapPoint(1, 2).y()

    def test_x_axis_points_right(self, qapp):
        c = _chart()
        c.grab()
        assert c.mapPoint(4, 2).x() > c.mapPoint(1, 2).x()

    def test_single_point_does_not_divide_by_zero(self, qapp):
        c = _chart((("One", [(5, 5)]),))
        c.grab()
        point = c.mapPoint(5, 5)
        assert point.x() == point.x()          # not NaN


class TestScatterHitTesting:
    def test_point_at_finds_a_marker(self, qapp):
        c = _chart()
        c.grab()
        target = c.mapPoint(*ALPHA[2])
        assert c.pointAt(target) == (0, 2)

    def test_point_at_misses_empty_space(self, qapp):
        c = _chart()
        c.grab()
        assert c.pointAt(QPointF(0, 0)) == (-1, -1)

    def test_later_series_wins_on_overlap(self, qapp):
        c = _chart((("Alpha", [(1, 1)]), ("Beta", [(1, 1)])))
        c.grab()
        assert c.pointAt(c.mapPoint(1, 1))[0] == 1

    def test_hover_signal(self, qapp):
        c = _chart()
        c.grab()
        seen = []
        c.pointHovered.connect(lambda s, p: seen.append((s, p)))
        c.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, c.mapPoint(*ALPHA[0]),
                                     Qt.NoButton, Qt.NoButton, Qt.NoModifier))
        assert seen == [(0, 0)]
        c.leaveEvent(QEvent(QEvent.Leave))
        assert seen == [(0, 0), (-1, -1)]

    def test_click_signal(self, qapp):
        c = _chart()
        c.grab()
        seen = []
        c.pointClicked.connect(lambda s, p: seen.append((s, p)))
        c.mouseReleaseEvent(QMouseEvent(
            QEvent.MouseButtonRelease, c.mapPoint(*ALPHA[1]),
            Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))
        assert seen == [(0, 1)]


class TestScatterDesigner:
    def test_points_csv_roundtrip(self, qapp):
        c = _chart(())
        c.pointsCsv = "Alpha=1,2;2,4|Beta=1,5"
        assert c.seriesCount() == 2 and c.pointCount() == 3
        assert c.pointsCsv == "Alpha=1,2;2,4|Beta=1,5"

    def test_points_csv_with_sizes(self, qapp):
        c = _chart(())
        c.pointsCsv = "Bubbles=1,2,10;3,4,20"
        assert c.series()[0][1][0] == (1.0, 2.0, 10.0)
        assert "1,2,10" in c.pointsCsv

    def test_points_csv_unnamed(self, qapp):
        c = _chart(())
        c.pointsCsv = "1,2;3,4"
        assert c.pointsCsv.startswith("Series 1=")

    def test_points_csv_skips_junk(self, qapp):
        c = _chart(())
        c.pointsCsv = "Alpha=1,2;bad;3|;|Beta=4,5"
        assert [n for n, _p in c.series()] == ["Alpha", "Beta"]

    def test_points_csv_replaces(self, qapp):
        c = _chart(())
        c.pointsCsv = "Alpha=1,2"
        c.pointsCsv = "Alpha=1,2"
        assert c.seriesCount() == 1

    def test_series_colors_csv(self, qapp):
        c = _chart((("Alpha", ALPHA), ("Beta", BETA)))
        c.seriesColorsCsv = "#ff0000,#00ff00"
        assert c.seriesColor(0).name() == "#ff0000"
        assert c.seriesColor(1).name() == "#00ff00"

    def test_numeric_properties_clamp(self, qapp):
        c = _chart()
        c.markerSize = 0
        c.markerOpacity = 5
        c.tickCount = 0
        assert c.markerSize >= 1.0 and c.markerOpacity == 1.0 and c.tickCount == 1

    def test_marker_shape_falls_back(self, qapp):
        c = _chart()
        c.markerShape = "nonsense"
        assert c.markerShape == "circle"

    def test_axis_titles_roundtrip(self, qapp):
        c = _chart()
        c.xAxisTitle = "Weight"
        c.yAxisTitle = "Height"
        assert (c.xAxisTitle, c.yAxisTitle) == ("Weight", "Height")


class TestScatterPainting:
    def test_paints(self, qapp):
        c = _chart((("Alpha", ALPHA), ("Beta", BETA)))
        img = c.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) > 2

    def test_marker_shapes_render_differently(self, qapp):
        a = _chart()
        b = _chart()
        b.markerShape = "square"
        assert a.grab().toImage() != b.grab().toImage()

    def test_grid_toggle_changes_render(self, qapp):
        on = _chart()
        off = _chart()
        off.showGrid = False
        assert on.grab().toImage() != off.grab().toImage()

    def test_axis_titles_change_render(self, qapp):
        plain = _chart()
        titled = _chart()
        titled.xAxisTitle = "Weight"
        titled.yAxisTitle = "Height"
        assert plain.grab().toImage() != titled.grab().toImage()

    def test_empty_chart_paints_without_raising(self, qapp):
        _chart(()).grab()

    def test_no_qtcharts_import(self, qapp):
        import ast
        import Custom_Widgets.QCustomScatterChart as mod
        tree = ast.parse(open(mod.__file__, encoding="utf-8").read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert not any("QtChart" in n for n in imported), imported

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        c = _chart()
        c.ensurePolished()
        assert c.axisColor.name().lower() == "#cbd5e1"
        qapp.setStyleSheet("")
