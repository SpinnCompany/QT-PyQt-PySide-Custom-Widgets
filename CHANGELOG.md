# Changelog

## 2.3.0 — 2026-08-05

The largest release in the project's history: the catalogue grows to **163
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
