"""QCustomMultiSelect — multiple selection, chips, popup, Designer CSV.

Imported through the flat public path on purpose: that is what users and .ui
files use, so it exercises the legacy-alias layer too.
"""
from qtpy.QtCore import Qt


class TestMultiSelectOptions:
    def test_default_options(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect()
        assert m.count() == 3 and m.selected() == []

    def test_value_equals_label_syntax(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["r=Red", "g=Green"])
        assert m.options() == [("r", "Red"), ("g", "Green")]
        assert m.labelFor("r") == "Red"

    def test_setting_options_drops_stale_selection(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"], selected=["a", "c"])
        seen = []
        m.selectionChanged.connect(seen.append)
        m.setOptions(["a", "b"])            # c is gone
        assert m.selected() == ["a"] and seen == [["a"]]

    def test_setting_identical_options_does_not_emit(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b"], selected=["a"])
        seen = []
        m.selectionChanged.connect(seen.append)
        m.setOptions(["a", "b"])
        assert seen == []


class TestMultiSelectSelection:
    def test_select_and_deselect(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"])
        toggles, changes = [], []
        m.optionToggled.connect(lambda v, on: toggles.append((v, on)))
        m.selectionChanged.connect(changes.append)
        m.selectOption("b")
        assert m.selected() == ["b"] and toggles == [("b", True)]
        m.selectOption("b", False)
        assert m.selected() == [] and toggles[-1] == ("b", False)
        assert changes == [["b"], []]

    def test_selecting_twice_is_a_noop(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b"])
        m.selectOption("a")
        seen = []
        m.selectionChanged.connect(seen.append)
        m.selectOption("a")
        assert seen == [] and m.selected() == ["a"]

    def test_toggle(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b"])
        m.toggleOption("a")
        assert m.isSelected("a") is True
        m.toggleOption("a")
        assert m.isSelected("a") is False

    def test_unknown_value_ignored(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b"])
        m.selectOption("zzz")
        assert m.selected() == []

    def test_set_selected_preserves_order_and_drops_dupes(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"])
        m.setSelected(["c", "a", "c", "nope"])
        assert m.selected() == ["c", "a"]

    def test_max_selection_blocks_extra(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"])
        m.maxSelection = 2
        m.selectOption("a"); m.selectOption("b"); m.selectOption("c")
        assert m.selected() == ["a", "b"]

    def test_lowering_max_selection_trims(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"], selected=["a", "b", "c"])
        m.maxSelection = 1
        assert m.selected() == ["a"]

    def test_clear_selection(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b"], selected=["a", "b"])
        seen = []
        m.selectionChanged.connect(seen.append)
        m.clearSelection()
        assert m.selected() == [] and seen == [[]]
        m.clearSelection()                  # already empty
        assert seen == [[]]

    def test_selected_labels(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["r=Red", "g=Green"], selected=["g"])
        assert m.selectedLabels() == ["Green"]


class TestMultiSelectPopup:
    def test_popup_reflects_selection(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"], selected=["b"])
        m.showPopup()
        listing = m._popup.listing
        states = [listing.item(i).checkState() for i in range(listing.count())]
        assert states == [Qt.Unchecked, Qt.Checked, Qt.Unchecked]
        m.hidePopup()

    def test_ticking_an_item_updates_selection(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b"])
        m.showPopup()
        m._popup.listing.item(1).setCheckState(Qt.Checked)
        assert m.selected() == ["b"]
        m.hidePopup()

    def test_max_selection_refusal_unticks_the_box(self, qapp):
        """Refusing the selection must not leave a ticked box lying."""
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"])
        m.maxSelection = 1
        m.selectOption("a")
        m.showPopup()
        m._popup.listing.item(1).setCheckState(Qt.Checked)
        assert m.selected() == ["a"]
        assert m._popup.listing.item(1).checkState() == Qt.Unchecked
        m.hidePopup()

    def test_search_filters_items(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["Apple", "Banana", "Cherry"])
        m.searchable = True
        m.showPopup()
        m._search.setText("an")
        listing = m._popup.listing
        visible = [listing.item(i).text() for i in range(listing.count())
                   if not listing.item(i).isHidden()]
        assert visible == ["Banana"]
        m.hidePopup()

    def test_toggling_searchable_rebuilds_popup(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a"])
        m.showPopup(); m.hidePopup()
        assert m._search is None
        m.searchable = True
        m.showPopup()
        assert m._search is not None
        m.hidePopup()


class TestMultiSelectInteraction:
    def test_backspace_removes_last(self, qapp):
        from qtpy.QtCore import QEvent
        from qtpy.QtGui import QKeyEvent
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b"], selected=["a", "b"])
        m.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace,
                                  Qt.NoModifier, ""))
        assert m.selected() == ["a"]

    def test_chip_close_removes_that_chip(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"], selected=["a", "b"])
        m.resize(320, 40)
        m.grab()                                  # populate chip hit rects
        assert len(m._chipRects) == 2
        value, _chip, close = m._chipRects[0]
        from qtpy.QtCore import QEvent, QPointF
        from qtpy.QtGui import QMouseEvent
        ev = QMouseEvent(QEvent.MouseButtonRelease, QPointF(close.center()),
                         Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        m.mouseReleaseEvent(ev)
        assert value not in m.selected() and m.selected() == ["b"]


class TestMultiSelectDesigner:
    def test_options_csv_roundtrip(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect()
        m.optionsCsv = "r=Red,g=Green,b=Blue"
        assert m.count() == 3 and m.optionsCsv == "r=Red,g=Green,b=Blue"

    def test_selected_csv_roundtrip(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c"])
        m.selectedCsv = "a,c"
        assert m.selected() == ["a", "c"] and m.selectedCsv == "a,c"

    def test_selected_csv_ignores_unknown(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b"])
        m.selectedCsv = "a,zzz"
        assert m.selected() == ["a"]

    def test_placeholder_and_size_variant(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect()
        m.placeholderText = "Pick some"
        assert m.placeholderText == "Pick some"
        m.sizeVariant = "lg"
        big = m.sizeHint().height()
        m.sizeVariant = "sm"
        assert m.sizeHint().height() < big

    def test_max_chips_collapses_to_overflow(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        m = QCustomMultiSelect(options=["a", "b", "c", "d"],
                               selected=["a", "b", "c", "d"])
        m.maxChips = 2
        shown, overflow = m._visibleChips()
        assert shown == ["a", "b"] and overflow == 2

    def test_paints_placeholder_and_chips_differently(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        empty = QCustomMultiSelect(options=["a", "b"])
        empty.resize(280, 40)
        filled = QCustomMultiSelect(options=["a", "b"], selected=["a"])
        filled.resize(280, 40)
        assert empty.grab().toImage() != filled.grab().toImage()

    def test_error_state_changes_render(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        ok = QCustomMultiSelect(options=["a"])
        ok.resize(280, 40)
        bad = QCustomMultiSelect(options=["a"])
        bad.state = "error"
        bad.resize(280, 40)
        assert ok.grab().toImage() != bad.grab().toImage()

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.QCustomMultiSelect import QCustomMultiSelect
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        m = QCustomMultiSelect(options=["a"])
        m.ensurePolished()
        assert m.fieldBackgroundColor.name().lower() == "#ffffff"     # surface
        assert m.fieldBorderErrorColor.name().lower() == "#dc2626"    # destructive
        qapp.setStyleSheet("")
