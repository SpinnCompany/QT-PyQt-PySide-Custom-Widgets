# Missing widgets — gap analysis from dashboard references

**Added:** 2026-07-24 — from a gap analysis of five reference dashboards
(fitness mobile cards, two donut cards, the "Loud" finance dashboard, and a
sentiment bubble chart) against the current catalog.
**Refreshed:** 2026-07-24 (session 2 — cash-flow / green-banking) — see the
Refresh block below.

This is a **backlog / build queue**, not a record of shipped work. Everything
below is *not yet built*. Implement one at a time following the painted-widget
convention (`WIDGET_ICON/TOOLTIP/MODULE/DOM_XML` constants + `__catalog__` +
typed `@Property`s + `valuesCsv`-style Designer inputs + qproperty colours that
tokenise on theme switch), register in `Plugins/register.py`, regenerate stubs,
add a headless paint test + a runnable `examples/PySide6/...` demo. Mirror
`QCustomSparkline` / `QCustomDonut` / `QCustomMiniBarChart`.

See also: [dashboard-widgets.md](dashboard-widgets.md) (the convention these
follow) and the standing "build more data-viz widgets" direction.

---

## 🔄 Refresh — 2026-07-24 (session 2, cash-flow / green-banking)

Re-ran the gap analysis after the CashFlow dashboard session, cross-referencing
**this session's references** (green banking / cash-flow, fitness cards, threat-
level gauges, dual-month calendar, sentiment bubble chart) against the **live
catalog** (`widgets_catalog` — 65 widgets).

**Catalog re-verification — every queue item below is still MISSING.** Confirmed
absent from the 65-widget catalog: `QCustomRadialGauge`, `QCustomHeatmap`,
`QCustomLiquidGauge`, `QCustomRulerPicker`, `QCustomWaveform`/`QCustomEqualizer`,
`QCustomAgendaList`, `QCustomBubbleChart`, `QCustomCompass`, `QCustomMapView`, and
an **inline dual-month** `QCustomDateRangePicker` (only the compact popup
`QCustomDateRangeEdit` exists).

**What the CashFlow session shipped was a *parallel* set — it closed NONE of this
queue.** Shipped: `QCustomDivergingBarChart` (income-up/expense-down cash-flow
bars), `QCustomCardStack` (interactive stacked cards), `QCustomMenu` (popup
menu), `QCustomModal` (centered modal), plus the **remote-font** capability.
Those came from the green-banking reference, which is now **fully covered** and
adds **no new widget** to this backlog (its remaining pieces map to shipped or
existing widgets — KPI → `QCustomStatCard`, activity table → `QCustomDataTable`,
"Total Balance" hero → `QCustomCard`+`QCustomTrendChip` composition per the reuse
rule, stacked cards → `QCustomCardStack`).

**Net:** the ranked queue below stands unchanged and de-duplicated; no new
reference this session introduced a widget the queue didn't already anticipate.
The fitness / threat-gauge / dual-month / bubble references all resolve to
existing queue items (RadialGauge, RulerPicker, Waveform, AgendaList,
DateRangePicker, BubbleChart). See the ranked list at the bottom.

---

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

### 1. ✅ QCustomHeatmap — HIGHEST VALUE — **SHIPPED 2026-07-24**

**Status:** BUILT. `Custom_Widgets.QCustomHeatmap`, registered (Charts group),
`.pyi`-stubbed, 8 headless tests (`tests/test_qcustom_heatmap.py`), `design_lint`
0 errors. `mode="grid"` (rows×cols, e.g. hours×weekdays — the "Activity by time"
reference) + `mode="calendar"` (GitHub year-of-days, flat list wrapped to 7×N).
low→high colour ramp (+`emptyColor` for missing cells), auto-normalise or
`setRange`, row/col labels, Less→More legend, `cellClicked(row,col,value)` +
hover tooltip, **flex cell sizing** (fits the box after labels+legend). See
`dashboard-widgets.md`. Original scope retained below.

<details><summary>Original scope (built)</summary>
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

</details>

---

### 2. ✅ QCustomRadialGauge — gauge family (tick / needle / threshold / countdown) — **SHIPPED 2026-07-24**

