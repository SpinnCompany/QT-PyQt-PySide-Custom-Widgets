"""QCustomButtonGroup - accessible button group with tokenized styling."""


class TestQCustomButtonGroup:
    def test_defaults(self, qapp):
        from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
        grp = QCustomButtonGroup()
        assert grp.variant == "outline"
        assert grp.sizeVariant == "md"
        assert grp.exclusive is True
        assert grp.orientation == "vertical"

    def test_add_buttons(self, qapp):
        from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
        grp = QCustomButtonGroup()
        grp.addButton("Option A", 0)
        grp.addButton("Option B", 1)
        # Check button group has 2 buttons
        assert len(grp._group.buttons()) == 2

    def test_set_buttons(self, qapp):
        from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
        grp = QCustomButtonGroup()
        grp.setButtons(["Red", "Green", "Blue"])
        assert len(grp._group.buttons()) == 3

    def test_selection_changed_signal(self, qapp):
        from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
        grp = QCustomButtonGroup()
        grp.addButton("A", 0)
        grp.addButton("B", 1)
        signal_spy = []

        def on_change(bid, text):
            signal_spy.append((bid, text))

        grp.selectionChanged.connect(on_change)
        # Click button to trigger signal
        buttons = grp._group.buttons()
        if buttons:
            buttons[0].click()
        assert len(signal_spy) == 1
        assert signal_spy[0] == (0, "A")

    def test_selected_id_and_text(self, qapp):
        from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
        grp = QCustomButtonGroup()
        grp.addButton("Option A", 10)
        grp.addButton("Option B", 20)
        grp.setSelectedId(10)
        assert grp.selectedId() == 10
        assert grp.selectedText() == "Option A"

    def test_variant_property(self, qapp):
        from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
        grp = QCustomButtonGroup()
        for v in ("primary", "secondary", "outline"):
            grp.variant = v
            assert grp.variant == v

    def test_size_variant_property(self, qapp):
        from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
        grp = QCustomButtonGroup()
        for s in ("sm", "md", "lg"):
            grp.sizeVariant = s
            assert grp.sizeVariant == s

    def test_exclusive_mode(self, qapp):
        from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup
        grp = QCustomButtonGroup(exclusive=False)
        assert grp.exclusive is False
        grp.exclusive = True
        assert grp.exclusive is True
