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

## QCustomAreaChart — borderless fill / top-line only (upgrade)
`Custom_Widgets/QCustomCharts/QCustomAreaChart.py` (added 2026-07-24, from the
`examples/PySide6/CryptoDashboard` build). A `QAreaSeries` pen strokes the
**whole** polygon outline, so a filled trend line shows steep vertical "walls"
where the fill closes down to the baseline at the first and last x (plus a
stroked baseline). New opt-in:

- `setAreaBorderEdges(enabled)` — `False` sets the area pen to `NoPen` (no side
  walls, no baseline stroke) and overlays a crisp **top-only** `QLineSeries`
  (kept out of the legend), giving the modern filled-trend-line look. `True`
  (default) preserves the original full-outline behaviour. `areaBorderEdges()`
  reads it back.
- Pair with `setGradientFill(True)` + `setFillOpacity(...)` for a fill that fades
  toward the baseline.

```python
chart.addSeries("Wallet", list(zip(xs, ys)), color=QColor(pal["chartLine"]), line_width=2.6)
chart.setAreaBorderEdges(False)   # no vertical edge walls; crisp top line only
chart.setGradientFill(True); chart.setFillOpacity(0.22)
```

Note: the `QCustomCharts` subpackage has **no `.pyi` stubs** (stubgen only covers
top-level `QCustom*`), so there's nothing to regenerate — verify on the live app.

## Registration / stubs
All three new widgets are registered in `Custom_Widgets/Plugins/register.py`
(Designer palette) and have regenerated `.pyi` stubs
(`python -m Custom_Widgets.mcp.stubgen --write`). The MCP catalog is AST-scanned
and `lru_cache`d per server process, so `widgets_catalog` / `render_widget` only
list new widgets after a server restart.

## 2026-07-24 additions (diverging chart + interactive widgets)
Extracted from the `examples/PySide6/CashFlowDashboard` build. Full report:
[session-2026-07-24-cashflow-widgets.md](session-2026-07-24-cashflow-widgets.md).

### QCustomDivergingBarChart  `Custom_Widgets.QCustomDivergingBarChart`
Painted **diverging (bipolar / up-down) bar chart**: one column per category with
an UP segment (income) and DOWN segment (expense) in two colours, split across a
zero axis. Key knob: **`zeroGap`** (px of clear space between the + and − bars).
`setData(up, down, labels)`, `setColors(up, down)`, `axisPrefix/axisSuffix`
(e.g. `€…K`), `gridColor`, `axisTextColor`; CSV props `upCsv/downCsv/labelsCsv`.
The diverging sibling of `QCustomMiniBarChart` — use it, not two grouped QtCharts
series, for a cash-flow chart.

### QCustomCardStack  `Custom_Widgets.QCustomCardStack`
Interactive stack of `QCustomPaymentCard` children (front full-size, backs peek up
+ inset). Click / `next()` / `previous()` cycles with an animated reshuffle.
`setCards([{brand,amount,number,top,bottom,fullNumber}])`,
`setCardColorsList([(top,bottom)…])` (per-card gradients, keeps index on a theme
flip), `currentChanged(int)`; `cardsJson` Designer prop.

### QCustomMenu  `Custom_Widgets.QCustomMenu`
Modern popup action menu for `…`/more buttons — frameless rounded elevated panel,
icon+label rows, hover, `addSeparator()`, `danger=` rows. `addAction(text, key,
icon, danger=)`, `popupAt(button, "right")`, `triggered(str)`. It is a TOP-LEVEL
popup: theme it from code with `applyColors(...)` (app QSS does not cascade in),
and it is NOT captured by `win.grab()`/`app_screenshot` — verify via a headless
`panel.grab()` test.

### QCustomModal  `Custom_Widgets.QCustomModal`
Modern centered modal: dims the parent window (scrim) + a centered rounded card
with title/subtitle, a **painted-X** close (a `QPushButton` subclass — never a
`×` glyph), a content slot and action buttons. `setTitle/setSubtitle`,
`addContent(widget)`, `addAction(text, key, primary=/danger=)`,
`clearContent()`/`clearActions()`, `showModal()`, `triggered(str)` + `closed()`.
As a child of the window it IS captured by `app_screenshot`.

