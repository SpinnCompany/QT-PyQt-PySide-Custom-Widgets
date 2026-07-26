# GlassHome — session handoff (2026-07-26)

**READ THIS FIRST in the new session, then build.** The user approved building
the visionOS-style glass smart-home dashboard ("build", reference image below).
The library groundwork is DONE and committed; the app itself is NOT started —
it must be built through the custom-widgets MCP loop (Designer visible, QSS
editor, designer_run_app), which failed to connect in the 2026-07-26 session
(cold-.pyc handshake timeout; caches are pre-warmed now, a fresh session
mounts instantly — verified: stdio handshake 1.9 s).

## State

- **DONE, committed on `feat/tiering-manifest`:**
  - `Custom_Widgets/QCustomGlassFrame.py` — the glassmorphism container
    (blurred-backdrop compositing, tint/grain/border, opt-in liquidEdge,
    liveBackdrop). API doc: `docs/design/dashboard-widgets.md` (bottom
    section). Tests: `tests/test_qcustom_glass_frame.py` (10 pass; full suite
    624 pass). Registered in `Plugins/register.py` (Containers,
    container=True), `.pyi` stubbed.
  - NB: the MCP widget catalog is lru-cached per process — QCustomGlassFrame
    appears in `widgets_catalog`/`render_widget` only after the MCP server
    (re)start, which a fresh session gives you anyway. A NEW widget in the
    Designer palette needs designer_quit → designer_launch.
- **NOT started:** `examples/PySide6/GlassHome` (nothing scaffolded — no
  folder exists yet).

## The reference (visionOS smart-home dashboard)

Full-bleed dusk living-room PHOTO backdrop. Floating over it:

- **Left floating nav rail** — a narrow vertical glass pill, detached from the
  main sheet: 5 icon buttons (dashboard/grid, devices, stats/bars, add,
  automation/tune) + a circular avatar at the bottom.
- **Main glass sheet** — one large rounded glass panel holding everything
  else; its right column is a slightly darker/denser glass than the left area.
  - **Device hero card** (top-left, lighter glass): lamp product image on the
    left; "Device / Luminens LED Modern Standing Lamp" + a small apps
    (4-dot) icon top-right; a stats row "4H 20M — Time Usage" | "72W — Energy
    Consumption" on a darker inset card; two dropdown pills "On from 06:00 PM"
    / "Off at 05:00 AM"; a brightness slider (sun icon, white filled track).
  - **Power Consumption (kWh)** card (top-right of the left area): vertical
    rounded bars Jan–Jun, y-scale 0/50/90/130/170, March highlighted BLUE with
    a "169 kWh" tooltip callout above it; other bars grey.
  - **Three stat cards** (middle row): "Current Consumption — 1,5 kWh",
    "Humidity — 48,2 %", "Temperature — 68° F" (label small, value large).
  - **Four device tiles** (bottom row): Gaabor Humidifier (ACTIVE — lighter
    glass + blue toggle ON), Amazon Echo Speaker (off), Bardi Smart Lamp (ON),
    Xiaomi Camera (off). Each: apps icon top-left, toggle top-right, vendor
    (small, muted) + device name (bold) bottom-left.
  - **Room tabs** (bottom-center, its own glass pill below the sheet):
    Living Room (active, darker pill) · Bedroom · Kitchen · Backyard · Garage
    + a round blue "+" button; page dots underneath.
  - **Right column** (darker glass, full height): "10:02 PM" clock + divider;
    "Thermostat" + toggle; thermostat RING 64° "(°Fahrenheit)" — blue arc on a
    grey track, white handle knob at the arc tip, "−"/"+" round buttons below;
    a 4-button mode row Hot / Eco / Fan / Cold (small glass squares, icon over
    label); music player card: "Ericdoa x Valorant — Greater Than One",
    progress bar 0:34 / 2:27, transport row (repeat, prev, play/pause-circle,
    next, cast).

## Build plan (forms pipeline, granular components)

Follow the MCP agent guide end-to-end (RULE #0 forms pipeline; edits visible in
Designer; QSS in the QSS editor; run via designer_run_app; pass
`project="examples/PySide6/GlassHome"` + an `agent` name on every call).