**Status:** BUILT. `Custom_Widgets.QCustomRadialGauge`, registered (Progressbars
group), `.pyi`-stubbed, 8 headless tests (`tests/test_qcustom_radial_gauge.py`),
`design_lint` 0 errors. One widget, two looks via **`gaugeStyle`** (`needle` |
`tick`). Verified against the Threat-Level semicircle (needle + zones + status
badge), the `17 Sec` radial-tick timer (gradient ticks + countdown), and a
light-theme threshold gauge. See `dashboard-widgets.md` for the shipped API. The
scope below is retained for reference. **Remaining follow-ups (optional):** a
continuous conical-gradient arc option; a dashed inner guide arc to mirror the
Threat reference exactly.

<details><summary>Original scope (built)</summary>
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

</details>

---

### 2b. ✅ QCustomLiquidGauge — wavy fill level gauge — **SHIPPED 2026-07-24**

**Status:** BUILT. `Custom_Widgets.QCustomLiquidGauge`, registered (Progressbars),
`.pyi`-stubbed, 6 headless tests (`tests/test_qcustom_liquid_gauge.py`),
`design_lint` 0 errors. Circular **or** rounded-rect container with an animated
two-wave sine liquid fill ∝ value (QTimer drift + `animated` level easing),
gradient fill, centre value+suffix (e.g. "3.61 gal" / "72%"), optional status
badge, flex sizing. See `dashboard-widgets.md`. Original scope retained below.

<details><summary>Original scope (built)</summary>
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

</details>

---

### 3. ✅ QCustomRulerPicker — tick-ruler value selector — **SHIPPED 2026-07-24**

**Status:** BUILT. `Custom_Widgets.QCustomRulerPicker`, registered (Input
Widgets), `.pyi`-stubbed, 7 headless tests
(`tests/test_qcustom_ruler_picker.py`), `design_lint` 0 errors. Minor/major ticks
+ numeric labels (current bold), indicator at the value; `centered` (fixed span
vs scrolling picker) × `orientation` (horizontal/vertical); drag / wheel / click,
`snap` to `step`, `unit`, optional big value readout; `valueChanged(float)`.
Capped tick length + centred strip (flex). Verified live via MCP (weight/height/
body-fat/thermostat demo). See `dashboard-widgets.md`. Original scope below.

<details><summary>Original scope (built)</summary>
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

</details>

---

### 4. ✅ QCustomWaveform / QCustomEqualizer — audio bars + ECG line — **SHIPPED 2026-07-24**

**Status:** BUILT as ONE widget `Custom_Widgets.QCustomWaveform` (chose a
standalone widget over a `QCustomSparkline` streaming mode). Registered (Charts),
`.pyi`-stubbed, 7 headless tests (`tests/test_qcustom_waveform.py`), `design_lint`
0 errors. `mode="bars"` (equalizer/audio, `mirror` for voice-message symmetry,
gradient + `glow`) + `mode="line"` (streaming ECG over an optional grid, optional
area fill, `glow`). Feed via `setValues([...])` / `valuesCsv` or stream with
`push(value)` (a `capacity` ring buffer scrolls); `animated` self-runs a demo
(audio levels / a PQRST heartbeat). Verified live via MCP (ECG + equalizer +
voice + neon). See `dashboard-widgets.md`. Original scope below.

<details><summary>Original scope (built)</summary>
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
  enhancement note below). → **DECIDED: separate widget (`QCustomWaveform`).**

</details>

---

### 5. ✅ QCustomAgendaList — schedule / event list — **SHIPPED 2026-07-24**

**Status:** BUILT. `Custom_Widgets.QCustomAgendaList`, registered (Display
Widgets), `.pyi`-stubbed, 5 headless tests (`tests/test_qcustom_agenda_list.py`),
`design_lint` 0 errors. Left connector rail + painted status markers
(done=check / active=filled dot + row highlight / pending=hollow ring — no
glyphs), per-row time range + bold title + muted subtitle. `setItems([{time,
endTime, title, subtitle, status, color}])` / `itemsJson`; `itemClicked(index)` +
hover; flex row height (sits in a QScrollArea). Verified live via MCP. See
`dashboard-widgets.md`. Original scope below.

<details><summary>Original scope (built)</summary>
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

</details>

---

### 6. ✅ QCustomBubbleChart — packed-circle chart — **SHIPPED 2026-07-24**