### Remote fonts (library, not a widget)
`Custom_Widgets.Utils.download_font(url)` + `json-styles Fonts.LoadFonts[].url`
(alongside `path`) + `QCustomTheme.loadRemoteFont(url, set_as_default=)`. TTF/OTF
only (no WOFF/WOFF2), cached under `generated-files/fonts/`, non-fatal on failure.
`Fonts.DefaultFont` applies the family app-wide. Fixes the bundled-Rosario
mono/system fallback (set a real sans like Inter).

### Preview / gotchas
All four widgets **seed guarded demo data in `__init__`** so they preview in
Designer / `render_widget`; the app replaces it via `setData`/`setCards`. See
`Custom_Widgets/mcp/guide.py` (HARD-WON GOTCHAS) and
[design-rules.md](design-rules.md) for the layout-geometry, native-bg-box,
scss-rgba-triples, popup-capture and painted-affordance lessons.

## 2026-07-24 addition — QCustomRadialGauge (gauge family)
`Custom_Widgets.QCustomRadialGauge` — the first item off the
[missing-widgets backlog](missing-widgets-from-references.md). ONE painted
gauge, two looks via **`gaugeStyle`**:

- **`gaugeStyle="needle"`** (default) — a thick coloured value arc over a muted
  track + a drawn **needle**, big centre value, `0`/`100` scale labels at the arc
  ends, and an optional coloured **status badge** below. Colour the arc by
  **zones** (`setZones([(0,33,green),(33,66,amber),(66,100,red)])` or the
  `zonesCsv` prop `"lo:hi:#hex, …"`) — the active band recolours the whole value
  arc **and** the badge — or by a two-stop gradient. Covers the speedometer /
  threshold / **Threat Level** semicircle references.
- **`gaugeStyle="tick"`** — a sweep of tick marks: passed ticks use the
  `gradientStart`→`gradientEnd` gradient, the rest a muted track. Covers the
  radial-tick **"17 Sec"** timer.

**Flexibility is the point** — one widget, not five gauge classes. Angles use the
Qt convention (deg, 0 at 3 o'clock, +CCW), so `startAngle`/`spanAngle` set **any**
start point and sweep: a downward semicircle is `180 / -180`, a 270° timer with a
bottom gap is `225 / -270`, a **full-circle dial** is `90 / -360`. Other knobs:
- **scale**, three independent layers — `showScaleLabels` (min/max end labels,
  needle style), `showGuide` (dashed inner scale ring, **both** styles), and
  `scaleLabelEvery=N` (numeric labels every N units around the arc; supersedes the
  end labels).
- **`roundedCaps`** — rounded vs flat arc/tick ends (arc "border radius").
- **`animated` + `animationDuration`** — value changes ease to the new position
  (arc, needle and centre number animate); `valueChanged(float)` still fires
  immediately with the logical target.
- **`emphasizeActiveTick`** + **`activeTickExtend`** (`inward`|`outward`|`both`)
  — the leading (last passed) tick drawn longer + brighter, extended in the
  chosen direction (tick style). Full-circle tick timers work too
  (`startAngle=90, spanAngle=-360`) — ticks space over `[0,1)` so the ends don't
  double up.
- **`scaleLabelRadius`** — override the numeric-label ring radius (fraction of
  the gauge radius; `0` = auto). On **needle** gauges the scale numbers render
  **outside** the arc band (speedometer style) and the dial auto-shrinks to leave
  room, so the needle — which sweeps the interior — can never cross a number. On
  **tick** gauges (no needle) they sit inside.
- **countdown** — `start(seconds=…)` / `stop()` (QTimer-backed) + `finished`.
- **`glow` + `glowStrength` + `glowRadius`** — a soft **painted** neon halo behind
  the value arc / lit ticks (opt-in, default off). It's a re-stroke bloom (the
  shape drawn a few times at growing width + falling alpha, ≈ a Gaussian-blur
  halo) coloured by the active zone/gradient — so it flips with the theme and
  needs **no** `QGraphicsDropShadowEffect` / `# allow-shadow:` waiver. This is the
  worked example behind the "shadows / glow / blur where necessary" guideline.

