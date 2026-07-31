"""QCustomRadioButton — selection, auto-exclusivity, tokens and painting."""


class TestRadioButton:
    def test_select_and_signals(self, qapp):
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        r = QCustomRadioButton(text="Option A", value="a")
        assert r.isChecked() is False
        toggles, picks = [], []
        r.toggled.connect(toggles.append)
        r.selected.connect(picks.append)
        r.setChecked(True)
        assert r.isChecked() is True and toggles == [True] and picks == ["a"]
        # Re-selecting an already-selected radio is a no-op, not a toggle-off.
        r.setChecked(True)
        assert toggles == [True] and picks == ["a"]

    def test_selected_falls_back_to_text(self, qapp):
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        r = QCustomRadioButton(text="Only Label")
        picks = []
        r.selected.connect(picks.append)
        r.setChecked(True)
        assert picks == ["Only Label"]

    def test_auto_exclusive_clears_siblings(self, qapp):
        from qtpy.QtWidgets import QWidget
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        host = QWidget()
        a = QCustomRadioButton(host, text="A", value="a")
        b = QCustomRadioButton(host, text="B", value="b")
        c = QCustomRadioButton(host, text="C", value="c")
        a.setChecked(True)
        assert (a.isChecked(), b.isChecked(), c.isChecked()) == (True, False, False)
        b.setChecked(True)
        assert (a.isChecked(), b.isChecked(), c.isChecked()) == (False, True, False)
        # a must have emitted toggled(False) when it lost the selection
        seen = []
        a.toggled.connect(seen.append)
        c.setChecked(True)
        assert b.isChecked() is False and c.isChecked() is True
        assert seen == []                         # a was already off

    def test_auto_exclusive_off_allows_multiple(self, qapp):
        from qtpy.QtWidgets import QWidget
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        host = QWidget()
        a = QCustomRadioButton(host, text="A")
        b = QCustomRadioButton(host, text="B")
        a.autoExclusive = False
        b.autoExclusive = False
        a.setChecked(True)
        b.setChecked(True)
        assert a.isChecked() is True and b.isChecked() is True

    def test_exclusivity_does_not_cross_parents(self, qapp):
        from qtpy.QtWidgets import QWidget
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        left, right = QWidget(), QWidget()
        a = QCustomRadioButton(left, text="A")
        b = QCustomRadioButton(right, text="B")
        a.setChecked(True)
        b.setChecked(True)
        assert a.isChecked() is True and b.isChecked() is True

    def test_checked_property(self, qapp):
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        r = QCustomRadioButton()
        r.checked = True
        assert r.checked is True and r.isChecked() is True

    def test_size_variant_changes_hint(self, qapp):
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        r = QCustomRadioButton(text="Label")
        r.sizeVariant = "sm"
        small = r.sizeHint().width()
        r.sizeVariant = "lg"
        assert r.sizeHint().width() > small

    def test_text_changes_hint(self, qapp):
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        r = QCustomRadioButton()
        bare = r.sizeHint().width()
        r.text = "A much longer label"
        assert r.sizeHint().width() > bare

    def test_colors_via_qproperty_and_paints(self, qapp):
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        r = QCustomRadioButton(text="Option", checked=True)
        r.ensurePolished()
        assert r.ringColor.name().lower() == "#cbd5e1"          # outline
        assert r.ringCheckedColor.name().lower() == "#2563eb"   # accent
        assert r.dotColor.name().lower() == "#2563eb"           # accent
        r.resize(140, 24)
        img = r.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 3)
                  for x in range(0, img.width(), 3)}
        assert len(colors) > 2                                  # actually painted
        qapp.setStyleSheet("")

    def test_unchecked_paints_no_dot(self, qapp):
        """The dot is the only difference between the two states."""
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        off = QCustomRadioButton(text="X")
        off.resize(60, 24)
        on = QCustomRadioButton(text="X", checked=True)
        on.resize(60, 24)
        a = off.grab().toImage()
        b = on.grab().toImage()
        assert a != b
