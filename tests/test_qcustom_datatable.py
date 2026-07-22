"""Tests for QCustomDataTable (free core): model, pagination proxy, widget.

Covers the model's Qt.UserRole raw-value sort seam, the row-windowing
pagination proxy, source-coordinate mapping through the proxy chain, and the
Designer-facing typed properties.
"""
from qtpy.QtCore import Qt


def _prop(widget, name):
    mo = widget.metaObject()
    for i in range(mo.propertyCount()):
        if mo.property(i).name() == name:
            return mo.property(i)
    return None


class TestModel:
    def _model(self):
        from Custom_Widgets.QCustomDataTable import QCustomDataTableModel, DataTableColumn
        cols = [DataTableColumn("name"),
                {"key": "price", "type": "number"},
                DataTableColumn("ok", type="bool")]
        rows = [{"name": "A", "price": 9,   "ok": True},
                {"name": "B", "price": 100, "ok": False},
                {"name": "C", "price": 25,  "ok": None}]
        return QCustomDataTableModel(cols, rows)

    def test_counts(self, qapp):
        m = self._model()
        assert m.rowCount() == 3 and m.columnCount() == 3

    def test_column_coercion(self, qapp):
        from Custom_Widgets.QCustomDataTable import QCustomDataTableModel
        m = QCustomDataTableModel(["a", "b"], [])
        assert [c.key for c in m.columns()] == ["a", "b"]

    def test_display_bool_and_none(self, qapp):
        m = self._model()
        assert m.data(m.index(0, 0)) == "A"
        assert m.data(m.index(0, 2)) == "Yes"
        assert m.data(m.index(1, 2)) == "No"
        assert m.data(m.index(2, 2)) == ""   # None -> empty string

    def test_userrole_raw_value(self, qapp):
        m = self._model()
        assert m.data(m.index(1, 1), Qt.UserRole) == 100

    def test_number_right_aligned(self, qapp):
        m = self._model()
        align = int(m.data(m.index(0, 1), Qt.TextAlignmentRole))
        assert align & int(Qt.AlignRight)

    def test_mutation(self, qapp):
        m = self._model()
        m.addRow({"name": "D", "price": 1, "ok": True})
        assert m.rowCount() == 4
        assert m.removeRows(0, 1) is True and m.rowCount() == 3
        m.clear()
        assert m.rowCount() == 0

    def test_formatter_fallback_on_error(self, qapp):
        from Custom_Widgets.QCustomDataTable import QCustomDataTableModel, DataTableColumn
        m = QCustomDataTableModel([DataTableColumn("x", formatter=lambda v: 1 / 0)],
                                  [{"x": 5}])
        assert m.data(m.index(0, 0)) == "5"   # bad formatter falls back to str


class TestSortSeam:
    def test_numeric_sort_via_userrole(self, qapp):
        from qtpy.QtCore import QSortFilterProxyModel
        from Custom_Widgets.QCustomDataTable import QCustomDataTableModel, DataTableColumn
        m = QCustomDataTableModel([DataTableColumn("n", type="number")],
                                  [{"n": 9}, {"n": 100}, {"n": 25}])
        p = QSortFilterProxyModel()
        p.setSourceModel(m)
        p.setSortRole(Qt.UserRole)
        p.sort(0, Qt.AscendingOrder)
        got = [p.data(p.index(r, 0), Qt.UserRole) for r in range(3)]
        assert got == [9, 25, 100]   # numeric, not lexical ['100','25','9']


class TestWidget:
    def _table(self):
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        t = QCustomDataTable()
        t.setColumns([DataTableColumn("name"), DataTableColumn("n", type="number")])
        t.setData([{"name": "row%02d" % i, "n": 100 - i} for i in range(23)])
        return t

    def test_pagination_windows(self, qapp):
        t = self._table()
        t.pageSize = 10
        assert t.pageCount() == 3
        assert t.view().model().rowCount() == 10
        t.setPage(2)
        assert t.view().model().rowCount() == 3    # 23 = 10 + 10 + 3
        assert t.currentPage() == 2

    def test_page_clamped_on_filter(self, qapp):
        t = self._table()
        t.pageSize = 10
        t.setPage(2)
        t.setFilterText("row1")            # matches row10..row19 -> 10 rows, 1 page
        assert t.pageCount() == 1
        assert t.currentPage() == 0        # clamped down from page 2

    def test_pagination_disabled(self, qapp):
        t = self._table()
        t.pageSize = 0
        assert t.pageCount() == 1
        assert t.view().model().rowCount() == 23

    def test_selection_maps_to_source(self, qapp):
        from qtpy.QtCore import QItemSelectionModel
        t = self._table()
        t.pageSize = 10
        t.sortBy(1, Qt.AscendingOrder)     # ascending by n; min n=78 at source row 22
        captured = []
        t.rowSelected.connect(lambda r: captured.append(r))
        t.view().selectionModel().setCurrentIndex(
            t.view().model().index(0, 0), QItemSelectionModel.SelectCurrent)
        assert captured and captured[-1] == 22
        assert t.selectedRows() == [22]

    def test_default_order_is_insertion(self, qapp):
        # sortable is on by default, but the table must NOT auto-sort; rows
        # show in insertion order until a header is clicked / sortBy is called.
        t = self._table()
        t.pageSize = 0
        vm = t.view().model()
        assert vm.data(vm.index(0, 1), Qt.UserRole) == 100   # first inserted row (n=100)

    def test_designer_properties_typed(self, qapp):
        t = self._table()
        assert _prop(t, "pageSize").typeName() == "int"
        assert _prop(t, "showPagination").typeName() == "bool"
        assert _prop(t, "selectionMode").typeName() == "int"

    def test_property_roundtrip(self, qapp):
        t = self._table()
        t.setProperty("pageSize", 5)
        assert t.pageSize == 5
        t.selectionMode = 2
        assert t.selectionMode == 2
        t.variant = "ghost"
        assert t.property("variant") == "ghost"

    def test_customize_bulk_config(self, qapp):
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        t = QCustomDataTable()
        t.customizeQCustomDataTable(columns=[DataTableColumn("x")],
                                    data=[{"x": 1}, {"x": 2}], pageSize=1)
        assert t.pageCount() == 2