The needle is a dark slate by default with a length gradient (bright base → dark
tip + bright pivot) so it reads on dark cards. Full prop list: `value`,
`minimum`, `maximum`, `gaugeStyle`, `startAngle`, `spanAngle`, `tickCount`,
`arcWidth`, `roundedCaps`, `zonesCsv`, `gradientStart`, `gradientEnd`,
`trackColor`, `needleColor`, `centerText`, `centerSuffix`, `statusText`,
`statusColor`, `centerTextColor`, `scaleColor`, `showNeedle`, `showScaleLabels`,
`showGuide`, `scaleLabelEvery`, `scaleLabelRadius`, `emphasizeActiveTick`,
`activeTickExtend`, `animated`, `animationDuration`, `glow`, `glowStrength`,
`glowRadius`. All colours are qproperties so they flip on a theme switch.

> **Guideline followed here — exhaust the variation space.** This widget is the
> worked example behind the "widgets are fully customizable" rule in the MCP
> `AGENT_GUIDE` / [[widgets-fully-customizable-rule]]: enumerate every plausible
> variation (shape, scale layers, rounded caps, animation, emphasis, centred
> value/unit, every colour/width/angle) and ship each as an opt-in knob that
> defaults to the current look — don't build the one look a single reference shows.
Naming gotchas respected: the look prop is **`gaugeStyle`** (not `style` — that
shadows `QWidget.style()`), and `value` is a Property only (no same-named
method; use `setValue()`). Seeds a needle/zones demo (value 55, "Medium") in
`__init__` so it previews in Designer / `render_widget`. Mirror:
`QCustomDonut` (painted arc) + `QCustomProgressRing`.

## 2026-07-24 addition — QCustomHeatmap (intensity grid)
`Custom_Widgets.QCustomHeatmap` — backlog item #1
([missing-widgets](missing-widgets-from-references.md)). A painted
colour-intensity grid, two **`mode`**s:

- **`mode="grid"`** (default) — a rows×cols matrix (e.g. hours×weekdays — the
  Loud "Activity by time" heatmap): each cell's colour = its value on a
  `lowColor`→`highColor` ramp, with row/col labels and a **Less→More** legend.
- **`mode="calendar"`** — a GitHub-style contributions calendar: a flat list of
  daily values wrapped into 7 rows (weekdays) × N columns (weeks).

Data via `setValues(list[list])` / a flat list (calendar) / the `valuesCsv`
Designer prop (rows `;`-separated, cells `,`-separated; empty cell = blank →
`emptyColor`). Cells **auto-normalise** across the data (min→max) unless
`setRange(lo,hi)` / `autoNormalize=False`. `cellClicked(row,col,value)` signal +
a per-cell hover tooltip. **Flex cell sizing** — cells fit the box left after the
labels + legend, so nothing clips as the widget grows/shrinks (the flex-sizing
rule in the guide). Key props: `mode`, `valuesCsv`, `lowColor`, `highColor`,
`emptyColor`, `rowLabelsCsv`, `colLabelsCsv`, `cellSize` (0 = auto), `cellGap`,
`cornerRadius`, `showLabels`, `showLegend`, `labelColor`, `autoNormalize`,
`minValue`, `maxValue`. Seeds a 6×7 activity grid in `__init__` for Designer /
`render_widget` preview. Mirror: `QCustomMiniBarChart` + `QCustomDonut`.

## 2026-07-24 addition — QCustomLiquidGauge (wavy fill level)
`Custom_Widgets.QCustomLiquidGauge` — backlog item #2b. A circular **or**
rounded-rect container with an **animated two-wave sine liquid fill** whose
height tracks `value` — the fuel / battery / tank / storage / humidity disc. A
`QTimer` drifts the waves (~30 fps, only while visible) and the fill level
**eases** to a new value when `animated`. A back wave (offset + lifted) behind a
gradient front wave gives the surface depth. Centre shows the value + suffix
(e.g. `3.61 gal`, `72%`) and an optional status badge below.

