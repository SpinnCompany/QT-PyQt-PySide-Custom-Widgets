# Missing widgets — gap analysis from dashboard references

**Added:** 2026-07-24 — from a gap analysis of five reference dashboards
(fitness mobile cards, two donut cards, the "Loud" finance dashboard, and a
sentiment bubble chart) against the current catalog.

This is a **backlog / build queue**, not a record of shipped work. Everything
below is *not yet built*. Implement one at a time following the painted-widget
convention (`WIDGET_ICON/TOOLTIP/MODULE/DOM_XML` constants + `__catalog__` +
typed `@Property`s + `valuesCsv`-style Designer inputs + qproperty colours that
tokenise on theme switch), register in `Plugins/register.py`, regenerate stubs,
add a headless paint test + a runnable `examples/PySide6/...` demo. Mirror
`QCustomSparkline` / `QCustomDonut` / `QCustomMiniBarChart`.

See also: [dashboard-widgets.md](dashboard-widgets.md) (the convention these
follow) and the standing "build more data-viz widgets" direction.

> **Already shipped (2026-07-24, outside this backlog)** — from the CashFlow
> dashboard build (`session-2026-07-24-cashflow-widgets.md`):
> `QCustomDivergingBarChart` (income-up/expense-down bars, the cash-flow chart),
> `QCustomCardStack` (interactive stacked cards), `QCustomMenu` (popup menu),
> `QCustomModal` (centered modal), plus the **remote-font** capability. The items
> below (Heatmap, RadialGauge, RulerPicker, …) are still open.

## Already covered (no action) — for reference

Steps ring → `QCustomProgressRing`; KPI pills/cards → `QCustomStatCard` /
`QCustomBadge`; weight line chart → `QCustomLineChart`; analytics area chart →
`QCustomAreaChart`; grouped bars → `QCustomBarChart` / `QCustomMiniBarChart`;
donut cards → `QCustomDonut` / `QCustomPieChart`; transaction list + tags →
`QCustomListRow` + `QCustomChip`/`QCustomBadge`; nav pills / Week·Month·Year →
`QCustomSegmentedControl` / `QCustomTabWidget`; checklist → `QCustomCheckBox` +
`QCustomListRow`.

---

## Build queue (ranked)

### 1. ⭐ QCustomHeatmap — HIGHEST VALUE
**Reference:** "Activity by time" grid in the Loud finance dashboard (img 4) —
a colored intensity grid with a **Less → More** legend. Also the classic
GitHub-contributions calendar heatmap.

**Why:** No widget renders a colored intensity grid. Appears in nearly every
analytics dashboard. Also explicitly named in the standing "build more data-viz"
note.

**Scope:**
- Two modes: `mode="grid"` (rows × cols matrix, e.g. hours × weekdays) and
  `mode="calendar"` (GitHub year-of-days).
- Data in via `setValues(list[list[float]])` or `valuesCsv`; auto-normalise to a
  min→max colour ramp.
- qproperties: `lowColor`, `highColor` (or a token ramp), `cellSize`,
  `cellGap`, `cornerRadius`, `rowLabels`/`colLabels` (CSV), `showLegend`.
- Signal: `cellClicked(row, col, value)`; tooltip per cell.
- Legend row (Less → More swatches) as an optional painted footer.

---

### 2. ⭐ QCustomRadialGauge — gauge family (tick / needle / threshold / countdown)
**Reference:** the "17 Sec" gradient-tick radial timer (fitness img 1); the
Haulix **speedometer** (0–150 mph, needle, green→red zone arc); and the three
**Threat Level** semicircle gauges (24% green / 55% yellow / 75% red, needle +
0–100 scale labels + center % + status badge). Three separate references now
demand this — it's the highest-recurring gap.

**Why:** Only the **legacy** `AnalogGaugeWidget` exists (skeuomorphic,
non-tokenized). Need one modern painted gauge that covers the common variants.

