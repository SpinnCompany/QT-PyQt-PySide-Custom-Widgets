"""QCustomWaveform — headless construction + paint smoke for bars/line, the
push() ring buffer, CSV props, and colour render."""

from qtpy.QtGui import QColor


def _img(w, size=(320, 120)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


def _has_color(img, target, tol=50):
    t = QColor(target)
    for y in range(0, img.height(), 3):
        for x in range(0, img.width(), 3):
            c = QColor(img.pixel(x, y))
            if (abs(c.red() - t.red()) + abs(c.green() - t.green())
                    + abs(c.blue() - t.blue())) <= tol:
                return True
    return False


class TestWaveform:
    def test_bars_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomWaveform import QCustomWaveform
        w = QCustomWaveform()
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 3

    def test_bar_colour_renders(self, qapp):
        from Custom_Widgets.QCustomWaveform import QCustomWaveform
        w = QCustomWaveform()
        w.setValues([0.2, 0.9, 0.5, 1.0, 0.3])
        w.barColor = "#22cc88"; w.barColor2 = "#22cc88"
        img = _img(w)
        assert _has_color(img, "#22cc88"), "bar colour missing"

    def test_line_mode_paints(self, qapp):
        from Custom_Widgets.QCustomWaveform import QCustomWaveform
        w = QCustomWaveform(mode="line")
        w.setValues([0, 0.2, -0.3, 1.0, -0.5, 0.1, 0.0, 0.4])
        w.lineColor = "#ff5566"; w.showGrid = True
        img = _img(w)
        assert _has_color(img, "#ff5566"), "line colour missing"

    def test_push_ring_buffer(self, qapp):
        from Custom_Widgets.QCustomWaveform import QCustomWaveform
        w = QCustomWaveform()
        w.capacity = 4
        w.setValues([1, 2, 3, 4])
        w.push(5)                       # oldest (1) drops
        assert w.values() == [2.0, 3.0, 4.0, 5.0]

    def test_values_csv(self, qapp):
        from Custom_Widgets.QCustomWaveform import QCustomWaveform
        w = QCustomWaveform()
        w.valuesCsv = "1, 2, 3"
        assert w.values() == [1.0, 2.0, 3.0]
        assert w.valuesCsv == "1,2,3"

    def test_mode_switch(self, qapp):
        from Custom_Widgets.QCustomWaveform import QCustomWaveform
        w = QCustomWaveform()
        w.mode = "line"
        assert w.mode == "line"
        _img(w)
        w.mode = "bars"
        assert w.mode == "bars"
        _img(w)

    def test_mirror_bars(self, qapp):
        from Custom_Widgets.QCustomWaveform import QCustomWaveform
        w = QCustomWaveform()
        w.mirror = True
        assert w.mirror is True
        _img(w)
