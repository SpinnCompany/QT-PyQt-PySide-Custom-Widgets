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

    def test_page_count_one_when_pagination_disabled(self, qapp):
        # pageCount()/currentPage() must reflect ACTIVE pagination, not a stale
        # value from the lingering pagination proxy.
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        t = QCustomDataTable()
        t.setColumns([DataTableColumn("n", type="number")])
        t.setData([{"n": i} for i in range(100)])
        t.pageSize = 10
        assert t.pageCount() == 10
        t.showPagination = False        # disable -> must report 1, not stale 10
        assert t.pageCount() == 1
        assert t.currentPage() == 0

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


class TestRichCells:
    """The delegate/renderer layer that makes a WorkEver-style rich table
    possible: status dots, links, colored text, two-line cells, badges,
    currency - driven by DataTableColumn renderer/color/subtitle rules and the
    model's rich-cell roles."""

    def _cols(self):
        from Custom_Widgets.QCustomDataTable import DataTableColumn
        return [
            DataTableColumn("job", title="JOB", renderer="status",
                            colorMap={"Tracking job": "#22c55e"}),
            DataTableColumn("amount", title="AMOUNT", type="number",
                            renderer="currency",
                            formatter=lambda v: "$%d" % v),
            DataTableColumn("site", title="SITE", renderer="twoline",
                            subtitleKey="site2"),
            DataTableColumn("scheduled", title="SCHEDULED", renderer="colored",
                            colorKey="schedColor"),
            DataTableColumn("invoiced", title="INVOICED", renderer="badge",
                            colorMap={"Issued": "#3b82f6"}),
            DataTableColumn("customer", title="CUSTOMER"),  # plain, no renderer
        ]

    def _rows(self):
        return [
            {"job": "Tracking job", "amount": 550,
             "site": "55 Kendell Street", "site2": "Shaw, OL2 2YA",
             "scheduled": "29/12/2020 09:30", "schedColor": "#f97316",
             "invoiced": "Issued", "customer": "Video Games Ltd"},
            {"job": "Tracking job", "amount": 550,
             "site": "55 Kendell Street", "site2": "Shaw, OL2 2YA",
             "scheduled": "29/12/2020 10:30", "schedColor": "#f97316",
             "invoiced": "Issued", "customer": "Video Games Ltd"},
        ]

    def _model(self):
        from Custom_Widgets.QCustomDataTable import QCustomDataTableModel
        return QCustomDataTableModel(self._cols(), self._rows())

    def test_model_serves_rich_roles(self, qapp):
        from Custom_Widgets.QCustomDataTable import (
            RendererRole, SubtitleRole, CellColorRole)
        m = self._model()
        idx = lambda r, c: m.index(r, c)
        # status: renderer + per-value dot colour from colorMap
        assert m.data(idx(0, 0), RendererRole) == "status"
        assert m.data(idx(0, 0), CellColorRole) == "#22c55e"
        # twoline: subtitle pulled from subtitleKey
        assert m.data(idx(0, 2), RendererRole) == "twoline"
        assert m.data(idx(0, 2), SubtitleRole) == "Shaw, OL2 2YA"
        # colored: per-row colour from colorKey
        assert m.data(idx(0, 3), CellColorRole) == "#f97316"
        # badge: colour from colorMap
        assert m.data(idx(0, 4), CellColorRole) == "#3b82f6"
        # currency display honours the formatter
        assert m.data(idx(0, 1), Qt.DisplayRole) == "$550"
        # plain column advertises no renderer / no colour
        assert m.data(idx(0, 5), RendererRole) == ""
        assert m.data(idx(0, 5), CellColorRole) == ""

    def test_delegate_installed_and_paints_without_error(self, qapp):
        from Custom_Widgets.QCustomDataTable import (
            QCustomDataTable, QCustomDataTableDelegate)
        t = QCustomDataTable()
        t.setColumns(self._cols())
        t.setData(self._rows())
        t.setCellAccentColor("#f97316")
        assert isinstance(t.delegate(), QCustomDataTableDelegate)
        assert t.view().itemDelegate() is t.delegate()
        t.resize(900, 300)
        pm = t.grab()                       # offscreen paint: must not crash
        assert not pm.isNull() and pm.width() > 0 and pm.height() > 0

    def test_twoline_rows_are_taller(self, qapp):
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        t = QCustomDataTable()
        t.setColumns([DataTableColumn("site", renderer="twoline",
                                      subtitleKey="site2")])
        t.setData([{"site": "55 Kendell Street", "site2": "Shaw, OL2 2YA"}])
        t.resize(400, 200)
        t.view().resizeRowsToContents()
        assert t.view().rowHeight(0) >= 40   # two lines need a taller row

    def test_twoline_actually_paints_both_lines(self, qapp):
        # A regression guard: the subtitle must be drawn, not just reserved for.
        # Render a coloured two-line cell and confirm TWO separated bands of the
        # cell colour appear (title line + subtitle line).
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        HUE = "#f97316"
        t = QCustomDataTable()
        t.customizeQCustomDataTable(
            columns=[DataTableColumn("sched", renderer="twoline",
                                     subtitleKey="sched2", colorKey="c")],
            showPagination=False)
        t.setData([{"sched": "29/12/2020 09:30", "sched2": "29/12/2020 10:30",
                    "c": HUE}])
        t.view().verticalHeader().setDefaultSectionSize(60)
        t.resize(360, 120)
        img = t.grab().toImage()
        oc = QColor(HUE)

        def orange_cols(y):
            return sum(1 for x in range(img.width())
                       if _close(img.pixelColor(x, y), oc))

        rows_with_ink = [y for y in range(img.height()) if orange_cols(y) > 3]
        # collapse contiguous y-runs into bands
        bands = []
        for y in rows_with_ink:
            if bands and y - bands[-1][-1] <= 2:
                bands[-1].append(y)
            else:
                bands.append([y])
        assert len(bands) >= 2, (
            "expected two orange text lines (title + subtitle), got %d" % len(bands))


