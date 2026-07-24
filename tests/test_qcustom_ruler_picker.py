"""QCustomRulerPicker — headless construction + paint smoke, snap/clamp,
value<->position mapping, wheel/drag, and the signal."""

from qtpy.QtGui import QColor


def _img(w, size=(360, 100)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


class TestRulerPicker:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
        w = QCustomRulerPicker(value=65)
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 2

    def test_snap_and_clamp(self, qapp):
        from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
        w = QCustomRulerPicker(minimum=0, maximum=100, step=5)
        w.setValue(63)
        assert w.value == 65.0          # snapped to nearest 5
        w.setValue(999)
        assert w.value == 100.0
        w.setValue(-5)
        assert w.value == 0.0

    def test_no_snap_keeps_value(self, qapp):
        from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
        w = QCustomRulerPicker(minimum=0, maximum=100, step=5)
        w.snap = False
        w.setValue(63.4)
        assert abs(w.value - 63.4) < 1e-6

    def test_value_changed_signal(self, qapp):
        from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
        w = QCustomRulerPicker(value=10, minimum=0, maximum=100, step=1)
        seen = []
        w.valueChanged.connect(seen.append)
        w.setValue(42)
        assert seen == [42.0]

    def test_position_roundtrip_fixed(self, qapp):
        from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
        w = QCustomRulerPicker(minimum=0, maximum=100, step=1)
        _img(w)
        a0, a1, *_ = w._strip_geom()
        x = w._pos(50, a0, a1)
        assert abs(w._value_at(x, a0, a1) - 50) < 1.0

    def test_wheel_steps(self, qapp):
        from qtpy.QtCore import QPoint, QPointF, Qt
        from qtpy.QtGui import QWheelEvent
        from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
        w = QCustomRulerPicker(value=50, minimum=0, maximum=100, step=2)
        _img(w)
        ev = QWheelEvent(QPointF(10, 10), QPointF(10, 10), QPoint(0, 0),
                         QPoint(0, 120), Qt.NoButton, Qt.NoModifier,
                         Qt.NoScrollPhase, False)
        w.wheelEvent(ev)
        assert w.value == 52.0

    def test_vertical_orientation(self, qapp):
        from Custom_Widgets.QCustomRulerPicker import QCustomRulerPicker
        w = QCustomRulerPicker(value=65, orientation="vertical")
        assert w.orientation == "vertical"
        _img(w, (100, 320))
