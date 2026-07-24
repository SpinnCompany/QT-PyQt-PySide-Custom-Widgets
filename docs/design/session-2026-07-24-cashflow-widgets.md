# Session report — CashFlowDashboard + 5 new widgets + remote fonts

**Date:** 2026-07-24
**Driven through:** the `custom-widgets` MCP (Designer + `designer_run_app` +
`app_screenshot` / `app_object_tree` / `render_widget`).
**Reference:** the green "Total Balance" banking dashboard mockups (diverging
cash-flow bars, KPI cards, activity table, stacked cards).

## What shipped

### A real forms-pipeline example app
`examples/PySide6/CashFlowDashboard` — built the maintainable way (RULE #0):
`ui/*.ui` → compiled `src/` → `json-styles/style.json` (Cashflow Light/Dark +
`ChartPalette`) → `Qss/scss/chrome.scss` ($TOKENS) → `gui/GuiFunctions.py`
(orchestrator + Manager + clock worker). Verified in **both themes** on the real
window via the MCP.

### Five NEW library widgets (registered, `.pyi` stubbed, tested)
| Widget | Group | What it is |
|---|---|---|
| `QCustomDivergingBarChart` | Charts | **Diverging / bipolar / up-down bar chart** — one column per category with an UP segment (income) and DOWN segment (expense) in two colours, split across a zero axis with a configurable **`zeroGap`**; optional €K y-axis + gridlines. Painted (no QtCharts). |
| `QCustomCardStack` | Containers | **Interactive stacked payment cards** — front full-size, backs peek up + inset; click / `next()`/`previous()` cycles with an animated reshuffle. `setCards([...])`, `setCardColorsList([(top,bottom)…])` for per-card gradients, `currentChanged(int)`. |
| `QCustomMenu` | Menus | **Modern popup action menu** for `…`/more buttons — rounded elevated panel, icon+label rows, hover, separators, danger rows; `popupAt(button)`, `triggered(str)`, `applyColors(...)`. |
| `QCustomModal` | Menus | **Modern centered modal** — dim scrim over the window + rounded card, title/subtitle, painted-X close, content slot, action buttons, rise-in animation, scrim/Esc dismiss; `triggered(str)` + `closed()`. |
| *(earlier this session)* | — | Gap analysis of the reference dashboards → `docs/design/missing-widgets-from-references.md`. |

Each follows the painted-widget convention (`WIDGET_*` constants + `__catalog__`
+ typed `@Property`s + CSV/JSON Designer inputs), is registered in
`Plugins/register.py`, `.pyi`-stubbed, theme-aware, and covered by tests
(`tests/test_qcustom_diverging_bar.py`, `tests/test_qcustom_stack_menu_modal.py`).
All four **seed guarded demo data** in `__init__` so they preview in Designer /
`render_widget`; the app replaces the seed the moment it calls `setData`/`setCards`.

### New LIBRARY capability — remote font loading
- `Custom_Widgets/Utils.py` → **`download_font(url, cache_dir=None)`** — stdlib
  urllib, cached under `generated-files/fonts/`, non-fatal on failure. TTF/OTF
  only (QFontDatabase does not read WOFF/WOFF2).
- `loadJsonStyle` `Fonts.LoadFonts[]` now accepts `{"name","url"}` (not just
  `path`); `Fonts.DefaultFont` resolves the family tolerantly and applies it
  **app-wide** (`QApplication.setFont`).
- `QCustomTheme.loadRemoteFont(url, set_as_default=True)` for imperative use.
- The dashboard loads **Inter** (`InterVariable.ttf` via jsDelivr) this way,
  fixing the "Failed to load the bundled Rosario font" mono/system fallback.
- Tests: `tests/test_remote_font.py` (mocked network).

## Process & design lessons folded into the guidelines
These were added to the MCP `AGENT_GUIDE` (`Custom_Widgets/mcp/guide.py`, the
`customwidgets://agent-guide` resource) and mirrored in
`memory/custom-widgets-forms-gotchas.md`:

1. **Diagnose layout from real geometry, not screenshots.** A card in a scroll
   area that overflows the viewport is pinned to its `minimumSize`; if that min
   is smaller than the content the rows COMPRESS AND OVERLAP (an icon tile
   overlapped the value by 2px here). Raising inner `spacing` makes it worse —
   raise the card's min height. Read rects with `app_object_tree`.
2. **`native="true"` QWidget containers paint the palette background** (a white/
   dark box) — invisible on a matching card, a visible box on a coloured surface
   (a % delta on the teal banner). Make the holder transparent.
3. **The SCSS engine has no `_R/_G/_B` rgba triples** unless the theme declares
   `Other-variables` — a stray `rgba($COLOR_ACCENT_1_R,…)` silently fails the
   WHOLE scss compile and the app renders unstyled. Use base tokens for tints.
4. **Top-level popups (Qt.Popup) aren't captured by `win.grab()`/`app_screenshot`**
   — verify a menu with a headless `panel.grab()` test; child-overlay modals ARE
   captured.
5. **Seed guarded demo data** so data-driven widgets preview in Designer; the app
   replaces it (gate on a `_built` flag; give `clear()`/`clearContent()`).
6. **A new `QCustom*.py` needs a Designer restart** to hit the palette;
   `render_widget` usually sees it without a full MCP restart.
7. **MCP cold-compile timeout** — pre-warm `.pyc` (`compileall`) then reconnect;
   never silently fall back to ad-hoc shell for build/run (RULE #1).
8. **Paint the affordance, don't type a glyph** — a modal close `x` as button text
   is a glyph-icons lint error; paint the X in a `QPushButton` subclass.

## Verification
- 25+ unit tests across the new widgets + remote font (all green).
- Live MCP `app_screenshot` in light + dark; `render_widget` previews for the
  seeded widgets; `app_object_tree` geometry checks for the KPI spacing fix.
- `design_lint` on the project: **0 errors** (only defensible hardcoded-hex
  warnings for SVG stroke-matching / fixed-teal banner text / palette fallbacks).

## Follow-ups (optional)
- Diverging bar: absolute-value bottom axis labels (`€3K` instead of `€-2K`).
- Card stack: drag-to-swipe.
- Modal: scrim fade-in.
