# DataTable Pro — first commercial SKU spec

**Status:** Proposed / not started — design only
**Owner:** TBD
**Created:** 2026-07-22
**Related:** commercial-product.md, variant-token-system.md, modernization-roadmap.md

## Summary

`QCustomDataTablePro` — a high-performance, production-grade data grid, sold as the
first `custom-widgets-pro` SKU. A **basic** `QCustomDataTable` ships free in the
LGPL core; Pro extends it with the features that only matter at scale
(virtualization, grouping, pinning, editing, lazy loading, export).

## Hard rule: Pro contains ONLY original code

The `custom-widgets-pro` package **must not bundle any third-party assets or
vendored code** — no fonts, no icon files, no copied source. Everything in Pro is
original, so the compiled commercial wheels carry **no attribution, redistribution,
or copyleft obligations**. Concretely:

- **Icons/indicators** (sort arrows, filter, expand/collapse, pin) are **painted
  programmatically with `QPainter`**, not shipped as SVG/PNG files. (If a themed
  icon is ever wanted, it is pulled at runtime from the free core's `iconify`
  — an LGPL *dependency*, never copied into Pro.)
- **Fonts:** none bundled. Text uses the application's/theme's font.
- **Export:** the XLSX writer is a **pure-stdlib** implementation (`zipfile` +
  `xml.etree`), so there is **no `openpyxl`/third-party dependency**. CSV uses the
  stdlib `csv` module.
- **Runtime deps:** only the free core + Qt (via `qtpy`). Keep Pro dependency-light
  so wheels stay clean and compile predictably.

## Free vs Pro split

| Capability | Free core (`QCustomDataTable`, LGPL) | Pro (`QCustomDataTablePro`) |
|---|---|---|
| Render, select | ✅ | ✅ (inherits) |
| Sort / filter | ✅ client-side | ✅ + multi-column, custom comparators |
| Pagination | ✅ | ✅ + virtualized scrolling |
| **Virtualization (100k+ rows)** | ❌ | ✅ windowed model, recycled delegates |
| **Frozen / pinned columns** | ❌ | ✅ |
| **Column reorder / resize persistence** | ❌ | ✅ |
| **Inline editing + validation** | ❌ (read-only) | ✅ |
| **Server-side / lazy loading** | ❌ | ✅ data-provider interface |
| **Grouping / pivot / aggregation** | ❌ | ✅ |
| **CSV / XLSX export** | ❌ | ✅ (pure-stdlib) |

Pro **extends** the free class so free examples/tutorials transfer directly — the
upgrade path is "swap the class, gain the features." Reinforces the funnel.

## Architecture (Qt model/view)

Built on Qt's model/view framework (`QTableView` + custom models), which already
renders only the visible viewport — the Pro value is the **model, delegates, and
feature layers** on top, not reinventing the view.

```
QCustomDataTablePro (QWidget)
├── QTableView (main)                     ← styled via core tokens/QSS
├── QTableView (frozen overlay)           ← pinned columns (classic frozen-col pattern)
├── DataTableModel (QAbstractTableModel)  ← windowed/lazy; canFetchMore/fetchMore
│     └── DataProvider (interface)        ← in-memory OR developer-supplied (server-side)
├── GroupingProxy / SortFilterProxy       ← grouping, pivot, sort, filter
├── EditDelegate(s)                       ← inline edit + validation
└── ExportEngine                          ← CSV + pure-stdlib XLSX
```

### Virtualization / large datasets
- `DataTableModel` exposes rows through a **`DataProvider`** abstraction so the
  widget never holds more than a window of rows for a lazy source.
- Implement `canFetchMore`/`fetchMore` for incremental loading; row count may be
  known (server total) or streaming.
- Delegates are lightweight and reused by the view (native cell recycling).

### Frozen / pinned columns
- Standard Qt "frozen column" technique: a second `QTableView` sharing the same
  model, overlaid on the left (or right), synced on scroll/resize/selection.

### Grouping / pivot / aggregation
- A grouping proxy builds a tree (group header rows + child rows) with per-group
  **aggregations** (sum/avg/count/min/max) supplied via a small aggregation spec.
