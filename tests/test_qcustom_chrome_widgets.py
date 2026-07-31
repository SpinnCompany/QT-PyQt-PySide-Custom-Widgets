"""Chrome & branding widgets: FeaturedIcon, CopyButton, SocialButton, HeaderNav."""
from qtpy.QtCore import QEvent, QPointF, Qt
from qtpy.QtGui import QKeyEvent, QMouseEvent

ICON = "Custom_Widgets/components/icons/rocket_launch.png"


def _click(widget, point):
    widget.mouseReleaseEvent(QMouseEvent(
        QEvent.MouseButtonRelease, QPointF(point), Qt.LeftButton,
        Qt.LeftButton, Qt.NoModifier))


class TestFeaturedIcon:
    def _icon(self, **kwargs):
        from Custom_Widgets.QCustomFeaturedIcon import QCustomFeaturedIcon
        w = QCustomFeaturedIcon(icon=ICON, **kwargs)
        w.resize(w.sizeHint())
        return w

    def test_size_variants(self, qapp):
        small = self._icon()
        small.sizeVariant = "sm"
        large = self._icon()
        large.sizeVariant = "xl"
        assert large.sizeHint().width() > small.sizeHint().width()

    def test_is_square(self, qapp):
        hint = self._icon().sizeHint()
        assert hint.width() == hint.height()

    def test_variants_render_differently(self, qapp):
        seen = []
        for variant in ("tinted", "filled", "outline", "gradient"):
            widget = self._icon(variant=variant)
            seen.append(widget.grab().toImage())
        for i in range(len(seen)):
            for j in range(i + 1, len(seen)):
                assert seen[i] != seen[j], "variants %d and %d look identical" % (i, j)

    def test_shapes_render_differently(self, qapp):
        circle = self._icon(shape="circle")
        square = self._icon(shape="square")
        assert circle.grab().toImage() != square.grab().toImage()

    def test_enum_fallbacks(self, qapp):
        widget = self._icon()
        widget.variant = "nonsense"
        widget.shape = "nonsense"
        assert widget.variant == "tinted" and widget.shape == "rounded"

    def test_missing_icon_still_paints(self, qapp):
        from Custom_Widgets.QCustomFeaturedIcon import QCustomFeaturedIcon
        widget = QCustomFeaturedIcon()
        widget.resize(48, 48)
        assert widget.hasIcon() is False
        widget.grab()

    def test_clicked(self, qapp):
        widget = self._icon()
        seen = []
        widget.clicked.connect(lambda: seen.append(True))
        _click(widget, widget.rect().center())
        assert seen == [True]


class TestCopyButton:
    def _button(self, payload="secret", **kwargs):
        from Custom_Widgets.QCustomCopyButton import QCustomCopyButton
        w = QCustomCopyButton(payload=payload, **kwargs)
        w.resize(w.sizeHint())
        return w

    def test_copy_puts_text_on_the_clipboard(self, qapp):
        button = self._button("sk-abc123")
        seen = []
        button.copied.connect(seen.append)
        assert button.copy() is True
        assert qapp.clipboard().text() == "sk-abc123"
        assert seen == ["sk-abc123"]
        assert button.isConfirming() is True

    def test_empty_payload_is_a_noop(self, qapp):
        """Confirming a copy that put nothing on the clipboard is worse than
        not confirming at all."""
        button = self._button("")
        seen = []
        button.copied.connect(seen.append)
        assert button.copy() is False
        assert seen == [] and button.isConfirming() is False

    def test_width_does_not_jump_on_confirm(self, qapp):
        """Sized against the longer caption so the layout does not shift."""
        button = self._button(text="Copy")
        button.copiedText = "Copied to clipboard!"
        before = button.sizeHint().width()
        button.copy()
        assert button.sizeHint().width() == before

    def test_reset_clears_confirmation(self, qapp):
        button = self._button()
        button.copy()
        button._reset()
        assert button.isConfirming() is False

    def test_confirmation_changes_render(self, qapp):
        idle = self._button()
        done = self._button()
        done.copy()
        assert idle.grab().toImage() != done.grab().toImage()

    def test_icon_only_is_square(self, qapp):
        button = self._button()
        button.iconOnly = True
        hint = button.sizeHint()
        assert hint.width() == hint.height()

    def test_keyboard_activates(self, qapp):
        button = self._button("kb")
        button.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Space,
                                       Qt.NoModifier, " "))
        assert qapp.clipboard().text() == "kb"

    def test_variant_falls_back(self, qapp):
        button = self._button()
        button.variant = "nonsense"
        assert button.variant == "outline"


