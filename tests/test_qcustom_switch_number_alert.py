"""QCustomSwitch + QCustomNumberInput + QCustomAlert."""


class TestSwitch:
    def test_toggle_and_signal(self, qapp):
        from Custom_Widgets.QCustomSwitch import QCustomSwitch
        s = QCustomSwitch()
        assert s.isChecked() is False
        seen = []
        s.toggled.connect(seen.append)
        s.setChecked(True)
        assert s.isChecked() is True and seen == [True]
        s.toggle()
        assert s.isChecked() is False and seen == [True, False]
        s.setChecked(False)                       # no-op, no extra signal
        assert seen == [True, False]

    def test_checked_property(self, qapp):
        from Custom_Widgets.QCustomSwitch import QCustomSwitch
        s = QCustomSwitch()
        s.checked = True
        assert s.checked is True and s.isChecked() is True

    def test_size_variant_changes_hint(self, qapp):
        from Custom_Widgets.QCustomSwitch import QCustomSwitch
        s = QCustomSwitch()
        s.sizeVariant = "sm"
        small = s.sizeHint().width()
        s.sizeVariant = "lg"
        assert s.sizeHint().width() > small

    def test_colors_via_qproperty_and_paints(self, qapp):
        from Custom_Widgets.QCustomSwitch import QCustomSwitch
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        s = QCustomSwitch(checked=True)
        s.ensurePolished()
        assert s.trackOnColor.name().lower() == "#2563eb"     # accent
        assert s.trackOffColor.name().lower() == "#cbd5e1"    # outline
        assert s.thumbColor.name().lower() == "#ffffff"       # surface
        s.resize(44, 26)
        img = s.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 3)
                  for x in range(0, img.width(), 3)}
        assert len(colors) > 2                                # actually painted
        qapp.setStyleSheet("")


class TestNumberInput:
    def test_step_and_clamp_int(self, qapp):
        from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
        n = QCustomNumberInput(minimum=0, maximum=10, value=5, step=2, decimals=0)
        assert n.value() == 5 and isinstance(n.value(), int)
        seen = []
        n.valueChanged.connect(seen.append)
        n.stepUp(); n.stepUp()
        assert n.value() == 9 and seen == [7, 9]
        n.stepUp()                                # 11 -> clamped to 10
        assert n.value() == 10 and n._up.isEnabled() is False
        n.setValue(-5)                            # clamp low
        assert n.value() == 0 and n._down.isEnabled() is False

    def test_float_decimals(self, qapp):
        from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
        f = QCustomNumberInput(minimum=0, maximum=1, value=0, step=0.1, decimals=2)
        f.setValue(0.25)
        assert f.value() == 0.25 and isinstance(f.value(), float)
        assert f.lineEdit().text() == "0.25"

    def test_edit_commits(self, qapp):
        from Custom_Widgets.QCustomNumberInput import QCustomNumberInput
        n = QCustomNumberInput(minimum=0, maximum=100, value=1, decimals=0)
        n.lineEdit().setText("42")
        n._onEdited()
        assert n.value() == 42
        n.lineEdit().setText("nonsense")          # invalid -> keeps last value
        n._onEdited()
        assert n.value() == 42


class TestAlert:
    def test_variant_glyph_and_property(self, qapp):
        from Custom_Widgets.QCustomAlert import QCustomAlert
        a = QCustomAlert(title="Heads up", text="msg", variant="warning")
        assert a.variant == "warning" and a._icon.text() == "⚠"
        a.variant = "success"
        assert a._icon.text() == "✓"
        a.variant = "bogus"                       # falls back to info
        assert a.variant == "info" and a._icon.text() == "ℹ"

    def test_title_text_visibility(self, qapp):
        from Custom_Widgets.QCustomAlert import QCustomAlert
        a = QCustomAlert()
        assert a._title.isHidden() and a._text.isHidden()
        a.setTitle("Hi"); a.setText("there")
        assert not a._title.isHidden() and not a._text.isHidden()

    def test_dismiss(self, qapp):
        from Custom_Widgets.QCustomAlert import QCustomAlert
        a = QCustomAlert(text="closeable")
        assert a._close.isHidden()                # not dismissible by default
        a.setDismissible(True)
        assert not a._close.isHidden()
        closed = []
        a.closed.connect(lambda: closed.append(1))
        a.closeButton().click()
        assert closed == [1] and a.isHidden()
