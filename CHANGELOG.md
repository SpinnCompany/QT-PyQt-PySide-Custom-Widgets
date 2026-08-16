# Changelog

## 2.4.0 — 2026-08-16

**Fleet-review hardening.** Six review tracks landed at once: thread-safe
theming, real security on the local sockets + HTTP daemon, an import-light
package root, one widget catalog, an accessibility surface for the
custom-painted widgets, and a CI example-boot gate.

### Security
- **`QLocalServer` sockets (Designer bridge + in-app control server) are
  restricted to the owning user and require a one-time token.** Both servers
  now set `UserAccessOption` and write a 0600 token under the user's cache
  dir; a client must present the token as the first line of every connection
  or the connection is aborted. This closes the "any local process (or a
  pre-listen) can drive Designer / the running app" hole. Clients fail
  closed when no token file exists.
- **The MCP HTTP daemon can require a bearer token.** `--token` (or
  `CUSTOM_WIDGETS_MCP_TOKEN`) turns on the mcp SDK's native bearer
  middleware — unauthenticated requests get a 401. Binding to a non-loopback
  host without a token is refused outright. Loopback without a token keeps
  working (matches existing configs).
- **`designer_launch` tracks the PIDs it starts** and `designer_quit`
  kills them directly instead of a `/proc` sweep; the `/proc` scan remains
  only as a fallback for Designers other sessions launched.
- **Zip-slip guard in the iconify fetcher**: members whose resolved path
  escapes the extraction directory are rejected before `extractall`.
- **QtLocation plugin parameters are QML-escaped and validated**: values can
  no longer break out of the `PluginParameter` literal, and keys are
  restricted to `[A-Za-z0-9_.-]`.

### Fixed
- **Theme changes applied to the GUI are guaranteed to run on the main
  thread.** The icon-generation worker's `finished` signal connected to
  `_themeChangeComplete` via a plain lambda (DirectConnection), so the whole
  completion — pixmap-cache clear, stylesheet, `QLocalSocket` I/O — ran on
  the worker thread. It now uses a `Qt.QueuedConnection`.
- **Rapid theme toggles cancel their predecessors.** `applyCompiledSass`
  stops the previous icon worker before starting the next and guards the
  completion with a generation counter, so a stale worker can't repaint the
  GUI after a newer theme already applied.
- **`getThemeVariableValue` no longer recomputes the colour-variable map on
  every lookup** — only when the theme's inputs change — removing dozens of
  `createVariables()` runs (colour maths + an `_variables.scss` write + a
  stat) per `loadJsonStyle` pass.
- **`QCustomSpinner` and `QFlowProgressBar` are no longer registered with Qt
  Designer.** Their `__init__` takes something other than a parent first
  (`lineWidth` / the step-detail list), so Designer's `createWidget(parent)`
  bound the parent to that slot, left the widget unparented, and crashed at
  paint time — the 2.3.3 registration made them placeable but broken. They are
  now waived in the tiering manifest alongside the anchored popups, and a
  regression test instantiates every registered widget exactly the way Designer
  does (`Class(parent)`), which would have caught it.
- **`QCustomEmbeddedWindow` no longer raises on small forms.** The random
  drop position computed `randint(0, width - 285)` which raised
  `ValueError: empty range` on any form smaller than 285×190 (or before the
  form is sized), so the widget could not be placed in Designer. Bounds are
  clamped to zero.
- **13 Designer palette icons fixed for the second batch.** The
  `_register_widget` helper passed widgets' bare-relative `WIDGET_ICON` to
  Designer instead of the package-anchored absolute path the rest of the file
  uses, so `QCustomActionButton`, `QCustomChatDivider`, `QCustomTypingIndicator`,
  `QCustomMediaGrid`, `QCustomChatList`, `QCustomChatThread`, `QCustomChatInput`,
  `QCustomImageViewer`, `QCustomVideoPlayer`, `QCustomFileCard`,
  `QCustomLinkPreview`, `QCustomReactionBar` and `QCustomMessageStatus` showed a
  blank palette icon.
- **`QCustomPerlinLoader` is only registered when the optional `[loaders]`
  extra is installed** (its constructor raises `ImportError` without it), so a
  bare package install can no longer fail a Designer drop for it.
- **Two regression tests added** (`tests/test_designer_registration.py`): every
  Designer-registered widget must construct with a positional parent, adopt it,
  and paint; and every registered palette icon must resolve to a file on disk.