class TestSocialButton:
    def _button(self, brand="github", **kwargs):
        from Custom_Widgets.QCustomSocialButton import QCustomSocialButton
        w = QCustomSocialButton(brand=brand, icon=ICON, **kwargs)
        w.resize(w.sizeHint())
        return w

    def test_known_brand_sets_colour_and_caption(self, qapp):
        button = self._button("github")
        assert button.isKnownBrand() is True
        assert button.brandColor.name() == "#24292f"
        assert "GitHub" in button.text

    def test_unknown_brand_is_kept(self, qapp):
        """brandColor still lets a caller support anything not in the table."""
        button = self._button("mastodon")
        assert button.isKnownBrand() is False
        assert button.brand == "mastodon"
        button.brandColor = "#6364ff"
        assert button.brandColor.name() == "#6364ff"

    def test_brand_is_normalised(self, qapp):
        button = self._button("  GitHub  ")
        assert button.brand == "github" and button.isKnownBrand() is True

    def test_explicit_text_survives_the_brand_default(self, qapp):
        from Custom_Widgets.QCustomSocialButton import QCustomSocialButton
        button = QCustomSocialButton(brand="github", text="Log in")
        assert button.text == "Log in"

    def test_foreground_contrast_flips_on_light_brands(self, qapp):
        """White on a yellow brand is unreadable, so the foreground is chosen
        by luminance rather than a fixed pairing."""
        button = self._button()
        button.brandColor = "#000000"
        assert button.foregroundColor().name() == "#ffffff"
        button.brandColor = "#ffdd00"
        assert button.foregroundColor().name() == "#0f172a"

    def test_outline_uses_the_brand_colour_for_text(self, qapp):
        button = self._button()
        button.variant = "outline"
        assert button.foregroundColor().name() == button.brandColor.name()

    def test_brand_names_listed(self, qapp):
        assert "github" in self._button().brandNames()

    def test_variants_and_shapes_render_differently(self, qapp):
        solid = self._button()
        soft = self._button()
        soft.variant = "soft"
        pill = self._button()
        pill.shape = "pill"
        assert solid.grab().toImage() != soft.grab().toImage()
        assert solid.grab().toImage() != pill.grab().toImage()

    def test_clicked(self, qapp):
        button = self._button()
        seen = []
        button.clicked.connect(lambda: seen.append(True))
        _click(button, button.rect().center())
        assert seen == [True]


