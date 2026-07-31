"""QCustomRadioGroup — options, exclusive selection, Designer CSV, painting."""


class TestRadioGroupOptions:
    def test_default_options(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup()
        assert g.count() == 3
        assert g.value() == "" and g.currentIndex() == -1

    def test_set_options_strings(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["A", "B"])
        assert g.options() == [("A", "A"), ("B", "B")]
        assert len(g.buttons()) == 2

    def test_value_equals_label_syntax(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["free=Community", "pro=Pro"])
        assert g.options() == [("free", "Community"), ("pro", "Pro")]
        assert g.buttons()[0].text == "Community"

    def test_tuple_and_dict_options(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=[("a", "Alpha"), {"value": "b", "label": "Beta"}])
        assert g.options() == [("a", "Alpha"), ("b", "Beta")]

    def test_setting_options_keeps_surviving_selection(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b", "c"], value="b")
        assert g.value() == "b"
        g.setOptions(["b", "c", "d"])            # b survives
        assert g.value() == "b" and g.currentIndex() == 0
        g.setOptions(["x", "y"])                 # b is gone
        assert g.value() == "" and g.currentIndex() == -1


class TestRadioGroupSelection:
    def test_set_value_emits_once(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b"])
        values, indexes = [], []
        g.valueChanged.connect(values.append)
        g.currentIndexChanged.connect(indexes.append)
        g.setValue("b")
        assert values == ["b"] and indexes == [1]
        g.setValue("b")                          # no-op
        assert values == ["b"]

    def test_selection_is_exclusive(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b", "c"])
        g.setValue("a")
        assert [b.isChecked() for b in g.buttons()] == [True, False, False]
        g.setValue("c")
        assert [b.isChecked() for b in g.buttons()] == [False, False, True]

    def test_clicking_a_button_drives_the_group(self, qapp):
        """The group must react to its own buttons, not just to setValue."""
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b"])
        seen = []
        g.valueChanged.connect(seen.append)
        g.buttons()[1].setChecked(True)          # as a user click would
        assert g.value() == "b" and seen == ["b"]
        assert g.buttons()[0].isChecked() is False

    def test_unknown_value_ignored(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b"], value="a")
        seen = []
        g.valueChanged.connect(seen.append)
        g.setValue("nope")
        assert g.value() == "a" and seen == []

    def test_current_index_and_label(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["free=Community", "pro=Pro"])
        g.setCurrentIndex(1)
        assert g.value() == "pro" and g.currentLabel() == "Pro"
        g.setCurrentIndex(99)                    # out of range: ignored
        assert g.value() == "pro"

    def test_clear_selection(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b"], value="a")
        seen = []
        g.valueChanged.connect(seen.append)
        g.clearSelection()
        assert g.value() == "" and seen == [""]
        assert not any(b.isChecked() for b in g.buttons())


class TestRadioGroupDesigner:
    def test_options_csv_roundtrip(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup()
        g.optionsCsv = "One,Two,Three"
        assert g.count() == 3 and g.optionsCsv == "One,Two,Three"

    def test_options_csv_with_values(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup()
        g.optionsCsv = "free=Community,pro=Pro"
        assert g.options() == [("free", "Community"), ("pro", "Pro")]
        assert g.optionsCsv == "free=Community,pro=Pro"

    def test_options_csv_accepts_semicolons_and_blanks(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup()
        g.optionsCsv = "A; B,,C ,"
        assert [lbl for _, lbl in g.options()] == ["A", "B", "C"]

    def test_selected_value_property(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b"])
        g.selectedValue = "b"
        assert g.selectedValue == "b" and g.value() == "b"

    def test_orientation_switch_keeps_options_and_selection(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b", "c"], value="b")
        g.orientation = "horizontal"
        assert g.orientation == "horizontal"
        assert g.count() == 3 and g.value() == "b"
        assert [btn.isChecked() for btn in g.buttons()] == [False, True, False]
        g.orientation = "vertical"
        assert g.count() == 3 and g.value() == "b"

    def test_size_variant_propagates_to_buttons(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b"])
        g.sizeVariant = "lg"
        assert all(btn.sizeVariant == "lg" for btn in g.buttons())

    def test_spacing_property(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        g = QCustomRadioGroup(options=["a", "b"])
        g.spacingPx = 24
        assert g.spacingPx == 24


class TestRadioGroupPainting:
    def test_title_paints(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        bare = QCustomRadioGroup(options=["a"])
        bare.resize(220, 80)
        titled = QCustomRadioGroup(options=["a"], title="Choose a plan")
        titled.resize(220, 80)
        assert bare.grab().toImage() != titled.grab().toImage()

    def test_colors_via_qproperty_and_paints(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        g = QCustomRadioGroup(options=["a", "b"], value="a", title="Plan")
        g.ensurePolished()
        assert g.titleColor.name().lower() == "#0f172a"      # on-surface
        g.resize(220, 90)
        img = g.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 3)
                  for x in range(0, img.width(), 3)}
        assert len(colors) > 2                               # actually painted
        qapp.setStyleSheet("")
