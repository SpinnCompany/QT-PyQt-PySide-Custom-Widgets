# QCustomMapView — project plan (its own track, NOT a core painted widget)

**Added:** 2026-07-24. **Status:** DOCUMENTED — decided to build as its own
project when prioritized, *not* as a painted widget in the core library.
Reference: the Haulix operations map (vehicle markers, a highlighted route
polyline, a focused-vehicle glow, pan/zoom, a compass + zoom/layer controls).
This is backlog item #9's "separate track" from
[missing-widgets-from-references.md](missing-widgets-from-references.md).

## Why it is NOT a core `QCustom*` painted widget

Every other backlog widget (RadialGauge … CompassDial) is **self-painted with
QPainter** — no external data, no network, crisp at any size, drops into the
Designer palette. A real map is a different animal:

- **It needs map DATA + tiles** — a tile provider (raster XYZ or vector), tile
  fetching/caching, projection (Web-Mercator), and pan/zoom/rotate math. That is
  a mapping engine, not a paint routine.
- **Heavy dependencies** — realistically `QtLocation`/`QtPositioning` (QML `Map`)
  **or** `QWebEngineView` + a JS map lib (Leaflet / MapLibre GL). Both are large,
  platform-sensitive, and pull in extra wheels — the opposite of the
  zero-dependency painted widgets. `QtWebEngine` alone is ~100 MB and is not
  available on every Qt build.
- **Network + keys + licensing** — tiles come from a provider (OSM, MapTiler,
  Mapbox, Google) with **API keys, usage limits, attribution and ToS**. That is
  config + secrets + legal surface the core LGPL library should not carry.
- **Different testing story** — can't be verified by an offscreen `grab()` pixel
  probe; needs a live GL/WebEngine context and network (or mocked tiles).

Bundling this into the core library would bloat it, add fragile deps, and drag in
provider licensing — so it lives on its own.

## Recommended shape — a separate project / optional extra

Ship it as **`examples/PySide6/MapView`** (a reference app) and/or an **optional
package** `custom-widgets-map` that depends on the core library, so users who
don't need a map never pay for the deps. `pip install custom-widgets[map]`
(extras) is the clean packaging.

Two viable engines (pick one; both wrap to the same `QCustomMapView` API):

| Engine | Pros | Cons |
|---|---|---|
| **QtLocation** (QML `Map` in a `QQuickWidget`) | native Qt, vector/raster, gestures built-in, no browser | QML bridge, plugin/provider setup, patchy across Qt builds |
| **QWebEngineView + MapLibre GL / Leaflet** | best-in-class maps, huge ecosystem, easy styling | ships Chromium (~100 MB), JS↔Py bridge via `QWebChannel`, heavier |

**Recommendation:** prototype with **MapLibre GL in `QWebEngineView`** (free
vector tiles, no Mapbox token, modern styling incl. dark themes to match the
dashboards), behind a thin Python facade so the engine can be swapped for
QtLocation later without changing app code.

## Proposed API (facade, engine-agnostic)

```python
map = QCustomMapView()
map.setTileProvider("maplibre-dark", apiKey=...)      # or "osm", "maptiler", …
map.setCenter(lat, lon); map.setZoom(12)
map.addMarker(id, lat, lon, icon=…, color=…, label=…, heading=…)   # vehicle
map.setRoute(id, [(lat, lon), …], color=…, width=…)                # polyline
map.focusMarker(id, glow=True)                        # highlighted vehicle
map.fitBounds([...])
# signals: markerClicked(id), mapClicked(lat, lon), regionChanged(bounds), ready()
```

Chrome that CAN be core painted widgets, composited **over** the map surface (so
the map stays a thin data layer): the zoom ± / layers / recenter controls, the
**`QCustomCompassDial`** heading rose, vehicle info popovers (a custom tooltip
card / `QCustomPopover`), the status pills. Reuse what we already shipped.

## Decision & next step

- **Now:** documented (this file). Not built — it is not a painted widget and
  would bloat/fragilise the core library.
- **When prioritized:** spin up `examples/PySide6/MapView` as its own project
  (own `.mcp.json`, own optional deps), prototype the MapLibre-in-WebEngine
  engine behind the `QCustomMapView` facade, and composite the existing painted
  widgets (CompassDial, zoom control, popovers) as the map chrome.
- Keep tile-provider keys/attribution/ToS out of the core repo; put them in the
  map project's config.

See also: [missing-widgets-from-references.md](missing-widgets-from-references.md)
(the rest of the backlog — all shipped) and
[dashboard-widgets.md](dashboard-widgets.md).
