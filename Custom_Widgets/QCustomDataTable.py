########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomDataTable - free core basic data table.
##
## This is the first model/view widget in the library. It provides a
## read-only, client-side sortable/filterable table that the commercial
## QCustomDataTablePro extends. See:
##     docs/design/datatable-free-impl-spec.md
##
## Layers in this module:
##   DataTableColumn / QCustomDataTableModel   - the model
##   _PaginationProxy                          - row-windowing pagination
##   QCustomDataTable                          - the QWidget (view + footer)
########################################################################
from enum import IntEnum

from qtpy.QtCore import (
    Qt, QModelIndex, QAbstractTableModel, QAbstractProxyModel,
    QSortFilterProxyModel, Signal, Property,
)
from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, QAbstractItemView,
    QLabel, QPushButton,
)


########################################################################
## Default per-type cell alignment
########################################################################
_TYPE_ALIGN = {
    "number": Qt.AlignRight | Qt.AlignVCenter,
    "bool":   Qt.AlignCenter,
    "date":   Qt.AlignLeft | Qt.AlignVCenter,
    "text":   Qt.AlignLeft | Qt.AlignVCenter,
}


class DataTableColumn(object):
    """Lightweight column descriptor for QCustomDataTable.

    key        row-dict key this column reads.
    title      header text (defaults to key).
    type       "text" | "number" | "date" | "bool" - drives default
               alignment and (via the sort proxy) sort comparison.
    width      column width in pixels, or None for automatic.
    align      Qt alignment flag, or None to use the type default.
    formatter  optional callable(value) -> str for display.
    sortable   whether this column may be sorted.
    """

    def __init__(self, key, title=None, type="text", width=None,
                 align=None, formatter=None, sortable=True):
        self.key = key
        self.title = key if title is None else title
        self.type = type
        self.width = width
        self.align = align
        self.formatter = formatter
        self.sortable = sortable

    @classmethod
    def ensure(cls, column):
        """Coerce a DataTableColumn, dict, or bare key into a DataTableColumn."""
        if isinstance(column, cls):
            return column
        if isinstance(column, dict):
            return cls(**column)
        return cls(str(column))

    def defaultAlign(self):
        return _TYPE_ALIGN.get(self.type, _TYPE_ALIGN["text"])


class QCustomDataTableModel(QAbstractTableModel):
    """Simple in-memory table model backed by a list of row dicts.

    Columns are DataTableColumn descriptors; rows are dicts keyed by
    ``column.key``. The model is read-only in the free tier (editing lives
    in QCustomDataTablePro).

    The raw, unformatted cell value is exposed through ``Qt.UserRole`` so a
    QSortFilterProxyModel configured with ``setSortRole(Qt.UserRole)`` sorts
    by real Python types instead of the display string. This raw-value seam
    is part of the stable contract the Pro model relies on.
    """

    def __init__(self, columns=None, rows=None, parent=None):
        super().__init__(parent)
        self._columns = [DataTableColumn.ensure(c) for c in (columns or [])]
        self._rows = list(rows or [])

    # ------------------------------------------------------------------ #
    ## Qt model interface
    # ------------------------------------------------------------------ #
    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if not (0 <= row < len(self._rows)) or not (0 <= col < len(self._columns)):
            return None
        column = self._columns[col]
        value = self._rows[row].get(column.key)

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self._display(column, value)
        if role == Qt.TextAlignmentRole:
            align = column.align if column.align is not None else column.defaultAlign()
            return int(align)
        if role == Qt.UserRole:
            return value
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if 0 <= section < len(self._columns):
                return self._columns[section].title
            return None
        return section + 1  # 1-based row numbers on the vertical header

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def removeRows(self, row, count, parent=QModelIndex()):
        if parent.isValid() or count <= 0 or row < 0 or row + count > len(self._rows):
            return False
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        del self._rows[row:row + count]
        self.endRemoveRows()
        return True

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def columns(self):
        return list(self._columns)

    def setColumns(self, columns):
        self.beginResetModel()
        self._columns = [DataTableColumn.ensure(c) for c in (columns or [])]
        self.endResetModel()

    def rows(self):
        return list(self._rows)

    def setRows(self, rows):
        self.beginResetModel()
        self._rows = list(rows or [])
        self.endResetModel()

    def addRow(self, row):
        pos = len(self._rows)
        self.beginInsertRows(QModelIndex(), pos, pos)
        self._rows.append(dict(row))
        self.endInsertRows()

    def addRows(self, rows):
        rows = list(rows or [])
        if not rows:
            return
        pos = len(self._rows)
        self.beginInsertRows(QModelIndex(), pos, pos + len(rows) - 1)
        self._rows.extend(dict(r) for r in rows)
        self.endInsertRows()

    def clear(self):
        if not self._rows:
            return
        self.beginResetModel()
        self._rows = []
        self.endResetModel()

    def rawValue(self, row, col):
        """Unformatted cell value at (row, col) in source coordinates."""
        if 0 <= row < len(self._rows) and 0 <= col < len(self._columns):
            return self._rows[row].get(self._columns[col].key)
        return None

    # ------------------------------------------------------------------ #
    ## Formatting helpers
    # ------------------------------------------------------------------ #
    def _display(self, column, value):
        if column.formatter is not None:
            try:
                return column.formatter(value)
            except Exception:
                pass  # fall back to the default formatting on a bad formatter
        return self._format(column, value)

    @staticmethod
    def _format(column, value):
        if value is None:
            return ""
        if column.type == "bool":
            return "Yes" if value else "No"
        return str(value)