`setValue`/`setRange`, `setColors(fill1, fill2, background)`, `setBadge(text,
color)`, `shape` (`circle`|`roundedRect`) + `cornerRadius`. Props: `value`,
`minimum`, `maximum`, `shape`, `cornerRadius`, `fillColor`, `fillColor2`,
`backgroundColor`, `ringColor`, `ringWidth`, `waveAmplitude`, `waveLength`,
`waveSpeed`, `animated`, `centerText`, `centerSuffix`, `centerTextColor`,
`badgeText`, `badgeColor`. **Flex sizing** — the disc + centre text fit the box,
reserving room for the badge (per the flex rule). `value` is a Property only (no
same-named method; use `setValue()`); seeds `value=68` for preview. Mirror:
`QCustomProgressRing` + `QCustomRadialGauge`.

## 2026-07-24 addition — QCustomRulerPicker (tick-ruler selector)
`Custom_Widgets.QCustomRulerPicker` — backlog item #3. A measurement-style ruler
(the weight/height "55 … 65 … 90" picker): a strip of minor ticks with taller
**major ticks + numeric labels** (the current one bold) and an indicator at the
value. Two looks via **`centered`**: `False` (default) is a **fixed** ruler
(min→max across the width, indicator slides to the value — the reference weight
card); `True` is a **scrolling** picker (value pinned under a fixed centre
indicator, the scale scrolls). `orientation` = `horizontal` | `vertical`.
**Drag / scroll-wheel / click** to change; `snap` to `step`. Optional big
value + `unit` readout (`showValue`). `valueChanged(float)`; `setValue`/`setRange`.

Props: `orientation`, `minimum`, `maximum`, `value`, `step`, `majorEvery`,
`centered`, `tickSpacing` (px/step in centered mode), `snap`, `unit`,
`showValue`, `tickColor`, `majorTickColor`, `indicatorColor`, `labelColor`,
`valueColor`. **Flex** — the tick length is capped and the [labels+ticks] block
is centred in the short axis, so a tall/short card keeps short ticks (a bug the
live preview caught: uncapped `depth` stretched ticks to full card height).
`value` is a Property only (use `setValue()`). Mirror: `QCustomRangeSlider`.

## 2026-07-24 addition — QCustomDateRangePicker (inline range calendar)
`Custom_Widgets.QCustomDateRangePicker` — backlog item #5, the inline dual-month
travel-dates range picker (the piece the compact popup `QCustomDateRangeEdit`
lacks). N month grids side by side (`monthsVisible`, responsive → stacks when
narrow), a painted **in-range band** between the two chosen days (rounded at the
range ends **and** each week wrap via a selective-corner path), green **endpoint
circles**, a **today** marker, and painted-chevron month **nav arrows**. Click a
day to set the start (clears the end); a later day sets the end (earlier moves the
start). `setStartDate`/`setEndDate`/`setRange(QDate…)`, `setSelectableRange(min,
max)`, `showMonth(y,m)`; **`rangeChanged(QDate start, QDate end)`**. Uses stdlib
`calendar` (Sunday-first) for the month matrices. Props: `monthsVisible`,
`accentColor`, `rangeBandColor`, `todayColor`, `textColor`, `mutedColor`,
`headerColor`, `selectedTextColor`. Bind `startDate()`/`endDate()` to your own
fields + a Save button (see `examples/PySide6/DateRangeDemo`). Mirror:
`QCustomDateRangeEdit` (sibling — this is the inline panel form).

## 2026-07-24 addition — QCustomWaveform (equalizer / streaming ECG)
`Custom_Widgets.QCustomWaveform` — backlog item #6, a standalone (NOT chat-bound
like `QCustomVoiceMessage`) waveform visualiser, two **`mode`**s:

