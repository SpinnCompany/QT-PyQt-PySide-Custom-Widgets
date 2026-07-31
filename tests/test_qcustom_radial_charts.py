"""QCustomRadialBars and QCustomRadialLines — the polar chart pair.

Both build on the polar helpers in _chart_axis, so a winding-direction check
covers all three radial widgets at once.
"""
import math

from qtpy.QtCore import QEvent, QPointF, Qt
from qtpy.QtGui import QMouseEvent

BARS = [("Move", 82), ("Exercise", 64), ("Stand", 95)]
WEEK = [30, 45, 60, 52, 48, 70, 64]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _bars(bars=BARS, size=(300, 300)):
    from Custom_Widgets.QCustomRadialBars import QCustomRadialBars
    c = QCustomRadialBars(bars=list(bars))
    c.resize(*size)
    return c


def _lines(series=(("Weekday", WEEK),), labels=DAYS, size=(300, 300)):
    from Custom_Widgets.QCustomRadialLines import QCustomRadialLines
    c = QCustomRadialLines(series=[(n, list(v)) for n, v in series],
                           labels=list(labels))
    c.resize(*size)
    return c


class TestPolarHelpers:
    def test_clockwise_winds_the_chart_way(self, qapp):
        from Custom_Widgets.widgets.charts._chart_axis import polarAngle
        first = polarAngle(0, 4)
        second = polarAngle(1, 4)
        assert first > second          # clockwise decreases the angle

    def test_counter_clockwise_is_opt_in(self, qapp):
        from Custom_Widgets.widgets.charts._chart_axis import polarAngle
        assert polarAngle(1, 4, clockwise=False) > polarAngle(0, 4, clockwise=False)

    def test_slot_zero_starts_at_the_top(self, qapp):
        from Custom_Widgets.widgets.charts._chart_axis import polarAngle, polarPoint
        x, y = polarPoint(0, 0, 10, polarAngle(0, 4))
        assert abs(x) < 1e-9 and abs(y + 10) < 1e-9    # screen y grows down

    def test_evenly_spaced(self, qapp):
        from Custom_Widgets.widgets.charts._chart_axis import polarAngle
        angles = [polarAngle(i, 5) for i in range(5)]
        steps = {round((angles[i] - angles[i + 1]) % (2 * math.pi), 9)
                 for i in range(4)}
        assert len(steps) == 1


class TestRadialBarsData:
    def test_bars(self, qapp):
        c = _bars()
        assert c.barCount() == 3 and c.bars()[0] == ("Move", 82.0)

    def test_malformed_dropped(self, qapp):
        c = _bars([("A", 1), ("B",), None, ("C", "x")])
        assert c.barCount() == 1

    def test_negative_clamped(self, qapp):
        assert _bars([("A", -5)]).bars()[0][1] == 0.0

    def test_fraction_clamped_to_one(self, qapp):
        """A value above the maximum must not wrap past its own start and
        read as a smaller number."""
        c = _bars([("Over", 250)])
        c.maxValue = 100
        assert c.fractionFor(0) == 1.0

    def test_auto_maximum_when_zero(self, qapp):
        c = _bars()
        c.maxValue = 0
        assert c.maximum() == 95.0

    def test_maximum_never_zero(self, qapp):
        c = _bars([("A", 0)])
        c.maxValue = 0
        assert c.maximum() == 1.0

    def test_empty_is_safe(self, qapp):
        c = _bars([])
        c.grab()
        assert c.barCount() == 0