### Changed
- **`import Custom_Widgets` is now import-light.** The package root no longer
  eagerly imports the Qt + theme/widget stack (qtsass, JSonStyles,
  QCustomTheme, HotReload, ImageLoader, ...) — every public name resolves
  lazily via PEP 562 `__getattr__` (with `__all__` so
  `from Custom_Widgets import *` still works). Tools that only touch the
  package (design linter, stubgen, docs) no longer pay ~1.1s and the full Qt
  GUI library chain for an import. `QCustomMainWindow` moved to its own
  module; the `from Custom_Widgets import *` API is unchanged.
- **The design-token machinery moved to `Custom_Widgets/theming/tokens.py`.**
  `JSonStyles/tokens.py` is now a re-export shim, so both import paths resolve
  to the same module object. The dead `Custom_Widgets/Theme/` package and the
  `from Custom_Widgets import *` inside `QCustomQMainWindow` are gone.
- **The widget catalog has one implementation** (`Custom_Widgets/mcp/catalog.py`),
  imported by the MCP server, the stub generator and the launch-gate scanner
  instead of three drifting copies. Pure stdlib + AST, still nothing imported.
- **The interactive custom-painted widgets now expose an accessible name**
  (their text, tooltip, or a sensible default) via the new
  `Custom_Widgets/accessibility.py` helper — screen readers no longer announce
  a switch/radio/rating/slider/button/pagination/breadcrumb/cover-flow as an
  anonymous pane. Roles are applied too on bindings that still support
  `setAccessibleRole` (removed in Qt 6.4+).
- **The example survey detects blank windows.** `tools/survey_examples.py`
  downsamples the grab and flags a near-single-colour window as `blank`
  instead of `ok`; it gains an `--only=<substring>` filter, a `--timeout`,
  and exits nonzero when any app is not `ok`, so CI can gate on it.
- **New CI job `example-boot`** boots a flagship example subset headless
  (WinningDashboard, GlassHome, NewWidgetsShowcase, DesignTokens,
  QCustomDataTable) and fails on any crash/hang/blank/no-window.
- **New tests**: socket auth + refusal (`tests/test_security_sockets.py`,
  plus auth cases in the bridge/app-control suites), theme thread-safety
  (main-thread affinity, stale-generation guard, variable-map memoization),
  the MCP HTTP daemon (401 without token, acceptance with token, non-loopback
  refusal), and the widget accessibility surface (`tests/test_accessibility.py`).

## 2.3.3 — 2026-08-06

**Qt Designer release.** Every widget is supposed to be authorable in Designer.
In practice 19 could not be dropped onto a form at all, and most of the palette
showed no icon.

### Added
- **19 widgets registered with Qt Designer**, so they can be placed on a form
  like any other: the four loaders (`QCustom3CirclesLoader`, `QCustomArcLoader`,
  `QCustomPerlinLoader`, `QCustomSpinner`), `QFlowProgressBar`,
  `QCustomProgressIndicator`, `QCustomQSlider`, `QTagEdit`, `QCustomForm`,
  `QCustomInput`, `QCustomButtonGroup`, `QCustomQPushButtonGroup`,
  `QCustomCommandPalette`, `QCustomDrawer`, `QCustomSlideMenu`,
  `QCustomEmbeddedWindow`, `QCustomCodeEditor`, `QCustomDonut`,
  `QCustomSparkline`. Four of those already declared the full Designer contract
  and were simply never registered.

### Fixed
- **The Designer palette was mostly iconless: 19 of 102 registered widgets
  showed an icon, now all 102 do.** Most widgets declare a relative
  `WIDGET_ICON`, which Designer resolved against its own working directory
  instead of the package — so 44 widgets had working icons Designer could not
  find. Icon paths are now anchored to the package centrally, and a path that
  cannot be resolved yields Designer's own placeholder rather than a broken
  image.
- 58 `WIDGET_ICON` declarations named files that were never drawn; each now
  points at one of the ~2370 Material icons the package already ships.
- `QCustomQProgressBar` and `QCustomRoundProgressBar` had icon paths containing
  `../`, which escaped the package directory entirely.

### Notes
- Widgets that legitimately cannot be Designer-registered are now recorded as
  such rather than counted as gaps: `QCustomToast`, `QCustomQToolTip` and
  `QCustomEmojiPicker` need more than a parent to construct (Designer supplies
  only a parent), `QCustomTipOverlay` / `QCustomPopover` / `QCustomQDialog` are
  transient overlays positioned at runtime, `QCustomMapView` would pull
  QtLocation into every Designer start-up for an optional extra, and
  `QCustomModals` is a namespace of nested modal types rather than a widget.
