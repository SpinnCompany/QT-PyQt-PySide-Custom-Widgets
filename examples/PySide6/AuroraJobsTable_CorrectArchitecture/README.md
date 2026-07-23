# Aurora Jobs — Correct Architecture

The WorkEver-style **Jobs** screen (`QCustomDataTable` + `QCustomTableToolbar`)
built the **right** Custom_Widgets way — the forms pipeline — instead of a
hand-coded `main.py`. It is the corrected counterpart to
`../AuroraJobsTable/` (whose `ARCHITECTURE_REVIEW.md` documents what that pure-code
prototype broke).

## What makes it "correct"

```
ui/MainWindow.ui        rail + topbar + animated pageStack + jobsContainer
ui/JobsComponent.ui     the page: title + card(toolbar + datatable)   ── structure only
   └─ src/ui_*.py        compiled  (Custom_Widgets --convert-ui)
json-styles/style.json  Aurora Light / Dark CustomThemes  +  StatusPalette (semantic
                        data hues)  +  Brand (theme-independent dark rail)
Qss/scss/chrome.scss    ALL chrome from $TOKENS — no hard-coded hex, flips per theme,
                        incl. the DataTable's internal view (#dataTableView)
gui/theme.py            reads colours from style.json (roles + StatusPalette + Brand)
gui/data.py             rows / statuses / filter chips (data, not view)
gui/workers.py          JobsLoaderWorker — rows arrive off-thread (Worker→Signal→GUI)
gui/GuiFunctions.py     orchestrator + JobsManager: configures the DataTable columns
                        and Toolbar statuses IN CODE (Designer can't), wires signals,
                        and re-themes the delegate/toolbar on theme change
main.py                 minimal boot (QCustomMainWindow + loadJsonStyle + QAppSettings)
```

Key architectural choices:

- **Icons are set in QSS, never from Python.** Every glyph (rail nav, hamburger,
  topbar search/help/bell, add-job plus, avatar caret) is declared in
  `chrome.scss` as `qproperty-icon: url(theme-icons:icons/feather/<name>.svg)` and
  recolours to the theme's Icons-color automatically. On a theme switch Python
  only **re-polishes** (`style().unpolish()/polish()`) so the widgets reload the
  recoloured icons — no `setIcon`/`setPixmap`. (Set pixmaps in Designer with
  `scaledContents` if you must use a `QLabel`.)
- **No hard-coded hex** in code, `.ui`, or `.scss`. Chrome uses `$COLOR_*` tokens;
  the DataTable delegate/toolbar *paint* colours (not icons) are read from the
  theme roles + `StatusPalette` and re-applied on `onThemeChangeComplete`.
- **Theme switch BY NAME** (`themeEngine.setTheme("Aurora Dark")`), never the generic
  Light/Dark toggle — required for the custom themes' icon sets to recolour.
- **Collapsible icon rail** (`QCustomSidebar`): starts collapsed at 72px (icons
  only); the hamburger `sidebarToggle` expands it to 240px to reveal labels
  (`collapsedWidth`/`expandedWidth` must differ or the width animation is skipped).
- Library widgets Designer cannot configure (DataTable **columns**, Toolbar
  **statuses**) are set in the Manager in code — exactly like chart series.
- The DataTable's internal view is themed via `#dataTableView` selectors in
  `chrome.scss` (no inline `setStyleSheet`).
- Rows are loaded by a **background worker** and delivered via a signal.

## Run

Through the Custom_Widgets MCP (`designer_run_app`), or directly:

```bash
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src   # after any .ui edit
python main.py
```

Toggle the avatar (top-right) to switch Aurora Light / Dark.

## Notes / gotchas hit while building

- **QCustomSidebar as a fixed 72px icon rail**: its width animation is *skipped*
  when `collapsedWidth == expandedWidth`, so it stays at its 300px default. Set
  `expandedWidth` different from `collapsedWidth` (here 240 vs 72) with
  `defaultWidth=72` so it collapses to 72.
- **`Background-color` is the surface (card) colour**; the generator derives a
  slightly darker page shade (`BG_2`/`BG_3`) for the window — so cards read as white
  panels on a soft page without any hard-coded hex.