- Pivot = grouping on row + column dimensions with a value aggregation.

### Inline editing + validation
- Editable `QStyledItemDelegate` subclasses per column type (text/number/date/
  choice), with a **validation hook** (`validate(value) -> ok|error`) that surfaces
  inline error styling (via the token system's `destructive`/`focus-ring` roles).

### Server-side / lazy loading
- Developer implements a `DataProvider` (fetch a row window, total count, sort/
  filter push-down). The widget calls it; no assumption of in-memory data.

### Export (pure-stdlib)
- **CSV** via `csv`. **XLSX** via a minimal writer: an `.xlsx` is a zip of XML
  parts — implement with `zipfile` + `xml.etree.ElementTree`. No third-party dep.
- Exports respect current sort/filter/grouping (what you see is what you export).

## Styling & catalog (reuse the free system)

- Styled entirely through the **design-token / variant system**
  (variant-token-system.md): `variant`/`size` dynamic properties + QSS attribute
  selectors, semantic tokens for surface/outline/accent/destructive. No bespoke
  colors.
- Ships a `__catalog__` descriptor (props, signals, tokens used) so the MCP/agent
  catalog can introspect it like any core widget.

## Public API (sketch)

```python
from custom_widgets_pro import QCustomDataTablePro

table = QCustomDataTablePro()
table.setColumns([
    Column("name",  "Name",  type="text",   editable=True),
    Column("price", "Price", type="number", editable=True,
           validate=lambda v: v >= 0 or "must be ≥ 0", aggregate="sum"),
    Column("date",  "Date",  type="date"),
])
table.setDataProvider(MyServerProvider())     # or table.setRows([...]) for in-memory
table.pinColumns(["name"])                    # frozen
table.groupBy(["category"])                   # grouping + aggregation
table.setProperty("variant", "outline"); table.setProperty("size", "sm")
table.exportTo("out.xlsx")                    # or "out.csv"
```

## Licensing hook

- On import in a **development** context, `custom_widgets_pro` runs the **dev-time
  entitlement check** (commercial-product.md): valid Gumroad/LS key *or* Patreon
  membership, cached with offline grace. **No runtime check in shipped apps.**
- Widget code contains no per-instance license calls — enforcement lives in the
  package's import/activation layer only.

## Performance targets (acceptance criteria)

- Smooth scroll (no visible jank) at **100k rows × 30 columns** in-memory.
- First paint of a lazy/server source in **< 200 ms** for the first window.
- Sort/filter on 100k in-memory rows feels interactive (< ~150 ms) or is offloaded
  to the provider for server-side.
- Export of 100k rows to XLSX completes without loading the whole sheet in memory
  as strings (stream rows into the zip).

## Build & packaging

- Compiled to native `.so`/`.pyd` (Cython/Nuitka) per commercial-product.md; wheel
  matrix via `cibuildwheel`. Pure-stdlib + core + Qt only → clean, portable wheels.
- Delivered via the store-gated private index.

## Open questions

- Grouping/pivot: custom tree model vs a grouping proxy over the flat model — which
  scales better for large grouped sets? (Decide with a spike.)
- Frozen columns: the two-view overlay vs a single custom `QAbstractItemView`
  (more control, more work). Start with the two-view pattern.
- Server-side push-down: how much sort/filter/group logic to standardize in the
  `DataProvider` interface vs leave to the developer.
- XLSX feature scope for v1: values + basic formatting only? (Styling/formulas
  later.)
- Cell virtualization for very wide (many-column) tables — is native viewport
  recycling enough, or is column windowing needed?

## Phased implementation

1. **Free `QCustomDataTable`** in the core (basic table; also closes roadmap Gap #1)
   — styled via tokens, `__catalog__`, read-only + sort/filter/paginate.
2. **Pro model layer** — `DataTableModel` + `DataProvider` + virtualization.
3. **Frozen columns + reorder/resize persistence.**
4. **Inline editing + validation.**
5. **Grouping / pivot / aggregation.**
6. **Server-side provider** reference implementation.
7. **Export engine** (CSV + pure-stdlib XLSX).
8. **Compile + license hook + private-index delivery**; launch alongside go-to-market.