- **`mode="bars"`** (default) — an equalizer / audio-level bar viz (the "Water"
  card): one rounded bar per value, gradient (`barColor`→`barColor2`), optional
  centre **`mirror`** (voice-message symmetry) and **`glow`** (neon spectrum).
- **`mode="line"`** — a streaming line viz (the "110 bpm" ECG card): a polyline
  over an optional faint **grid**, optional gradient **`fillArea`** under it,
  optional `glow`.

Feed a fixed series with `setValues([...])` / `valuesCsv`, or **stream** live with
**`push(value)`** — a `capacity` ring buffer scrolls (newest at right). Turn on
**`animated`** for a self-running demo (deterministic audio levels in bars mode, a
PQRST **heartbeat** in line mode) so it previews live without a data source.
`valuePushed(float)` fires on each push. Props: `mode`, `valuesCsv`, `capacity`,
`barColor`, `barColor2`, `barWidth` (0=auto), `barGap`, `cornerRadius`, `mirror`,
`lineColor`, `lineWidth`, `showGrid`, `gridColor`, `fillArea`, `glow`,
`glowStrength`, `animated`. Auto-normalises (bars → 0..max; line → ±max abs so a
signed ECG centres). **Flex** — bars/line fit the box. Mirror:
`QCustomSparkline` + `QCustomMiniBarChart`.

## 2026-07-24 addition — QCustomAgendaList (schedule timeline)
`Custom_Widgets.QCustomAgendaList` — backlog item #7, the day-plan / schedule card
(Running / Cycling / Gym / Swimming). Each row has a left **connector rail** with a
painted per-item **status marker** — `done` = a painted check in a filled disc,
`active` = a filled dot **plus a highlighted rounded row background**, `pending` =
a hollow ring (all painted, **no glyph fonts**) — and a **time range + bold title
+ muted subtitle**. `setItems([{time, endTime, title, subtitle, status, color}])`
or the `itemsJson` Designer prop; `itemClicked(index)` + hover highlight. **Flex
row height** fits the text, and `sizeHint`/`heightForWidth` report the full height
so it drops into a `QScrollArea` (widgetResizable). Props: `itemsJson`,
`rowHeight` (0=auto), `railColor`, `doneColor`, `activeColor`, `pendingColor`,
`titleColor`, `subtitleColor`, `timeColor`, `activeBgColor`, `showRail`. Richer
than `QCustomTimeline`; mirror: `QCustomTimeline` + `QCustomListRow`.

## 2026-07-24 addition — QCustomBubbleChart (packed-circle chart)
`Custom_Widgets.QCustomBubbleChart` — backlog item #8, the sentiment / share
bubble cloud. Circle **area ∝ value**, packed into a tight cluster by a small
**deterministic force relaxation** (push overlaps apart + gentle gravity to the
centre — no RNG, so tests are stable), then scaled to fill the widget. Coloured
per **category** (`setCategoryColors({cat: colour})` / `categoriesJson`), with
in-bubble **elided labels** above `minLabelRadius` and a slight shade variation
for depth, optional **`groupByCategory`** (per-category lobes on an anchor circle —
the sentiment layout). **Fully interactive** (the reference has zoom + search):
- **hover** → a **custom painted tooltip card** (category dot + label + value —
  *never* the native `QToolTip`) + a grow animation + glow on the hovered bubble.
- **zoom/pan** → wheel zooms toward the cursor, a painted **± control**, drag to
  pan, double-click resets; `zoomIn()`/`zoomOut()`/`resetView()`, `zoomChanged`.
- **search** → `setSearchQuery(text)` dims the non-matching bubbles; the painted
  search button emits `searchRequested()` (wire it to your own field).
- **click** → `bubbleClicked(label)` (fires on release, so a drag-pan doesn't
  trigger it).

`setItems([{label, value, category}])` / `itemsJson`. Props: `itemsJson`,
`categoriesJson`, `padding`, `showLabels`, `minLabelRadius`, `labelColor`,
`defaultColor`, `shadeVariation`, `hoverGlow`, `hoverScale`, `groupByCategory`,
`zoomable`, `showControls`, `searchQuery`, `tooltips`, `tooltipBgColor`,
`controlColor`. **Flex** — the whole cluster rescales to any size. This is the
worked example behind the "interactive + custom tooltips (not native)" guideline.
Mirror: `QCustomDonut` (painted, category colours).

