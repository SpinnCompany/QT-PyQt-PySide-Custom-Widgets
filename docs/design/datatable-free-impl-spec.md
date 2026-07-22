# QCustomDataTable (free core) — implementation spec

**Status:** Ready to implement
**Owner:** TBD
**Created:** 2026-07-22
**Related:** datatable-pro-spec.md, variant-token-system.md, commercial-product.md

## Summary

`QCustomDataTable` — the **free**, LGPL-core basic data table. Read-only rendering,
client-side sort/filter, optional pagination, selection, theming. It is the class
`QCustomDataTablePro` extends, so its structure is designed for that (overridable
model/view factories). Also closes modernization-roadmap Gap #1 (basic DataTable).

**Note:** this is the codebase's **first model/view widget** (all existing widgets
are custom-painted). It establishes the model/view conventions for future data
widgets — keep it clean and idiomatic.

## Files

```
Custom_Widgets/QCustomDataTable.py      # widget + model + column + proxies
Custom_Widgets/Plugins/register.py      # add Designer registration entry
tests/test_qcustom_datatable.py         # pytest suite (headless-safe)
```

Single module (matches the repo's one-file-per-widget convention). Public classes:
`QCustomDataTable`, `QCustomDataTableModel`, `DataTableColumn`.

## Conventions to follow (from existing widgets)

- Imports via **`qtpy`** only (`from qtpy.QtCore import ...`), never PySide6/PyQt6.
- Designer-facing config as **`@Property(type)`** getter/setter; enums via **`QEnum`**.
- A **`customizeQCustomDataTable(**customValues)`** bulk-config method ending in a
  refresh, mirroring `customizeQCustomCheckBox`.
- Designer registration via class attrs `WIDGET_MODULE`, `WIDGET_TOOLTIP`,
  `WIDGET_DOM_XML`, `WIDGET_ICON` + an entry in `Plugins/register.py`.
- Styling through the token/variant system (`variant`/`size` dynamic props + QSS);
  no hardcoded colors. Until the token engine lands, style via `objectName`d
  sub-parts + theme QSS.

## Column definition

```python
class DataTableColumn:
    """Lightweight column descriptor."""
    def __init__(self, key, title=None, type="text", width=None,
                 align=None, formatter=None, sortable=True):
        self.key = key                      # row-dict key
        self.title = title or key
        self.type = type                    # "text" | "number" | "date" | "bool"
        self.width = width                  # px or None (auto)
        self.align = align                  # Qt.Alignment or None (type default)
        self.formatter = formatter          # callable(value) -> str, optional
        self.sortable = sortable
```

Rows are **list-of-dicts** keyed by `column.key` (friendly API). Type drives
default alignment (numbers right, bool centered) and sort comparison.

## Model — `QCustomDataTableModel(QAbstractTableModel)`

```python
class QCustomDataTableModel(QAbstractTableModel):
    def __init__(self, columns=None, rows=None, parent=None):
        super().__init__(parent)
        self._columns = list(columns or [])
        self._rows = list(rows or [])

    # --- required overrides ---
    def rowCount(self, parent=QModelIndex()):    return 0 if parent.isValid() else len(self._rows)
    def columnCount(self, parent=QModelIndex()): return 0 if parent.isValid() else len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid(): return None
        col = self._columns[index.column()]
        value = self._rows[index.row()].get(col.key)
        if role in (Qt.DisplayRole, Qt.EditRole):
            return col.formatter(value) if col.formatter else self._format(col, value)
        if role == Qt.TextAlignmentRole:
            return int(col.align if col.align is not None else self._defaultAlign(col))
        if role == Qt.UserRole:                  # raw value (for Pro/sorting)
            return value
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._columns[section].title
        return None

    def flags(self, index):                      # read-only in free tier
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    # --- data API ---
    def setColumns(self, columns): self.beginResetModel(); self._columns = list(columns); self.endResetModel()
    def setRows(self, rows):       self.beginResetModel(); self._rows = list(rows); self.endResetModel()
    def addRow(self, row): ...     # begin/endInsertRows
    def clear(self): ...
    def rawValue(self, r, c): return self._rows[r].get(self._columns[c].key)
```

- `_format(col, value)` → type-aware string (dates via `str`/ISO, numbers via
  locale-aware formatting, bool → "Yes"/"No"; keep minimal).
- `Qt.UserRole` returns the **raw** value so the sort proxy compares real types,
  not display strings. This is the seam Pro reuses.

## Proxies (sort / filter / pagination)

- **Sort + filter:** a `QSortFilterProxyModel` configured with
  `setSortRole(Qt.UserRole)` (type-correct sort) and a case-insensitive
  multi-column text filter (`filterAcceptsRow` scanning all columns, or
  `setFilterKeyColumn(-1)`).
- **Pagination (optional):** a small `_PaginationProxy(QAbstractProxyModel)` that
  maps only the current page window `[page*pageSize : (page+1)*pageSize]` from the
  sort/filter proxy. Active only when `showPagination` is true and `pageSize > 0`.

Stacking: `model → sortFilterProxy → (paginationProxy) → view`. Pro replaces this
stack with a virtualized model (no pagination), via the factory seams below.

## Widget — `QCustomDataTable(QWidget)`

Composition (a `QWidget` with an internal `QTableView` + optional footer), so a
pagination bar and future Pro chrome have a home.

```python
class QCustomDataTable(QWidget):
    # Designer registration
    WIDGET_MODULE  = "Custom_Widgets.QCustomDataTable"
    WIDGET_TOOLTIP = "A modern data table with sort, filter and pagination"
    WIDGET_ICON    = ...     # core-provided; NOT a Pro concern
    WIDGET_DOM_XML = "<ui>...<widget class='QCustomDataTable' name='dataTable'/>...</ui>"

    # signals
    rowSelected   = Signal(int)          # source-model row index
    cellClicked   = Signal(int, int)     # row, col (source coords)
    sortChanged   = Signal(int, object)  # column, Qt.SortOrder
    pageChanged   = Signal(int)          # new page index

    @QEnum
    class SelectionMode(Enum):
        NoSelection = 0; SingleRow = 1; MultiRow = 2; Cell = 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._model  = self._createModel()          # overridable (Pro seam)
        self._view   = self._createView()           # overridable (Pro seam)
        self._sortFilter = QSortFilterProxyModel(self); self._sortFilter.setSourceModel(self._model)
        self._sortFilter.setSortRole(Qt.UserRole); self._sortFilter.setFilterKeyColumn(-1)
        self._pageProxy = None
        self._pageSize = 25; self._page = 0
        self._buildUi()                              # view + footer, objectNames set
        self._wireSignals()

    # --- overridable factories (Pro overrides these) ---
    def _createModel(self): return QCustomDataTableModel(parent=self)
    def _createView(self):  return QTableView(self)
```

### `_buildUi`
- Layout: `QVBoxLayout` → `self._view` + `self._footer` (pagination widget).
- `objectName`s for QSS/token targeting: the widget, `dataTableView`,
  `dataTableFooter`, `dataTablePageLabel`, prev/next buttons.
- View config: `setAlternatingRowColors`, `horizontalHeader().setSortIndicatorShown`,
  `setSelectionBehavior/Mode` per `SelectionMode`, `verticalHeader().setVisible(False)`
  by default, `setShowGrid` per property.
- Apply column widths from `DataTableColumn.width`.

### Public API
```python
def setColumns(self, columns): ...          # list[DataTableColumn] or dicts
def setData(self, rows): ...                # list[dict]; alias setRows
def addRow(self, row): ...
def clear(self): ...
def setFilterText(self, text): ...          # updates sortFilter
def sortBy(self, column, order=Qt.AscendingOrder): ...
def setPage(self, index): ...               # pagination nav
def nextPage(self); def prevPage(self); def pageCount(self): ...
def selectedRows(self) -> list[int]: ...    # source-model rows
def customizeQCustomDataTable(self, **customValues): ...   # bulk config + refresh
```

### Properties (Designer, typed + QEnum)
| Property | Type | Default | Notes |
|---|---|---|---|
| `pageSize` | `int` | 25 | 0 disables pagination |
| `showPagination` | `bool` | True | toggles footer + page proxy |
| `selectionMode` | `SelectionMode` (QEnum) | SingleRow | maps to view selection |
| `sortable` | `bool` | True | header sort indicator + enable |
| `filterable` | `bool` | True | gates `setFilterText` |
| `alternatingRowColors` | `bool` | True | |
| `showGrid` | `bool` | False | |
| `showHeader` | `bool` | True | horizontal header visibility |
| `variant` | `str` | "outline" | token system (forward-compat) |
| `size` | `str` | "md" | token system (forward-compat) |

`variant`/`size` setters call `_repolish()` (unpolish/polish/update) per
variant-token-system.md so QSS re-applies on change (Designer + runtime).

### `__catalog__`
```python
__catalog__ = {
  "name": "QCustomDataTable",
  "props": {
    "pageSize": {"type": "int", "default": 25},
    "selectionMode": {"type": "enum",
        "values": ["NoSelection","SingleRow","MultiRow","Cell"], "default": "SingleRow"},
    "variant": {"type": "enum",
        "values": ["primary","secondary","outline","ghost"], "default": "outline"},
    "size": {"type": "enum", "values": ["sm","md","lg"], "default": "md"},
  },
  "signals": ["rowSelected","cellClicked","sortChanged","pageChanged"],
  "tokens_used": ["surface","on-surface","surface-muted","outline","accent","focus-ring"],
}
```

## Signal mapping (proxy coordinates)

The view sees proxied indices; always **map back to source** before emitting
public signals (`sortFilterProxy.mapToSource`, and the page proxy if present) so
consumers get stable source-model rows regardless of sort/filter/page.

## Empty / edge states

- No columns → show a themed "No columns configured" placeholder in the viewport.
- No rows (or filtered to zero) → "No data" placeholder.
- `pageSize == 0` or `showPagination == False` → hide footer, bypass page proxy.

## Theming

- Style via theme QSS targeting the `objectName`s; header, rows, alternating
  colors, selection, footer buttons all use **semantic tokens** once the token
  engine lands (surface/on-surface/outline/accent/focus-ring).
- Selection + focus use `accent` / `focus-ring` roles (a11y-friendly).

## Designer registration

Add to `Plugins/register.py` following the existing pattern:
```python
from Custom_Widgets.QCustomDataTable import QCustomDataTable
try:
    QtDesigner.QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QCustomDataTable, module=QCustomDataTable.WIDGET_MODULE,
        tool_tip=QCustomDataTable.WIDGET_TOOLTIP, xml=QCustomDataTable.WIDGET_DOM_XML,
        icon=QCustomDataTable.WIDGET_ICON, container=False, group="Item Views")
except Exception as e:
    logException(e, message="Error registering QCustomDataTable")
```

## Tests (`tests/test_qcustom_datatable.py`)

Headless-safe (construct with `QApplication`, skip if unavailable). Cover:
- Construct; `setColumns`/`setData` populate `rowCount`/`columnCount`.
- Type-aware **sort** (numbers sort numerically via `Qt.UserRole`, not lexically).
- **Filter** reduces visible rows; case-insensitive; multi-column.
- **Pagination**: `pageCount`, `setPage`/`next`/`prev` windows correctly; `pageSize=0`
  disables.
- **Selection** emits `rowSelected` with **source** row after sort/filter.
- `customizeQCustomDataTable(**...)` applies config.
- Runs under both bindings (`QT_API=pyqt6`).

## Pro extension seams (design for datatable-pro-spec.md)

Pro subclasses `QCustomDataTable` and overrides:
- `_createModel()` → virtualized/lazy `DataTableModel` + `DataProvider`.
- `_createView()` → view with frozen-column overlay.
- Adds editing (`flags` writable + delegates), grouping/pivot, export, column
  pinning/reorder — all without touching the free class's public API.

Keep `_createModel`/`_createView` and the `Qt.UserRole` raw-value seam stable —
they are the Pro contract.

## Open questions

- Pagination proxy vs footer-driven `setRowHidden` — proxy is cleaner and matches
  the Pro seam; confirm no perf issue for the free tier's expected sizes.
- Date/number formatting: locale-aware now, or a later `formatter`-only approach?
- Should `SelectionMode.Cell` ship in free v1 or defer (rows-only first)?

## Implementation checklist

- [ ] `DataTableColumn`, `QCustomDataTableModel` (+ `Qt.UserRole` raw seam)
- [ ] `QSortFilterProxyModel` config (sort role, multi-column filter)
- [ ] `_PaginationProxy` (+ toggle)
- [ ] `QCustomDataTable` widget: factories, `_buildUi`, footer, properties, signals
- [ ] `variant`/`size` + `_repolish` (forward-compat)
- [ ] `__catalog__` + `WIDGET_*` attrs + `register.py` entry
- [ ] `customizeQCustomDataTable`
- [ ] Empty/edge-state placeholders
- [ ] Tests (both bindings) + a runnable example under `examples/`