**Status:** BUILT. `Custom_Widgets.QCustomBubbleChart`, registered (Charts),
`.pyi`-stubbed, 6 headless tests (`tests/test_qcustom_bubble_chart.py`),
`design_lint` 0 errors. Circle **area ∝ value**, packed by a deterministic force
relaxation (push overlaps apart + gravity to centre), then scaled to fill the
widget. Per-category colours (`setCategoryColors`/`categoriesJson`), in-bubble
**elided labels**, optional `groupByCategory` lobes. **Fully interactive** (the
reference has zoom + search): a **custom painted tooltip card** on hover (NOT the
native `QToolTip`) + grow/glow, **zoom/pan** (wheel toward cursor / painted ± /
drag / double-click reset), **search** (`setSearchQuery` dims non-matches +
`searchRequested`), `bubbleClicked(label)`. `setItems([{label, value,
category}])`/`itemsJson`. Verified live via MCP. See `dashboard-widgets.md`.
Original scope below.

<details><summary>Original scope (built)</summary>
**Reference:** the sentiment bubble chart (img 5) — packed circles sized by
value, coloured by category (positive/negative), labelled.

**Why:** Distinctive but niche. Lowest priority of the new widgets.

**Scope:**
- Circle-packing layout of `setItems([{label, value, category}])`; size ∝
  value; per-category colour; label inside when the bubble is large enough.
- qproperties: `padding`, `categoryColors` (map), `showLabels`, min label size
  threshold. Signal: `bubbleClicked(label)`.
- Circle-packing is the real work — a simple force/greedy pack is fine to start.
- **Hover interactivity (added on feedback):** `bubbleClicked` + a hover
  **tooltip** (label · value · category), a **grow** animation and a **glow** on
  the hovered bubble (`hoverGlow`, `hoverScale`).

</details>

---

### 7. ✅ QCustomDateRangePicker — inline dual-month range calendar — **SHIPPED 2026-07-24**

**Status:** BUILT. `Custom_Widgets.QCustomDateRangePicker`, registered (Input
Widgets), `.pyi`-stubbed, 7 headless tests
(`tests/test_qcustom_date_range_picker.py`), `design_lint` 0 errors. N months
side by side (`monthsVisible`, responsive stack), painted **in-range band**
(rounded at range ends + each week wrap) + green endpoint circles, today marker,
painted chevron month-nav, click start→end selection, `setSelectableRange`
min/max, `rangeChanged(QDate,QDate)`. Verified live via MCP (travel-dates demo:
nav + selection + band + Start/End fields). See `dashboard-widgets.md`. Original
scope below.

<details><summary>Original scope (built)</summary>
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

</details>

---

### 8. ✅ QCustomCompass — heading / compass rose — **SHIPPED 2026-07-24**

**Status:** BUILT. `Custom_Widgets.QCustomCompass`, registered (Display Widgets),
`.pyi`-stubbed, 7 headless tests (`tests/test_qcustom_compass.py`), `design_lint`
0 errors. Tick ring + N/E/S/W (+ intercardinals), two-tone needle, centre 16-point
readout (auto-**fit-to-hub** text) + degrees. `rotateBezel` (needle rotates vs the
rose spins), `animated` shortest-path ease, **drag to set heading**,
`headingChanged(float)`. Text boxes are **sized to the measured string** so
2-letter labels never truncate (the calculate-text-to-fit rule). Verified live via
MCP. See `dashboard-widgets.md`. Original scope below.