## 2026-07-24 addition — QCustomCompass (heading rose)
`Custom_Widgets.QCustomCompass` — backlog item #9, the map/heading compass. A
painted rose: tick ring, N/E/S/W (+ intercardinals), a two-tone needle (coloured
north / muted south) and a centre readout — a **16-point cardinal** (N…SSW…) +
degrees, auto-**sized to fit the hub**. `heading` (0–360°, 0 = North = up) eases
along the **shortest** angular path when `animated`. Two looks via **`rotateBezel`**:
`False` (default) the needle rotates to the heading; `True` an aircraft/marine
**rotating card** — needle stays up, the rose spins so the heading sits on top.
**Drag around the centre to set the heading** (`interactive`); `headingChanged(float)`.
Props: `heading`, `rotateBezel`, `showIntercardinals`, `showReadout`, `animated`,
`interactive`, `northColor`, `southColor`, `ringColor`, `tickColor`,
`cardinalColor`, `readoutColor`, `hubColor`. **Text is measured to fit** — the
readout shrinks for 3-letter points and every label rect is sized to its string,
so nothing truncates at any widget size (the calculate-text-to-fit rule).
`heading` is a Property only (no same-named method — that gotcha bit here; use
`setHeading()`). Mirror: `QCustomRadialGauge` (painted dial).

## 2026-07-24 upgrade — QCustomDonut % callouts + hatch fills
`QCustomDonut` (segments mode) gained two **opt-in** enhancements (default OFF, so
the classic donut is unchanged) for the "Transfer history" reference:
- **`showPercentLabels`** — a `%` callout **pill on each arc** at its mid-angle
  (`percentLabelColor`, `percentPill` on/off, `percentPillColor`,
  `minLabelPercent` to suppress tiny slices).
