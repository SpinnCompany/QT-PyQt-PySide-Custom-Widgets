# Check Box — dashboard example

A faithful rebuild of the "Check Box" analytics dashboard (dark, lime-green +
orange accent) using the Custom_Widgets **forms pipeline** and the **granular
component** architecture. Runs in a dark and a light theme; every colour flips
on theme switch because it is token-driven.

## What it demonstrates

- **Granular, component-based UI.** The shell (`ui/MainWindow.ui`) is almost
  empty — it just hosts one `QCustomComponentContainer` per region, each loading
  a small component `.ui`:
  `TopNav`, `LeftRail`, `Header`, `CustomerCard`, `ProductCard`, `BeeswarmCard`,
  `TimelineCard`. Each is authored + hot-reloaded on its own.
- **Four painted data-viz widgets** built for this screen (all now in the
  library, Designer-droppable under the *Charts* group):
  - `QCustomSparkline` (multi-series mode) — the CUSTOMER two-line trend.
  - `QCustomDotMatrix` — the PRODUCT density dot grid.
  - `QCustomBeeswarm` — the PRODUCT numbered bubble-columns.
  - `QCustomGanttChart` — the PROJECTS TIMELINE bars (date axis, leading icon,
    trailing value).
- **Token-driven theming.** Chrome (shell, cards, pills, type) is pure SCSS
  tokens in `Qss/scss/chrome.scss` (`$COLOR_BACKGROUND_*`, `$COLOR_TEXT_*`,
  `$COLOR_ACCENT_*`). Every painted hue comes from the `ChartPalette` in
  `json-styles/style.json`, read by `gui/theme.py`, so the whole board recolours
  when you toggle the theme (the sliders button, top-right of the header).
- **Real media, best-effort + async.** The profile avatar is fetched from a
  free no-key provider (pravatar) in a worker thread, with an initials-circle
  fallback if offline. Icons are real feather SVGs, recoloured per theme.

## Pipeline

```
ui/*.ui  ->  src/ui_*.py            (Custom_Widgets --convert-ui)
json-styles/style.json              (CheckBox Dark / Light CustomThemes + ChartPalette)
Qss/scss/*.scss                     ($TOKENS, no hard-coded hex in chrome)
gui/GuiFunctions.py                 (orchestrator: fills every component + repaints on theme change)
gui/data.py                         (all runtime data — never in the .ui)
gui/workers.py                      (clock + avatar background workers)
```

Build + run through the Custom_Widgets MCP (Designer `Run`), or:

```bash
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
python main.py
```

## Component gotchas worth knowing

- **A component `.ui` loaded by `QCustomComponentContainer` must have a `QWidget`
  root, not `QFrame`.** The loader calls `setupUi(self)` where `self` is the
  loader (a `QWidget`); a `QFrame` root makes uic call `setFrameShape(...)` on
  it and the whole setup aborts. Wrap the card visual in an inner
  `QFrame[role="card"]` (StyledPanel) instead.
- **After a component hot-reload, `container.component` is stale** (it points at
  the deleted old Ui instance). Read the live one from `container.form.ui`.
  `GuiFunctions` does this and re-applies all code-set content (icons + data) on
  a debounced `src/` watcher so the live-reload dev loop keeps working.
