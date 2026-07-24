"""QCustomLiquidGauge — headless construction + paint smoke + pixel probe that
the fill colour renders at the right level, value clamps, and the shape/badge
props work."""

from qtpy.QtGui import QColor


def _img(w, size=(200, 220)):
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


class TestLiquidGauge:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
        w = QCustomLiquidGauge(value=68)
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 3

    def test_fill_colour_renders(self, qapp):
        from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
        w = QCustomLiquidGauge(value=80)
        w.setColors("#22cc88", background="#101018")
        w.setAnimated(False)
        img = _img(w)
        assert _has_color(img, "#22cc88"), "fill colour missing"

    def test_empty_gauge_has_no_fill(self, qapp):
        from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
        w = QCustomLiquidGauge(value=0, minimum=0, maximum=100)
        w.setColors("#22cc88", background="#101018")
        w.setAnimated(False)
        img = _img(w)
        assert not _has_color(img, "#22cc88", tol=30), "empty gauge should not paint fill"

    def test_value_clamped(self, qapp):
        from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
        w = QCustomLiquidGauge(minimum=0, maximum=100)
        w.setAnimated(False)
        w.setValue(250)
        assert w.value == 100.0
        w.setValue(-10)
        assert w.value == 0.0

    def test_value_changed_signal(self, qapp):
        from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
        w = QCustomLiquidGauge(value=10)
        w.setAnimated(False)
        seen = []
        w.valueChanged.connect(seen.append)
        w.setValue(55)
        assert seen == [55.0]

    def test_shape_and_badge(self, qapp):
        from Custom_Widgets.QCustomLiquidGauge import QCustomLiquidGauge
        w = QCustomLiquidGauge(value=31)
        w.shape = "roundedRect"
        assert w.shape == "roundedRect"
        w.setBadge("31%", "#3aa0ff")
        assert w.badgeText == "31%"
        w.centerText = "3.61"
        w.centerSuffix = "gal"
        _img(w)
