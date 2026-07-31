"""QCustomVerificationCode — OTP entry, editing behaviour, paste, Designer."""

from qtpy.QtCore import Qt, QEvent
from qtpy.QtGui import QKeyEvent


def _type(widget, text):
    for ch in text:
        widget.keyPressEvent(QKeyEvent(QEvent.KeyPress, 0, Qt.NoModifier, ch))


def _key(widget, key):
    widget.keyPressEvent(QKeyEvent(QEvent.KeyPress, key, Qt.NoModifier, ""))


class TestVerificationCodeEntry:
    def test_typing_fills_boxes_left_to_right(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=6)
        _type(v, "123456")
        assert v.code == "123456" and v.isComplete() is True

    def test_completed_fires_once_full(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4)
        done, changed = [], []
        v.completed.connect(done.append)
        v.codeChanged.connect(changed.append)
        _type(v, "123")
        assert done == [] and changed[-1] == "123"
        _type(v, "4")
        assert done == ["1234"]

    def test_typing_past_the_end_overwrites_last_box(self, qapp):
        """The caret parks on the final box; it must not silently drop input."""
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=3)
        _type(v, "12345")
        assert v.code == "125"

    def test_numeric_mode_rejects_letters(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4, inputMode="numeric")
        _type(v, "1a2b")
        assert v.code == "12"

    def test_alpha_mode_rejects_digits(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4, inputMode="alpha")
        _type(v, "a1b2")
        assert v.code == "AB"

    def test_alphanumeric_accepts_both(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4, inputMode="alphanumeric")
        _type(v, "a1b2")
        assert v.code == "A1B2"

    def test_uppercase_can_be_disabled(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4, inputMode="alpha")
        v.uppercase = False
        _type(v, "abcd")
        assert v.code == "abcd"


class TestVerificationCodeEditing:
    def test_backspace_clears_current_then_steps_back(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4)
        _type(v, "12")                      # caret now on box 2 (empty)
        _key(v, Qt.Key_Backspace)           # empty box -> step back, clear "2"
        assert v.code == "1"
        _key(v, Qt.Key_Backspace)
        assert v.code == ""

    def test_backspace_on_filled_box_clears_in_place(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=3)
        _type(v, "123")                     # caret parked on last box
        _key(v, Qt.Key_Backspace)
        assert v.code == "12"

    def test_backspace_at_start_is_safe(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4)
        _key(v, Qt.Key_Backspace)
        assert v.code == ""

    def test_arrow_keys_move_without_destroying(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4)
        _type(v, "1234")
        _key(v, Qt.Key_Home)
        _type(v, "9")
        assert v.code == "9234"
        _key(v, Qt.Key_End)
        _type(v, "8")
        assert v.code == "9238"

    def test_delete_clears_in_place(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=3)
        _type(v, "123")
        _key(v, Qt.Key_Home)
        _key(v, Qt.Key_Delete)
        assert v.code == "23"

    def test_clear(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4)
        _type(v, "1234")
        v.clear()
        assert v.code == "" and v.isComplete() is False


class TestVerificationCodePaste:
    def test_set_code_text_ignores_formatting(self, qapp):
        """A code copied as '123 456' or '123-456' must still land."""
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=6)
        v.setCodeText("123 456")
        assert v.code == "123456"
        v.setCodeText("123-456")
        assert v.code == "123456"

    def test_paste_truncates_to_digits(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4)
        v.setCodeText("123456789")
        assert v.code == "1234"

    def test_paste_shorter_than_digits(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=6)
        v.setCodeText("12")
        assert v.code == "12" and v.isComplete() is False

    def test_ctrl_v_pastes_from_clipboard(self, qapp):
        from qtpy.QtGui import QKeySequence
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        qapp.clipboard().setText("987654")
        v = QCustomVerificationCode(digits=6)
        v.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_V,
                                  Qt.ControlModifier, "v"))
        assert v.code == "987654"


class TestVerificationCodeDesigner:
    def test_code_property_roundtrip(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=6)
        v.code = "424242"
        assert v.code == "424242"

    def test_changing_digits_keeps_what_fits(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=6)
        v.code = "123456"
        v.digits = 4
        assert v.code == "1234"
        v.digits = 6
        assert v.code == "1234"           # grew back, keeps what it had

    def test_digits_clamped_to_at_least_one(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=6)
        v.digits = 0
        assert v.digits == 1

    def test_changing_input_mode_refilters_existing(self, qapp):
        """A mode change must not leave forbidden characters in the boxes."""
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4, inputMode="alphanumeric")
        v.code = "A1B2"
        v.inputMode = "numeric"
        assert v.code == "12"

    def test_unknown_input_mode_falls_back(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=4)
        v.inputMode = "nonsense"
        assert v.inputMode == "numeric"

    def test_size_hint_tracks_box_metrics(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=6)
        base = v.sizeHint().width()
        v.boxWidth = 60
        assert v.sizeHint().width() > base
        v.boxSpacing = 24
        assert v.sizeHint().width() > base

    def test_separator_widens_the_widget(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        plain = QCustomVerificationCode(digits=6)
        split = QCustomVerificationCode(digits=6)
        split.separatorAfter = 3
        assert split.sizeHint().width() > plain.sizeHint().width()

    def test_masked_changes_render(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        plain = QCustomVerificationCode(digits=4)
        plain.code = "1234"
        plain.resize(200, 56)
        masked = QCustomVerificationCode(digits=4)
        masked.code = "1234"
        masked.masked = True
        masked.resize(200, 56)
        assert plain.grab().toImage() != masked.grab().toImage()

    def test_error_state_changes_render(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        ok = QCustomVerificationCode(digits=4)
        ok.resize(200, 56)
        bad = QCustomVerificationCode(digits=4)
        bad.state = "error"
        bad.resize(200, 56)
        assert ok.grab().toImage() != bad.grab().toImage()

    def test_paints(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        v = QCustomVerificationCode(digits=6)
        v.code = "123456"
        v.resize(280, 56)
        img = v.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 3)
                  for x in range(0, img.width(), 3)}
        assert len(colors) > 2

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.QCustomVerificationCode import QCustomVerificationCode
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        v = QCustomVerificationCode(digits=4)
        v.ensurePolished()
        assert v.boxBorderErrorColor.name().lower() == "#dc2626"   # destructive
        assert v.boxBackgroundColor.name().lower() == "#ffffff"    # surface
        qapp.setStyleSheet("")
