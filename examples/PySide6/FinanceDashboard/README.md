# Finance — Dashboard

A pixel-faithful rebuild of a light finance dashboard reference, built the
**correct Custom_Widgets way** (the forms pipeline, not a pure-code app). It
doubles as the canonical reference for **how to develop a Custom_Widgets app**
(procedure + rules below).

```
ui/*.ui            -> src/ui_*.py            (Custom_Widgets --convert-ui)
json-styles/style.json   Finance Light / Finance Dark CustomThemes + ChartPalette
Qss/scss/chrome.scss     $TOKEN-driven chrome (no hard-coded hex)
gui/GuiFunctions.py      orchestrator + DashboardManager + ClockWorker
main.py                  minimal boot
```

Six library widgets were extracted from this build so the dashboard needs
**zero hand-painting** of its data surfaces — `QCustomPaymentCard` (VISA cards,
with an eye-reveal of the full number), `QCustomMiniBarChart` (monthly bars:
per-bar colours + green highlight + day labels), `QCustomListRow` (transaction
rows), `QCustomTrendChip` (income/expense arrows), `QCustomAvatar` (sidebar
avatar + status dot) and `QCustomPageDots` (the two pagers). Full API:
`docs/design/dashboard-widgets.md`.

## What's on screen
- `QCustomSidebar` that is **icon-only when collapsed** and **expands to labels**
  (hamburger toggle); an in-app **theme toggle** button and a `QCustomAvatar`.
- Top-bar breadcrumb + a **live clock** driven by a background `ClockWorker`
  (Worker → Signal → GUI).
- **My cards**: a dashed add-card tile + a gradient and a flat `QCustomPaymentCard`
  (click the eye to reveal the full PAN).
- **Balance** with `QCustomTrendChip` income (green ↗) / expense (red ↘) chips.
- **Monthly summary**: dashed income/expense box + a `QCustomMiniBarChart` (grey
  idle / accent / one highlighted green bar) with a `QCustomPageDots` pager.
- **Latest transaction** `QCustomListRow`s + primary / outline action buttons.

## Run
Build & run through the Custom Widgets MCP (preferred), or from a shell:

```bash
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
python main.py
```

## Theme
`Finance Light` is the default (matches the reference). `Finance Dark` is a full
token-driven dark variant; every data-viz hue lives in `ChartPalette` so it flips
with the theme. Toggle in-app from the sidebar, or in code via
`window.toggleTheme()`. (Qt persists the last theme in QSettings across runs; the
`Default-Theme` flag only governs the first run — clear the app's `.conf` for a
deterministic default.)

---

# Development procedure & rules

This is the workflow every change to this app (and any Custom_Widgets app) should
follow. It is not optional polish — the pipeline **is** the product.

## 1. MCP-first
Do the entire **build → run → observe** loop through the Custom Widgets MCP
(`designer_*` / `app_*` / `designer_run_app` / `design_lint` / `render_widget`),
never via ad-hoc `python`/shell. Shell is only for bootstrapping. If a capability
is missing, add it to the MCP rather than working around it. Read the MCP agent
guide + `customwidgets://skills` before starting.

## 2. The forms pipeline (never a pure-code app)
- **`ui/*.ui`** — structure + `objectName`s only. No inline `styleSheet` in `.ui`.
- Compile after every `.ui` edit: `project_convert_ui` (⇒ `src/ui_*.py`).
- **`json-styles/style.json`** — `CustomThemes` (colours) + a custom `ChartPalette`
  section for multi-hue data-viz. **Never hard-code hex** in code or `.ui`.
- **`Qss/scss/chrome.scss`** — chrome via `$TOKENS` + `objectName`/`[role]`
  selectors only. Never edit the generated `_variables.scss` / `_styles.scss`.
  Light theme: `BG_1` is the base and higher numbers get **darker** (dark theme is
  the reverse), so here panels/sidebar = `BG_1` (white), the page band = `BG_2`.
- **`gui/GuiFunctions.py`** — one orchestrator + one Manager per page reached via
  `container.component`; runtime data, painted config and interactions live here,
  not in the `.ui`. Background data = **Worker → Signal → GUI** on a `QThread`.

## 3. Theming
- Drive data-viz colours from `ChartPalette` (per theme name) so they flip on
  switch. Switch themes **BY NAME** (`themeEngine.setTheme("Finance Dark")`), and
  recolour painted widgets in the Manager's `recolor()` on
  `themeEngine.onThemeChangeComplete` (icon regen is async).
- Track the active nav page and re-assert `setChecked` when repainting chrome —
  theme/sidebar toggles can steal an autoExclusive checked state.

## 4. Prefer library widgets — and promote when you can't
If a design needs a surface no widget covers, **build the widget** (painted,
`WIDGET_*` consts + `__catalog__` + typed `@Property`s + `valuesCsv`-style inputs),
register it in `Plugins/register.py`, regenerate stubs
(`python -m Custom_Widgets.mcp.stubgen --write`), and use it here. Every widget in
this app was extracted that way — do not leave hand-painted data surfaces in a
manager.

## 5. Verify before done
Screenshot the running app in **both themes** and read the PNGs back. Drive real
interactions: sidebar collapse/expand shows labels, theme flip recolours every
data widget, the card eye reveals/masks, the pager active index is right. Fix what
the screenshot shows. Run `design_lint` (no glyph icons, no hard-coded hex in
chrome, no unjustified drop-shadow) and keep it at 0/0.

## Gotchas banked from this build
- **Qt hex is `#AARRGGBB`**, not `#RRGGBBAA` (a faint white is `#14ffffff`).
- **Sidebar labels**: `QCustomSidebarButton` shows `labelText` on expand and hides
  it on collapse automatically — an empty expand just means `labelText` was unset.
  Use `text-align:left` + `padding-left` so the icon still centres when collapsed.
- **Painted-label clipping**: reserve the real `QFontMetrics.height()` (not the
  point size) for a chart's label band, or descenders/edges clip.
- **Don't name a method and a `@Property` the same** (e.g. `count`) — the Property
  shadows the method and `w.count()` throws "int not callable". Read via the
  Property.
- **`.ui` custom-property order**: a custom `activeIndex` may be applied before
  `count`; set index-dependent props from the Manager (after `setCount`).
