# Build progress — modernization + open-core widget catalog

**Status:** In progress (local branches, not pushed)
**Updated:** 2026-07-23

Snapshot of what has been built toward the modern widget catalog and the
commercial Pro package. Everything is **committed locally and not pushed** (per
the "no push until the full commercial product is ready" decision).

## Repositories & branches

| Repo | Location | Branch | Commits (this effort) | Tests |
|---|---|---|---|---|
| Free core | `QT-PyQt-PySide-Custom-Widgets` | `feat/qcustom-datatable` | 42 ahead of `main`² | 259 passing¹ |
| Pro (private) | `custom-widgets-pro` (dist `QT-PyQt-PySide-Custom-Widgets-Pro`) | `main` | 11 | 86 passing |

¹ Two unrelated failures are excluded: `test_dev_server.py::test_classify` (an
uncommitted parallel-session change to `DevServer.py`) and
`test_mcp_server.py::test_expected_tools_registered` (needs `pytest-asyncio`,
not installed).

² Total divergence from `main`; includes parallel-session Designer/DevServer
commits, not only this effort's widget/compliance/licensing work.

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

## Free widgets added (34 modern widgets — 33 new + `QCustomBadge` modernization)

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
| QCustomKbd | keyboard-shortcut keycaps (`<kbd>` equivalent), string/list, separator |
| QCustomSplitter | QSplitter with tokenized hover-accent handle |
| QCustomCarousel | one-slide-at-a-time + prev/next + dot indicators, wrap, auto-advance |

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

Licence verification is **implemented** (2026-07-23): real Gumroad / LemonSqueezy
key verification + Patreon membership via stdlib `urllib` (no new dep), with a
signed offline-grace/perpetual-fallback cache and an `activate()` flow — see
`custom_widgets_pro/_license.py` (20 tests, HTTP mocked). Product ids /
campaign id are env-overridable baked constants to fill at launch.
This completes all five DataTable Pro capability layers (virtualization, frozen
columns, inline editing, grouping/pivot, export); the SKU is feature-complete
bar native compile + filling the store/campaign ids.

## Documentation (separate Docusaurus repo)