class TestHeaderNav:
    def _nav(self, items=("Home", "Docs", "Pricing", "Blog"), brand="Spinn UI",
             size=(640, 56)):
        from Custom_Widgets.QCustomHeaderNav import QCustomHeaderNav
        nav = QCustomHeaderNav(items=list(items), brand=brand)
        nav.resize(*size)
        return nav

    def test_items_and_default_selection(self, qapp):
        nav = self._nav()
        assert nav.count() == 4
        assert nav.currentKeyValue() == "Home"

    def test_key_equals_label_syntax(self, qapp):
        nav = self._nav(items=["home=Home", "docs=Docs"])
        assert nav.items() == [("home", "Home"), ("docs", "Docs")]
        assert nav.labelFor("docs") == "Docs"

    def test_selection_emits_once(self, qapp):
        nav = self._nav()
        seen = []
        nav.itemSelected.connect(seen.append)
        nav.setCurrentKey("Docs")
        assert seen == ["Docs"] and nav.currentIndex() == 1
        nav.setCurrentKey("Docs")
        assert seen == ["Docs"]

    def test_unknown_key_ignored(self, qapp):
        nav = self._nav()
        assert nav.setCurrentKey("nope") is False
        assert nav.currentKeyValue() == "Home"

    def test_setting_items_keeps_a_surviving_selection(self, qapp):
        nav = self._nav()
        nav.setCurrentKey("Docs")
        nav.setItems(["Docs", "Blog"])
        assert nav.currentKeyValue() == "Docs"

    def test_setting_items_falls_back_to_the_first(self, qapp):
        nav = self._nav()
        nav.setCurrentKey("Docs")
        nav.setItems(["Alpha", "Beta"])
        assert nav.currentKeyValue() == "Alpha"

    def test_items_laid_out_left_to_right(self, qapp):
        nav = self._nav()
        rects = nav.itemRects()
        assert len(rects) == 4
        assert rects[0].left() < rects[1].left() < rects[2].left()

    def test_brand_reserves_room(self, qapp):
        with_brand = self._nav()
        without = self._nav(brand="")
        assert with_brand.itemRects()[0].left() > without.itemRects()[0].left()

    def test_narrow_width_collapses_into_overflow(self, qapp):
        """Items drop from the end rather than being squeezed: half a link is
        unreadable, and "+N" is honest about what is hidden."""
        nav = self._nav(size=(300, 56))
        assert nav.hiddenCount() > 0
        assert len(nav.itemRects()) < nav.count()

    def test_wide_width_shows_everything(self, qapp):
        nav = self._nav(size=(900, 56))
        assert nav.hiddenCount() == 0

    def test_click_selects(self, qapp):
        nav = self._nav()
        seen = []
        nav.itemSelected.connect(seen.append)
        _click(nav, nav.itemRects()[2].center())
        assert seen == ["Pricing"]

    def test_brand_click(self, qapp):
        nav = self._nav()
        seen = []
        nav.brandClicked.connect(lambda: seen.append(True))
        nav.grab()
        _click(nav, nav._brandRect.center())
        assert seen == [True]

    def test_overflow_click(self, qapp):
        nav = self._nav(size=(300, 56))
        seen = []
        nav.overflowClicked.connect(lambda: seen.append(True))
        nav.grab()
        _click(nav, nav._overflowRect.center())
        assert seen == [True]

    def test_indicator_styles_render_differently(self, qapp):
        underline = self._nav()
        pill = self._nav()
        pill.indicator = "pill"
        none = self._nav()
        none.indicator = "none"
        assert underline.grab().toImage() != pill.grab().toImage()
        assert underline.grab().toImage() != none.grab().toImage()

    def test_alignment_moves_the_items(self, qapp):
        left = self._nav()
        centre = self._nav()
        centre.alignment = "center"
        assert centre.itemRects()[0].left() > left.itemRects()[0].left()

    def test_csv_roundtrip(self, qapp):
        nav = self._nav()
        nav.itemsCsv = "a=Alpha,b=Beta"
        assert nav.itemsCsv == "a=Alpha,b=Beta"
        assert nav.count() == 2


class TestChromeTokens:
    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        from Custom_Widgets.QCustomCopyButton import QCustomCopyButton
        from Custom_Widgets.QCustomHeaderNav import QCustomHeaderNav
        applyDesignTokens(qapp, theme="light")
        button = QCustomCopyButton()
        nav = QCustomHeaderNav()
        button.ensurePolished()
        nav.ensurePolished()
        assert button.successColor.name().lower() == "#16a34a"
        assert nav.accentColor.name().lower() == "#2563eb"
        qapp.setStyleSheet("")