- **Backdrop**: MainWindow root holds a full-bleed `QLabel` objectName
  `wallpaper` (scaledContents) UNDER everything; load a REAL photo async via
  `Custom_Widgets.load_image` from picsum
  (`https://picsum.photos/seed/glasshome/1600/1000`), gradient fallback
  offline, per [[use-free-online-media]]. When the photo ARRIVES, call
  `refreshBackdrop()` on every glass frame (manager wires the loader callback).
- **Glass panels**: every panel is a `QCustomGlassFrame` with
  `backdropSource="wallpaper"`. Suggested recipe — main sheet: blurRadius 30,
  tint rgba(18,22,32,~120); right column + inset cards: heavier tint
  (~150–170); hero/active tile: LIGHT glass (tint rgba(235,240,250,~90),
  brightness 1.1). `liquidEdge=true, edgeIntensity≈0.4` on the main sheet and
  hero only. Tints come from QSS `qproperty-tintColor` with theme tokens — do
  NOT put a background-color rule on a glass frame (paints over the glass).
- **Component .ui files** (each root = plain QWidget — QFrame root aborts
  setupUi, see [[component-ui-root-and-stale-component]]): `NavRail`,
  `DeviceHero`, `PowerChart`, `StatCard` (one component reused 3× via
  containers, texts set per-instance from the manager), `DeviceTile` (glass
  frame + apps icon + `QCustomSwitch` + vendor/name labels; active state via a
  dynamic property driving tint), `RoomTabs`, `ThermostatPanel`, `ModeRow`,
  `PlayerCard`. Compose in `MainWindow.ui` via `QCustomComponentContainer`
  (filePath → compiled `src/ui/ui_<Name>.py`).
- **Widget mapping** (REUSE, don't hand-paint): thermostat ring =
  `QCustomRadialGauge` ring recipe (`showNeedle=False, showHandle=True,
  roundedCaps=True, zonesCsv=""`, span ≈270° open at the bottom, track grey,
  blue gradient arc — see the recipe in `docs/design/dashboard-widgets.md`);
  power chart = `QCustomMiniBarChart` (`highlightIndex(2, blue)`, labelsCsv
  Jan..Jun, showLabels; the "169 kWh" callout: check if the widget has a
  per-bar callout hook — if not, ADD one as an opt-in prop per
  [[widgets-fully-customizable-rule]], don't overlay a hand-built label);
  toggles = `QCustomSwitch`; brightness = the styled `QSlider` pattern from
  SmartHomeDashboard; player = `QCustomPlayerBar` (RhythmoTune); room tabs =
  `QCustomSegmentedControl` (check pill styling bends far enough — else add
  hooks) + `QCustomPageDots`; mode buttons = 4 small `QCustomTileButton`s in a
  QButtonGroup; nav rail = `QCustomSidebar` collapsed-only or a glass frame of
  icon `QCustomQPushButton`s + `QCustomAvatar`.
- **Icons**: feather/material SVGs via QSS `qproperty-icon:
  url($PATH_RESOURCES+'feather/...')` / `iconName`+`qproperty-iconColor`,
  NEVER setIcon in Python. Lamp product image = QPixmap (large image rule).
- **Theming**: `json-styles/style.json` with TWO CustomThemes — "Glass Dusk"
  (default, the reference) and "Glass Day" (light glass over a bright photo) —
  incl. Other-variables _R/_G/_B triples; scss in `Qss/scss/defaultStyle.scss`
  nested per component objectName; switch BY NAME; glass tints re-assert via
  setProperty on `onThemeChangeComplete` (qproperty live-switch gap).
- **Wiring**: minimal `main.py` → `GuiFunctions` orchestrator + per-panel
  Managers; demo data (device states, chart values, clock QTimer, simulated
  player progress) from managers/workers only.

## Verify

Both themes live via MCP (`designer_run_app` → `app_screenshot`,
`app_object_tree` for real geometry), element-by-element diff against the
reference, plus a pytest offscreen probe for the glass panels over the app's
own wallpaper. Keep runs visible; don't manage windows.
