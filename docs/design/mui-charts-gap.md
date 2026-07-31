# Chart gap analysis — MUI X Charts

**Added:** 2026-07-31. Source: <https://mui.com/x/react-charts/> (shipped and
planned lists) plus <https://mui.com/x/react-charts/candlestick/>.

Reference target for the charts subsystem. This is a **build queue**, not a
record of shipped work — except where a row is explicitly marked SHIPPED.

---

## THE CONSTRAINT — read before building any chart

**Qt Charts is GPLv3-or-commercial. There is no LGPL option**
(<https://doc.qt.io/qt-6/qtcharts-index.html>).

18 modules in this repo import it, including **all four Charts Pro anchors**
(`QCustomAreaChart`, `QCustomBarChart`, `QCustomLineChart`, `QCustomPieChart`).
Consequences:

- Charts Pro **cannot ship as a proprietary wheel** built on those anchors
  without a commercial Qt licence.
- The planned GPLv3 -> LGPLv3 relicense of the core **does not rescue anything
  chart-related**, because the encumbrance is Qt's, not ours.

**Therefore: every new chart is written with `QPainter` only, no QtCharts.**
That keeps it eligible for a proprietary wheel and matches Pro's existing
"only original code" rule. `QCustomCandlestickChart` carries a test asserting
its import graph stays QtCharts-free; new charts should do the same.

Existing painted, unencumbered charts to mirror: `QCustomSparkline`,
`QCustomDonut`, `QCustomBubbleChart`, `QCustomHeatmap`, `QCustomRadialGauge`,
`QCustomLiquidGauge`, `QCustomCandlestickChart`.

---

## Coverage against MUI's shipped charts

| MUI chart | Ours | Status |
|---|---|---|
| Bar | `QCustomBarChart`, `QCustomMiniBarChart`, `QCustomDivergingBarChart` | covered (QtCharts-encumbered) |
| Line | `QCustomLineChart`, `QCustomSparkline` | covered (Sparkline is clean) |
| Area | `QCustomAreaChart` | covered (QtCharts-encumbered) |
| Pie / Donut | `QCustomPieChart`, `QCustomDonut` | covered (Donut is clean) |
| Scatter | — | **MISSING** |
| Sparkline | `QCustomSparkline` | covered, clean |
| Gauge | `QCustomRadialGauge`, `QCustomLiquidGauge`, `AnalogGaugeWidget` | covered, clean |
| Radar | `QCustomRadarChart` | **SHIPPED 2026-08-01**, clean — the first polar chart in the catalog |
| Heatmap | `QCustomHeatmap` | covered, clean |
| Funnel | — | **MISSING** |
| Pyramid | — | **MISSING** (a flipped funnel; build with Funnel) |
| Sankey | — | **MISSING** — the largest of these by far |
| Range Bar | — | **MISSING** |
| Candlestick | `QCustomCandlestickChart` | **SHIPPED 2026-07-31**, clean |
| Radial Bars | — | **MISSING** |
| Radial Lines | — | **MISSING** |
| Map | — | **MISSING** — already on the backlog as `QCustomMapView`; needs a
mapping engine, not a painter, so it is not comparable to the rest |

### Where we are ahead

MUI lists these as *planned, not shipped*; we already have them:
`QCustomBubbleChart`, `QCustomGanttChart`. Their remaining planned set
(Treemap, Waterfall, Boxplot, Sunburst, Chord, Polar Line, Range Area, Linear
Gauge, OHLC, 3D) is a **second-tier queue** — worth revisiting once the shipped
list above is closed, since matching a competitor's roadmap is lower value than
matching what they actually ship.

---

## Suggested build order

Cheapest-to-hardest, and front-loading the ones that are also the most commonly
requested:

1. ~~**`QCustomRadarChart`**~~ — **SHIPPED 2026-08-01.** Polar grid, N axes,
   filled polygon per series, polygon/circle grids, ring labels on the axis
   bisector. Its polar mapping (`_angleFor` / `_pointAt`) is what Radial Bars
   and Radial Lines should reuse rather than re-deriving.
2. **`QCustomScatterChart`** — the most conspicuous absence for a general chart
   library; x/y axes already need writing for it and Radar can share nothing,
   so do it second while the axis code is fresh.
3. **`QCustomFunnelChart`** (+ `pyramid` mode as a property, not a second
   widget — same geometry inverted).
4. **`QCustomRangeBarChart`** — a bar with two bounds; reuses candlestick's
   body geometry closely.
5. **`QCustomRadialBars`** / **`QCustomRadialLines`** — build together, they
   share the polar mapping written for Radar.
6. **`QCustomSankey`** — flow layout + link routing; genuinely hard, do last.

`QCustomMapView` stays on its own track (engine decision: QtLocation vs tiles).

---

## Improving the existing charts

- ~~All four Charts Pro anchors lack `__catalog__` and `.pyi`~~ — **DONE
  2026-08-01.** Catalogs are generated from each class's metaObject and a test
  asserts the two never drift.
- ~~The QtCharts charts cannot be authored in Designer~~ — **DONE 2026-08-01.**
  They published 27-37 styling properties but no way to put data in them, so a
  form author got a fully styled empty chart. `ChartDataProps` adds `seriesCsv`
  and `categoriesCsv` in the same convention the painted charts use.
  `WIDGET_MODULE` was also the package rather than the module on all four,
  which made Designer write a coarse header and collapsed every generated stub
  onto one path.

Still open:

- **A shared painted axis/scale helper does not exist.** Scatter and Range Bar
  both need one; writing it once (ticks, nice-number rounding, label thinning)
  avoids divergent implementations. `QCustomCandlestickChart` has a minimal
  version inline that should be extracted when the second consumer arrives.
  Radar did **not** need it — a polar chart has no cartesian axis — so the
  first real consumer is Scatter.
- **The polar mapping in `QCustomRadarChart`** (`_angleFor` / `_pointAt`) is
  the piece Radial Bars and Radial Lines should reuse. Extract it when the
  second consumer arrives rather than speculatively.
