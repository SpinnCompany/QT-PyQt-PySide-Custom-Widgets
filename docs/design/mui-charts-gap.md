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
| Scatter | `QCustomScatterChart` | **SHIPPED 2026-08-01**, clean |
| Sparkline | `QCustomSparkline` | covered, clean |
| Gauge | `QCustomRadialGauge`, `QCustomLiquidGauge`, `AnalogGaugeWidget` | covered, clean |
| Radar | `QCustomRadarChart` | **SHIPPED 2026-08-01**, clean — the first polar chart in the catalog |
| Heatmap | `QCustomHeatmap` | covered, clean |
| Funnel | `QCustomFunnelChart` | **SHIPPED 2026-08-01**, clean |
| Pyramid | `QCustomFunnelChart` (`shape="pyramid"`) | **SHIPPED 2026-08-01** — a mode, not a second widget |
| Sankey | `QCustomSankey` | **SHIPPED 2026-08-01**, clean |
| Range Bar | `QCustomRangeBarChart` | **SHIPPED 2026-08-01**, clean |
| Candlestick | `QCustomCandlestickChart` | **SHIPPED 2026-07-31**, clean |
| Radial Bars | `QCustomRadialBars` | **SHIPPED 2026-08-01**, clean |
| Radial Lines | `QCustomRadialLines` | **SHIPPED 2026-08-01**, clean |
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

## Build order — COMPLETE

Every painted chart on MUI's shipped list is now built, all QPainter-only:

| Widget | Notes |
|---|---|
| `QCustomCandlestickChart` | 2026-07-31 |
| `QCustomRadarChart` | first polar chart; owns the polar mapping |
| `QCustomScatterChart` | first consumer of the shared `_chart_axis` ticks |
| `QCustomFunnelChart` | pyramid is a `shape` mode, not a second widget |
| `QCustomRangeBarChart` | floating bars, shares the axis helper |
| `QCustomRadialBars` | activity rings |
| `QCustomRadialLines` | polar line chart for cyclical data |
| `QCustomSankey` | flow layout derived from a bare link list |

Shared infrastructure, extracted only when a second consumer appeared:
`_chart_axis.py` holds nice-number ticks, tick formatting and label thinning
(Candlestick + Scatter + Range Bar) plus the polar mapping (Radar + both
radial charts). Writing "nice ticks" or "where does slot i sit on a circle"
three times is how charts start disagreeing with each other.

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

- **`QCustomMapView`** — the only unbuilt item from MUI's shipped list. Needs a
  mapping engine (QtLocation or a tile client), not a painter, so it is a
  different kind of job from everything above and stays on its own track.
- **The QtCharts anchors remain encumbered.** They are now fully
  Designer-authorable, but that does not change the licensing: Area, Bar, Line
  and Pie still cannot ship in a proprietary wheel. The painted set above is
  the clean alternative, and between Candlestick, Scatter, Radar, Funnel,
  Range Bar, the radial pair and Sankey there is now enough unencumbered
  surface to build Charts Pro without QtCharts at all — worth deciding
  deliberately rather than by default.
