"""QCustomToast: corner stacking + reflow, variant/tokenized styling, and the
convenience constructors."""
from qtpy.QtWidgets import QWidget
from qtpy.QtTest import QTest


def _parent(qapp):
    w = QWidget()
    w.resize(600, 400)
    w.show()
    return w


class TestStacking:
    def test_two_toasts_stack_downward(self, qapp):
        from Custom_Widgets.QCustomToast import QCustomToast
        p = _parent(qapp)
        a = QCustomToast(p, "first", duration=0, position="top-right").showToast()
        b = QCustomToast(p, "second", duration=0, position="top-right").showToast()
        assert a.x() == b.x()                 # same column (right-aligned)
        assert b.y() > a.y()                  # second stacked below the first
        assert a.y() >= 16                     # top margin

    def test_left_and_right_columns(self, qapp):
        from Custom_Widgets.QCustomToast import QCustomToast
        p = _parent(qapp)
        r = QCustomToast(p, "r", duration=0, position="top-right").showToast()
        l = QCustomToast(p, "l", duration=0, position="top-left").showToast()
        assert l.x() == 16                     # left margin
        assert r.x() == p.width() - r.width() - 16

    def test_reflow_on_dismiss(self, qapp):
        from Custom_Widgets.QCustomToast import QCustomToast, QCustomToastManager
        p = _parent(qapp)
        a = QCustomToast(p, "a", duration=0, position="top-right").showToast()
        b = QCustomToast(p, "b", duration=0, position="top-right").showToast()
        top_y = a.y()
        a.dismiss()
        QTest.qWait(300)                       # let the fade-out finish
        # a is gone; b reflowed up into the top slot
        assert QCustomToastManager.instance().stackFor(p, "top-right") == [b]
        assert b.y() == top_y


class TestVariant:
    def test_glyph_and_variant(self, qapp):
        from Custom_Widgets.QCustomToast import QCustomToast
        p = _parent(qapp)
        t = QCustomToast(p, "ok", variant="success", duration=0)
        assert t.variant == "success"
        assert t._icon.text() == "✓"
        t.variant = "error"
        assert t._icon.text() == "✕"
        assert t.property("variant") == "error"     # QSS attribute selector reads this

    def test_accent_bar_painted(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomToast import QCustomToast
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        p = _parent(qapp)
        t = QCustomToast(p, "saved", variant="success", duration=0).showToast()
        t._opacity.setOpacity(1.0)             # skip fade for the grab
        t.ensurePolished()
        img = t.grab().toImage()
        # left accent bar should carry the success token colour (#16a34a)
        found = any(QColor(img.pixel(x, t.height() // 2)).name().lower() == "#16a34a"
                    for x in range(0, 6))
        assert found
        qapp.setStyleSheet("")


class TestConvenience:
    def test_classmethods_set_variant(self, qapp):
        from Custom_Widgets.QCustomToast import QCustomToast
        p = _parent(qapp)
        assert QCustomToast.success(p, "s", duration=0).variant == "success"
        assert QCustomToast.error(p, "e", duration=0).variant == "error"
        assert QCustomToast.warning(p, "w", duration=0).variant == "warning"
        assert QCustomToast.info(p, "i", duration=0).variant == "info"

    def test_auto_dismiss_removes_from_stack(self, qapp):
        from Custom_Widgets.QCustomToast import QCustomToast, QCustomToastManager
        p = _parent(qapp)
        QCustomToast.info(p, "bye", duration=50, position="bottom-left")
        assert len(QCustomToastManager.instance().stackFor(p, "bottom-left")) == 1
        QTest.qWait(400)                       # duration + fade
        assert QCustomToastManager.instance().stackFor(p, "bottom-left") == []