class _PaginationProxy(QAbstractProxyModel):
    """Row-windowing proxy exposing only the current page of its source.

    Sits on top of the sort/filter proxy: proxy row r maps to source row
    ``r + page * pageSize``. Columns pass through unchanged. Page count and
    clamping track the (already sorted/filtered) source row count, so sorting
    and filtering upstream automatically reshape the visible page.

    The free tier uses this for classic pagination; Pro replaces the whole
    chain with a virtualized model and drops pagination entirely.
    """

    paginationChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pageSize = 25
        self._page = 0

    # ------------------------------------------------------------------ #
    ## Pagination state
    # ------------------------------------------------------------------ #
    def _offset(self):
        return self._page * self._pageSize if self._pageSize > 0 else 0

    def pageSize(self):
        return self._pageSize

    def setPageSize(self, size):
        size = max(0, int(size))
        if size == self._pageSize:
            return
        self.beginResetModel()
        self._pageSize = size
        self._clampPage()
        self.endResetModel()
        self.paginationChanged.emit()

    def page(self):
        return self._page

    def setPage(self, page):
        page = self._clampValue(page)
        if page == self._page:
            return
        self.beginResetModel()
        self._page = page
        self.endResetModel()
        self.paginationChanged.emit()

    def pageCount(self):
        src = self.sourceModel()
        if src is None or self._pageSize <= 0:
            return 1
        total = src.rowCount()
        return max(1, (total + self._pageSize - 1) // self._pageSize)

    def _clampValue(self, page):
        return max(0, min(int(page), self.pageCount() - 1))

    def _clampPage(self):
        self._page = self._clampValue(self._page)

    # ------------------------------------------------------------------ #
    ## Source model tracking (QAbstractProxyModel does not auto-connect)
    # ------------------------------------------------------------------ #
    def setSourceModel(self, source):
        prev = self.sourceModel()
        if prev is not None:
            for sig in (prev.modelReset, prev.layoutChanged, prev.rowsInserted,
                        prev.rowsRemoved, prev.columnsInserted, prev.columnsRemoved):
                try:
                    sig.disconnect(self._sourceReshaped)
                except (TypeError, RuntimeError):
                    pass
            try:
                prev.dataChanged.disconnect(self._sourceDataChanged)
            except (TypeError, RuntimeError):
                pass
        super().setSourceModel(source)
        if source is not None:
            source.modelReset.connect(self._sourceReshaped)
            source.layoutChanged.connect(self._sourceReshaped)
            source.rowsInserted.connect(self._sourceReshaped)
            source.rowsRemoved.connect(self._sourceReshaped)
            source.columnsInserted.connect(self._sourceReshaped)
            source.columnsRemoved.connect(self._sourceReshaped)
            source.dataChanged.connect(self._sourceDataChanged)
        self._sourceReshaped()

    def _sourceReshaped(self, *args):
        self.beginResetModel()
        self._clampPage()
        self.endResetModel()
        self.paginationChanged.emit()

    def _sourceDataChanged(self, topLeft, bottomRight, roles=None):
        rows, cols = self.rowCount(), self.columnCount()
        if rows > 0 and cols > 0:
            self.dataChanged.emit(self.index(0, 0), self.index(rows - 1, cols - 1),
                                  roles or [])

    # ------------------------------------------------------------------ #
    ## QAbstractProxyModel interface
    # ------------------------------------------------------------------ #
    def rowCount(self, parent=QModelIndex()):
        src = self.sourceModel()
        if parent.isValid() or src is None:
            return 0
        total = src.rowCount()
        if self._pageSize <= 0:
            return total
        return max(0, min(self._pageSize, total - self._offset()))

    def columnCount(self, parent=QModelIndex()):
        src = self.sourceModel()
        if parent.isValid() or src is None:
            return 0
        return src.columnCount()

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid():
            return QModelIndex()
        if 0 <= row < self.rowCount() and 0 <= column < self.columnCount():
            return self.createIndex(row, column)
        return QModelIndex()

    def parent(self, index=QModelIndex()):
        return QModelIndex()

    def mapToSource(self, proxyIndex):
        src = self.sourceModel()
        if src is None or not proxyIndex.isValid():
            return QModelIndex()
        return src.index(proxyIndex.row() + self._offset(), proxyIndex.column())

    def mapFromSource(self, sourceIndex):
        if not sourceIndex.isValid():
            return QModelIndex()
        row = sourceIndex.row() - self._offset()
        if 0 <= row < self.rowCount():
            return self.createIndex(row, sourceIndex.column())
        return QModelIndex()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        src = self.sourceModel()
        if src is None:
            return None
        if orientation == Qt.Vertical:
            return src.headerData(section + self._offset(), orientation, role)
        return src.headerData(section, orientation, role)

    def sort(self, column, order=Qt.AscendingOrder):
        src = self.sourceModel()
        if src is not None:
            src.sort(column, order)


class QCustomDataTable(QWidget):
    """Modern, read-only data table with client-side sort, filter and
    optional pagination. Styled through the theme/token system.

    This is the free-core base that QCustomDataTablePro extends. The
    ``_createModel`` / ``_createView`` factories and the model's
    ``Qt.UserRole`` raw-value seam are the stable Pro extension contract.
    """

    # -- Designer registration constants --
    WIDGET_ICON = "components/icons/table.png"
    WIDGET_TOOLTIP = "A modern data table with sort, filter and pagination"
    WIDGET_MODULE = "Custom_Widgets.QCustomDataTable"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomDataTable' name='customDataTable'>
            <property name='geometry'>
                <rect>
                    <x>0</x>
                    <y>0</y>
                    <width>480</width>
                    <height>320</height>
                </rect>
            </property>
        </widget>
    </ui>
    """

    # -- Rich editors for the Designer "Custom Properties" dock --
    DESIGNER_CUSTOM_PROPS = [
        {"name": "pageSize", "kind": "int", "group": "Data Table"},
        {"name": "showPagination", "kind": "bool", "group": "Data Table"},
        {"name": "selectionMode", "kind": "choice", "enum": "SelectionMode",
         "group": "Data Table"},
        {"name": "sortable", "kind": "bool", "group": "Data Table"},
        {"name": "filterable", "kind": "bool", "group": "Data Table"},
        {"name": "alternatingRowColors", "kind": "bool", "group": "Appearance"},
        {"name": "showGrid", "kind": "bool", "group": "Appearance"},
        {"name": "showHeader", "kind": "bool", "group": "Appearance"},
        {"name": "variant", "kind": "str", "group": "Appearance"},
        {"name": "size", "kind": "str", "group": "Appearance"},
    ]

    # -- Machine-readable catalog (MCP / agent introspection) --
    __catalog__ = {
        "name": "QCustomDataTable",
        "props": {
            "pageSize": {"type": "int", "default": 25},
            "selectionMode": {"type": "enum",
                              "values": ["NoSelection", "SingleRow", "MultiRow", "Cell"],
                              "default": "SingleRow"},
            "variant": {"type": "enum",
                        "values": ["primary", "secondary", "outline", "ghost"],
                        "default": "outline"},
            "size": {"type": "enum", "values": ["sm", "md", "lg"], "default": "md"},
        },
        "signals": ["rowSelected", "cellClicked", "sortChanged", "pageChanged"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "focus-ring"],
    }

    class SelectionMode(IntEnum):
        NoSelection = 0
        SingleRow = 1
        MultiRow = 2
        Cell = 3

    # -- signals (all row indices are SOURCE-model coordinates) --
    rowSelected = Signal(int)
    cellClicked = Signal(int, int)
    sortChanged = Signal(int, object)
    pageChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        # defaults
        self._pageSize = 25
        self._showPagination = True
        self._selectionMode = QCustomDataTable.SelectionMode.SingleRow
        self._sortable = True
        self._filterable = True
        self._alternatingRowColors = True
        self._showGrid = False
        self._showHeader = True
        self._variant = "outline"
        self._size = "md"
        self._pageProxy = None
        self._selModel = None
        self._lastPage = -1

        # model chain: model -> sort/filter -> (pagination) -> view
        self._model = self._createModel()
        self._sortFilter = QSortFilterProxyModel(self)
        self._sortFilter.setSourceModel(self._model)
        self._sortFilter.setSortRole(Qt.UserRole)
        self._sortFilter.setFilterKeyColumn(-1)
        self._sortFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self._view = self._createView()
        self._buildUi()
        self._installModel()
        self._applyViewProps()

    # ------------------------------------------------------------------ #
    ## Overridable factories (Pro overrides these)
    # ------------------------------------------------------------------ #
    def _createModel(self):
        return QCustomDataTableModel(parent=self)

    def _createView(self):
        return QTableView(self)

    # ------------------------------------------------------------------ #
    ## UI
    # ------------------------------------------------------------------ #
    def _buildUi(self):
        self.setObjectName("QCustomDataTable")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._view.setObjectName("dataTableView")
        self._view.verticalHeader().setVisible(False)
        self._view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # read-only in free tier
        self._view.setWordWrap(False)
        self._view.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self._view)

        self._footer = QWidget(self)
        self._footer.setObjectName("dataTableFooter")
        foot = QHBoxLayout(self._footer)
        foot.setContentsMargins(8, 4, 8, 4)
        self._prevBtn = QPushButton("Previous", self._footer)
        self._prevBtn.setObjectName("dataTablePrev")
        self._nextBtn = QPushButton("Next", self._footer)
        self._nextBtn.setObjectName("dataTableNext")
        self._pageLabel = QLabel("", self._footer)
        self._pageLabel.setObjectName("dataTablePageLabel")
        self._pageLabel.setAlignment(Qt.AlignCenter)
        foot.addWidget(self._prevBtn)
        foot.addStretch(1)
        foot.addWidget(self._pageLabel)
        foot.addStretch(1)
        foot.addWidget(self._nextBtn)
        layout.addWidget(self._footer)

        self._prevBtn.clicked.connect(self.prevPage)
        self._nextBtn.clicked.connect(self.nextPage)
        self._view.clicked.connect(self._onCellClicked)
        self._view.horizontalHeader().sortIndicatorChanged.connect(self._onSortIndicatorChanged)

    def _installModel(self):
        """(Re)build the view's model chain based on pagination settings."""
        paginate = self._showPagination and self._pageSize > 0
        if paginate:
            if self._pageProxy is None:
                self._pageProxy = _PaginationProxy(self)
                self._pageProxy.paginationChanged.connect(self._onPaginationChanged)
            self._pageProxy.setPageSize(self._pageSize)
            self._pageProxy.setSourceModel(self._sortFilter)
            self._setViewModel(self._pageProxy)
        else:
            self._setViewModel(self._sortFilter)
        self._footer.setVisible(paginate)
        self._applyColumnWidths()
        self._onPaginationChanged()

    def _setViewModel(self, model):
        if self._selModel is not None:
            try:
                self._selModel.currentRowChanged.disconnect(self._onCurrentRowChanged)
            except (TypeError, RuntimeError):
                pass
        self._view.setModel(model)
        self._selModel = self._view.selectionModel()
        if self._selModel is not None:
            self._selModel.currentRowChanged.connect(self._onCurrentRowChanged)

    def _applyViewProps(self):
        self._view.setAlternatingRowColors(self._alternatingRowColors)
        self._view.setShowGrid(self._showGrid)
        self._view.horizontalHeader().setVisible(self._showHeader)
        self._view.setSortingEnabled(self._sortable)
        if self._sortable:
            # setSortingEnabled(True) otherwise auto-sorts by column 0; start
            # unsorted so rows show in insertion order until a header is clicked.
            self._view.horizontalHeader().setSortIndicator(-1, Qt.AscendingOrder)
        self._applySelectionMode()

    def _applySelectionMode(self):
        mode = self._selectionMode
        SM = QCustomDataTable.SelectionMode
        if mode == SM.NoSelection:
            self._view.setSelectionMode(QAbstractItemView.NoSelection)
        elif mode == SM.MultiRow:
            self._view.setSelectionBehavior(QAbstractItemView.SelectRows)
            self._view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        elif mode == SM.Cell:
            self._view.setSelectionBehavior(QAbstractItemView.SelectItems)
            self._view.setSelectionMode(QAbstractItemView.SingleSelection)
        else:  # SingleRow
            self._view.setSelectionBehavior(QAbstractItemView.SelectRows)
            self._view.setSelectionMode(QAbstractItemView.SingleSelection)

    def _applyColumnWidths(self):
        for i, col in enumerate(self._model.columns()):
            if col.width:
                self._view.setColumnWidth(i, int(col.width))

    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setColumns(self, columns):
        self._model.setColumns(columns)
        self._applyColumnWidths()

    def setData(self, rows):
        self._model.setRows(rows)
        self.setPage(0)

    setRows = setData

    def addRow(self, row):
        self._model.addRow(row)

    def clear(self):
        self._model.clear()

    def model(self):
        return self._model

    def view(self):
        return self._view

    # ------------------------------------------------------------------ #
    ## Sorting / filtering
    # ------------------------------------------------------------------ #
    def setFilterText(self, text):
        if not self._filterable:
            return
        self._sortFilter.setFilterFixedString(text or "")
        self.setPage(0)

    def sortBy(self, column, order=Qt.AscendingOrder):
        self._sortFilter.sort(column, order)
        self._view.horizontalHeader().setSortIndicator(column, order)

    # ------------------------------------------------------------------ #
    ## Pagination
    # ------------------------------------------------------------------ #
    def pageCount(self):
        return self._pageProxy.pageCount() if self._pageProxy is not None else 1

    def currentPage(self):
        return self._pageProxy.page() if self._pageProxy is not None else 0

    def setPage(self, index):
        if self._pageProxy is not None:
            self._pageProxy.setPage(index)

    def nextPage(self):
        if self._pageProxy is not None:
            self._pageProxy.setPage(self._pageProxy.page() + 1)

    def prevPage(self):
        if self._pageProxy is not None:
            self._pageProxy.setPage(self._pageProxy.page() - 1)

    def _onPaginationChanged(self):
        if self._pageProxy is None or not self._footer.isVisible():
            return
        page = self._pageProxy.page()
        pages = self._pageProxy.pageCount()
        self._pageLabel.setText("Page %d of %d" % (page + 1, pages))
        self._prevBtn.setEnabled(page > 0)
        self._nextBtn.setEnabled(page < pages - 1)
        if page != self._lastPage:
            self._lastPage = page
            self.pageChanged.emit(page)

    # ------------------------------------------------------------------ #
    ## Selection
    # ------------------------------------------------------------------ #
    def selectedRows(self):
        """Return the selected SOURCE-model row indices (sorted, unique)."""
        rows = set()
        if self._selModel is not None:
            for idx in self._selModel.selectedIndexes():
                r = self._toSourceRow(idx)
                if r >= 0:
                    rows.add(r)
        return sorted(rows)

    def _toSourceRow(self, viewIndex):
        if not viewIndex.isValid():
            return -1
        idx = viewIndex
        if self._pageProxy is not None and self._view.model() is self._pageProxy:
            idx = self._pageProxy.mapToSource(idx)
        src = self._sortFilter.mapToSource(idx)
        return src.row()

    def _onCurrentRowChanged(self, current, previous):
        row = self._toSourceRow(current)
        if row >= 0:
            self.rowSelected.emit(row)

    def _onCellClicked(self, viewIndex):
        row = self._toSourceRow(viewIndex)
        if row >= 0:
            self.cellClicked.emit(row, viewIndex.column())

    def _onSortIndicatorChanged(self, column, order):
        self.sortChanged.emit(column, order)

    # ------------------------------------------------------------------ #
    ## Bulk config
    # ------------------------------------------------------------------ #
    def customizeQCustomDataTable(self, **customValues):
        if "columns" in customValues:
            self.setColumns(customValues["columns"])
        if "data" in customValues:
            self.setData(customValues["data"])
        elif "rows" in customValues:
            self.setData(customValues["rows"])
        for name in ("pageSize", "showPagination", "selectionMode", "sortable",
                     "filterable", "alternatingRowColors", "showGrid", "showHeader",
                     "variant", "size"):
            if name in customValues:
                setattr(self, name, customValues[name])
        if "filterText" in customValues:
            self.setFilterText(customValues["filterText"])
        self.update()

    # ------------------------------------------------------------------ #
    ## Properties (Designer)
    # ------------------------------------------------------------------ #
    @Property(int)
    def pageSize(self):
        return self._pageSize

    @pageSize.setter
    def pageSize(self, value):
        self._pageSize = max(0, int(value))
        self._installModel()

    @Property(bool)
    def showPagination(self):
        return self._showPagination

    @showPagination.setter
    def showPagination(self, value):
        self._showPagination = bool(value)
        self._installModel()

    @Property(int)
    def selectionMode(self):
        return int(self._selectionMode)

    @selectionMode.setter
    def selectionMode(self, value):
        self._selectionMode = QCustomDataTable.SelectionMode(int(value))
        self._applySelectionMode()

    @Property(bool)
    def sortable(self):
        return self._sortable

    @sortable.setter
    def sortable(self, value):
        self._sortable = bool(value)
        self._view.setSortingEnabled(self._sortable)

    @Property(bool)
    def filterable(self):
        return self._filterable

    @filterable.setter
    def filterable(self, value):
        self._filterable = bool(value)

    @Property(bool)
    def alternatingRowColors(self):
        return self._alternatingRowColors

    @alternatingRowColors.setter
    def alternatingRowColors(self, value):
        self._alternatingRowColors = bool(value)
        self._view.setAlternatingRowColors(self._alternatingRowColors)

    @Property(bool)
    def showGrid(self):
        return self._showGrid

    @showGrid.setter
    def showGrid(self, value):
        self._showGrid = bool(value)
        self._view.setShowGrid(self._showGrid)

    @Property(bool)
    def showHeader(self):
        return self._showHeader

    @showHeader.setter
    def showHeader(self, value):
        self._showHeader = bool(value)
        self._view.horizontalHeader().setVisible(self._showHeader)

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        self._variant = str(value)
        self.setProperty("variant", self._variant)  # for QSS attribute selectors
        self._repolish()

    @Property(str)
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = str(value)
        self.setProperty("size", self._size)
        self._repolish()
