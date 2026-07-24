# Cash Flow — Dashboard

A green "Total Balance" banking dashboard built the **forms-pipeline** way
(`.ui` → compiled `src/` → `json-styles/style.json` themes → `Qss/scss` tokens →
`gui/GuiFunctions.py` orchestrator + Manager + worker). Reproduces a modern
fintech reference in **both light and dark** themes (switch by name via the
sidebar toggle).

## What it showcases
- **`QCustomDivergingBarChart`** — the Cash Flow chart: income up / expense down,
  split across a zero axis with a `zeroGap` and €K gridlines.
- **`QCustomCardStack`** — the interactive "My Cards" stack (click to cycle;
  per-card gradients).
- **`QCustomMenu`** / **`QCustomModal`** — the `…`/more popup menu and the Send
  modal.
- **Remote fonts** — loads **Inter** over the network via
  `json-styles Fonts.LoadFonts[].url` (`Custom_Widgets.Utils.download_font`).
- KPI cards, a `QCustomListRow`-style activity table with status pills, a teal
  gradient balance banner, and token-driven theming (`ChartPalette`).

## Run (through the Custom Widgets MCP)
Build and run via the MCP (`project_convert_ui` → `designer_run_app`), never
ad-hoc `python`. See `docs/design/session-2026-07-24-cashflow-widgets.md` for the
full build report and the widget APIs in `docs/design/dashboard-widgets.md`.