> **Bonus — `QCustomCompassDial`** (2026-07-24): a **premium beveled** instrument
> sibling (the Haulix map dial — metal rim + domed face + brass ticks + metallic
> cap), built as a SEPARATE widget so the flat `QCustomCompass` stays untouched
> (user pref: add a variant, don't change a shipped widget). 7 tests, lint clean.

<details><summary>Original scope (built)</summary>
**Reference:** the "NW" compass rose in the Haulix map (top-right).

**Why:** Niche, but no heading indicator exists. Cheap to paint.

**Scope:** painted rose (N/E/S/W + intercardinals), rotating needle/bezel,
`heading` (0–360°) qproperty, `cardinalText`, `headingChanged`. Low priority.

</details>

---

### 9. 📄 QCustomMapView — map surface (DECISION: DOCUMENT-ONLY, its own project)
**Reference:** the Haulix operations map — vehicle markers, a highlighted route
polyline, a focused vehicle glow, pan/zoom.

**DECIDED 2026-07-24 — document-only, build as its own project when prioritized.**
It is NOT a painted widget: it needs a mapping engine (`QtLocation` **or**
`QWebEngine` + MapLibre/Leaflet), tiles, a provider + API keys + attribution/ToS,
and a live GL/WebEngine context to test — bundling it would bloat and fragilise
the core LGPL library. Full plan (why-not-core, engine trade-offs, the
engine-agnostic `QCustomMapView` facade API, packaging as an optional
`custom-widgets[map]` extra + `examples/PySide6/MapView`, and reusing the shipped
painted widgets — CompassDial / zoom control / popovers — as the map chrome):
**[qcustommapview-project-plan.md](qcustommapview-project-plan.md).**

---

## Enhancements to existing widgets (not new widgets)

- ✅ **`QCustomDonut` on-segment % callouts + hatch fills — SHIPPED 2026-07-24.**
  Opt-in (segments mode, default OFF so the classic look is unchanged):
  `showPercentLabels` draws a `%` pill on each arc (`percentLabelColor`,
  `percentPill`, `percentPillColor`, `minLabelPercent` to hide tiny slices), and
  `hatchCsv` (+ `hatchPattern` bdiag/fdiag/cross/…) renders chosen segment
  indices with a hatch over a dim base (`setHatchIndices`/`setShowPercentLabels`).
  Matches the "Transfer history" reference. 6 tests
  (`tests/test_qcustom_donut_enhance.py`), lint 0-err. (`QCustomPieChart` still
  legend-only — enhance separately if needed.)
- **`QCustomSparkline`:** a **live/streaming** mode (ring buffer + `push()`) for
  the ECG use-case — may satisfy item 4's line half.

---

## Suggested build order

1. ~~`QCustomRadialGauge`~~ — **✅ SHIPPED 2026-07-24** (needle + tick, zones,
   status badge, countdown, glow, flex).
2. ~~`QCustomHeatmap`~~ — **✅ SHIPPED 2026-07-24** (grid + calendar, ramp,
   labels, legend, cellClicked, flex).
3. ~~`QCustomLiquidGauge`~~ — **✅ SHIPPED 2026-07-24** (wavy fill disc/rect,
   gradient, badge, animated, flex).
4. ~~`QCustomRulerPicker`~~ — **✅ SHIPPED 2026-07-24** (fixed/centered ×
   h/v, ticks+labels, drag/wheel/click, snap, flex).
5. ~~`QCustomDateRangePicker`~~ — **✅ SHIPPED 2026-07-24** (inline N-month range
   band, endpoints, nav, min/max, rangeChanged).
6. ~~`QCustomWaveform` / `QCustomEqualizer`~~ — **✅ SHIPPED 2026-07-24**
   (bars + streaming ECG line, push() ring buffer, mirror, glow, animated).
7. ~~`QCustomAgendaList`~~ — **✅ SHIPPED 2026-07-24** (rail + done/active/pending
   markers, time+title+subtitle rows, itemClicked, flex).
8. ~~`QCustomBubbleChart`~~ — **✅ SHIPPED 2026-07-24** (force-packed circles,
   category colours, elided labels, hover tooltip/grow/glow, bubbleClicked).
9. ~~`QCustomCompass`~~ — **✅ SHIPPED 2026-07-24** (rose, two-tone needle,
   rotate-bezel, 16-pt fit-to-hub readout, drag-to-set, headingChanged).
   **→ the whole painted-widget backlog is now built; only MapView remains.**
10. Donut/Pie callout-label + hatch enhancement
- **Separate track:** ~~`QCustomMapView`~~ — **DECIDED: document-only, its own
  project** (see [qcustommapview-project-plan.md](qcustommapview-project-plan.md)).
  **The entire painted-widget backlog is now shipped.**

Rationale: the gauge family and heatmap have **zero** current coverage, are core
dashboard surfaces, and are already on the roadmap note. `QCustomLiquidGauge`
rides alongside the gauge work. Bubble chart, compass, and the donut enhancement
are polish; the map is its own project.