- **`hatchCsv`** (+ **`hatchPattern`** = bdiag / fdiag / cross / horizontal /
  vertical / dense) — the listed **segment indices** render with a hatch pattern
  over a dimmed base (a "hatched" slice like the reference's *Other*). Code API:
  `setShowPercentLabels(bool)`, `setHatchIndices([...])`, `setHatchPattern(name)`.

Both painted; verified with `render_widget` + `tests/test_qcustom_donut_enhance.py`.

### QCustomCompassDial — premium beveled sibling
`Custom_Widgets.QCustomCompassDial` — a **skeuomorphic-modern** instrument
compass (the Haulix map dial), built as a **separate** widget so the flat
`QCustomCompass` is untouched. Same API (heading / `rotateBezel` / `animated`
ease / drag-to-set / `headingChanged`) with a premium painted look: a **beveled
metal rim** (top-lit → bottom-shadowed `QLinearGradient`), a **domed glass face**
(`QRadialGradient`), a **fine watch-bezel tick ring** with **brass** (`accentColor`)
majors at the cardinals, and a **metallic centre cap** carrying the fit-to-cap
16-point readout + degrees. All depth is painted (gradients, no effect object —
theme-safe, no `drop-shadow` waiver). Extra props over the flat one: `bezelColor`,
`faceColor`, `accentColor`, `capColor` (+ `northColor`/`southColor`/`tickColor`/
`cardinalColor`/`readoutColor`). Use the flat `QCustomCompass` for a minimal UI,
this dial for a rich instrument panel.

## Check Box dashboard viz (2026-07-24)

Three painted widgets + a Sparkline extension, built for the "Check Box"
(Nixtio) dashboard reproduction — `examples/PySide6/CheckBoxDashboard`. All
follow the painted-widget convention (`WIDGET_*` + `__catalog__` + typed
`@Property`s + `valuesCsv`-style CSV inputs), seed guarded demo data, and take
their live colours from the app's token-driven `ChartPalette` so they flip on
theme switch.

## QCustomDotMatrix
`Custom_Widgets/QCustomDotMatrix.py` — a density / category **dot grid**. Each
cell carries a STATE: 0 = empty (`emptyColor`, faint), 1..N pick from
`colorsCsv`. `setData([[0,1,2,...], ...])` (row-major 2-D int list) or the
`dataCsv` prop (rows by `;`, cells by `,`). Props: `rows`, `cols`,
`dotDiameter` (0 = auto-fit to the box), `gapRatio`, `emptyOpacity`, `square`.

## QCustomBeeswarm
`Custom_Widgets/QCustomBeeswarm.py` — a **column beeswarm / numbered
bubble-stack**. Each column is a thin guide line carrying a vertical stack of
rounded "pill" bubbles; every bubble shows its VALUE and is coloured by CATEGORY
(`colorsCsv` fills + `textColorsCsv` number colours); pill height scales the
value between `minSize`..`maxSize`. `setData(columns)` where `columns` is a list
of columns, each a list of `(value, category)`; or `dataCsv` (columns by `;`,
items `value:category` by `,`). Props: `lineColor`, `bubbleWidth`, `gap`,
`showValues`, `jitter`. Draw the legend + total as sibling labels (reuse).

## QCustomGanttChart
`Custom_Widgets/QCustomGanttChart.py` — a **horizontal timeline / gantt** of
rounded pill bars. Each row is one bar on a shared numeric x-axis by `start` +
`length`, with a left date LABEL, a trailing VALUE, and an optional leading
circular ICON (a QPixmap clipped to a circle) or coloured dot; a light x-grid
with tick labels runs underneath. `setData([{label,start,length,category,value,
icon}])` (icon = path or QPixmap) or `dataCsv` (`label,start,length,category,
value` rows by `;`). Props: `xMax`, `gridStep`, `barHeight`, `colorsCsv`/
`textColorsCsv`, `labelColor`, `axisTextColor`, `gridColor`, `showGrid`,
`showMarkers`.

## QCustomSparkline — multi-series
`setSeries([[...], ...], colors=[...])` (or `setSeriesColors`) overlays N lines
on ONE shared y-scale with fill suppressed — for a clean multi-line read. Designer
props `seriesCsv` (series by `;`) / `seriesColorsCsv`. The single-`values` mode is
untouched.

## Smart-home dashboard widgets (2026-07-24)

From the `examples/PySide6/SmartHomeDashboard` build ("My Home" reference).

## QCustomTileButton
`Custom_Widgets/QCustomTileButton.py` — a selectable device / action **tile**: a
rounded-rectangle `QAbstractButton` with a line ICON above a CAPTION. It is
CHECKABLE — the selected tile paints a two-stop diagonal GRADIENT
(`gradientStart`→`gradientEnd`) with light icon+text (`activeColor`), the rest a
flat `bgColor` with muted `iconColor`. `setIconPath(.svg)` + `caption`; props
`gradientStart`/`gradientEnd`/`bgColor`/`iconColor`/`activeColor`/`cornerRadius`/
`iconSize`. Emits `clicked()`/`toggled(bool)` — drop several in a `QButtonGroup`
(exclusive) for a single-select device grid. The caption wraps for long names.

## QCustomRadialGauge — ring-gauge extensions
Added three opt-in hooks so the needle gauge also renders the modern
ring-with-knob look (with `showNeedle=False`):
- `showHandle` (+ `handleColor`) — a white end-cap knob at the value-arc tip.
- `centerIcon` (+ `iconColor`) — a recoloured SVG icon centred above the value.
- `innerColor` — a filled inner disc behind the value (e.g. a white disc with a
  dark value, as on the Temperature / Power gauges).

Recipe for a reference ring gauge: `showNeedle=False, showHandle=True,
showGuide=False, showScaleLabels=False, roundedCaps=True, zonesCsv=""` (clear the
default zones so the two-stop `gradientStart`→`gradientEnd` is used), a ~285°
span (`startAngle≈232, spanAngle≈-284`), `innerColor` = white,
`centerTextColor` = dark, `centerIcon` = a thermometer / lightning svg.
