"""QCustomBadge - the modern tokenized badge (replaces the legacy QBadgeWidget)."""


class TestModes:
    def test_text_mode(self, qapp):
        from Custom_Widgets.QCustomBadge import QCustomBadge
        b = QCustomBadge("New")
        assert b.text() == "New" and b.isDot() is False and b.count() is None

    def test_count_mode_and_cap(self, qapp):
        from Custom_Widgets.QCustomBadge import QCustomBadge
        b = QCustomBadge()
        b.setCount(12)
        assert b.text() == "12" and b.count() == 12
        b.setCount(150, maxCount=99)
        assert b.text() == "99+"

    def test_count_zero_hidden_unless_showzero(self, qapp):
        from Custom_Widgets.QCustomBadge import QCustomBadge
        b = QCustomBadge()
        b.setCount(0)
        assert b.isHidden() is True and b.text() == ""
        b.setShowZero(True)
        assert b.isHidden() is False and b.text() == "0"

    def test_dot_mode_is_square_and_textless(self, qapp):
        from Custom_Widgets.QCustomBadge import QCustomBadge
        b = QCustomBadge("x")
        b.sizeVariant = "md"
        b.setDot(True)
        assert b.isDot() is True and b.text() == ""
        assert b.width() == b.height() == 10        # md dot size
        b.sizeVariant = "lg"
        assert b.width() == 12

    def test_setters_switch_modes(self, qapp):
        from Custom_Widgets.QCustomBadge import QCustomBadge
        b = QCustomBadge()
        b.setCount(5)
        b.setText("hi")                              # text clears count
        assert b.count() is None and b.text() == "hi"
        b.setDot(True)                               # dot clears text
        assert b.isDot() and b.text() == ""


class TestVariant:
    def test_variant_property_and_fallback(self, qapp):
        from Custom_Widgets.QCustomBadge import QCustomBadge
        b = QCustomBadge("ok", variant="success")
        assert b.variant == "success"
        b.variant = "bogus"
        assert b.variant == "default"

    def test_variant_colors_via_qss(self, qapp):
        from Custom_Widgets.QCustomBadge import QCustomBadge
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        b = QCustomBadge("Live", variant="destructive")
        b.ensurePolished()
        b.resize(60, 22)
        img = b.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 3)
                  for x in range(0, img.width(), 3)}
        assert len(colors) > 2                        # painted a filled pill
        qapp.setStyleSheet("")


class TestBehaviour:
    def test_clicked_signal(self, qapp):
        from qtpy.QtCore import Qt, QPoint
        from qtpy.QtGui import QMouseEvent
        from Custom_Widgets.QCustomBadge import QCustomBadge
        b = QCustomBadge("tap")
        seen = []
        b.clicked.connect(lambda: seen.append(1))
        ev = QMouseEvent(QMouseEvent.MouseButtonPress, QPoint(2, 2),
                         Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        b.mousePressEvent(ev)
        assert seen == [1]

    def test_attach_positions_in_corner(self, qapp):
        from qtpy.QtWidgets import QWidget
        from Custom_Widgets.QCustomBadge import QCustomBadge
        host = QWidget()
        host.resize(100, 100)
        host.show()
        qapp.processEvents()
        b = QCustomBadge()
        b.setCount(3)
        b.attachTo(host, corner="topright")
        assert b.parent() is host
        # right edge tracks the host's right edge (x + width == host width)
        assert b.x() + b.width() == host.width() and b.y() == 0
        host.resize(140, 100)                         # resize -> reposition
        qapp.processEvents()
        assert b.x() + b.width() == 140
