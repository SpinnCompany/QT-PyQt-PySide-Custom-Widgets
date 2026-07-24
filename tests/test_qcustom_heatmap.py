"""QCustomHeatmap — headless construction + paint smoke + pixel probes that the
low/high ramp renders, normalization + CSV Designer props parse, and the
grid/calendar modes lay out."""

from qtpy.QtGui import QColor


def _img(w, size=(340, 230)):
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


class TestHeatmap:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
        w = QCustomHeatmap()
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 4

    def test_low_high_ramp_renders(self, qapp):
        from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
        w = QCustomHeatmap()
        w.setValues([[0, 5, 10], [10, 5, 0]])
        w.setColors("#101030", "#e0d0ff")
        w.showLegend = False
        img = _img(w)
        assert _has_color(img, "#101030"), "low colour missing"
        assert _has_color(img, "#e0d0ff"), "high colour missing"

    def test_empty_cells_use_empty_colour(self, qapp):
        from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
        w = QCustomHeatmap()
        w.setColors("#101030", "#e0d0ff", empty="#00ff00")
        w.setValues([[1, None], [None, 2]])
        w.showLegend = False
        w.showLabels = False
        img = _img(w)
        assert _has_color(img, "#00ff00"), "empty colour missing"

    def test_values_csv_designer_prop(self, qapp):
        from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
        w = QCustomHeatmap()
        w.valuesCsv = "1,2,3;4,5,6"
        assert w.values() == [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        assert w.valuesCsv.startswith("1,2,3;4,5,6")
        _img(w)

    def test_labels_csv(self, qapp):
        from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
        w = QCustomHeatmap()
        w.rowLabelsCsv = "A,B"
        w.colLabelsCsv = "X,Y,Z"
        assert w.rowLabelsCsv == "A,B"
        assert w.colLabelsCsv == "X,Y,Z"

    def test_calendar_mode_wraps_flat_list(self, qapp):
        from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
        w = QCustomHeatmap(mode="calendar")
        w.setValues(list(range(21)))          # 3 weeks
        rows, cols, get = w._matrix()
        assert rows == 7 and cols == 3
        assert get(0, 0) == 0 and get(0, 1) == 7 and get(6, 2) == 20
        _img(w)

    def test_fixed_range(self, qapp):
        from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
        w = QCustomHeatmap()
        w.setRange(0, 100)
        assert w.autoNormalize is False
        assert w._norm_range() == (0.0, 100.0)

    def test_cell_clicked_signal(self, qapp):
        from qtpy.QtCore import QPointF, Qt, QEvent
        from qtpy.QtGui import QMouseEvent
        from Custom_Widgets.QCustomHeatmap import QCustomHeatmap
        w = QCustomHeatmap()
        w.setValues([[1, 2], [3, 4]])
        w.showLegend = False
        w.showLabels = False
        _img(w)                                # builds the cell rects
        seen = []
        w.cellClicked.connect(lambda r, c, v: seen.append((r, c, v)))
        rect = w._rects[(1, 1)]
        pt = rect.center()
        ev = QMouseEvent(QEvent.MouseButtonPress, pt, Qt.LeftButton,
                         Qt.LeftButton, Qt.NoModifier)
        w.mousePressEvent(ev)
        assert seen and seen[0][0] == 1 and seen[0][1] == 1
