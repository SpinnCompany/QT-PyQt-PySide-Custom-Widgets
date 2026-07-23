# Deck Pro — MCP build plan (Custom_Widgets Designer project)

Execution checklist for rebuilding **Aurora Deck Pro** the sanctioned way: a
Custom_Widgets Designer project, authored and driven entirely through the
`custom-widgets` MCP (RULE #1). This replaces the off-MCP `deck_pro.py` script.

**Preconditions:** `custom-widgets` MCP mounted (see [AGENTS.md](../../AGENTS.md));
read `customwidgets://agent-guide` + `customwidgets://skills` first.

> **Session-2 corrections (read [deck-pro-session-handoff.md](deck-pro-session-handoff.md) first).**
> The project now lives in `examples/PySide6/AuroraDeckPro/` and the MCP is
> remounted there (a restart is required). Also: there are **no `$SPACING_*` or
> `_R/_G/_B` tokens** — use `$COLOR_BACKGROUND_1..6` / `$COLOR_TEXT_1..4` /
> `$COLOR_ACCENT_1..4` / `$SIZE_BORDER_RADIUS` with literal layout spacing; page
> canvas = `$COLOR_BACKGROUND_3`, cards/panels = `$COLOR_BACKGROUND_1` (flips
> correctly). Charts are `Custom_Widgets.QCustomCharts.QCustomLineChart` /
> `…QCustomPieChart` (subpackage, not top-level). The handoff has the verified
> token model, structural-widget property names and promotion XML.

**Golden loop for every form:** `designer_new_form_xml`/`designer_set_form_xml`
→ `designer_open_files` → `designer_screenshot` → refine via
`designer_set_widget_property` → (later) `project_convert_ui` → run via
`designer_run_app` → observe via `app_*`.

---

## Target structure

```
ui/                      hand/MCP-authored .ui forms
  MainWindow.ui          class MainWindow  (QCustomQMainWindow)
  OverviewComponent.ui   class OverviewComponent (QCustomComponent)
  StationsComponent.ui
  ForecastComponent.ui
  AnalyticsComponent.ui
  GalleryComponent.ui
  SettingsComponent.ui
src/ui/ui_*.py           compiled forms (project_convert_ui)
json-styles/style.json   Aurora Dark + Aurora Light CustomThemes
Qss/scss/defaultStyle.scss  $TOKEN-based component styles
generated-files/         intermediates
main.py + gui/           minimal boot + GuiFunctions orchestrator + managers
```

Composition rule: ONE `QCustomQMainWindow`; every page is a `QCustomComponent`
embedded via a `QCustomComponentContainer` whose `filePath` → the COMPILED child
(`src/ui/ui_<Page>Component.py`), `previewComponent=false` in production. Route
with an inner animated `QCustomQStackedWidget`; switch by `setCurrentWidget(page)`,
never by index. objectNames below are the stable public API for wiring.

---

## Phase 0 — Preflight
1. `designer_status`; if not running → `designer_launch`.
2. Read `customwidgets://agent-guide` + `customwidgets://skills`.
3. `designer_list_templates` (confirm QCustomQMainWindow / QCustomComponent templates).

## Phase 1 — Theme first (so every form renders themed)
1. Write `json-styles/style.json` with two `CustomThemes`:
   - **Aurora Dark** (default `appTheme`): Background `#0a0e1a`/`#121a2e`, Text
     `#e8edf9`, Accent `#4fe3a6` (aurora green), Icons light. Include `_R/_G/_B`
     triples for rgba tokens.
   - **Aurora Light**: Background `#eef1f8`/`#ffffff`, Text `#0c1122`, Accent
     `#12a074`.
2. `designer_qss_window(action='open')` → `project_write_style` the component
   styles using `$TOKENS` ($COLOR_ACCENT_1, $COLOR_BACKGROUND_1/2, $COLOR_TEXT_1,
   $SPACING_*), `&:hover/&:pressed` states. NO hardcoded hex, never in .ui.
3. `designer_qss_screenshot` to confirm the editor shows it.

## Phase 2 — Main shell (MainWindow.ui)
- Root `QCustomQMainWindow` → central `QWidget` (margins/spacing 0) → `QHBoxLayout`:
  - **Sidebar**: `QCustomSidebar` (`toggleButtonName`, `collapsedWidth=64`,
    `expandedWidth=216`) with `QCustomSidebarLabel` "✦ AURORA" + one
    `QCustomSidebarButton` per page (`labelText`, icon from qrc): `navOverview`,
    `navStations`, `navForecast`, `navAnalytics`, `navGallery`, `navSettings`;
    bottom `QCustomThemeDarkLightToggle` (`themeToggle`).
  - **Body**: `QStackedWidget` → inner animated `QCustomQStackedWidget` `pageStack`
    (`slideTransition=true`, `transitionDirection=horizontal`, `transitionTime=420`)
    holding 6 `QCustomComponentContainer`s: `overviewContainer` … `settingsContainer`,
    each `filePath` → `src/ui/ui_<Page>Component.py`.
- Build by pushing .ui XML via `designer_new_form_xml("MainWindow", xml)`; declare
  every promoted class in `<customwidgets>` (class/extends/header, `<container>1`
  for containers). `designer_screenshot` → refine. Link icons qrc in `<resources>`.

## Phase 3 — Page components (each is a QCustomComponent root)
Author each, `designer_open_files`, `designer_screenshot`, refine. Promote the
token widgets in `<customwidgets>` (they render as real class at runtime; if a
widget lacks a Designer plugin it shows as a plain QWidget placeholder in Designer
— verify with `designer_get_object_info`, that's expected, not a failure).

1. **OverviewComponent** — hero `QFrame` band; row of 4 `QCustomStatCard`
   (`kpStat` etc.); dismissible `QCustomAlert`; `QCustomTimeline` (activity) +
   `QCustomAvatarGroup` + `QCustomBadge`s in `QCustomCard`s.
2. **StationsComponent** — toolbar: `QCustomComboBox` `regionCombo`,
   `QCustomNumberInput` `minKp`, `QCustomSwitch` `liveOnly`, `QLineEdit`
   `searchBox`, `QCustomRangeSlider` `cloudRange`; `QCustomDataTable`
   `stationsTable` (columns call/region/kp/clouds/status, `pageSize=8`).
3. **ForecastComponent** — `QCustomSplitter`: left `QCustomCarousel`
   `forecastCarousel` (auto-advance) + 3 `QCustomProgressRing`; right
   `QCustomStepper` `phaseStepper` + `QCustomAccordion` briefing.
4. **AnalyticsComponent** — `QCustomLineChart` `kpChart` + `QCustomPieChart`
   `regionPie`. (Charts render at runtime; use `QCustomEmptyState` placeholder in
   Designer if the plugin isn't present.)
5. **GalleryComponent** — `QScrollArea` (`widgetResizable=true`) over a
   `QCustomFlowWidget`/grid of cards showcasing Rating, Switch, Badge, Chip,
   SegmentedControl, RangeSlider, NumberInput, Kbd, Breadcrumbs, Pagination,
   ColorPicker, ProgressRing, Skeleton, ComboBox, AvatarGroup, EmptyState, and
   Toast trigger buttons. (Scroll-reveal fade+slide is runtime manager code.)
6. **SettingsComponent** — `QCustomThemeDarkLightToggle` +
   `QCustomSegmentedControl` (theme), `QCustomColorPicker`, `QCustomSwitch` rows,
   `QCustomQPushButton` `saveBtn` (variant=primary) → success `QCustomToast`.

## Phase 4 — Compile + wire
1. `project_convert_ui` for each form → `src/ui/ui_*.py`.
2. Minimal `main.py`: `setupUi` → `loadJsonStyle(self, self.ui,
   jsonFiles={"json-styles/style.json"})` → `show()` →
   `QAppSettings.updateAppSettings(self)` → `GuiFunctions(self).initialize()`.
3. `gui/GuiFunctions.py`: holds one `Manager(QObject)` per page; `navigateTo(name)`
   maps name→page widget, `pageStack.setCurrentWidget(...)`, sets active sidebar
   button, lazy-inits the page. Each manager reaches its component via
   `container.component` and wires child widgets by objectName.
4. Runtime logic in managers (not the .ui): Stations filter (region/minKp/cloud/
   live/search → `stationsTable.setData`), the live Kp pulse (QTimer → `kpStat`),
   Gallery scroll-reveal (QScrollArea scroll → per-card opacity+slide animation),
   Settings save → toast. Workers emit signals only; toggle QSS state via
   `setProperty` + `unpolish/polish`.

## Phase 5 — Run + observe (Designer's Run ONLY)
1. `designer_run_app`. Then for EACH page: `app_click(navX)` →
   `app_screenshot` → `app_object_tree`/`app_find` to verify widgets present.
2. Exercise interactions: `app_set_text(searchBox, ...)`, `app_click` chips/toggle,
   confirm table filters and theme flips. `designer_app_logs` on any error.
3. Keep windows visible; do NOT move/raise/place them.

## Phase 6 — Teardown
`designer_qss_window(action='close')` → `designer_stop_app` → `designer_quit`
(reports `had_unsaved_forms`; marks clean so no save prompt). Never shell-kill.

---

## Verification gates
- After Phase 2: shell screenshot shows sidebar + empty themed page stack.
- After each Phase 3 form: `designer_screenshot` matches intent.
- After Phase 5: every page screenshot in both themes; no `designer_app_logs`
  errors; filter/nav/theme interactions observably work via `app_*`.

## Known caveats to check live
- Which token widgets (StatCard, DataTable, Carousel, ProgressRing, charts) have
  Designer plugins vs. render as runtime-only promoted widgets — verify early with
  `designer_get_object_info`; missing plugin ≠ failure, the class is real at run.
- If any capability is missing from the MCP to author a form cleanly, ADD it to
  the MCP (`Custom_Widgets/mcp/server.py` + bridge) rather than hand-editing .ui.
