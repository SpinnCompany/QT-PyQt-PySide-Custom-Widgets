# Finance — Dashboard

A pixel-faithful rebuild of a light finance dashboard reference, built the
**correct Custom_Widgets way** (the forms pipeline, not a pure-code app):

```
ui/*.ui            -> src/ui_*.py            (Custom_Widgets --convert-ui)
json-styles/style.json   Finance Light / Finance Dark CustomThemes + ChartPalette
Qss/scss/chrome.scss     $TOKEN-driven chrome (no hard-coded hex)
gui/GuiFunctions.py      orchestrator + DashboardManager + ClockWorker
main.py                  minimal boot
```

Three library widgets were extracted from this build so the dashboard needs
**zero hand-painting** of its data surfaces: `QCustomPaymentCard` (the VISA
cards), `QCustomMiniBarChart` (the monthly bars, per-bar colours + green
highlight + day labels) and `QCustomListRow` (the transaction rows). See
`docs/design/dashboard-widgets.md`.

## What's on screen
- Icon-only `QCustomSidebar` (home / activity / cards / settings + add), avatar
  with a live notification dot.
- Top bar breadcrumb (`Dashboard | Hello Matt…`) + a **live clock** driven by a
  background `ClockWorker` (Worker → Signal → GUI).
- **My cards**: a dashed add-card tile + a gradient VISA card and a muted VISA
  card (painted from the token-driven `ChartPalette`).
- **Balance** panel with income / expense chips (green ↗ / red ↘).
- **Monthly summary**: dashed income/expense box + a painted per-bar chart
  (grey idle / accent / one highlighted green bar) with a date pager.
- **Latest transaction** rows + primary / outline action buttons.

## Run
Build & run through the Custom Widgets MCP (`designer_run_app`), or:

```bash
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
python main.py
```

## Theme
`Finance Light` is the default (matches the reference). `Finance Dark` is a full
token-driven dark variant; every data-viz hue lives in `ChartPalette` so it
flips with the theme. Toggle from code via `window.toggleTheme()`.
