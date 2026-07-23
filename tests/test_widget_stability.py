"""Stability regression tests: feed edge-case data (empty / single / all-equal /
all-zero / negative / huge) to the painted data widgets and force a paint, so the
classic normalization crashes (divide-by-zero when max==min or total==0, empty
indexing) can never regress. Part of the hardening pass toward the tiering gate."""
import pytest

# value-list widgets: setter takes a flat list of numbers
VALUE_EDGES = {
    "empty": [], "single": [5], "all_equal": [7, 7, 7], "all_zero": [0, 0, 0],
    "negatives": [-3, 4, -1], "huge": list(range(20000)),
}
# xy charts: list of (x, y) tuples
XY_EDGES = {
    "empty": [], "single": [(0, 5)], "all_equal_y": [(0, 7), (1, 7), (2, 7)],
    "negatives": [(0, -3), (1, 5)], "huge": [(i, i % 9) for i in range(15000)],
}
# label/value charts (pie): list of (label, value) tuples
LV_EDGES = {
    "empty": [], "single": [("a", 5)], "all_equal": [("a", 4), ("b", 4)],
    "all_zero": [("a", 0), ("b", 0)], "negatives": [("a", -2), ("b", 5)],
}


def _grab(w):
    w.resize(200, 140)
    w.ensurePolished()
    w.grab()                       # forces paintEvent (where normalization divides)


def _run(make, feed, edges):
    for name, data in edges.items():
        w = make()
        feed(w, data)              # must not raise on any edge
        _grab(w)


class TestValueWidgets:
    @pytest.mark.parametrize("edge", list(VALUE_EDGES))
    def test_sparkline(self, qapp, edge):
        from Custom_Widgets.QCustomSparkline import QCustomSparkline
        w = QCustomSparkline(); w.setValues(VALUE_EDGES[edge]); _grab(w)

    @pytest.mark.parametrize("edge", list(VALUE_EDGES))
    def test_donut(self, qapp, edge):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        w = QCustomDonut(); w.setData(VALUE_EDGES[edge]); _grab(w)

    @pytest.mark.parametrize("edge", list(VALUE_EDGES))
    def test_mini_bar_chart(self, qapp, edge):
        from Custom_Widgets.QCustomMiniBarChart import QCustomMiniBarChart
        w = QCustomMiniBarChart(); w.setData(VALUE_EDGES[edge]); _grab(w)


class TestCharts:
    @pytest.mark.parametrize("edge", list(XY_EDGES))
    def test_area_chart(self, qapp, edge):
        from Custom_Widgets.QCustomCharts.QCustomAreaChart import QCustomAreaChart
        w = QCustomAreaChart(); w.addSeries("s", XY_EDGES[edge]); _grab(w)

    @pytest.mark.parametrize("edge", list(XY_EDGES))
    def test_line_chart(self, qapp, edge):
        from Custom_Widgets.QCustomCharts.QCustomLineChart import QCustomLineChart
        w = QCustomLineChart(); w.addSeries("s", XY_EDGES[edge]); _grab(w)

    @pytest.mark.parametrize("edge", list(VALUE_EDGES))
    def test_bar_chart(self, qapp, edge):
        from Custom_Widgets.QCustomCharts.QCustomBarChart import QCustomBarChart
        w = QCustomBarChart(); w.addSeries("s", VALUE_EDGES[edge]); _grab(w)

    @pytest.mark.parametrize("edge", list(LV_EDGES))
    def test_pie_chart(self, qapp, edge):
        # all-zero is the classic pie crash (total == 0 -> divide by zero)
        from Custom_Widgets.QCustomCharts.QCustomPieChart import QCustomPieChart
        w = QCustomPieChart(); w.addSeries("s", LV_EDGES[edge]); _grab(w)


class TestGauge:
    @pytest.mark.parametrize("v", [0, -50, 999999, 42])
    def test_analog_gauge(self, qapp, v):
        from Custom_Widgets.AnalogGaugeWidget import AnalogGaugeWidget
        w = AnalogGaugeWidget(); w.setValue(v); _grab(w)
