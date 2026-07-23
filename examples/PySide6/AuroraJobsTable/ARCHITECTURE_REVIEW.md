# AuroraJobsTable — Architecture Review (rules broken)

This folder (`examples/PySide6/AuroraJobsTable/main.py`) renders the WorkEver
"Jobs" screen correctly, but it was built as a **single hand-coded `main.py`**.
Per the Custom Widgets MCP agent guide that is an architectural **failure**, even
though it looks right. This report enumerates the rules it violates and how the
correct build differs. The corrected build lives in
`examples/PySide6/AuroraJobsTable_CorrectArchitecture/`.

> RULE #0 — *"THE FORMS PIPELINE **IS** THE PRODUCT. A single hand-built `main.py`
> full of hard-coded hex is a FAILURE even if it renders correctly — it throws
> away theming, Designer, and maintainability."*

## Rules broken

| # | Rule (from `customwidgets://agent-guide` / skill `custom-widgets-app`) | How `main.py` breaks it | Correct approach |
|---|---|---|---|
| 1 | **Forms pipeline is the product** — screens are `.ui` forms compiled to `src/ui_*.py`. | The entire UI is built imperatively in Python (`_build()`, `QHBoxLayout(...)`, `addWidget`). No `.ui`, nothing compiled, Designer can never open it. | `ui/MainWindow.ui` + `ui/JobsComponent.ui` → `Custom_Widgets --convert-ui` → `src/ui_*.py`. |
| 2 | **No hard-coded hex in code/.ui** — colour comes from token roles / theme JSON. | `GREEN="#22c55e"`, `ORANGE="#f97316"`, `rail="#0f172a"`, `#ffffff`, huge inline `setStyleSheet` blocks with literal hex throughout. | Colours live in `json-styles/style.json` (`Aurora Light`/`Aurora Dark` + a `StatusPalette` for semantic data hues); chrome in `Qss/scss/chrome.scss` using `$TOKENS` only. |
| 3 | **Theming via `style.json` CustomThemes, switch BY NAME** | Theme is a bespoke `DesignTokens(theme=...)` + `apply_theme()` that rebuilds every stylesheet string by hand; the "toggle" is a hand-rolled light/dark flip, not the icon-pipeline theme engine. | `loadJsonStyle(...)` + `QAppSettings.updateAppSettings`; `themeEngine.setTheme("Aurora Dark")`; recolour on `onThemeChangeComplete`. |
| 4 | **QSS lives in `.scss` with objectName/`[role]` selectors, never inline** | Dozens of inline `setStyleSheet("... %s ...")` calls with f-string hex (`_chrome`, `_tableQss`, rail buttons, avatar…). | `chrome.scss` selectors: `#railButton:checked`, `QFrame[role="card"]`, `#dataTableView::item`, `QHeaderView::section`, etc. |
| 5 | **One `QCustomQMainWindow`; screens are `QCustomComponent` embedded via `QCustomComponentContainer`; reach with `container.component`** | Single `JobsWindow(QWidget)`; no component boundary, no container, no `objectName` public API. | `MainWindow(QCustomMainWindow)` shell + `JobsComponent` embedded through `jobsContainer` (`filePath=ui/JobsComponent.ui`, `previewComponent=false`). |
| 6 | **A `GuiFunctions` orchestrator holds one Manager per page; workers run Worker→Signal→GUI** | All wiring, data and behaviour sit in the window class. No orchestrator, no manager, no background worker. | `gui/GuiFunctions.py` (orchestrator) + `JobsManager` + `gui/workers.py` `JobsLoaderWorker` (loads rows off-thread, emits a signal). |
| 7 | **Data belongs in a data module, not the view** | `sample_rows()`, `STATUSES`, column defs are literals inside the window file. | `gui/data.py` (rows, statuses, columns), read by the manager. |
| 8 | **Nav = `QCustomSidebar`/`QCustomSidebarButton`; route a `QCustomQStackedWidget` by widget** | The rail is hand-built `QFrame` + `QPushButton` subclass with painted glyphs; no stacked-widget routing. | `QCustomSidebar` rail with `QCustomSidebarButton`s; `pageStack.setCurrentWidget(page)`. |

## What was still correct (kept)
- **No unicode glyphs as icons** — icons are painted/SVG (passes `design_lint`
  `glyph-icons`). The correct build uses the shipped **feather SVG** set recoloured
  per theme (`gui/GuiFunctions.feather_pixmap`), which is cleaner still.
- The **library widgets** themselves (`QCustomDataTable`, `QCustomTableToolbar`)
  are correct and reused unchanged — only the *app around them* was wrong.

## Net
`main.py` was a **pure-code prototype mislabelled as the example**. It is kept
only as the "what not to do" counterpart; the real, maintainable build is
`AuroraJobsTable_CorrectArchitecture/`, which produces the identical screen from
`.ui` forms + JSON themes + SCSS tokens + a GuiFunctions/Manager/worker stack.
