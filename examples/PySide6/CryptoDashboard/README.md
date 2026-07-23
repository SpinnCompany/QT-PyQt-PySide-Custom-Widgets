# Crypto — Wallet & Trading Dashboard

A pixel-faithful rebuild of a crypto wallet/trading dashboard reference, built
the **correct Custom_Widgets way** (the forms pipeline, not a pure-code app).
It mirrors the procedure documented in `examples/PySide6/FinanceDashboard`.

```
ui/*.ui            -> src/ui_*.py            (Custom_Widgets --convert-ui)
json-styles/style.json   Crypto Light / Crypto Dark themes + ChartPalette + Coins
Qss/scss/chrome.scss     $TOKEN-driven chrome (no hard-coded hex)
gui/GuiFunctions.py      orchestrator + DashboardManager + MarketWorker
main.py                  minimal boot
```

## What's on screen
- A **dark floating rail** (`QCustomSidebar` + `QCustomSidebarButton`) that is
  **icon-only when collapsed and expands to labels** via a hamburger toggle
  (`customizeQCustomSlideMenu` with `collapsedWidth != expandedWidth`), with an
  accent logo/wordmark, a `moon`/`sun` **theme toggle**, and an active-page accent pill.
- Top-bar page title + a **user chip** (`QCustomAvatar` + name/ID + caret).
- **Overview of all wallets**: a `QCustomSegmentedControl` range switch
  (1D/1W/1M/6M), the big BTC/USD value, a green `QCustomTrendChip` +8.89%, and a
  smooth **`QCustomAreaChart`** with a painted time axis (its interactive toolbar
  hidden).
- **Market**: a real **`QCustomDataTable`** — brand-coloured coin status dots, a
  two-line ticker/name cell, coloured 24h-change, and a `Trade` **badge** column
  (click fires `cellClicked`). Rows arrive from a background `MarketWorker`
  (Worker → Signal → GUI).
- A **gradient promo card** with a `QCustomAvatarGroup` of coins.
- A **Trade** card: Buy/Sell/Exchange `QCustomSegmentedControl` (retitles the
  action button), coin + amount fields (`QCustomAvatar` badges), an exchange-rate
  line, a receipt block, and a primary **Buy ETH** `QCustomQPushButton`.

## Run
Build & run through the Custom Widgets MCP (preferred), or from a shell:

```bash
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
python main.py
```

## Theme
`Crypto Light` is the default (matches the reference). `Crypto Dark` is a full
token-driven dark variant; every data-viz hue lives in `ChartPalette` and every
coin brand colour in `Coins`, so they flip with the theme. Toggle from the
sidebar or in code via `window.toggleTheme()`. (Qt persists the last theme in
QSettings; clear the app's `.conf` for a deterministic default.)

## Notes on fidelity (things worth knowing)
- **Icons are painted per-widget** (feather SVG → recoloured pixmap), not via a
  single global QSS `Icons-color`: this UI mixes a **dark rail** and **light
  cards**, and one global icon colour can't read on both surfaces. Each icon is
  tinted for the surface it sits on (rail vs card), exactly like FinanceDashboard.
- **The Market grid is a real widget**, not hand-rolled rows: per the "promote,
  don't hand-paint" rule, the table is a `QCustomDataTable` configured in the
  manager (columns/renderers/colours in code, like charts).
- **`applyDesignTokens` is not called** by a `loadJsonStyle` app, so the
  `QCustomSegmentedControl` track/pill is styled by `#segmentButton` QSS in
  chrome.scss and the control gets `WA_StyledBackground` so its track paints.
- **Qt hex is `#AARRGGBB`**; the area chart's interactive toolbar is hidden with
  `setToolbarVisible(False)`; the bundled Rosario font may be missing, so a clean
  sans-serif family is set in chrome.scss.

Verified on the real running window (MCP `designer_run_app` → `app_screenshot`)
in **both themes**, with `design_lint` at 0 errors / 0 warnings.
