"""Headless paint smoke + pixel probes for the "Check Box" dashboard widgets:
QCustomDotMatrix, QCustomBeeswarm, QCustomGanttChart, plus the multi-series
mode added to QCustomSparkline."""

from qtpy.QtGui import QColor


def _img(w, size=(560, 300)):
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


def _distinct(img, step=6):
    return {img.pixel(x, y) for y in range(0, img.height(), step)
            for x in range(0, img.width(), step)}


class TestDotMatrix:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomDotMatrix import QCustomDotMatrix
        w = QCustomDotMatrix()
        img = _img(w, (280, 130))
        assert len(_distinct(img)) > 3

    def test_category_colours_render(self, qapp):
        from Custom_Widgets.QCustomDotMatrix import QCustomDotMatrix
        w = QCustomDotMatrix()
        w.setColors(["#8fe36b", "#ffffff", "#f6912b"])
        w.setData([[1, 2, 3, 1, 2, 3]] * 4)
        img = _img(w, (280, 130))
        assert _has_color(img, "#8fe36b")
        assert _has_color(img, "#f6912b")

    def test_data_csv_designer_prop(self, qapp):
        from Custom_Widgets.QCustomDotMatrix import QCustomDotMatrix
        w = QCustomDotMatrix()
        w.dataCsv = "0,1,2;2,1,0"
        assert w.data() == [[0, 1, 2], [2, 1, 0]]
        _img(w, (120, 80))


class TestBeeswarm:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomBeeswarm import QCustomBeeswarm
        w = QCustomBeeswarm()
        img = _img(w)
        assert len(_distinct(img)) > 3

    def test_colours_render(self, qapp):
        from Custom_Widgets.QCustomBeeswarm import QCustomBeeswarm
        w = QCustomBeeswarm()
        w.setData([[(90, 1)], [(40, 2)], [(60, 0)]])
        w.setColors(["#ffffff", "#8fe36b", "#f6912b"])
        img = _img(w)
        assert _has_color(img, "#8fe36b")
        assert _has_color(img, "#f6912b")

    def test_data_csv_designer_prop(self, qapp):
        from Custom_Widgets.QCustomBeeswarm import QCustomBeeswarm
        w = QCustomBeeswarm()
        w.dataCsv = "52:0,81:2;96:1,25:0"
        assert w.data() == [[(52.0, 0), (81.0, 2)], [(96.0, 1), (25.0, 0)]]
        _img(w)


class TestGanttChart:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomGanttChart import QCustomGanttChart
        w = QCustomGanttChart()
        img = _img(w, (560, 360))
        assert len(_distinct(img)) > 3

    def test_bar_colours_render(self, qapp):
        from Custom_Widgets.QCustomGanttChart import QCustomGanttChart
        w = QCustomGanttChart()
        w.setColors(["#8fe36b", "#f6912b", "#ffffff"])
        w.setData([{"label": "a", "start": 2, "length": 8, "category": 0, "value": 16},
                   {"label": "b", "start": 10, "length": 8, "category": 1, "value": 29}])
        img = _img(w, (560, 360))
        assert _has_color(img, "#8fe36b")
        assert _has_color(img, "#f6912b")

    def test_data_csv_designer_prop(self, qapp):
        from Custom_Widgets.QCustomGanttChart import QCustomGanttChart
        w = QCustomGanttChart()
        w.dataCsv = "30.09,2,8,0,16;29.09,18,8,1,29"
        rows = w.data()
        assert rows[0]["label"] == "30.09" and rows[0]["value"] == "16"
        assert rows[1]["category"] == 1
        _img(w, (560, 360))


class TestSparklineMultiSeries:
    def test_multi_series_paints_each_colour(self, qapp):
        from Custom_Widgets.QCustomSparkline import QCustomSparkline
        w = QCustomSparkline()
        w.setSeries([[3, 5, 2, 6, 4, 7], [5, 3, 6, 2, 5, 4]],
                    ["#f6912b", "#8fe36b"])
        img = _img(w, (300, 120))
        assert _has_color(img, "#f6912b")
        assert _has_color(img, "#8fe36b")

    def test_series_csv_designer_prop(self, qapp):
        from Custom_Widgets.QCustomSparkline import QCustomSparkline
        w = QCustomSparkline()
        w.seriesCsv = "1,2,3;4,5,6"
        assert w.series() == [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]

    def test_single_series_still_works(self, qapp):
        from Custom_Widgets.QCustomSparkline import QCustomSparkline
        w = QCustomSparkline(values=[1, 2, 3, 2, 4])
        img = _img(w, (120, 44))
        assert len(_distinct(img)) > 1