User docs live in `Docs-QT-PyQt-PySide-Custom-Widgets`. Written this effort (all
local, not pushed; internal tracker at that repo's root `BUILD-PROGRESS.md`):

- Reference pages for the 6 new widgets (Switch, NumberInput, Alert, StatCard,
  ProgressRing, Card) + `QCustomBadge` + its migration note.
- `QCustomDataTable` + `QCustomDataTablePro` reference pages ("Data & Tables").
- 5 DataTable usage recipes (basics, virtualization/server-side, editing,
  grouping/pivot, frozen/export).
- A **Licensing** page (current = GPLv3; Qt responsibility; third-party
  attributions — no LGPL/pricing claims yet).
- A **draft** release blog post (`draft: true`, not published).

✅ **Full site build verified** (2026-07-23): `npm ci && npm run build` passes
(`onBrokenLinks: throw`) with every new page + the draft post. Also fixed two
**pre-existing** broken Troubleshooting links that had been failing the build.

## What's next (open threads)

- ~~More free widgets (switch, number-stepper, alert, stat card, progress ring,
  card, badge)~~ **done** — 6 added + `QBadgeWidget` modernized into
  `QCustomBadge` (clean break; legacy file removed). Docs-repo migration note +
  `QCustomBadge` page written (v3-migration.md, `#qbadgewidget-to-qcustombadge`).
  ~~Further ideas: splitter, carousel, kbd~~ **done** — `QCustomKbd`,
  `QCustomSplitter`, `QCustomCarousel` added (tokenized QSS + `__catalog__` +
  Designer registration + tests + a combined demo). Docs-repo reference pages
  written for all three (Display & Information / Navigation & Layout; full-site
  build re-verified green).
- **Compliance fixes before any launch** (see THIRD_PARTY_NOTICES.draft.md) —
  *in progress:*
  - ✅ **Product Sans removed** — 12 unused proprietary `.ttf` deleted;
    `loadProductSansFont`→`loadAppFont` (already loaded OFL Rosario).
  - ✅ **`mock` runtime dep** — confirmed already resolved (not in pyproject, no
    runtime import).
  - ✅ **BlurWindow.py** — **clean-room rewritten** from the documented OS APIs
    (DWM / SetWindowCompositionAttribute, NSVisualEffectView, KWin hint); source
    header dropped, public API preserved + fail-soft. Removed the provenance risk
    (GWSL ambiguous "Modified MIT" / zhiyiYo unlicensed). *Windows/macOS blur
    behaviour still needs on-target verification.*
  - ✅ **Font Awesome attribution** — CC BY 4.0 attribution now visible in the
    README Credits section (GitHub + PyPI), the shipped notices, and
    `font_awesome/LICENSE.txt`.
  - ✅ **License-text bundle** — `Custom_Widgets/licenses/` ships Apache-2.0 /
    CC-BY-4.0 / Feather-MIT / OFL-1.1 + index; per-icon-set `LICENSE.txt`; notices
    promoted to `Custom_Widgets/THIRD_PARTY_NOTICES.md`. Core runtime-dep licenses
    verified (MIT/BSD).
  - *Non-blocking follow-ups:* confirm optional-extra + 3 vendored-code licenses
    at release; on-Windows/macOS functionality check of the new blur code.
- **Licensing prerequisites** — *groundwork done (2026-07-23), execution
  counsel-gated:*
  - ✅ `.mailmap` consolidates owner identities (owner = 408/414 ≈ 98.6%).
  - ✅ **External-contribution audit** (`docs/relicense/`): authoritative
    git-blame sweep — only **11 de-minimis lines** survive (8 package-dictated
    imports + 3 tool-generated example lines); 4/5 externals have **zero**
    surviving lines. Consent axis effectively clear pending counsel.
  - ✅ Ready-to-post consent tracking issue + template.
  - ✅ **Relicense changeset staged** (`docs/relicense/changeset/`): dry-run-tested
    `apply_relicense.py` + COPYING/COPYING.LESSER/LICENSE — ready to run after
    counsel sign-off (not applied; live tree stays GPL).
  - ✅ **Docs-repo Licensing page** added (`docs/07-Appendices/licensing.md`,
    Resources sidebar): states the current license = **GPLv3** + the Qt
    responsibility + third-party attributions; deliberately does **not** claim
    LGPL or publish commercial terms. Update it when the flip lands.
  - ⏳ **Counsel review** of the de-minimis calls → then execute the flip
    (COPYING.LESSER, LICENSE, `pyproject.toml`, SPDX, README) and land the
    CLA + bot + CONTRIBUTING.md + promote LICENSING.md. Drafts ready in
    `docs/design/`. **Not done autonomously — legal + owner decision.**
  - ✅ **Real Gumroad/LemonSqueezy/Patreon verification** implemented in the Pro
    package (stdlib-only, signed cache, offline grace, `activate()`; 20 tests).
    Left for launch: fill the baked store product id + Patreon campaign id.
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
- **Running-app observe + navigate** — the app `runApp` launches is a separate
  process Designer couldn't see into. It now hosts an in-app control server
  (`Custom_Widgets/AppControl.py`, per-project socket, auto-started by
  `QAppSettings.updateAppSettings` when the dev server sets
  `CUSTOM_WIDGETS_APP_CONTROL=1`). Nine MCP tools drive it: `app_status`,
  `app_list_windows`, `app_screenshot`, `app_object_tree`, `app_find`,
  `app_click`, `app_set_text`, `app_set_property`, `app_invoke`. Headless-tested
  (`tests/test_app_control.py`) and **verified live** — screenshotted the real
  running window, toggled a checkbox, and set a QLineEdit, all observed via
  screenshot. Agents can now SEE and DRIVE the running app, not just Designer.
- **Bridge quirk fixes** (verified live) — `openFiles` dedupes (reveals an
  already-open form instead of duplicating it); `getScreenShot type=current`
  follows `activeFormWindow()` instead of `forms[0]`.
- **SCSS unresolved-import error** — a dangling `@import` (e.g. a leftover
  `@import 'custom'`) made qtsass fail opaquely and `applyCompiledSass` silently
  fall back to STALE CSS (wrong/"red" theme). Now `tokens.find_unresolved_imports`
  / `describe_scss_compile_error` surface a clear "…could not be resolved…"
  message at both apply sites; the demo's stray import was removed.
  (`tests/test_design_tokens.py::TestScssImportDiagnostics`.)

Still open:

- ~~**User-facing docs** (Docusaurus repo) — pages for container `.py`-only +
  `.ui` auto-resolve, hot reload (component + main-window), the QSS/Theme editor,
  Paint entire Designer, and the new MCP tools~~ **done** — new
  `03-Advanced/hot-reload.md` (component + main-window + `.ui` auto-resolve),
  refreshed `03-Advanced/designer-tools.md` MCP section (QSS-window driving +
  `app_*` running-app tools + form/template/dialog tools), and container-page
  updates (`.ui` auto-resolve + `hotReload` property). Full-site build green.

See: `modernization-roadmap.md`, `commercial-product.md`, `variant-token-system.md`,
`datatable-pro-spec.md`, `lgpl-relicense-plan.md`, `THIRD_PARTY_NOTICES.draft.md`,
`designer-theming-tooling.md`.
