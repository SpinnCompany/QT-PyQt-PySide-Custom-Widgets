# Build progress — modernization + open-core widget catalog

**Status:** In progress (local branches, not pushed)
**Updated:** 2026-07-23

Snapshot of what has been built toward the modern widget catalog and the
commercial Pro package. Everything is **committed locally and not pushed** (per
the "no push until the full commercial product is ready" decision).

## Repositories & branches

| Repo | Location | Branch | Commits (this effort) | Tests |
|---|---|---|---|---|
| Free core | `QT-PyQt-PySide-Custom-Widgets` | `feat/qcustom-datatable` | 21 ahead of `main` | 229 passing¹ |
| Pro (private) | `custom-widgets-pro` (dist `QT-PyQt-PySide-Custom-Widgets-Pro`) | `main` | 10 (+demo) | 66 passing |

¹ Two unrelated failures are excluded: `test_dev_server.py::test_classify` (an
uncommitted parallel-session change to `DevServer.py`) and
`test_mcp_server.py::test_expected_tools_registered` (needs `pytest-asyncio`,
not installed).

## Design-token system (foundation)

- `Custom_Widgets/JSonStyles/tokens.py` — hybrid tokens (Tailwind-like primitives
  + Material-like semantic roles), light/dark, `{ref}` resolution.
- `variant` / `sizeVariant` declared properties + QSS attribute selectors
  (pilot: `QCustomQPushButton`). **Gotchas learned:** never name a prop `size`
  (shadows `QWidget.size()`); a declared `@Property` setter must not call
  `setProperty(sameName)` (recurses).
- Painted widgets get token colours via QSS `qproperty-...` (skeleton, timeline,
  popover, range slider).
- Wired into the SCSS engine: `token('role')` custom function (`compile_scss`,
  `sass_functions`) bridged into `QCustomTheme`, following the live theme.
- Every widget below is tokenized; each commit includes a pixel-verified paint test.

## Free widgets added (30 new widgets across 32 classes)

| Widget | Notes |
|---|---|
| QCustomDataTable | model/view, client sort/filter, pagination, `Qt.UserRole` sort seam, `_createModel/_createView` Pro seams |
| QCustomToast | stacked, auto-dismiss, 6 corners, reflow |
| QCustomComboBox | searchable / substring autocomplete |
| QCustomDateEdit / QCustomTimeEdit / QCustomDateRangeEdit | calendar popup; range keeps start≤end |
| QCustomCommandPalette | fuzzy launcher (Ctrl/Cmd+K), keyboard nav |
| QCustomTabWidget | underline / pills / enclosed styles |
| QCustomAccordion | animated collapse, exclusive mode |
| QCustomTreeWidget | nested `setItems`, tokenized |
| QCustomDrawer | slide-in side sheet (any edge) |
| QCustomStepper | completed/active/pending states |
| QCustomRichTextEditor | formatting toolbar over QTextEdit |
| QCustomColorPicker | swatch + hex + preset popup + dialog |
| QCustomBreadcrumbs | clickable trail |
| QCustomRating | hover-preview stars |
| QCustomChip / QCustomChipGroup | closable + filter chips (flow layout) |
| QCustomSkeleton | shimmer placeholder (line/rect/circle) |
| QCustomAvatarGroup | overlapping avatars + overflow |
| QCustomTimeline | painted rail + dots |
| QCustomPagination | prev/next + ellipsis |
| QCustomPopover | anchored panel + arrow |
| QCustomSegmentedControl | single-select connected buttons |
| QCustomEmptyState | glyph + title + action |
| QCustomFileDropZone | drag-drop + browse, extension filter |
| QCustomRangeSlider | dual-handle range |
| QCustomSwitch | painted on/off toggle, animated thumb, sizeVariant |
| QCustomNumberInput | −/field/+ stepper, int/float, clamp, edit-commit |
| QCustomAlert | inline callout, info/success/warning/destructive variants, dismissible |
| QCustomStatCard | KPI tile: label + value + trend-coloured delta + caption |
| QCustomProgressRing | painted determinate circular %, tokenized ring/track |
| QCustomCard | surface container w/ optional header + body (Designer container) |

Also: `QCustomQPushButton` gained variant/sizeVariant; `QCustomFlowLayout`
teardown crash fixed; `QCustomTheme` gained the `token()` SCSS integration.
Each widget: tokenized QSS, `__catalog__`, Designer registration where droppable,
a headless test file, and a runnable `examples/PySide6/...` demo.

## Pro package (`custom-widgets-pro`)

Separate private repo. LGPL-core-extending, native-compile-ready, dual-entitlement
(Gumroad/LemonSqueezy key OR Patreon), dev-time licence check (royalty-free
runtime), 100% original code (no bundled assets).

**DataTable Pro** (`QCustomDataTablePro`, extends the free table via the seams):
- Virtualization — lazy `DataProvider` windows via `canFetchMore`/`fetchMore`.
- Server-side **sort/filter push-down** (whole-set ordering, stays lazy).
- **CSV / XLSX export** — pure-stdlib (zipfile+xml), streamed, real-reader verified.
- **Frozen (pinned) columns** — synced two-view overlay.
- **Inline editing** — per-column editable + type coercion + validation + bool
  checkboxes; `cellEdited` / `validationFailed`.
- **Grouping + aggregation** — group by one or more columns as a flat outline
  (header rows interleaved with data rows, so the frozen overlay/proxy/view chain
  is untouched); per-group sum/avg/count/min/max/first/last or a callable;
  click / `expand|collapseAllGroups` toggle; `groupToggled`. Pure `GroupingEngine`
  is Qt-free + unit-tested. Materialises the current sort/filter while grouped,
  restores lazy mode when cleared.
- **Pivot (cross-tab)** — `pivot(index, columns, values, aggfunc)` reshapes into
  a matrix (row dims × distinct column values × aggregated cell + row totals) via
  a pure `pivot_table` transform rendered through the ordinary flat table;
  `clearPivot` restores; mutually exclusive with grouping.

Licence verification is still **stubbed** (deliberately deferred to last).
This completes all five DataTable Pro capability layers (virtualization, frozen
columns, inline editing, grouping/pivot, export) — the SKU is feature-complete
bar the licence hook + native compile.

## What's next (open threads)

- ~~More free widgets (switch, number-stepper, alert, stat card, progress ring, card)~~
  **done** — 6 added (see the table above). Further ideas: badge (modernize the
  legacy `QBadgeWidget`), splitter, carousel, kbd.
- **Compliance fixes before any launch** (see THIRD_PARTY_NOTICES.draft.md):
  remove bundled **Product Sans** (proprietary), verify **BlurWindow.py** provenance,
  Font Awesome attribution, `mock` runtime dep.
- **Licensing prerequisites**: CLA + GPLv3→LGPLv3 relicense (owner holds ~97.6%),
  promote LICENSING.md — then real Gumroad/LemonSqueezy/Patreon verification.
- Go-to-market: refocus the YouTube channel, PPP price ladder, point-of-need selling.

See: `modernization-roadmap.md`, `commercial-product.md`, `variant-token-system.md`,
`datatable-pro-spec.md`, `lgpl-relicense-plan.md`, `THIRD_PARTY_NOTICES.draft.md`.
