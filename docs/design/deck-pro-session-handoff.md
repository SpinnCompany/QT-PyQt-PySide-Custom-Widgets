# Deck Pro — session handoff (2026-07-23, session 2)

Continuity for the next MCP-mounted session. Everything here is committed on
`feat/qcustom-datatable` (per the commit-locally rule; nothing pushed).

## ⚠️ FIRST: the MCP has been remounted at a dedicated folder — RESTART REQUIRED

This session discovered that the `custom-widgets` MCP was pinned to the **repo
root** (its Run/QSS-editor/convert all target `projectRoot`, fixed at mount
time; the Designer "UI Workspace" dock showing `examples/svg_icons_demo` was
only that panel's cosmetic browse folder). Switching Designer's workspace
mid-session rebinds the bridge socket and disconnects the MCP, so a workspace
change is impossible without a remount.

**Decision (user-approved): build Deck Pro in its own folder + remount the MCP.**

- Target project folder: **`examples/PySide6/AuroraDeckPro/`** (scaffolded, see
  below).
- `/.mcp.json` `--project-dir` was changed from `"."` to the absolute
  `…/examples/PySide6/AuroraDeckPro`. **To restore library-root MCP work later,
  set it back to `"."`.**
- **The next session must be a fresh Claude Code start** so the MCP mounts on
  the new folder. Verify with `designer_status` → `project_dir` should be
  `…/examples/PySide6/AuroraDeckPro`.

## Scaffold already in place (`examples/PySide6/AuroraDeckPro/`)

```
main.py                     # framework template (PLACEHOLDER — Phase 4 rewrites it)
ui/QCustomQMainWindow.ui    # framework template (PLACEHOLDER — Phase 2 replaces w/ MainWindow.ui)
gui/__init__.py             # empty — Phase 4 adds GuiFunctions.py + managers
json-styles/style.json      # ✅ REAL: Aurora Dark (default) + Aurora Light themes
Qss/scss/defaultStyle.scss  # empty starter — Phase 1 appends $TOKEN component styles
generated-files/            # empty — project_convert_ui fills it
```

`Qss/icons/_icons.qrc`, `generated-files/*`, `src/ui/ui_*.py` are **not yet
generated** — they need a Qt runtime, so they were deliberately deferred to the
next session's MCP-driven `project_convert_ui` (avoids headless segfaults).

## Do this next (resume the build plan at Phase 1)

Read `docs/design/deck-pro-build-plan.md`, then:
1. `designer_status` (confirm project_dir = AuroraDeckPro) → `designer_launch`.
   Confirm the Designer window is visible in your workspace before building.
2. **Phase 1** theme is half-done: `json-styles/style.json` is written. Still to
   do: open QSS editor (`designer_qss_window open`) and `project_write_style`
   the component chrome using real `$TOKENS` (see token model below).
3. **Phase 2–6** exactly as the build plan: MainWindow.ui shell → 6
   QCustomComponent pages → `project_convert_ui` + GuiFunctions/managers →
   `designer_run_app` + verify each page in both themes via `app_*` → teardown.

## Verified technical findings (use these — they correct the plan)

**Widget catalog is now live after restart.** This session committed the MCP
catalog/render capability (`9984b39`): `widgets_catalog` tool, `render_widget`
tool, and `customwidgets://catalog` resource now work once the MCP restarts.
Use `widgets_catalog(name=…)` for exact props/enums instead of reading source.
(They were broken this session only because the running process predated the
commit.) 37 token widgets are droppable.

**Theme token model (engine: `QCustomTheme.createVariables`).** Generated tokens
are `$COLOR_BACKGROUND_1..6`, `$COLOR_TEXT_1..4`, `$COLOR_ACCENT_1..4`,
`$BORDER_1..3`, `$BORDER_SELECTION_1..3`, `$SIZE_BORDER_RADIUS`.
- `BACKGROUND_1` = the declared `Background-color` **in both themes**; `_2..6`
  go progressively deeper/more-contrasting (darker in dark theme, darker-gray in
  light). So for elevation that flips correctly: **page canvas =
  `$COLOR_BACKGROUND_3`, cards/sidebar/panels = `$COLOR_BACKGROUND_1`** (cards
  read lighter than canvas in dark, white-on-gray in light).
- `TEXT_1` brightest → `_4` dimmest (muted text = `_3`). `ACCENT_1` brightest.
- **There are NO `$SPACING_*` or `_R/_G/_B` tokens** (the build plan is wrong on
  that). Put literal spacing in the .ui layouts (scale 0/10/16/20/24/40); use
  `$SIZE_BORDER_RADIUS` or literal radii; never hard-code hex colors in SCSS/.ui.

**Charts live in a subpackage.** `QCustomLineChart` / `QCustomPieChart` are under
`Custom_Widgets.QCustomCharts.*` (NOT top-level). Promote with
`<header>Custom_Widgets.QCustomCharts.QCustomLineChart</header>`. Also available:
`QCustomBarChart`, `QCustomAreaChart` (same subpackage).

**Structural-widget Qt property names** (not in the token catalog — from source):
- `QCustomSidebar`: defaultWidth, collapsedWidth, expandedWidth,
  toggleButtonName, iconCollapsed, iconExpanded, animationDuration, shadowColor,
  shadowBlurRadius/XOffset/YOffset.
- `QCustomSidebarButton`: labelText, textPrefixSpaces, hideOnCollapse,
  showOnCollapse, labelHidden (+ standard `icon`).
- `QCustomSidebarLabel`: text, icon, iconSize, hideOnCollapse, showOnCollapse.
- `QCustomComponentContainer`: filePath, formClassName, previewComponent,
  hotReload.
- `QCustomQStackedWidget`: slideTransition, fadeTransition, transitionDirection
  (Qt::Horizontal/Vertical enum), transitionTime, fadeTime, fadeDelay, …
- All Custom_Widgets props are dynamic (`stdset="0"`) in .ui.

**Promotion XML convention** (per `<customwidget>`):
`<class>QCustomX</class><extends>QWidget</extends>`
`<header>Custom_Widgets.QCustomX</header>` (+ `<container>1</container>` for
QCustomComponent / QCustomComponentContainer / QCustomQStackedWidget).

**Content/data** to reuse (fictional aurora-monitoring theme) lives in the
off-MCP reference `examples/PySide6/AuroraCommandDeck/deck_pro.py`
(STATIONS list, FORECASTS, nav items ◉ Overview / ▤ Stations / ◈ Forecast /
Analytics / Gallery / Settings). Reference only — do not ship it.

## Known caveats / gotchas
- MCP mounts only at session start; you cannot re-point it mid-session.
- Keep app runs visible; do NOT move/place/raise windows (user manages them).
- `render_widget`/theme functions segfault if called without a QApplication — do
  Qt-dependent work through the MCP (Designer/dev-server), not ad-hoc python.
- If the MCP still lacks a capability (e.g. an `openWorkspace` MCP tool — the
  bridge has the method, no tool wraps it yet), ADD it to
  `Custom_Widgets/mcp/server.py`, don't shell around it.
