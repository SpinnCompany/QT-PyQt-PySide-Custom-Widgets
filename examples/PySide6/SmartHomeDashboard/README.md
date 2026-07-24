# My Home — smart-home dashboard

A faithful rebuild of the "My Home" smart-home control panel (dark indigo, with
a purple→pink gradient signature) using the Custom_Widgets **forms pipeline**
and the **granular component** architecture. Runs in a dark and a light theme;
every gradient / painted hue flips on theme switch because it is token-driven.

## What it demonstrates

- **Granular, component-based UI.** The shell (`ui/MainWindow.ui`) just hosts one
  `QCustomComponentContainer` per region, each loading a small component `.ui`:
  `TopBar`, `HelloCard`, `GaugesCard`, `DevicesCard`, `LightingCard`,
  `SecurityCard`.
- **Reuse first, then extend, then build** (the widget rules):
  - **Reused** `QCustomSwitch` (the *Locked* toggle), a styled `QSlider` (the
    gradient brightness track), `QCustomComponentContainer`.
  - **Extended** `QCustomRadialGauge` with three opt-in ring-gauge hooks —
    `showHandle` (an end-cap knob at the value-arc tip), `centerIcon` (an icon
    above the value) and `innerColor` (a filled inner disc) — to render the
    Temperature / Power ring gauges. Set `zonesCsv=""` to use the two-stop
    gradient instead of the default green/amber/red zones.
  - **Built** `QCustomTileButton` — a checkable rounded-tile with an icon +
    caption that paints a gradient when selected (the device grid; a
    `QButtonGroup` makes it single-select).
- **Token-driven theming.** Chrome (shell, cards, type) is pure SCSS tokens in
  `Qss/scss/chrome.scss`. Every gradient surface (header bar, active tile, ring
  gauges, brightness slider, lock switch) is painted in `gui/GuiFunctions.py`
  from the `ChartPalette` in `json-styles/style.json`, so the whole board
  recolours when you toggle the theme (the ⚙ nav icon).
- **Real, recoloured icons.** Feather + Material SVG icons, tinted per theme with
  a universal SVG-alpha tint (works for stroke- and fill-based sets — the
  lightbulb comes from Material). The profile avatar is fetched from a free
  no-key provider (pravatar) with a painted fallback.

## Pipeline

```
ui/*.ui  ->  src/ui_*.py            (Custom_Widgets --convert-ui)
json-styles/style.json              (SmartHome Dark / Light CustomThemes + ChartPalette)
Qss/scss/*.scss                     ($TOKENS, no hard-coded hex in chrome)
gui/GuiFunctions.py                 (orchestrator: fills every component + repaints on theme change)
gui/data.py                         (all runtime data — never in the .ui)
```

Build + run through the Custom_Widgets MCP (Designer `Run`), or:

```bash
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
python main.py
```

## Component notes

- A component `.ui` loaded by `QCustomComponentContainer` must have a **QWidget
  root** (a QFrame root aborts `setupUi`); each card wraps its visual in an inner
  `QFrame[role="card"]`.
- After a component hot-reload, read the live form via `container.form.ui`
  (the cached `container.component` goes stale); `GuiFunctions` re-applies all
  code-set content on a debounced `src/` watcher.
- No unicode glyphs as icons (enforced by the design linter): the `◄ ►` steppers
  and the members `▾` are real recoloured SVG chevrons.
