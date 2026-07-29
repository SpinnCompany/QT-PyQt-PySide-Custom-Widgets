"""QCustomInput - modern text input with variant/sizeVariant properties."""


class TestQCustomInputVariants:
    def test_defaults(self, qapp):
        from Custom_Widgets.QCustomInput import QCustomInput
        inp = QCustomInput()
        assert inp.variant == "outline"
        assert inp.sizeVariant == "md"
        assert inp.state == "default"

    def test_variant_property_set_and_get(self, qapp):
        from Custom_Widgets.QCustomInput import QCustomInput
        inp = QCustomInput()
        for v in ("primary", "secondary", "outline", "ghost"):
            inp.variant = v
            assert inp.variant == v
            assert inp.property("variant") == v

    def test_size_variant_set_and_get(self, qapp):
        from Custom_Widgets.QCustomInput import QCustomInput
        inp = QCustomInput()
        for s in ("sm", "md", "lg"):
            inp.sizeVariant = s
            assert inp.sizeVariant == s
            assert inp.property("sizeVariant") == s

    def test_height_changes_with_size(self, qapp):
        from Custom_Widgets.QCustomInput import QCustomInput
        inp = QCustomInput()
        inp.sizeVariant = "sm"
        h_sm = inp.minimumHeight()
        inp.sizeVariant = "lg"
        h_lg = inp.minimumHeight()
        assert h_lg > h_sm

    def test_error_state_and_tooltip(self, qapp):
        from Custom_Widgets.QCustomInput import QCustomInput
        inp = QCustomInput()
        inp.setError("This field is required")
        assert inp.state == "error"
        assert inp.toolTip() == "This field is required"
        inp.setError(None)
        assert inp.state == "default"
        assert inp.toolTip() == ""

    def test_focus_state_change(self, qapp):
        from Custom_Widgets.QCustomInput import QCustomInput
        inp = QCustomInput()
        assert inp.state == "default"
        # Manually set state to simulate focus
        inp.state = "focused"
        assert inp.state == "focused"
        inp.state = "default"
        assert inp.state == "default"
