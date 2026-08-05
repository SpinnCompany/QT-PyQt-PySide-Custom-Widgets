"""QCustomDivergingBarChart — the diverging (up/down) bar chart.

Headless construction + paint smoke + pixel probes that the up (income) and
down (expense) segments actually render in their own colours on either side of
the zero axis, and that the CSV Designer props parse."""

from qtpy.QtGui import QColor


def _img(w, size=(420, 220)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


def _has_color(img, target, tol=40):
    t = QColor(target)
    for y in range(0, img.height(), 3):
        for x in range(0, img.width(), 3):
            c = QColor(img.pixel(x, y))
            if (abs(c.red() - t.red()) + abs(c.green() - t.green())
                    + abs(c.blue() - t.blue())) <= tol:
                return True
    return False


class TestDivergingBarChart:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart
        w = QCustomDivergingBarChart(up=[1, 3, 2], down=[1, 2, 1], labels=["a", "b", "c"])
        img = _img(w)
        # a non-trivial number of distinct colours means it actually painted
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 3

    def test_up_and_down_colours_render(self, qapp):
        from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart
        w = QCustomDivergingBarChart()
        w.setData([4, 2, 3, 1], [1, 3, 2, 2], ["", "", "", ""])
        w.setColors("#123f39", "#34d17a")   # up teal / down green
        w.showAxis = False                    # keep the probe about the bars only
        img = _img(w)
        assert _has_color(img, "#123f39"), "income (up) colour missing"
        assert _has_color(img, "#34d17a"), "expense (down) colour missing"

    def test_down_values_stored_as_magnitude(self, qapp):
        from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart
        w = QCustomDivergingBarChart()
        w.setData([1, 2], [-3, -1])           # negative down accepted
        assert w.downValues() == [3.0, 1.0]

    def test_zero_gap_property(self, qapp):
        from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart
        w = QCustomDivergingBarChart(up=[2], down=[2])
        w.zeroGap = 24
        assert w.zeroGap == 24
        _img(w)                               # still paints with a large gap

    def test_csv_designer_props(self, qapp):
        from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart
        w = QCustomDivergingBarChart()
        w.upCsv = "1, 2, 3"
        w.downCsv = "0.5; 1.5; 2"
        w.labelsCsv = "Jan,Feb,Mar"
        assert w.upValues() == [1.0, 2.0, 3.0]
        assert w.downValues() == [0.5, 1.5, 2.0]
        assert w.labelsCsv == "Jan,Feb,Mar"
        _img(w)

    def test_axis_prefix_suffix(self, qapp):
        from Custom_Widgets.QCustomDivergingBarChart import QCustomDivergingBarChart
        w = QCustomDivergingBarChart(up=[5], down=[3])
        w.axisPrefix = "€"
        w.axisSuffix = "K"
        assert w._fmt(5) == "€5K"