def _close(c, ref, tol=70):
    return (abs(c.red() - ref.red()) < tol and abs(c.green() - ref.green()) < tol
            and abs(c.blue() - ref.blue()) < tol and c.alpha() > 100)


class TestSelectionColumn:
    """The leading checkbox column + select-all header."""

    def _table(self):
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        t = QCustomDataTable()
        t.customizeQCustomDataTable(
            columns=[DataTableColumn("name"),
                     DataTableColumn("n", type="number")],
            selectable=True, showPagination=False)
        t.setData([{"name": "row%d" % i, "n": i} for i in range(5)])
        return t

    def test_select_column_added_and_offsets_data(self, qapp):
        from qtpy.QtCore import Qt
        t = self._table()
        m = t.model()
        assert m.columnCount() == 3           # select + 2 data columns
        # data-column titles are offset past the select column
        assert m.headerData(0, Qt.Horizontal) == ""       # select header blank
        assert m.headerData(1, Qt.Horizontal) == "name"
        assert m.headerData(2, Qt.Horizontal) == "n"

    def test_select_column_is_checkable_only(self, qapp):
        from qtpy.QtCore import Qt
        t = self._table()             # keep the widget alive (owns the C++ model)
        m = t.model()
        assert bool(m.flags(m.index(0, 0)) & Qt.ItemIsUserCheckable)
        assert not bool(m.flags(m.index(0, 1)) & Qt.ItemIsUserCheckable)

    def test_checkstate_toggle_via_setdata(self, qapp):
        from qtpy.QtCore import Qt
        t = self._table()
        m = t.model()
        assert m.data(m.index(2, 0), Qt.CheckStateRole) == Qt.Unchecked
        assert m.setData(m.index(2, 0), Qt.Checked, Qt.CheckStateRole) is True
        assert m.data(m.index(2, 0), Qt.CheckStateRole) == Qt.Checked
        assert t.checkedRows() == [2]
        # non-select columns reject setData
        assert m.setData(m.index(2, 1), Qt.Checked, Qt.CheckStateRole) is False

    def test_select_all_and_clear(self, qapp):
        t = self._table()
        m = t.model()
        assert m.headerCheckState() == 0
        t.setRowChecked(1)
        assert m.headerCheckState() == 1              # some
        t.setAllChecked(True)
        assert t.checkedRows() == [0, 1, 2, 3, 4]
        assert m.headerCheckState() == 2              # all
        t.clearChecked()
        assert t.checkedRows() == [] and m.headerCheckState() == 0

    def test_selection_checked_signal(self, qapp):
        t = self._table()
        seen = []
        t.selectionCheckedChanged.connect(lambda rows: seen.append(list(rows)))
        t.setRowChecked(3)
        assert seen and seen[-1] == [3]

    def test_header_select_all_toggle(self, qapp):
        t = self._table()
        # the custom header emits selectAllToggled -> model.setAllChecked
        t._hheader.selectAllToggled.emit(True)
        assert t.checkedRows() == [0, 1, 2, 3, 4]
        t._hheader.selectAllToggled.emit(False)
        assert t.checkedRows() == []

    def test_setrows_clears_checked(self, qapp):
        t = self._table()
        t.setAllChecked(True)
        t.setData([{"name": "x", "n": 1}])
        assert t.checkedRows() == []

    def test_toggling_selectable_off_removes_column(self, qapp):
        t = self._table()
        t.setAllChecked(True)
        t.setSelectable(False)
        assert t.model().columnCount() == 2          # back to data-only
        assert t.checkedRows() == []

    def test_removed_rows_shift_checked(self, qapp):
        t = self._table()
        t.setRowChecked(3)
        t.setRowChecked(4)
        t.model().removeRows(0, 2)     # drop rows 0,1 -> 3,4 become 1,2
        assert t.checkedRows() == [1, 2]


