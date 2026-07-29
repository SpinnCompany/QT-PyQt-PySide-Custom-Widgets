# Agent guide — QT-PyQt-PySide Custom Widgets

> **⛔ RULE #1 (read before any task).** Work on this project **through the
> `custom-widgets` MCP**, not ad-hoc shell. Before starting: **mount the MCP,
> then read its agent guide + skills.** If you can't reach the MCP tools, STOP
> and ask the user to mount it — don't fall back to a raw `python`/Bash run.

## Mount the MCP (HTTP daemon — required)

The MCP runs as a **persistent HTTP daemon** (stdio transport is unreliable with
this client). Before any session, start the daemon:

```bash
cd /home/p/git/QT-PyQt-PySide-Custom-Widgets
./start-mcp-daemon.sh        # starts on port 8765
```

Or manually:
```bash
python -m Custom_Widgets.mcp --transport http --port 8765 &
```

Config (both formats):
- **opencode.json** — `"type": "remote"`, `"url": "http://127.0.0.1:8765/mcp"`
- **.mcp.json** (Claude Code) — `"type": "http"`, `"url": "http://127.0.0.1:8765/mcp"`

Requires the MCP extra: `pip install -e .[mcp]`. Kill with `pkill -f "Custom_Widgets.mcp"`.

## Read these first (RULE #1 step 2)

1. `customwidgets://agent-guide` — the operating guide (also `AGENT_GUIDE` in
   [`Custom_Widgets/mcp/guide.py`](Custom_Widgets/mcp/guide.py)). It leads with
   RULE #1 and covers the visible-and-teachable workflow, how to build
   professional screens, theming, and app wiring.
2. `customwidgets://skills` — pointers to the shipped skills/knowledge.
3. Pick the RIGHT build skill:
   - [`.claude/skills/custom-widgets-app/SKILL.md`](.claude/skills/custom-widgets-app/SKILL.md)
     — **REAL apps / dashboards / multi-page tools**: the forms pipeline
     (`.ui` → compiled `src/` → `json-styles` themes → `Qss/scss` `$TOKENS` →
     GuiFunctions managers + workers). This is how production apps must be built.
   - [`.claude/skills/custom-widgets-demo/SKILL.md`](.claude/skills/custom-widgets-demo/SKILL.md)
     — the quick pure-code token demo only (a single styled `main.py`).

## ⭐ RULE #0 — the forms pipeline IS the product; don't ship a pure-code app

For any production-shaped build, the deliverable is `.ui` forms + `json-styles`
CustomThemes + `Qss/scss` `$TOKENS` + `GuiFunctions` managers/workers — NOT a
hand-built `main.py` with hard-coded hex. A code-only app that "looks right" is
still a failure for maintenance. Mirror `examples/PySide6/AuroraDeckPro` and
`examples/PySide6/WinningDashboard_CorrectArchitecture`. Compile forms with
`Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src`.
Switch themes BY NAME (`themeEngine.setTheme("<Custom Theme>")`). Read the
custom-widgets-app skill for the full procedure and the hard-won gotchas
(Qt hex is `#AARRGGBB`; token widgets need inline styling under `loadJsonStyle`;
use `QCustomDonut` not a QChart pie in small panels; etc.).

## The golden path (all through MCP tools)

```
designer_launch → designer_open_files / designer_new_form_xml   # build forms, VISIBLE in Designer
designer_qss_window(open) → project_write_style                 # style in the QSS editor, VISIBLE
designer_run_app → app_screenshot / app_click / app_object_tree # run + observe the REAL app
designer_stop_app → designer_quit                               # tear down cleanly
```

## ⭐ RULE #4 — showcase images: 2 themed, polished, non-blank

Every widget rendered for the documentation showcase **must produce 2 PNGs**
(light theme + dark theme) that show the widget's **full visual potential**:

- **Styled**: populate meaningful data/props so the widget isn't blank or tiny
  — data-driven widgets (DataTable, ChipGroup, ChatList, CardStack, etc.)
  need seed data set via their public API *before* the grab (e.g.
  `setColumns`+`setData` on DataTable, `setChips([...])` on ChipGroup,
  `setAvatars([...])` on AvatarGroup).
- **Themed**: apply the design-token theme using `applyDesignTokens` with
  `theme="light"`/`"dark"` AND the green docs-brand accent
  (`primary="#41CD52"`, `accent="#41CD52"`). Override `DesignTokens` default
  blue with:
  ```python
  tokens = DesignTokens(theme="light",
      semantic={"light": {"primary": "#41CD52", "accent": "#41CD52"}})
  ```