class TestRadialBarsGeometry:
    def test_rings_nest_inward(self, qapp):
        c = _bars()
        c.grab()
        widths = [c.ringRect(i).width() for i in range(c.barCount())]
        assert widths == sorted(widths, reverse=True)

    def test_hole_ratio_limits_the_inset(self, qapp):
        """Without the clamp, enough rings would invert the innermost rect."""
        c = _bars([("A", 1)] * 12)
        c.grab()
        assert all(c.ringRect(i).width() > 0 for i in range(12))

    def test_sweep_is_negative_when_clockwise(self, qapp):
        c = _bars()
        _start, span = c._sweepFor(0)
        assert span < 0
        c.clockwise = False
        _start, span = c._sweepFor(0)
        assert span > 0

    def test_bar_at_hits_the_ring_band(self, qapp):
        c = _bars()
        c.grab()
        ring = c.ringRect(0)
        probe = QPointF(ring.center().x(), ring.top())
        assert c.barAt(probe) == 0

    def test_bar_at_misses_the_hole(self, qapp):
        c = _bars()
        c.grab()
        assert c.barAt(c._plotRect().center()) == -1

    def test_hover_and_click(self, qapp):
        c = _bars()
        c.grab()
        hovered, clicked = [], []
        c.barHovered.connect(hovered.append)
        c.barClicked.connect(clicked.append)
        ring = c.ringRect(1)
        probe = QPointF(ring.center().x(), ring.top())
        c.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, probe, Qt.NoButton,
                                     Qt.NoButton, Qt.NoModifier))
        c.mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease, probe,
                                        Qt.LeftButton, Qt.LeftButton,
                                        Qt.NoModifier))
        assert hovered == [1] and clicked == [1]


class TestRadialBarsDesigner:
    def test_bars_csv_roundtrip(self, qapp):
        c = _bars([])
        c.barsCsv = "Move=82,Stand=95"
        assert c.barCount() == 2 and c.barsCsv == "Move=82,Stand=95"

    def test_bars_csv_skips_junk(self, qapp):
        c = _bars([])
        c.barsCsv = "A=1,,B=x,C=3"
        assert [l for l, _v in c.bars()] == ["A", "C"]

    def test_colors_csv(self, qapp):
        c = _bars()
        c.colorsCsv = "#ff0000"
        assert c.barColor(0).name() == "#ff0000"
        assert c.barColor(1).isValid()

    def test_numeric_clamps(self, qapp):
        c = _bars()
        c.thickness = 0
        c.spacing = -4
        c.holeRatio = 5
        assert c.thickness == 1 and c.spacing == 0 and c.holeRatio == 0.95

    def test_paints_and_variants_differ(self, qapp):
        a = _bars()
        b = _bars()
        b.rounded = False
        assert a.grab().toImage() != b.grab().toImage()
        c = _bars()
        c.showTrack = False
        assert a.grab().toImage() != c.grab().toImage()


class TestRadialLinesData:
    def test_series_and_samples(self, qapp):
        c = _lines((("Weekday", WEEK), ("Weekend", [20] * 7)))
        assert c.seriesCount() == 2 and c.sampleCount() == 7

    def test_non_numeric_values_dropped(self, qapp):
        c = _lines((("S", [1, "x", 3]),), labels=[])
        assert c.series()[0][1] == [1.0, 3.0]

    def test_sample_count_is_the_longest_series(self, qapp):
        c = _lines((("A", [1, 2]), ("B", [1, 2, 3, 4])), labels=[])
        assert c.sampleCount() == 4

    def test_maximum_auto_and_explicit(self, qapp):
        c = _lines()
        assert c.maximum() == 70.0
        c.maxValue = 100
        assert c.maximum() == 100.0

    def test_empty_is_safe(self, qapp):
        c = _lines((), labels=[])
        assert c.maximum() == 1.0
        c.grab()

    def test_all_zero_is_safe(self, qapp):
        c = _lines((("Z", [0, 0, 0]),), labels=[])
        assert c.maximum() == 1.0
        c.grab()


