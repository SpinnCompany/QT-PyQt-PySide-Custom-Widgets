# GlassHome — visionOS-style glass smart-home dashboard

A full glassmorphism dashboard: every panel is a `QCustomGlassFrame` sampling a
full-bleed wallpaper photo (`backdropSource="wallpaper"`) — real blurred-backdrop
glass, not translucent fills. Built the CORRECT Custom_Widgets way (forms
pipeline, granular components, token themes) via the custom-widgets MCP.

```
ui/*.ui                 granular component forms (NavRail, DeviceHero, PowerChart,
                        StatCard ×3, DeviceTile ×4, RoomTabs, ThermostatPanel,
                        ModeRow, PlayerCard) composed in MainWindow.ui via
                        QCustomComponentContainer
src/ui_*.py             compiled (Custom_Widgets --convert-ui / project_convert_ui)
json-styles/style.json  "Glass Dusk" (default) + "Glass Day" CustomThemes; glass
                        tints & panel colours as Other-variables (#AARRGGBB)
Qss/scss/chrome.scss    ALL chrome — glass qproperty-tintColor tints, icons via
                        qproperty-icon/qproperty-pixmap urls, role-based type
gui/GuiFunctions.py     per-panel managers: wallpaper async load (picsum) +
                        refreshBackdrop fanout, live clock, thermostat ± ,
                        device-tile active state, player progress sim
```

Key patterns proven here:
- Glass panels are tinted from QSS (`qproperty-tintColor: $GLASS_SHEET`) —
  never a `background-color` rule (it would paint over the glass).
- Component containers on glass need `WA_TranslucentBackground` (the native
  holder otherwise paints the palette — see GuiFunctions).
- Theme flips BY NAME (`themeEngine.setTheme("Glass Day")` — click the nav
  avatar) + a full repolish on `onThemeChangeComplete` so qproperty colours
  re-land live.
- Widget hooks added for this reference: QCustomMiniBarChart
  `calloutText`/`yLabelsCsv`, QCustomPlayerBar `compactMode` (see
  docs/design/dashboard-widgets.md).

Run: `python main.py` (or `designer_run_app` via the MCP).
Probe: `tests/test_glasshome_example.py` (offscreen glass-over-wallpaper).