- No API or behaviour changes. Full suite green (1316 tests).

## 2.3.2 — 2026-08-06

**A missing Qt binding now tells you what to do.** `pip install
QT-PyQt-PySide-Custom-Widgets` followed by `import Custom_Widgets` used to
raise qtpy's bare `QtBindingsNotFoundError: No Qt bindings could be found`,
which never says how to fix it — and that is the first thing a new user does.
The import now explains itself:

```
Custom_Widgets needs a Qt binding, and none is installed.

    pip install PySide6

Or install PyQt6 instead and set QT_API=pyqt6.
```

### Added
- **`[pyside6]` extra** — `pip install QT-PyQt-PySide-Custom-Widgets[pyside6]`
  installs the binding in one step, for anyone with no preference.

### Notes
- A Qt binding is still **not** a hard dependency, deliberately. qtpy exists so
  you can choose PySide6 or PyQt6; pinning one would force a second ~200 MB Qt
  download on anyone who already has the other. Base dependencies unchanged.
- No widget or behaviour changes. Full suite green (1316 tests).

## 2.3.1 — 2026-08-05

Metadata-only patch: **the Python floor is declared honestly as 3.10**.
2.3.0 claimed `>=3.9`, but several modules evaluate PEP 604 union
annotations (`QWidget | QFrame`) at import time — a `TypeError` on 3.9 —
and PySide6 itself requires `>=3.10,<3.15`, so Python 3.9 could never run
the library anyway. Classifiers now list 3.10–3.14 and the project
graduates to Production/Stable. No code changes.

## 2.3.0 — 2026-08-05

The largest release in the project's history: the catalogue grows to **164
documented widgets**, every public example is rebuilt and verified, and the
reference documentation is generated straight from the code so it can no
longer drift.

### Added
- **Painted chart family** — Scatter, Funnel, RangeBar, Radial gauges, Sankey,
  Candlestick, Beeswarm, DivergingBar, Bubble (zoom/pan/search + painted
  tooltips), DotMatrix, Sparkline, MiniBar and the ring/segment `QCustomDonut`;
  QPainter-native, theme-token driven, crisp at any size.
- **`QCustomMapView`** as the optional `[map]` extra (QtLocation OSM backend,
  offline `itemsoverlay` provider by default — no API key, no Chromium).
- **`QCustomDataTable`** — rich renderers (two-line, status, currency, link),
  synthetic select/actions columns, sortable headers, per-column alignment.
- **Chrome & motion widgets** — hamburger menu, slide menu with animated
  expand/collapse, animated stacked-widget transitions, flow layout/widget
  with animated reflow, component containers, compass dial, liquid/radial
  gauges, skeletons, typewriter/sparkles/gradient text and more.
- **Design-token theming** (`applyDesignTokens`) with light/dark palettes and
  role-based QSS across the widget set.
- **Design-rule linter** (`Custom_Widgets.lint`, spec in
  `Custom_Widgets/lint/DESIGN_RULES.md`): glyph-icons, hardcoded-hex,
  drop-shadow, large-icon.
- **MCP server** (`Custom_Widgets-mcp`, `[mcp]` extra): agent control of Qt
  Designer, live app observation, widget catalog/signature/render tools.
- **Generated reference docs** — every widget page, screenshot and animation
  is produced by `tools/gen_widget_docs.py`; the gallery and app showcase are
  generated too.
- Typed `.pyi` stubs for the whole widget set (`py.typed`, mypy-clean).

### Changed
- All 82 example apps rebuilt to the full structure (`ui/` + compiled `src/`
  + themed `Qss`/`json-styles` + icons), Qt Designer editable, zero inline
  styles, each verified headlessly.
- Project domain is now **customwidgets.org**; documentation lives at
  https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/.

### Fixed
- `QSettings` write-if-changed — cured multi-second boot hangs in
  component-heavy apps.
- Theme identity ordering on startup; `QCustomQStackedWidget` slide/fade
  transitions; `QCustomSlideMenu` "auto" sizing; `QCustomButtonGroup`
  orientation; `QCustomHeatmap.setData` compatibility alias.
- QtLocation provider lifetime segfault; annotation canvas without a project
  folder; chart theme listeners can no longer fire into deleted widgets.

### Notes
- Python ≥ 3.9 (the `[mcp]` extra needs ≥ 3.10 and pins `mcp>=1.9,<2`).
- Free package license is GPLv3. The Pro package (DataTable Pro and friends)
  and the premium example applications are available to supporters at
  https://customwidgets.org/pricing/.