- **Margins**: wrap every widget in a container with **≥24px padding**
  so the widget breathes — no cramped/cropped edges. Use a `QMainWindow`
  with a central widget whose layout has `setContentsMargins(24,24,24,24)`.
- **Show()**: call `.show()` on the parent window before grabbing so Qt's
  paint system renders fonts, sub-controls, and native styling fully. An
  offscreen widget that is never shown can render blank or clipped.
- **Sized correctly**: use generous explicit sizes that let painted elements
  (gauges, charts, arcs, text) breathe. Never clip labels or value readouts.
- **Both themes**: produce a `<name>.png` (light) and
  `<name>-dark.png` (dark) pair. The canonical Docs path is
  `static/img/showcase/<name>[-dark].png`.
- **Meta present**: the associated doc `.md` page references **both** images
  (e.g. a light/dark toggle or side-by-side), along with the widget name and
  a sentence on what it does.

A widget render that is blank, cropped, shows only an unstyled default state,
or lacks a dark-theme variant is **not acceptable** for the showcase — fix
the render script or add seed data to the widget before delivering.

**Reference pattern** — see GlassHome (`examples/PySide6/GlassHome/`) for the
gold standard of modern widget styling: glassmorphism surfaces with the
design-token theme, green accent, proper spacing, and seeded data.

## Design rules (enforced — not optional)

The library ships a design-rule linter (`Custom_Widgets.lint`) that enforces the
project's **visual** rules a type checker can't see. It runs automatically on
every file edit (a PostToolUse hook in [`.claude/settings.json`](.claude/settings.json)),
in pre-commit, and in CI — and is exposed to MCP agents as the `design_lint`
tool. Canonical spec: [`docs/design/design-rules.md`](docs/design/design-rules.md).

- **`glyph-icons` (error)** — never use a unicode glyph as an icon in UI text
  (no `◑ ＋ ⚙ ✦ ➤ ✓ ↗` / emoji). Use a real themed-SVG or painted icon that
  recolours per theme. A new violation **blocks the edit**.
- **`hardcoded-hex` (warning)** — drive chrome colour from token roles, not raw
  `#rrggbb` (ALL-CAPS palette constants are allowed).
- **`drop-shadow` (warning)** — no `QGraphicsDropShadowEffect` without a
  `# allow-shadow: <reason>` justification.

Run it yourself before finishing a screen: `python -m Custom_Widgets.lint`
(or the `design_lint` MCP tool). Pre-existing debt is grandfathered by
`.custom_widgets_lint_baseline.json`; only **new** violations fail. Suppress a
genuine false positive with `# noqa: <rule-id>`.

## Where things live

| Path | What |
| --- | --- |
| [`Custom_Widgets/mcp/`](Custom_Widgets/mcp/) | MCP server (`server.py`), agent guide (`guide.py`), `python -m` entry |
| [`Custom_Widgets/DesignerBridge.py`](Custom_Widgets/DesignerBridge.py) | live link that runs inside Qt Designer + the app |
| `Custom_Widgets/` | the widget library (import `from Custom_Widgets.QCustom… import …`) |
| `examples/PySide6/` | runnable examples / showcases |
| [`Custom_Widgets/lint/`](Custom_Widgets/lint/) | design-rule linter (rules in `rules.py`); spec in [`docs/design/design-rules.md`](docs/design/design-rules.md) |
| `.claude/skills/` | Claude Code skills for this repo |

**If a capability is missing, add it to the MCP** — don't work around it in a shell.

## ⭐ RULE #3 — artifact/content boundary (repo vs docs)

**All documentation, guides, tutorials, blog posts, changelogs, API docs, and showcase screenshots** belong in:
- `/home/p/git/Docs-QT-PyQt-PySide-Custom-Widgets/` — the canonical Docusaurus documentation site (free + pro)

**The pro website** (`/home/p/git/custom-widgets-pro-website/`) handles billing, pricing, downloads, and high-level feature pages only — no long-form docs or showcase screenshots.

**Code repos** are for code and README only:
- `/home/p/git/QT-PyQt-PySide-Custom-Widgets/` — the library + examples (`examples/` READMEs are fine, but long-form docs go to Docs)
- `/home/p/git/QT-PyQt-PySide-Custom-Widgets-Pro/` — pro add-ons

