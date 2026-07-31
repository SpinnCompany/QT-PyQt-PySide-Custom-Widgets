"""QCustomTextArea — multi-line input, char limit, counter, auto-grow."""


class TestTextAreaBasics:
    def test_is_multiline(self, qapp):
        """The whole reason this widget exists: QCustomInput cannot do this."""
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.setPlainText("line one\nline two\nline three")
        assert t.toPlainText().count("\n") == 2
        assert t.length() == len("line one\nline two\nline three")

    def test_placeholder_via_ctor(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(placeholder="Say something")
        assert t.placeholderText() == "Say something"

    def test_length_changed_signal(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        seen = []
        t.lengthChanged.connect(seen.append)
        t.setPlainText("abc")
        assert seen[-1] == 3

    def test_clear_text(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.setPlainText("something")
        t.clearText()
        assert t.toPlainText() == "" and t.length() == 0


class TestTextAreaLimit:
    def test_no_limit_by_default(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.setPlainText("x" * 5000)
        assert t.length() == 5000
        assert t.remaining() == -1 and t.isOverLimit() is False

    def test_truncates_to_max_length(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(maxLength=10)
        t.setPlainText("0123456789ABCDEF")
        assert t.toPlainText() == "0123456789"
        assert t.length() == 10

    def test_remaining_counts_down(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(maxLength=10)
        t.setPlainText("abc")
        assert t.remaining() == 7
        t.setPlainText("abcdefghij")
        assert t.remaining() == 0 and t.isOverLimit() is True

    def test_limit_reached_signal(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(maxLength=5)
        seen = []
        t.limitReached.connect(seen.append)
        t.setPlainText("abc")
        assert seen == []
        t.setPlainText("abcde")
        assert seen == [True]

    def test_truncation_does_not_recurse(self, qapp):
        """setPlainText inside textChanged would loop without the guard."""
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(maxLength=4)
        t.setPlainText("way too long for the limit")
        assert t.toPlainText() == "way "

    def test_setting_max_length_truncates_existing(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.setPlainText("0123456789")
        t.maxLength = 4
        assert t.toPlainText() == "0123"

    def test_negative_max_length_clamps_to_zero(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.maxLength = -5
        assert t.maxLength == 0
        t.setPlainText("unbounded")
        assert t.length() == 9


class TestTextAreaRows:
    def test_min_rows_sets_minimum_height(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        small = QCustomTextArea()
        small.minRows = 2
        tall = QCustomTextArea()
        tall.minRows = 10
        assert tall.minimumHeight() > small.minimumHeight()

    def test_max_rows_cannot_sit_below_min_rows(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.minRows = 6
        t.maxRows = 2               # contradictory: min must follow
        assert t.minRows <= t.maxRows

    def test_min_rows_cannot_exceed_max_rows(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.maxRows = 3
        t.minRows = 9
        assert t.minRows <= t.maxRows

    def test_rows_clamp_to_at_least_one(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.minRows = 0
        t.maxRows = -4
        assert t.minRows >= 1 and t.maxRows >= 1

    def test_auto_grow_bounds_height(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.minRows, t.maxRows = 2, 4
        t.autoGrow = True
        t.resize(280, 10)
        floor = t.minimumHeight()
        t.setPlainText("\n".join("line %d" % i for i in range(40)))
        assert t.maximumHeight() <= t._heightForRows(4)
        assert t.minimumHeight() >= floor

    def test_auto_grow_off_leaves_height_free(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.autoGrow = False
        assert t.maximumHeight() == 16777215


class TestTextAreaDesigner:
    def test_variant_and_size_roundtrip(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.variant = "ghost"
        t.sizeVariant = "lg"
        assert t.variant == "ghost" and t.sizeVariant == "lg"

    def test_state_property_and_set_error(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        assert t.state == "default"
        t.setError("Too short")
        assert t.state == "error" and t.toolTip() == "Too short"
        t.setError(None)
        assert t.state == "default" and t.toolTip() == ""

    def test_error_state_survives_focus(self, qapp):
        """Focusing an invalid field must not silently clear the error."""
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.setError("bad")
        t.focusInEvent(_focusEvent())
        assert t.state == "error"
        t.focusOutEvent(_focusEvent(False))
        assert t.state == "error"

    def test_focus_toggles_state_when_valid(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.focusInEvent(_focusEvent())
        assert t.state == "focused"
        t.focusOutEvent(_focusEvent(False))
        assert t.state == "default"

    def test_show_counter_reserves_space(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        off = QCustomTextArea(maxLength=20)
        off.resize(280, 96)
        on = QCustomTextArea(maxLength=20)
        on.showCounter = True
        on.resize(280, 96)
        assert on.viewportMargins().bottom() > off.viewportMargins().bottom()

    def test_counter_text_tracks_the_content(self, qapp):
        """Assert the counter's actual text.

        An earlier version painted this with QPainter(self), which is never
        active inside a QAbstractScrollArea's viewport paintEvent, so nothing
        was drawn at all — and an image-comparison test still passed because
        reserving the strip shifted the layout. Check the value, not the pixels.
        """
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(maxLength=20)
        t.showCounter = True
        t.resize(280, 96)
        t.setPlainText("hello")
        # isHidden(), not isVisible(): a child only reports visible once its
        # ancestors are shown, and these tests never show a top-level window.
        assert t._counterLabel.isHidden() is False
        assert t._counterLabel.text() == "5/20"
        t.setPlainText("hello there")
        assert t._counterLabel.text() == "11/20"

    def test_counter_without_limit_shows_bare_count(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea()
        t.showCounter = True
        t.resize(280, 96)
        t.setPlainText("abcd")
        assert t._counterLabel.text() == "4"

    def test_counter_hidden_when_disabled(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(maxLength=20)
        t.resize(280, 96)
        t.setPlainText("hello")
        assert t._counterLabel.isHidden() is True

    def test_counter_turns_over_colour_at_the_limit(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(maxLength=5)
        t.showCounter = True
        t.resize(280, 96)
        t.setPlainText("abc")
        assert t._counterOverColor.name() not in t._counterLabel.styleSheet()
        t.setPlainText("abcde")
        assert t._counterOverColor.name() in t._counterLabel.styleSheet()

    def test_counter_stays_inside_the_widget(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(maxLength=20)
        t.showCounter = True
        t.resize(280, 96)
        t.setPlainText("hello")
        geo = t._counterLabel.geometry()
        assert geo.right() <= t.width() and geo.bottom() <= t.height()
        t.resize(400, 140)
        geo = t._counterLabel.geometry()
        assert geo.right() <= t.width() and geo.bottom() <= t.height()

    def test_counter_colors_via_qproperty(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        t = QCustomTextArea(maxLength=5)
        t.showCounter = True
        t.ensurePolished()
        assert t.counterOverColor.name().lower() == "#dc2626"   # destructive
        qapp.setStyleSheet("")

    def test_paints(self, qapp):
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        t = QCustomTextArea(placeholder="Say something")
        t.resize(280, 96)
        img = t.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) >= 2


def _focusEvent(gained=True):
    from qtpy.QtCore import QEvent
    from qtpy.QtGui import QFocusEvent
    return QFocusEvent(QEvent.FocusIn if gained else QEvent.FocusOut)
