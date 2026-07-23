# Build progress — modernization + open-core widget catalog

**Status:** In progress (local branches, not pushed)
**Updated:** 2026-07-23

Snapshot of what has been built toward the modern widget catalog and the
commercial Pro package. Everything is **committed locally and not pushed** (per
the "no push until the full commercial product is ready" decision).

## Repositories & branches

| Repo | Location | Branch | Commits (this effort) | Tests |
|---|---|---|---|---|
| Free core | `QT-PyQt-PySide-Custom-Widgets` | `feat/qcustom-datatable` | 23 ahead of `main` | 238 passing¹ |
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
| QCustomBadge | pill/count/dot, 8 variants, overlay attach (replaces legacy QBadgeWidget) |

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

- ~~More free widgets (switch, number-stepper, alert, stat card, progress ring,
  card, badge)~~ **done** — 6 added + `QBadgeWidget` modernized into
  `QCustomBadge` (clean break; legacy file removed). Docs-repo migration note +
  `QCustomBadge` page written (v3-migration.md, `#qbadgewidget-to-qcustombadge`).
  Further ideas: splitter, carousel, kbd.
- **Compliance fixes before any launch** (see THIRD_PARTY_NOTICES.draft.md) —
  *in progress:*
  - ✅ **Product Sans removed** — 12 unused proprietary `.ttf` deleted;
    `loadProductSansFont`→`loadAppFont` (already loaded OFL Rosario).
  - ✅ **`mock` runtime dep** — confirmed already resolved (not in pyproject, no
    runtime import).
  - 🔬 **BlurWindow.py provenance** — researched: GWSL = ambiguous "Modified MIT",
    digsby = PSF-derived permissive, zhiyiYo = unlicensed blog (usually GPLv3).
    No confirmed copyleft; **clean-room rewrite recommended** (owner decision;
    needs Windows/macOS to verify).
  - ⏳ **Font Awesome attribution** — CC BY 4.0 text added to the notices;
    in-app/About placement still pending.
  - ⏳ **License-text bundle** (`licenses/`) + confirm all "(verify)" licenses,
    then promote the notices to `/THIRD_PARTY_NOTICES`.
- **Licensing prerequisites**: CLA + GPLv3→LGPLv3 relicense (owner holds ~97.6%),
  promote LICENSING.md — then real Gumroad/LemonSqueezy/Patreon verification.
- Go-to-market: refocus the YouTube channel, PPP price ladder, point-of-need selling.

## Designer follow-ups

In-repo code batch (**done**):

- **Container `.ui` back-compat** — the component loader accepts compiled `.py`
  only, but `QCustomComponentContainer`/`QCustomComponentLoader` now transparently
  resolve a `filePath` that still points at a raw `.ui` to the sibling
  `ui_<stem>.py` (`_resolve_ui_to_compiled`: checks alongside the `.ui`, then the
  default `src/` output dir). Users' existing forms load with no edit; only a
  form with no compiled module at all is rejected (with a clearer message).
  Covered by `tests/test_component_loader_resolve.py`.
- **Hot reload in new projects** — ProjectMaker's `components/python/main.py`
  template now uses the `build()` + `enable_hot_reload(self, self.build)` pattern
  (Ui import moved *inside* `build()`), so generated apps get main-window hot
  reload for free.
- **Polish** — designer faulthandler log truncates on startup with a timestamped
  session header (stale dumps no longer read as current); the benign
  "already deleted" selection-read `RuntimeError` on form replace is swallowed
  silently; `examples/svg_icons_demo/ui/testnew.ui` **kept** — it is the inner
  form of the nested-container demo (`mainwindow.ui` → `ui_newtest.py` →
  `ui_testnew.py`), not stray.
- **QSS-window MCP driver** — the floating QSS / Theme editor is a separate
  top-level window the dock/screenshot/action helpers can't reach, so the
  bridge gained a `qssWindow` method (`DesignerBridge._qssWindow`) with actions
  `open` / `close` / `status` / `paint` (the "Paint entire Designer" toggle) /
  `screenshot`. Two MCP tools expose it: `designer_qss_window(action, enabled)`
  and `designer_qss_screenshot()`. The whole QSS/theming surface is now
  MCP-verifiable (open the window, toggle Paint-entire-Designer, grab a PNG by
  objectName `customWidgetsQssWindow`). Headless-tested in
  `tests/test_designer_bridge.py` (fake-window injection), and **verified
  end-to-end against a live pyside6-designer** (open → paint on → screenshot →
  paint off, all over the bridge). This closes the original "live GUI
  verification" gap.

Still open:

- **User-facing docs** (Docusaurus repo) — pages for container `.py`-only +
  `.ui` auto-resolve, hot reload (component + main-window), the QSS/Theme editor,
  Paint entire Designer, and the new MCP tools (`designer_new_form`,
  `designer_list_templates`, `designer_list_dialogs`, `designer_qss_window`,
  `designer_qss_screenshot`, `entireApp`).

See: `modernization-roadmap.md`, `commercial-product.md`, `variant-token-system.md`,
`datatable-pro-spec.md`, `lgpl-relicense-plan.md`, `THIRD_PARTY_NOTICES.draft.md`,
`designer-theming-tooling.md`.
