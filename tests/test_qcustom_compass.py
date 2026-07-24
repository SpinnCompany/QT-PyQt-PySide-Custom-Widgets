"""QCustomCompass — headless construction + paint smoke, heading wrap/clamp,
cardinal conversion, needle colour, signal, drag-to-set."""

from qtpy.QtGui import QColor


def _img(w, size=(200, 200)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


def _has_color(img, target, tol=45):
    t = QColor(target)
    for y in range(0, img.height(), 3):
        for x in range(0, img.width(), 3):
            c = QColor(img.pixel(x, y))
            if (abs(c.red() - t.red()) + abs(c.green() - t.green())
                    + abs(c.blue() - t.blue())) <= tol:
                return True
    return False


class TestCompass:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomCompass import QCustomCompass
        w = QCustomCompass(heading=315)
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 3

    def test_heading_wraps(self, qapp):
        from Custom_Widgets.QCustomCompass import QCustomCompass
        w = QCustomCompass()
        w.setHeading(370)
        assert abs(w.heading - 10.0) < 1e-6
        w.setHeading(-30)
        assert abs(w.heading - 330.0) < 1e-6

    def test_cardinal_conversion(self, qapp):
        from Custom_Widgets.QCustomCompass import QCustomCompass
        assert QCustomCompass.cardinal16(0) == "N"
        assert QCustomCompass.cardinal16(90) == "E"
        assert QCustomCompass.cardinal16(315) == "NW"
        assert QCustomCompass.cardinal16(45) == "NE"

    def test_north_needle_colour(self, qapp):
        from Custom_Widgets.QCustomCompass import QCustomCompass
        w = QCustomCompass(heading=0)
        w.northColor = "#ff2200"
        w.animated = False
        img = _img(w)
        assert _has_color(img, "#ff2200"), "north needle colour missing"

    def test_heading_changed_signal(self, qapp):
        from Custom_Widgets.QCustomCompass import QCustomCompass
        w = QCustomCompass(heading=0)
        w.animated = False
        seen = []
        w.headingChanged.connect(seen.append)
        w.setHeading(120)
        assert seen == [120.0]

    def test_drag_sets_heading(self, qapp):
        from qtpy.QtCore import QPointF, Qt, QEvent
        from qtpy.QtGui import QMouseEvent
        from Custom_Widgets.QCustomCompass import QCustomCompass
        w = QCustomCompass(heading=0)
        w.animated = False
        _img(w, (200, 200))
        # click directly to the right of centre -> due East (90°)
        ev = QMouseEvent(QEvent.MouseButtonPress, QPointF(190, 100), Qt.LeftButton,
                         Qt.LeftButton, Qt.NoModifier)
        w.mousePressEvent(ev)
        assert abs(w.heading - 90.0) < 2.0

    def test_rotate_bezel_mode(self, qapp):
        from Custom_Widgets.QCustomCompass import QCustomCompass
        w = QCustomCompass(heading=200)
        w.rotateBezel = True
        assert w.rotateBezel is True
        _img(w)
