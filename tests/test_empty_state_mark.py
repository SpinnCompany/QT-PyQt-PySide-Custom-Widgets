"""QCustomEmptyState's default mark is painted, not a glyph.

It used to default to an emoji, which the design lint bans: a glyph does not
tint with the theme, does not scale cleanly, and renders as a different picture
on every platform. The violation was sitting in the lint baseline, so nothing
caught it until it appeared in a public documentation screenshot.
"""
import pytest


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
        expected = DesignTokens(theme="dark").role("on-surface-muted").lower()
        assert widget.markColor.name().lower() == expected
        qapp.setStyleSheet("")

    def test_mark_and_glyph_slots_agree(self, qapp):
        """The painted mark and a caller's glyph share one slot, so one role.

        They drifted apart once: #emptyIcon moved to the muted foreground role
        and qproperty-markColor stayed on "outline", so the built-in mark was
        invisible while a supplied glyph in the same position was not.
        """
        from Custom_Widgets.theming.tokens import DesignTokens, emptystate_qss
        for theme in ("light", "dark"):
            css = emptystate_qss(DesignTokens(theme))
            mark = css.split("qproperty-markColor:")[1].split(";")[0].strip()
            glyph = css.split("#emptyIcon { color:")[1].split(";")[0].strip()
            assert mark == glyph, "%s: mark %s != glyph %s" % (theme, mark, glyph)

    @pytest.mark.parametrize("theme,surface", [("light", "#ffffff"),
                                               ("dark", "#0f172a")])
    def test_mark_clears_the_graphical_contrast_minimum(self, qapp, theme, surface):
        """Thin line art has to be visible: WCAG wants 3:1 for graphics."""
        from Custom_Widgets.theming.tokens import DesignTokens

        def luminance(value):
            value = value.lstrip("#")
            channels = []
            for pair in (value[0:2], value[2:4], value[4:6]):
                c = int(pair, 16) / 255.0
                channels.append(c / 12.92 if c <= 0.03928
                                else ((c + 0.055) / 1.055) ** 2.4)
            return (0.2126 * channels[0] + 0.7152 * channels[1]
                    + 0.0722 * channels[2])

        mark = DesignTokens(theme).role("on-surface-muted")
        high, low = sorted((luminance(mark), luminance(surface)), reverse=True)
        assert (high + 0.05) / (low + 0.05) >= 3.0


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