**Scope (variants — should be one widget with a `style`/`mode` switch):**
- **tick** — arc of tick marks sweeping min→max; passed ticks use an accent
  gradient, remaining a muted track (the "17 Sec" timer).
- **needle** — smooth coloured **zone arc** + a drawn needle pointer
  (speedometer / threshold gauge). Support `zones=[(0,33,green),(33,66,amber),
  (66,100,red)]` or a continuous gradient arc.
- **semicircle vs full-sweep** — `spanAngle` covers 180° (Threat Level) and
  ~270° (speedometer). Optional min/max scale labels at the arc ends ("0"/"100").
- **countdown** — drive from a `QTimer`; `start(seconds)`/`stop()`/`finished`.
- Center: big value + suffix (`gal`/`mph`/`%`/`Sec`) + optional **status badge**
  below ("Medium"/"High"/"Very Low") whose colour tracks the active zone.
- qproperties: `minimum`, `maximum`, `value`, `startAngle`, `spanAngle`,
  `tickCount`, `style` (tick|needle), `zones`/`gradientStart`/`gradientEnd`,
  `trackColor`, `needleColor`, `centerText`, `centerSuffix`, `statusText`,
  `showScaleLabels`.

---

### 2b. ⭐ QCustomLiquidGauge — wavy fill level gauge
**Reference:** the Haulix **Fuel level** widget (img: circular gauge with an
animated wavy liquid fill, "3.61 gal", 31% badge).

**Why:** No fill-level widget exists. Distinct from RadialGauge (this is a
liquid-fill disc, not an arc). Great for fuel / battery / tank / storage.

**Scope:**
- Circular (and optional rounded-rect) container with a **sine-wave fill** whose
  height ∝ value; animated horizontal wave drift via a `QTimer`.
- qproperties: `value` (0–100 or min/max), `fillColor` (or two-stop gradient),
  `waveAmplitude`, `waveSpeed`, `centerText`, `centerSuffix`, `animated`.
- Center label overlays the fill; optional secondary chip (e.g. "72°F").

---

### 3. ⭐ QCustomRulerPicker — tick-ruler value selector
**Reference:** the horizontal weight ruler "55 … 65 … 90" with a center
selector line (img 1, "Wight/Weight" card).

**Why:** No measurement-style value picker exists. `QCustomRangeSlider` /
`QCustomQSlider` don't do numbered ticks + a scrollable scale.

**Scope:**
- Horizontal (and vertical) ruler of minor/major ticks with numeric labels on
  majors; a fixed center indicator; drag/scroll to change value.
- `minimum`, `maximum`, `step`, `majorEvery`, `value`, `unit` (e.g. "Kg"),
  `tickColor`, `indicatorColor`, `snap` (bool).
- Signal: `valueChanged(float)`. Optional big value readout above the ruler.

---

### 4. QCustomWaveform / QCustomEqualizer — audio bars + ECG line
**Reference:** the "Water" audio-bar viz and the "110 bpm" live ECG line
(img 1, Heart-rate card).

**Why:** `QCustomVoiceMessage` has a waveform but it's chat-bound. Need a
standalone equalizer-bars widget and a streaming ECG-style line.

**Scope:**
- `QCustomWaveform` bars: `setValues(list[float])` / live `push(value)` ring
  buffer; `barColor`, `barWidth`, `barGap`, `cornerRadius`, `mirror` (bool),
  `animated`.
- ECG/line mode (or fold into `QCustomSparkline` as a `streaming=True` mode):
  scrolling live line with a grid background, accent stroke.
- Decide: separate widget vs. `QCustomSparkline` streaming mode (see
  enhancement note below).

---

### 5. QCustomAgendaList — schedule / event list
**Reference:** the Running / Cycling / Gym / Swimming timeline (img 1, right
column): time-range + activity icon + subtitle (location) + status dot
(done / pending).

**Why:** Richer than `QCustomTimeline` (painted rail + dots). Today you'd
hand-compose rows of icon + two-line text + time + status.

**Scope:**
- `setItems([{time, endTime, title, subtitle, icon, status}])`; painted
  connector rail on the left with a per-item state colour.