Never save screenshots, documentation pages, or marketing assets into the code repos. An agent that generates a screenshot must save it to the Docs repo, not anywhere under `QT-PyQt-PySide-Custom-Widgets/`, `QT-PyQt-PySide-Custom-Widgets-Pro/`, or the pro website repo.

## ⭐ RULE #5 — Qt Designer Layout & Spacing (enforced)

**Spacing between widgets must be handled by the parent layout**, never by QSS `margin` or by assuming `padding` on arbitrary widgets.

- **Layout owns spacing**: `Contents Margins`, `Spacing`, stretch factors, and alignment are set in Qt Designer / the `.ui` file / layout code — never via QSS `margin`.
- **QSS `padding`** may be used only on widgets where Qt reliably supports it (e.g. `QPushButton`, `QToolButton`). Do not assume `padding` works on every widget; verify first.
- **QSS `margin` is never a spacing tool** — many widgets ignore it. Use parent-layout properties instead.
- **Separation**: `.ui` = placement / margins / spacing / stretch / size policies. External QSS/theme = colours / borders / border-radius / fonts / icons / states / widget appearance. Never intermix them.

Before a change, classify the issue:
- **visual styling** → external QSS/theme
- **spacing or layout** → `.ui` / Qt Designer layout properties

### Alignment Over Spacers

Do not insert `QSpacerItem`s unless actually needed. For simple positioning, use the layout's alignment properties:
- Align Left / Right / Top / Bottom / Center / HCenter / VCenter

Use `QSpacerItem` only when flexible empty space is required (pushing widgets to opposite ends, distributing extra space proportionally, responsive expansion). Avoid stacking multiple spacers — first consider alignment, stretch factors, or layout properties.

### Use Icons, Not Boring UIs

Every showcase/app must use themed SVG icons (feather set) on buttons, nav items, and action controls. A professional UI without icons is a failure — icons give visual anchors that text alone cannot. Set `qproperty-icon` in the `.ui` / QSS with `$PATH_RESOURCES+'feather/<name>.svg'` and drive colour via `qproperty-iconColor` token so they flip with the theme.

## ⭐ Operational Rules (from hard-won debugging)

### Never `setStyleSheet()` in Python
All styling comes from QSS/SCSS files. In Python you may only `setProperty` (incl. custom-widget Qt properties), `style().polish()`/`unpolish()`, and set CONTENT (setText). **Never call `setStyleSheet(...)`** anywhere — not the window, a region container, a code-built row, or a child.

### `applyCompiledSass(generateIcons=True)` Deadlocks
The `generateIcons=True` path starts a `Worker` thread that accesses `QSettings()` at `QCustomTheme.py:1511`. If the main thread also touches `QSettings()` during startup, Qt's lock-file mechanism deadlocks the entire process. **Fix:** pass `generateIcons=False` on startup; icons regenerate on theme switch anyway.

### Don't Mix `enable_hot_reload` with `applyCompiledSass`
`enable_hot_reload(window, build)` sets up a `QFileSystemWatcher` + `QTimer` after `build()` returns. If `build()` calls `applyCompiledSass`, the background icon thread combined with the watcher setup deadlocks. **Fix:** call build logic directly in `__init__`; the dev server handles file watching externally.

### `.venv` + `QT_API=pyside6` Required
Every example must use the project `.venv` and set `os.environ["QT_API"] = "pyside6"` before any import. Compiled `.ui` files hard-code `PySide6` while `qtpy` defaults to `PyQt5`; mismatched QT_API causes type errors.

### `QAppSettings.updateAppSettings()` Hangs in Constructors
Calling `QAppSettings.updateAppSettings(self)` inside `__init__`/`build()` can hang due to the icon-generation thread deadlock. **Fix:** inline the equivalent steps manually (QSettings, reloadJsonStyles, applyCompiledSass(generateIcons=False), maybe_start_app_control).

### No Circular @import in SCSS
`main.scss` already does `@import 'defaultStyle'`. Never write `@import 'defaultStyle'` inside `defaultStyle.scss` itself — that creates a circular self-import that breaks SCSS compilation and can hang the compilers. When using `project_write_style` to write to `defaultStyle.scss`, strip any `@import` line the tool might append.

### AppControl Server Summary
- Socket path: `/tmp/customwidgets-app-{sha1(projectRoot)[:12]}`
- Server starts via `maybe_start_app_control()` inside `QAppSettings.updateAppSettings()` when `CUSTOM_WIDGETS_APP_CONTROL=1`
- Dev server sets this env var automatically when running `designer_run_app`
- The MCP `app_status` tool checks reachability via `QLocalSocket` connection
