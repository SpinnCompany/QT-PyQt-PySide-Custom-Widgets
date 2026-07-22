"""QCustomComboBox: items API, substring autocomplete, variant/size props."""
from qtpy.QtCore import Qt


class TestItemsApi:
    def test_mixed_item_forms(self, qapp):
        from Custom_Widgets.QCustomComboBox import QCustomComboBox
        c = QCustomComboBox()
        c.setItems(["Apple",                       # bare string
                    ("Grape", 3),                  # (label, data)
                    {"label": "Kiwi", "value": 9}])  # dict
        assert c.count() == 3
        assert c.itemText(0) == "Apple" and c.itemData(0) == "Apple"
        assert c.itemText(1) == "Grape" and c.itemData(1) == 3
        assert c.itemText(2) == "Kiwi" and c.itemData(2) == 9

    def test_current_value(self, qapp):
        from Custom_Widgets.QCustomComboBox import QCustomComboBox
        c = QCustomComboBox()
        c.setItems([("A", 1), ("B", 2)])
        c.setCurrentIndex(1)
        assert c.currentText() == "B"
        assert c.currentData() == 2 and c.currentValue() == 2

    def test_current_index_changed_signal(self, qapp):
        from Custom_Widgets.QCustomComboBox import QCustomComboBox
        c = QCustomComboBox()
        c.setItems(["x", "y", "z"])
        seen = []
        c.currentIndexChanged.connect(seen.append)
        c.setCurrentIndex(2)
        assert seen and seen[-1] == 2


class TestAutocomplete:
    def test_substring_completion(self, qapp):
        from Custom_Widgets.QCustomComboBox import QCustomComboBox
        c = QCustomComboBox(editable=True)
        c.setItems(["Apple", "Banana", "Grape", "Pineapple"])
        comp = c.completer()
        assert comp is not None
        assert comp.filterMode() == Qt.MatchContains
        assert comp.caseSensitivity() == Qt.CaseInsensitive
        # "ap" is a substring of Apple, Grape, Pineapple (not Banana)
        comp.setCompletionPrefix("ap")
        matches = {comp.completionModel().index(i, 0).data()
                   for i in range(comp.completionCount())}
        assert matches == {"Apple", "Grape", "Pineapple"}

    def test_no_insert_on_edit(self, qapp):
        from qtpy.QtWidgets import QComboBox
        from Custom_Widgets.QCustomComboBox import QCustomComboBox
        c = QCustomComboBox(editable=True)
        assert c.insertPolicy() == QComboBox.NoInsert

    def test_placeholder(self, qapp):
        from Custom_Widgets.QCustomComboBox import QCustomComboBox
        c = QCustomComboBox(editable=True)
        c.setPlaceholderText("Search fruit...")
        assert c.placeholderText() == "Search fruit..."


class TestStyling:
    def test_variant_size_props_no_recursion(self, qapp):
        from Custom_Widgets.QCustomComboBox import QCustomComboBox
        c = QCustomComboBox()
        c.variant = "ghost"
        c.sizeVariant = "lg"
        assert c.variant == "ghost" and c.property("variant") == "ghost"
        assert c.sizeVariant == "lg"
        assert c.size() is not None            # QWidget.size() not shadowed

    def test_tokenized_background(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomComboBox import QCustomComboBox
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        c = QCustomComboBox(editable=False)
        c.setItems(["one", "two"])
        c.resize(200, 34)
        c.ensurePolished()
        # sample left-of-centre to avoid the drop-down arrow region
        px = QColor(c.grab().toImage().pixel(40, 17)).name().lower()
        assert px == "#ffffff"                 # surface (light)
        qapp.setStyleSheet("")