- Status enum: `done` / `active` / `pending` (colour + glyph).
- Signal: `itemClicked(index)`. Highlighted (active) row styling like the "Gym"
  row in the reference.

---

### 6. QCustomBubbleChart — packed-circle chart
**Reference:** the sentiment bubble chart (img 5) — packed circles sized by
value, coloured by category (positive/negative), labelled.

**Why:** Distinctive but niche. Lowest priority of the new widgets.

**Scope:**
- Circle-packing layout of `setItems([{label, value, category}])`; size ∝
  value; per-category colour; label inside when the bubble is large enough.
- qproperties: `padding`, `categoryColors` (map), `showLabels`, min label size
  threshold. Signal: `bubbleClicked(label)`.
- Circle-packing is the real work — a simple force/greedy pack is fine to start.

---

### 7. QCustomDateRangePicker — inline dual-month range calendar
**Reference:** the travel-dates picker (dual-month desktop + stacked mobile):
two month grids, start/end fields, a **range band** highlight between the two
selected days, and a Save action.

**Why:** `QCustomDateRangeEdit` exists but is a compact **popup** that keeps
start≤end — it doesn't render an inline multi-month grid with a highlighted
range band. Extend that widget (or add a sibling) for the inline panel form.

**Scope:**
- Inline calendar showing N months side-by-side (`monthsVisible`, responsive →
  stacked on narrow width); click start then end to define a range.
- Painted **in-range band** + rounded start/end endpoints; today marker.
- Bound `startDate`/`endDate` fields (reuse existing date-edit), `rangeChanged`
  signal, optional min/max selectable dates, `save`/confirm button slot.

---

### 8. QCustomCompass — heading / compass rose
**Reference:** the "NW" compass rose in the Haulix map (top-right).

**Why:** Niche, but no heading indicator exists. Cheap to paint.

**Scope:** painted rose (N/E/S/W + intercardinals), rotating needle/bezel,
`heading` (0–360°) qproperty, `cardinalText`, `headingChanged`. Low priority.

---

### 9. QCustomMapView — map surface with markers + route (LARGE / optional)
**Reference:** the Haulix operations map — vehicle markers, a highlighted route
polyline, a focused vehicle glow, pan/zoom.

**Why:** No map widget exists. **Heavy** — realistically a wrapper over
`QtLocation`/`QWebEngine`+Leaflet/MapLibre, with tile-provider config. Flagged
here for completeness; treat as its own project, not a quick painted widget.
Decide build-vs-document-only separately.

---

## Enhancements to existing widgets (not new widgets)

- **`QCustomDonut` / `QCustomPieChart`:** on-segment **% callout labels** and
  **hatch/pattern fills** (img 3 "Transfer history" — the 30% / 23% / 18%
  labels sit on the arcs, and some segments are hatched). Currently legend-only.
- **`QCustomSparkline`:** a **live/streaming** mode (ring buffer + `push()`) for
  the ECG use-case — may satisfy item 4's line half.

---

## Suggested build order

1. `QCustomRadialGauge` — gauge family (tick/needle/threshold/countdown); now
   demanded by **three** references — promoted to #1.
2. `QCustomHeatmap`
3. `QCustomLiquidGauge` — wavy fuel/level gauge (pairs with the gauge work).
4. `QCustomRulerPicker`
5. `QCustomDateRangePicker` — inline dual-month range calendar.
6. `QCustomWaveform` / `QCustomEqualizer` (+ decide sparkline streaming mode)
7. `QCustomAgendaList`
8. `QCustomBubbleChart`
9. `QCustomCompass` (niche)
10. Donut/Pie callout-label + hatch enhancement
- **Separate track:** `QCustomMapView` (large; decide build vs document-only).

Rationale: the gauge family and heatmap have **zero** current coverage, are core
dashboard surfaces, and are already on the roadmap note. `QCustomLiquidGauge`
rides alongside the gauge work. Bubble chart, compass, and the donut enhancement
are polish; the map is its own project.
