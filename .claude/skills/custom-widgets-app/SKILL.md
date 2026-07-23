---
name: custom-widgets-app
description: >-
  Build a REAL Custom_Widgets application the correct, maintainable way — the
  forms pipeline (.ui + compiled src/ + json-styles themes + Qss/scss $TOKENS +
  GuiFunctions managers + background workers). Use this for any production-shaped
  app, dashboard, or multi-page tool. NOT the quick pure-code token demo (that is
  custom-widgets-demo). Mirrors examples/PySide6/AuroraDeckPro and
  examples/PySide6/WinningDashboard_CorrectArchitecture.
---

# Building a real Custom_Widgets app (the forms pipeline)

## ⛔ RULE #1 — MCP first (unchanged)
Mount the `customwidgets` MCP and read its agent guide + skills BEFORE anything.
Drive Designer / QSS editor / run through the MCP when it is connected. Only if
the MCP is genuinely unreachable in the session, fall back to the CLI below —
never silently pretend the MCP path doesn't exist.

## ⭐ RULE #0 — the pipeline IS the product; do NOT ship a pure-code app
The library's value is `.ui` forms + QSS/SCSS + JSON theming + component/manager
composition — that is what makes an app maintainable. A single hand-built
`main.py` full of hard-coded hex is a FAILURE for a production build, even if it
looks right. Real apps look like `examples/PySide6/AuroraDeckPro`:

```
ui/*.ui            hand/Designer-authored forms (structure + objectNames only)
  -> src/ui_*.py   compiled  (Custom_Widgets --convert-ui)
json-styles/style.json   CustomThemes (colours) — NEVER hard-code hex in code/.ui
Qss/scss/*.scss    chrome via $TOKENS + objectName/[role] selectors
gui/GuiFunctions.py  orchestrator + one Manager per page + background workers
main.py            minimal boot
```

## Golden build loop (no live MCP)
```bash
# 1. scaffold: copy the structure of examples/PySide6/AuroraDeckPro (Qss/ has the
#    icons _icons.qrc + scss skeleton). Keep _styles.scss / _variables.scss —
#    they are GENERATED; only write chrome.scss / defaultStyle.scss.
# 2. compile forms after EVERY .ui edit:
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
#    (also: --new-ui NAME to scaffold a form with the icons qrc; --create-project)
# 3. run + verify offscreen, screenshot BOTH themes, read the PNGs back:
QT_QPA_PLATFORM=offscreen .venv/bin/python driver.py --shots DIR
```

## Boot sequence (main.py) — copy verbatim
```python
from Custom_Widgets.Project import setProjectRoot; setProjectRoot(__file__)
from Custom_Widgets import *                      # QCustomMainWindow, loadJsonStyle, enable_hot_reload
from Custom_Widgets.QAppSettings import QAppSettings
class MainWindow(QCustomMainWindow):
    def __init__(self): QCustomMainWindow.__init__(self); enable_hot_reload(self, self.build)
    def build(self):
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow(); self.ui.setupUi(self)
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})
        self.show()
        QAppSettings.updateAppSettings(self)       # AFTER show(): icons + compile scss + paint
        self.gui = GuiFunctions(self); self.gui.initialize()
```

## Composition & navigation
- ONE `QCustomQMainWindow`. Every screen is a `QCustomComponent` (`.ui` root
  class), embedded via a `QCustomComponentContainer` whose `filePath` points at
  `ui/<Name>Component.ui` (`previewComponent=false`). Reach it in code with
  `container.component`.
- Route with `QCustomQStackedWidget` (`slideTransition`). `navigateTo(name)`
  switches BY WIDGET (`setCurrentWidget`), never by index; marks the active
  sidebar button; lazy-inits that page's Manager (`onShown`).
- Nav = `QCustomSidebar` + `QCustomSidebarButton` (`labelText`, not `text`) +
  `QCustomSidebarLabel` for section headers.

## Theming (token-driven, flips at runtime)
- `style.json` → `QSettings.ThemeSettings.CustomThemes[]`: each has
  `Background-color`, `Text-color`, `Accent-color`, `Icons-color`. The generator
  derives `$COLOR_BACKGROUND_1..6`, `$COLOR_TEXT_1..4`, `$COLOR_ACCENT_1..4` (+
  `_R/_G/_B` triples). **Dark theme: `BG_1` is DARKEST, higher numbers get
  LIGHTER** → window `BG_1`, sidebar `BG_2`, panels/cards `BG_3`. `CT_1` = text,
  higher = more muted. `CA_1` = accent.
