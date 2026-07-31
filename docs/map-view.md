# QCustomMapView — the optional map extra

```bash
pip install QT-PyQt-PySide-Custom-Widgets[map]
```

```python
from Custom_Widgets.map import QCustomMapView

view = QCustomMapView()
view.loadDefaultEngine()                     # QtLocation + OSM, no API key
view.setCenter(-1.286389, 36.817223)
view.setZoom(13)
view.addMarker("truck-1", -1.283, 36.812, label="KBZ 123A", color="#dc2626")
view.setRoute("leg-1", [(-1.283, 36.812), (-1.292, 36.826)], width=5)
view.focusMarker("truck-1")
```

---

## Why it is an extra and not a core widget

[qcustommapview-project-plan.md](design/qcustommapview-project-plan.md) decided
this in 2026-07: a map needs a mapping engine, tile providers, API keys and
provider ToS — config, secrets and legal surface an LGPL widget library should
not carry. Nothing in the core imports `Custom_Widgets.map`, and a test
enforces that, so users who never want a map pay nothing for it.

## Engine

The shipped backend is **QtLocation** (QML `Map` in a `QQuickWidget`), not the
plan's original MapLibre/QWebEngine suggestion. QtLocation ships with Qt, needs
no Chromium (~100 MB saved) and no API key to get started.

The facade is engine-agnostic on purpose. A WebEngine backend can be dropped in
later by implementing the same handful of methods (`setCenter`, `setZoom`,
`addMarker`, `setRoute`, `focusMarker`, …) — no application code changes.

## ⚠ Tiles, API keys and attribution

**The default tiles carry an "API Key Required" watermark.** QtLocation's `osm`
plugin proxies through Thunderforest, which wants a key. That is not a bug in
this widget and it is exactly the provider surface the plan warned about.

Your options, all of which keep the key in *your* config and never in this
library:

```python
# 1. Your own tile server (the production answer)
view.setTileProvider("osm", **{
    "osm.mapping.custom.host": "https://tiles.example.com/",
    "osm.mapping.copyright": "© Example",
})

# 2. A different style the provider offers
view.mapStyles()        # ['Street Map', 'Cycle Map', 'Transit Map', …]
view.setMapStyle(2)

# 3. A provider that takes a key
view.setTileProvider("mapbox", **{"mapbox.access_token": TOKEN})
```

`mapStyles()` returns `[]` until the provider resolves them, which is
asynchronous — read it again after the map has drawn once.

**Attribution is not optional.** OSM tiles require it and are subject to the
[OSMF tile usage policy](https://operations.osmfoundation.org/policies/tiles/).
QtLocation renders the attribution itself; do not suppress it, and do not point
this at a bulk tile scrape.

## API

| Call | Notes |
|---|---|
| `setCenter(lat, lon)` / `center()` | latitude **clamps** to ±85.05° (Web-Mercator); longitude **wraps** |
| `setZoom(z)` / `zoom()` / `zoomIn()` / `zoomOut()` | clamped to 0–20 |
| `fitMarkers(padding=0.15)` | centre + zoom to contain every marker |
| `addMarker(id, lat, lon, label=, color=, heading=, icon=)` | same id replaces |
| `updateMarker(id, lat=, lon=, **style)` | moves/restyles in place |
| `removeMarker(id)` / `clearMarkers()` / `marker(id)` / `markers()` | |
| `focusMarker(id, glow=True, recenter=True)` | highlights; clears if removed |
| `setRoute(id, points, color=, width=)` | polyline; same id replaces |
| `removeRoute(id)` / `clearRoutes()` / `route(id)` / `routes()` | |
| `setTileProvider(name, **options)` | options become plugin parameters |
| `mapStyles()` / `setMapStyle(index)` | provider styles |
| `loadDefaultEngine()` | raises `MapEngineUnavailable` with the reason |
| `attachEngine(engine)` | replays current state into a custom backend |

Signals: `centerChanged(float, float)`, `zoomChanged(float)`,
`markerClicked(str)`, `engineFailed(str)`.

Qt properties for Designer: `latitude`, `longitude`, `zoomLevel`,
`tileProviderName`, `interactive`.

## Testing

The facade holds all the state and the engine only renders it, so the state is
testable with no engine at all — `tests/test_qcustom_map_view.py` runs 34 cases
headlessly. Only two of them need a live QtLocation, and they skip cleanly when
it is missing.

That split is what makes the widget verifiable. The project plan said a map
"can't be verified by an offscreen `grab()` pixel probe" — true of the engine,
not of the state, provided the two are not tangled together.

## Troubleshooting

- **Blank widget** — call `loadDefaultEngine()`; without an engine the facade
  stores state but draws nothing. It raises `MapEngineUnavailable` with the
  reason rather than failing silently, and `showPlaceholder(msg)` puts that
  reason on screen.
- **"API Key Required" across the tiles** — see the section above.
- **`mapStyles()` returns `[]`** — the provider has not resolved yet; read it
  again after the first paint.
- **Markers near the poles look wrong** — latitude is clamped to ±85.05°,
  which is the Web-Mercator limit, not a bug.