class TestRowActions:
    """The trailing kebab (⋮) row-actions column + rowActionTriggered."""

    def _table(self):
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        t = QCustomDataTable()
        t.customizeQCustomDataTable(
            columns=[DataTableColumn("name"), DataTableColumn("n", type="number")],
            rowActions=[("view", "View"), ("edit", "Edit"), "delete"],
            showPagination=False)
        t.setData([{"name": "row%d" % i, "n": i} for i in range(4)])
        return t

    def test_actions_column_added(self, qapp):
        from Custom_Widgets.QCustomDataTable import ACTIONS_RENDERER, RendererRole
        t = self._table()
        m = t.model()
        assert m.columnCount() == 3                       # 2 data + actions
        last = m.columnCount() - 1
        assert m.data(m.index(0, last), RendererRole) == ACTIONS_RENDERER
        assert m.headerData(last, Qt.Horizontal) == ""

    def test_actions_normalized(self, qapp):
        t = self._table()
        assert t.rowActions() == [("view", "View"), ("edit", "Edit"),
                                  ("delete", "delete")]

    def test_row_action_menu_triggers_signal(self, qapp):
        t = self._table()
        fired = []
        t.rowActionTriggered.connect(lambda r, k: fired.append((r, k)))
        menu = t.buildRowActionsMenu(2)          # source row 2
        acts = menu.actions()
        assert [a.text() for a in acts] == ["View", "Edit", "delete"]
        acts[1].trigger()                         # pick "Edit"
        assert fired == [(2, "edit")]

    def test_selectable_and_actions_together(self, qapp):
        from Custom_Widgets.QCustomDataTable import (ACTIONS_RENDERER, RendererRole)
        from qtpy.QtCore import Qt
        t = self._table()
        t.setSelectable(True)
        m = t.model()
        assert m.columnCount() == 4               # select + 2 data + actions
        assert bool(m.flags(m.index(0, 0)) & Qt.ItemIsUserCheckable)
        last = m.columnCount() - 1
        assert m.data(m.index(0, last), RendererRole) == ACTIONS_RENDERER
        # data column titles sit between the two synthetic columns
        assert m.headerData(1, Qt.Horizontal) == "name"

    def test_actions_paint_without_error(self, qapp):
        t = self._table()
        t.setSelectable(True)
        t.resize(700, 240)
        pm = t.grab()
        assert not pm.isNull() and pm.width() > 0
