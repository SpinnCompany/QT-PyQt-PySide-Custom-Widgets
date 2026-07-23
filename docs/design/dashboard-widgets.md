# Dashboard widgets — payment card, mini bar chart, list row (+ bar-chart per-bar colours)

**Added:** 2026-07-23 — from the `examples/PySide6/FinanceDashboard` build. Rule of
thumb that drove these: *anything a dashboard manager has to hand-paint or
hand-assemble repeatedly should be a first-class, Designer-promotable widget.*
Each of these replaced hand-rolled code in that example.

All follow the painted-widget convention (`WIDGET_ICON/TOOLTIP/MODULE/DOM_XML`
constants + `__catalog__` + typed `@Property`s + `valuesCsv`-style Designer
inputs), mirroring `QCustomSparkline` / `QCustomDonut`. Colours are qproperties
so a theme/manager tokenises them and they flip on theme switch.

> **Guideline — promote, don't hand-paint.** When an app design needs a data
> surface no widget covers, build the widget (this convention), register it in
> `Plugins/register.py`, regenerate stubs, and use it — don't leave hand-painted
> surfaces in a manager. The end-to-end **development procedure and rules** are
> documented in `examples/PySide6/FinanceDashboard/README.md`, the reference app
> that these widgets were extracted from.

## QCustomPaymentCard
`Custom_Widgets/QCustomPaymentCard.py` — a painted credit/debit card surface.

- `variant="gradient"` (default): two-stop diagonal gradient, light text (an
  "active" card). `variant="flat"`: single fill with a controllable text colour
  (a muted secondary card).
- Content: `setBrand(str)`, `setAmount(str)`, `setNumber(str)` (auto-masks to
  `•••• •••• •••• {last4}`). `setColors(start, end)` / `setVariant()`.
- Designer props: `brand`, `amount`, `number`, `variant`, `gradientStart`,
  `gradientEnd`, `flatColor`, `textColor`, `cornerRadius`, `showChip`.

```python
card.setVariant("gradient"); card.setColors(pal["cardTop"], pal["cardBottom"])
card.setAmount("$5 400.55"); card.setNumber("4558")
```

## QCustomMiniBarChart
`Custom_Widgets/QCustomMiniBarChart.py` — the painted, axis-less **bar** sibling
of `QCustomSparkline`. Use it (not the QtCharts `QCustomBarChart`) when you want
per-bar colours and labels in a small panel.

- `setData(values, colors=None, labels=None)`, `setBarColors([...])`,
  `setLabels([...])`, `highlightIndex(i, color=None)` (one accented bar),
  `setIdleThreshold(v)` (bars ≤ v render in `idleColor`).
- Rounded tops, even column layout, optional labels under each bar.
- Designer props: `valuesCsv`, `colorsCsv`, `labelsCsv`, `barColor`, `idleColor`,
  `highlightColor`, `barWidth`, `cornerRadius`, `showLabels`, `labelColor`.

## QCustomListRow
`Custom_Widgets/QCustomListRow.py` — a leading-icon list item (transaction /
activity / leaderboard / notification row). Composed from a layout + `QLabel`s
(not painted) so text uses real fonts and can be themed by `role` QSS, with
sensible inline defaults for standalone use.

- Leading chip: `setIcon(QPixmap|QIcon)` or `setIconText("S")`.
- `setTitle/setSubtitle/setValue/setMeta`.
- Designer props: `title`, `subtitle`, `value`, `meta`, `iconText`, `chipColor`,
  `chipTextColor`, `subtitleColor`, `valueColor`, `chipSize`, `chipRadius`.
- Child label roles for extra QSS: `listRowTitle/Subtitle/Value/Meta`.

## QCustomTrendChip
`Custom_Widgets/QCustomTrendChip.py` — a painted directional delta indicator
(green up / red down / grey flat) with an optional value label.

- `variant="circle"` (default): arrow in a tinted circle (the classic
  income/expense chip). `"soft"`: tinted pill + arrow + text. `"plain"`: arrow +
  text, no fill.
- `setDirection("up"|"down"|"flat")` or `setValue(number, text=None)` (infers
  direction from sign). The arrow is drawn with QPainter (no glyph font).
- Designer props: `text`, `direction`, `variant`, `upColor`, `downColor`,
  `flatColor`, `tintOpacity`, `cornerRadius`.

## QCustomAvatar
`Custom_Widgets/QCustomAvatar.py` — a single circular avatar (initials or image)
with an optional status/notification dot and outer ring. Complements the
existing `QCustomAvatarGroup`.

- `setText(initials)` / `setImage(pixmap|path)`; `setStatus(visible, color)`.
- Status dot has a border ring (`statusBorderColor`) so it reads cleanly over any
  surface; `statusPosition` = `top-right|bottom-right|top-left|bottom-left`.
- Emits `clicked` (usable as a profile button).
- Designer props: `text`, `bgColor`, `textColor`, `showStatus`, `statusColor`,
  `statusPosition`, `statusBorderColor`, `ringColor`, `ringWidth`.

## QCustomPaymentCard — eye reveal (upgrade)
The card can now reveal its full number. Set `revealable=True` and provide the
complete PAN via `fullNumber` ("4539 1482 0343 4558"); a painted eye toggles at
top-right (slashed when revealed). API: `setRevealable`, `setFullNumber`,
`setRevealed`, `toggleReveal`; signal `numberRevealed(bool)`. Masked shows
`•••• •••• •••• {last4}`; revealed regroups the digits in fours.

## QCustomPageDots
`Custom_Widgets/QCustomPageDots.py` — a carousel / pager indicator: a row (or
column) of dots where the active page is an elongated pill. Painted; optionally
clickable — clicking a dot sets it active and emits `pageChanged(index)`, so it
can drive a `QCustomQStackedWidget` / carousel.

- `setCount(n)`, `setActiveIndex(i)`, `setColors(dot, active)`.
- Designer props: `count`, `activeIndex`, `dotColor`, `activeColor`,
  `dotDiameter`, `activePillLength`, `spacing`, `orientation`, `clickable`.
- Note: set `activeIndex` from code (manager) when it matters — a `.ui` custom
  property can be applied before `count`, so an explicit `setActiveIndex` after
  `setCount` is the reliable path.

## QCustomBarChart — per-bar colours + highlight (upgrade)
`Custom_Widgets/QCustomCharts/QCustomBarChart.py` (+ `_RoundedBarOverlay` in
`QCustomBarChartBase.py`). The QtCharts bar chart previously coloured a whole
series at once. New:

- `setBarColors(colors, series_name=None)` — a list parallel to the series
  values (use `None` to keep the series colour for a bar).
- `highlightIndex(index, color=None, series_name=None)` — accent one bar
  (defaults to a lightened series colour). `clearHighlight()` / `clearBarColors()`.
- Applied natively via `QBarSet.setColor(i, c)` **and** honoured by the
  rounded-bar overlay (it reads `owner._colorForBar`), so square and
  rounded-top rendering match. Rounded tops themselves already existed via
  `setBarCornerRadius(px)`.

## Registration / stubs
All three new widgets are registered in `Custom_Widgets/Plugins/register.py`
(Designer palette) and have regenerated `.pyi` stubs
(`python -m Custom_Widgets.mcp.stubgen --write`). The MCP catalog is AST-scanned
and `lru_cache`d per server process, so `widgets_catalog` / `render_widget` only
list new widgets after a server restart.