class TestRadialLinesGeometry:
    def test_points_stay_inside_the_plot(self, qapp):
        c = _lines()
        c.grab()
        rect = c._plotRect()
        radius = rect.width() / 2.0
        for i in range(c.sampleCount()):
            point = c.pointFor(0, i)
            distance = math.hypot(point.x() - rect.center().x(),
                                  point.y() - rect.center().y())
            assert distance <= radius + 1e-6

    def test_larger_value_sits_further_out(self, qapp):
        c = _lines((("S", [10, 70]),), labels=[])
        c.grab()
        centre = c._plotRect().center()
        near = c.pointFor(0, 0)
        far = c.pointFor(0, 1)
        assert math.hypot(far.x() - centre.x(), far.y() - centre.y()) > \
            math.hypot(near.x() - centre.x(), near.y() - centre.y())

    def test_first_sample_is_at_the_top(self, qapp):
        c = _lines((("S", [70, 10, 10, 10]),), labels=[])
        c.grab()
        centre = c._plotRect().center()
        point = c.pointFor(0, 0)
        assert abs(point.x() - centre.x()) < 1.0 and point.y() < centre.y()

    def test_series_at_and_sample_at(self, qapp):
        c = _lines()
        c.grab()
        assert c.seriesAt(c._plotRect().center()) == 0
        assert c.sampleAt(c.pointFor(0, 2)) == (0, 2)
        assert c.sampleAt(QPointF(1, 1)) == (-1, -1)

    def test_hover_and_click(self, qapp):
        c = _lines()
        c.grab()
        hovered, clicked = [], []
        c.seriesHovered.connect(hovered.append)
        c.pointClicked.connect(lambda s, i: clicked.append((s, i)))
        c.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, c._plotRect().center(),
                                     Qt.NoButton, Qt.NoButton, Qt.NoModifier))
        c.mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease,
                                        c.pointFor(0, 3), Qt.LeftButton,
                                        Qt.LeftButton, Qt.NoModifier))
        assert hovered == [0] and clicked == [(0, 3)]
        c.leaveEvent(QEvent(QEvent.Leave))
        assert hovered == [0, -1]


class TestRadialLinesDesigner:
    def test_series_csv_roundtrip(self, qapp):
        c = _lines((), labels=[])
        c.seriesCsv = "A=1,2,3;B=4,5,6"
        assert c.seriesCount() == 2
        assert c.seriesCsv == "A=1,2,3;B=4,5,6"

    def test_labels_csv_roundtrip(self, qapp):
        c = _lines((), labels=[])
        c.labelsCsv = "Mon, Tue ,Wed,"
        assert c.labels() == ["Mon", "Tue", "Wed"]

    def test_series_csv_skips_junk(self, qapp):
        c = _lines((), labels=[])
        c.seriesCsv = "A=1,x,3;;B=;C=4"
        assert [n for n, _v in c.series()] == ["A", "C"]

    def test_numeric_clamps(self, qapp):
        c = _lines()
        c.rings = 0
        c.lineWidth = -1
        c.fillOpacity = 5
        c.startAngle = 450
        assert c.rings == 1 and c.lineWidth == 0.0
        assert c.fillOpacity == 1.0 and c.startAngle == 90

    def test_open_and_closed_render_differently(self, qapp):
        closed = _lines()
        opened = _lines()
        opened.closed = False
        assert closed.grab().toImage() != opened.grab().toImage()

    def test_markers_change_render(self, qapp):
        plain = _lines()
        marked = _lines()
        marked.showMarkers = True
        assert plain.grab().toImage() != marked.grab().toImage()


class TestRadialCleanliness:
    def test_no_qtcharts_import(self, qapp):
        import ast
        import Custom_Widgets.QCustomRadialBars as bars
        import Custom_Widgets.QCustomRadialLines as lines
        for mod in (bars, lines):
            tree = ast.parse(open(mod.__file__, encoding="utf-8").read())
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(a.name for a in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module)
            assert not any("QtChart" in n for n in imported), (mod, imported)

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        b = _bars()
        l = _lines()
        b.ensurePolished()
        l.ensurePolished()
        assert b.labelColor.name().lower() == "#0f172a"
        assert l.labelColor.name().lower() == "#0f172a"
        qapp.setStyleSheet("")