- `Qss/scss/chrome.scss`: `$TOKENS` only, `objectName` / `[role="…"]` selectors.
  NEVER hard-code hex. NEVER edit `_variables.scss` (generated) or `_styles.scss`.
- **Switch themes BY NAME**: `themeEngine = getattr(win,"themeEngine",None);
  themeEngine.setTheme("My Dark"/"My Light")`. The generic Light/Dark toggle
  never matches a CUSTOM theme name (icon recolour would fall back to default).
  Recolour code widgets on `themeEngine.onThemeChangeComplete` (icon regen is
  async on a worker thread).
- Extra chart hues (multi-accent) don't fit the single Accent-color: put a custom
  `ChartPalette` section (theme-name → colours) in `style.json` and read it in
  code (`json.load`), so hues still live with the theme and flip on switch.

## Charts & data
- Charts are configured in Managers (code), not in the `.ui` (you can't set series
  in Designer). Promote them in the form (`QCustomBarChart` /`QCustomAreaChart`/
  `QCustomLineChart`, header `Custom_Widgets.QCustomCharts.<Cls>`); the Manager
  sets series/colours after load, coloured from the ChartPalette.
- Background data = **Worker→Signal→GUI**: a `QObject` worker `moveToThread(QThread)`,
  emits signals only, never touches widgets. Stop it on `QApplication.aboutToQuit`.

## GOTCHAS (hard-won — each cost real debugging)
1. **Qt QColor hex is `#AARRGGBB`, not `#RRGGBBAA`.** A faint white grid is
   `"#14ffffff"` (alpha 0x14) — `"#ffffff14"` is parsed as opaque yellow.
2. **Token widgets (QCustomBadge, …) need `applyDesignTokens` for their variant
   QSS.** A `loadJsonStyle` app does NOT call that, so badges render as plain
   text — style them inline (or add `[variant="…"]` QSS) in the Manager.
3. **`QCustomPieChart` collapses to a hairline ring in small/constrained panels**
   (a QtCharts pie-sizing quirk). For dashboard donuts use the painted
   **`QCustomDonut`** widget instead (crisp at any size). The pie is fine at large
   sizes; its rebuild-blank bug (animated remove/re-add) is fixed — `updateChart`
   now rebuilds with animation suppressed, and `addSeries(colors=[…])` /
   `setSliceColors()` are the rebuild-safe colour APIs.
4. **Sidebar collapse**: wire the toggle ONCE (`sidebarToggle.clicked.connect(
   sidebar.toggleMenu)`), or rely on `toggleButtonName`. A disconnect bug in
   `QCustomSlideMenu.activateMenuButton` (connected a lambda, disconnected the
   bound method) used to stack connections so an even count made a click
   toggle-and-untoggle — now fixed, but explicit single-wire is safest.
5. **QSettings persists the theme across runs.** For a deterministic default
   (e.g. dark) on a fresh demo, clear
   `~/.config/<Org>/<App>.conf`. `Default-Theme:true` only governs first run.
6. **`QCustomSidebarLabel` section headers**: use `$COLOR_TEXT_3` (not `_4`) or
   they're invisible in dark mode.
7. Fixed `min==max` width on the sidebar does NOT block collapse (the slide menu
   animates min+max), but keep the sidebar's `collapsedWidth`/`expandedWidth` set.
8. Custom widgets in a `.ui` MUST take `parent` as the first ctor arg (library
   widgets already do). Native container widgets (`QWidget native="true"`) whose
   layout you fill from code need an explicit layout in the `.ui`.

## New library widgets available (use them)
- `QCustomSparkline` — axis-less trend line (values, lineColor, fill, smooth).
- `QCustomDonut` — painted radial chart, crisp at any size. `mode="rings"`
  (default) = CONCENTRIC gauge rings (one per value, outer = largest, each over a
  faint `trackColor`, `maxSweep` degrees); `mode="segments"` = classic single
  split donut. `setData(values, colors)`, `setTrackColor`, `holeRatio`, `maxSweep`.
- `QCustomBarChart.setBarCornerRadius(px)` — rounded-top bars.
- `QCustomBarChart.setGridLineColor(c, alpha=)` / `setGridLineAlpha(a)`.

## Verify before done
Offscreen run + screenshot BOTH themes (read PNGs back). Functional checks driving
real signals: sidebar collapse (width 230→collapsed), nav exclusivity, worker
`tick` updating a KPI, theme round-trip recolouring charts. Fix what the PNG shows.
