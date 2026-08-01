"""QCustomEmptyState's default mark is painted, not a glyph.

It used to default to an emoji, which the design lint bans: a glyph does not
tint with the theme, does not scale cleanly, and renders as a different picture
on every platform. The violation was sitting in the lint baseline, so nothing
caught it until it appeared in a public documentation screenshot.
"""


class TestDefaultMark:
    def test_default_is_a_pixmap_not_text(self, qapp):
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        widget = QCustomEmptyState()
        assert widget._icon.text() == ""
        assert not widget._icon.pixmap().isNull()

    def test_mark_is_actually_drawn(self, qapp):
        """A transparent pixmap would pass the test above and show nothing."""
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        widget = QCustomEmptyState()          # keep a reference: a temporary
        image = widget._icon.pixmap().toImage()  # is collected mid-expression
        opaque = sum(1 for y in range(0, image.height(), 2)
                     for x in range(0, image.width(), 2)
                     if image.pixelColor(x, y).alpha() > 0)
        assert opaque > 20, "the mark drew nothing"

    def test_mark_color_repaints(self, qapp):
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        widget = QCustomEmptyState()
        before = widget._icon.pixmap().toImage()
        widget.markColor = "#ff0000"
        assert widget._icon.pixmap().toImage() != before

    def test_mark_size_repaints(self, qapp):
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        widget = QCustomEmptyState()
        widget.markSize = 96
        assert widget._icon.pixmap().width() >= 96

    def test_mark_follows_the_theme(self, qapp):
        """qproperty-markColor must be driven by the token QSS."""
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens, DesignTokens
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        applyDesignTokens(qapp, theme="dark")
        widget = QCustomEmptyState()
        widget.ensurePolished()
        expected = DesignTokens(theme="dark").role("outline").lower()
        assert widget.markColor.name().lower() == expected
        qapp.setStyleSheet("")


class TestSetIconStillWorks:
    def test_string_icon_is_honoured(self, qapp):
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        widget = QCustomEmptyState()
        widget.setIcon("!")
        assert widget._icon.text() == "!"
        assert widget._icon.pixmap().isNull()

    def test_none_restores_the_painted_default(self, qapp):
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        widget = QCustomEmptyState()
        widget.setIcon("!")
        widget.setIcon(None)
        assert widget._icon.text() == ""
        assert not widget._icon.pixmap().isNull()

    def test_pixmap_icon_is_honoured(self, qapp):
        from qtpy.QtGui import QPixmap
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        pixmap = QPixmap(32, 32)
        pixmap.fill()
        widget = QCustomEmptyState()
        widget.setIcon(pixmap)
        assert widget._icon.pixmap().width() == 32
