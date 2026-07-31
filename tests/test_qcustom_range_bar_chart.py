"""QCustomRangeBarChart — floating bars, value mapping, Designer CSV."""
from qtpy.QtCore import QEvent, QPointF, Qt
from qtpy.QtGui import QMouseEvent

RANGES = [("Mon", 4, 12), ("Tue", 6, 15), ("Wed", 3, 9),
          ("Thu", 8, 17), ("Fri", 5, 11)]


def _chart(ranges=RANGES, size=(420, 280)):
    from Custom_Widgets.QCustomRangeBarChart import QCustomRangeBarChart
    c = QCustomRangeBarChart(ranges=list(ranges))
    c.resize(*size)
    return c


class TestRangeBarData:
    def test_ranges(self, qapp):
        c = _chart()
        assert c.barCount() == 5
        assert c.ranges()[0] == ("Mon", 4.0, 12.0)

    def test_accepts_dicts(self, qapp):
        c = _chart([{"label": "A", "low": 1, "high": 5}])
        assert c.ranges()[0] == ("A", 1.0, 5.0)

    def test_reversed_pair_is_normalised(self, qapp):
        """A swapped low/high is a data slip, not a reason to drop the bar."""
        c = _chart([("A", 12, 4)])
        assert c.ranges()[0] == ("A", 4.0, 12.0)

    def test_malformed_dropped(self, qapp):
        c = _chart([("A", 1, 5), ("B", 1), None, ("C", 1, "x"), "junk"])
        assert c.barCount() == 1

    def test_data_bounds(self, qapp):
        assert _chart().dataBounds() == (3.0, 17.0)

    def test_empty_is_safe(self, qapp):
        c = _chart([])
        assert c.dataBounds() == (0.0, 1.0)
        c.grab()

    def test_value_range_snaps_to_nice_numbers(self, qapp):
        low, high = _chart().valueRange()
        assert low <= 3 and high >= 17

    def test_clear(self, qapp):
        c = _chart()
        c.clearRanges()
        assert c.barCount() == 0


class TestRangeBarGeometry:
    def test_one_rect_per_range(self, qapp):
        c = _chart()
        c.grab()
        assert len(c.barRects()) == 5

    def test_bar_spans_low_to_high(self, qapp):
        c = _chart()
        c.grab()
        bar = c.barRects()[0]
        assert abs(bar.top() - c.valueToPixel(12)) < 1.0
        assert abs(bar.bottom() - c.valueToPixel(4)) < 1.0

    def test_higher_value_is_higher_on_screen(self, qapp):
        c = _chart()
        c.grab()
        assert c.valueToPixel(17) < c.valueToPixel(3)

    def test_bar_height_tracks_span(self, qapp):
        c = _chart()
        c.grab()
        rects = c.barRects()
        # Thu spans 9, Wed spans 6 -> Thu must be the taller bar
        assert rects[3].height() > rects[2].height()

    def test_zero_span_still_draws(self, qapp):
        """A low == high range would otherwise be an invisible zero-height bar."""
        c = _chart([("Flat", 5, 5)])
        c.grab()
        assert c.barRects()[0].height() >= 1.0

    def test_horizontal_runs_across(self, qapp):
        c = _chart()
        c.orientation = "horizontal"
        c.grab()
        rects = c.barRects()
        assert rects[0].width() > rects[0].height()
        assert rects[1].top() > rects[0].top()

    def test_bar_width_ratio(self, qapp):
        thin = _chart()
        thin.barWidthRatio = 0.2
        thin.grab()
        fat = _chart()
        fat.barWidthRatio = 0.9
        fat.grab()
        assert fat.barRects()[0].width() > thin.barRects()[0].width()


class TestRangeBarInteraction:
    def test_bar_at(self, qapp):
        c = _chart()
        c.grab()
        assert c.barAt(c.barRects()[2].center()) == 2

    def test_bar_at_misses(self, qapp):
        c = _chart()
        c.grab()
        assert c.barAt(QPointF(1, 1)) == -1

    def test_hover_and_click(self, qapp):
        c = _chart()
        c.grab()
        hovered, clicked = [], []
        c.barHovered.connect(hovered.append)
        c.barClicked.connect(clicked.append)
        centre = c.barRects()[1].center()
        c.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, centre, Qt.NoButton,
                                     Qt.NoButton, Qt.NoModifier))
        c.mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease, centre,
                                        Qt.LeftButton, Qt.LeftButton,
                                        Qt.NoModifier))
        assert hovered == [1] and clicked == [1]
        c.leaveEvent(QEvent(QEvent.Leave))
        assert hovered == [1, -1]


class TestRangeBarDesigner:
    def test_ranges_csv_roundtrip(self, qapp):
        c = _chart([])
        c.rangesCsv = "Mon=4,12;Tue=6,15"
        assert c.barCount() == 2
        assert c.rangesCsv == "Mon=4,12;Tue=6,15"

    def test_ranges_csv_skips_incomplete(self, qapp):
        c = _chart([])
        c.rangesCsv = "Mon=4,12;Bad=7;;Tue=6,15"
        assert [l for l, _a, _b in c.ranges()] == ["Mon", "Tue"]

    def test_categories_csv_relabels(self, qapp):
        c = _chart()
        c.categoriesCsv = "A,B,C,D,E"
        assert [l for l, _a, _b in c.ranges()] == ["A", "B", "C", "D", "E"]
        assert c.categoriesCsv == "A,B,C,D,E"

    def test_categories_csv_shorter_keeps_the_rest(self, qapp):
        c = _chart()
        c.categoriesCsv = "A,B"
        labels = [l for l, _a, _b in c.ranges()]
        assert labels[:2] == ["A", "B"] and labels[2] == "Wed"

    def test_orientation_falls_back(self, qapp):
        c = _chart()
        c.orientation = "nonsense"
        assert c.orientation == "vertical"

    def test_numeric_properties_clamp(self, qapp):
        c = _chart()
        c.barWidthRatio = 5
        c.cornerRadius = -2
        c.tickCount = 0
        assert c.barWidthRatio == 1.0 and c.cornerRadius == 0 and c.tickCount == 1


class TestRangeBarPainting:
    def test_paints(self, qapp):
        c = _chart()
        img = c.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) > 2

    def test_orientation_changes_render(self, qapp):
        v = _chart()
        h = _chart()
        h.orientation = "horizontal"
        assert v.grab().toImage() != h.grab().toImage()

    def test_bounds_labels_change_render(self, qapp):
        off = _chart()
        on = _chart()
        on.showBounds = True
        assert off.grab().toImage() != on.grab().toImage()

    def test_empty_paints_without_raising(self, qapp):
        _chart([]).grab()

    def test_no_qtcharts_import(self, qapp):
        import ast
        import Custom_Widgets.QCustomRangeBarChart as mod
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
        assert c.barColor.name().lower() == "#2563eb"
        qapp.setStyleSheet("")
