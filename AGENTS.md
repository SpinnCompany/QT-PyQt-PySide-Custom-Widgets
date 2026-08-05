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

This bites the **tools** too, not just examples (2026-08-04): `gen_widget_docs.py`
run with a python that has PyQt5 installed bound to PyQt5 and failed in two
quiet ways — every GIF capture died with `sip.voidptr object has an unknown
size` (PyQt's `QImage.bits()` needs `setsize()`; PySide returns a sized
memoryview), and QCustomBarChart/QCustomPieChart failed to import through a
broken PyQt5 `libQt5Charts.so.5`. The tool now sets
`os.environ.setdefault("QT_API", "pyside6")` itself; keep that line when
touching its startup, and give any new capture/introspection tool the same
default.

### `git grep -- 'Custom_Widgets/**/*.py'` silently matches nothing
Git pathspec `**` requires the `:(glob)` magic prefix; without it the pattern
returns zero hits and reads as "no matches found" — this falsely "proved"
QtCharts was purged when 12 files still import it. Use plain
`grep -rlE <pat> Custom_Widgets/ --include='*.py'` (also faster here: git grep
stats the 63k-file worktree on HDD and can take minutes).

### `QAppSettings.updateAppSettings()` Hangs in Constructors
Calling `QAppSettings.updateAppSettings(self)` inside `__init__`/`build()` can hang due to the icon-generation thread deadlock. **Fix:** inline the equivalent steps manually (QSettings, reloadJsonStyles, applyCompiledSass(generateIcons=False), maybe_start_app_control).

### No Circular @import in SCSS
`main.scss` already does `@import 'defaultStyle'`. Never write `@import 'defaultStyle'` inside `defaultStyle.scss` itself — that creates a circular self-import that breaks SCSS compilation and can hang the compilers. When using `project_write_style` to write to `defaultStyle.scss`, strip any `@import` line the tool might append.

### AppControl Server Summary
- Socket path: `/tmp/customwidgets-app-{sha1(projectRoot)[:12]}`
- Server starts via `maybe_start_app_control()` inside `QAppSettings.updateAppSettings()` when `CUSTOM_WIDGETS_APP_CONTROL=1`
- Dev server sets this env var automatically when running `designer_run_app`
- The MCP `app_status` tool checks reachability via `QLocalSocket` connection

### Running an example headless from outside its folder (survey/screenshot harnesses)
Three bugs cost a full debugging session (2026-08-01, fixed in `tools/survey_examples.py`):
1. **`sys.path`, not just cwd.** `os.chdir(appDir)` is NOT enough to emulate `python main.py` — `runpy.run_path` does not add the script's directory to `sys.path`, so structured apps die with `ModuleNotFoundError: No module named 'gui'` (or `src`). Always `sys.path.insert(0, appDir)` too.
2. **Never schedule the capture timer before the app's `QApplication` exists.** A `QTimer.singleShot` created pre-QApplication never fires, so every working app looks like a hang. Wrap `QApplication.exec`/`exec_` and schedule the timer inside the wrapper (i.e., at event-loop entry).
3. **Stale `~/.config/Custom Widgets/*.conf.lock` files deadlock QSettings.** Any killed run can leave one; the next app run blocks forever inside `QLockFile::tryLock`/`fdatasync` (stack shows `QSettings` destructor). Delete `"~/.config/Custom Widgets/"*.lock` before batch runs, and suspect this first whenever an app hangs with zero output.
Also: export `QT_QPA_PLATFORM=offscreen` explicitly — with a live display the "headless" run flashes real windows on the user's desktop.

### Example-overhaul findings (2026-08-01, batch fixes)
- **`python3 -m Custom_Widgets` does not work** (no `__main__`): use the installed `Custom_Widgets` console script or `from Custom_Widgets.CMD import run_command`.
- **`Default-Theme: true` in style.json is silently ignored** whenever a stale `THEME` exists in QSettings at JSON-parse time (parsed before org/app names are set, so the wrong store is read). Boot code must explicitly fall back: if `QSettings().value("THEME")` names no theme in the current style.json, set the json's default (or first) theme by name.
- **style.json schema keys** are `Theme-name`/`Background-color`/`Text-color`/`Accent-color`/`Icons-color`/`Default-Theme`. `examples/PySide6/QCustomQSlider/json-styles/style.json` used wrong keys (`name`/`Background`) and only looked right via a leftover builtin theme — don't copy json keys from it.
- **JSonStyles `QCustomCheckBox.animationEasingCurve` crashed every app whose style.json used it**: `JSonStyles/__init__.py` called `self.returnAnimationEasingCurve(...)` (self = the user's window) instead of the imported free function. Fixed 2026-08-01.
- **QCustomQStackedWidget**: `setSlideTransition()`/`setFadeTransition()` restored as backward-compatible setters; `_initializeAllWidgetsOpacity` no longer zeroes the *current* page (fade-enabled stacks booted blank).
- When verifying headless runs, set `PYTHONUNBUFFERED=1` or the `SURVEY:OK` print can be lost to block buffering (runner exits via `os._exit`).
- **`QCustomComponentContainer` silently kills QSS backgrounds on a component root's direct children**: on every refresh it sets `WA_TranslucentBackground` on them (`widgets/containers/QCustomComponentContainer.py:110-115`; the comment claiming explicit QSS backgrounds still paint is wrong). A `role="card"` frame or gradient bar as a direct child of a component root renders transparent — buttons are unaffected, which hides the bug. In-app workaround: clear the attribute on rebuild (see `_solid()` in SmartHomeDashboard/CheckBoxDashboard GuiFunctions).
- **Clearing `WA_TranslucentBackground` is not enough** — it implies `WA_NoSystemBackground`, which is NOT auto-cleared and alone still suppresses the QSS fill. Clear both.
- **`Other-variables` in style.json are the sanctioned way to get per-theme non-token colours into scss** (available as `$NAME` after reload) — including inside `qlineargradient()`. That is how gradient chrome leaves `setStyleSheet` without hard-coding hex.
- **A stale `Unknown Organization/main.py.conf` QSettings store poisons theme seeding**: `loadJsonStyle` checks QSettings for an existing `THEME` while org/app names are still unset, so it reads the shared pre-identity store; a stale `THEME` there cancels every `Default-Theme` flag and the app boots a BUILT-IN theme. **Primary fix: call `QCoreApplication.setOrganizationName/setApplicationName BEFORE `loadJsonStyle`.** Belt-and-braces: after the settings block, if `THEME` still names no current theme, set the app's default explicitly + `INIT-THEME-SET`.
- **design_lint via the MCP daemon mis-scopes example apps** (`project=<app>` lints the whole repo; `project=<repo>` + `paths=[example]` scans 0 files). Reliable CLI gate: `PYTHONPATH=$R python3 -m Custom_Widgets.lint examples/PySide6/<App> [--no-baseline]`.
- **`QCustomTheme.setTheme()` defaults to `applyCompiledSass(generateIcons=True)`** — for a runtime theme toggle, write `THEME` to QSettings yourself and call `applyCompiledSass(generateIcons=False, paintEntireApp=True)` to avoid the icon-worker deadlock path.
- **Qt.Popup top-levels (emoji picker, tip overlays) are invisible to `window.grab()`** — verify them with a dedicated script that opens the popup and grabs the popup widget itself. Child overlays (command palettes, modals parented into the window) ARE captured.
- **Theme flips persist** (`THEME=` in `~/.config/Custom Widgets/<App>.conf`) and re-tint `Qss/icons`. Any headless dark-theme test must reset `THEME` to the default afterward, or the next before/after comparison boots in the wrong theme.
- **First-ever flip to a theme whose icons were never generated can transiently drop a QtCharts series from the grab** — re-run before calling it a regression. Separately (pre-existing on pristine HEAD): `QCustomAreaChart` keeps its boot-time series colour after a recolor.
- **design_lint with `paths:["."]` lints the entire repo** regardless of `project` (60–90s/call) — filter findings to the app folder, or use the CLI (`python3 -m Custom_Widgets.lint <folder>`).
- **`_styles.scss` gives every plain QWidget an opaque `BACKGROUND_1` fill** — a native QWidget holder or QPainter-drawn widget sitting on a card needs an explicit `background: transparent` rule under its objectName or it paints a solid box over the card.
- **`qproperty-<name>` in scss works for custom Python `Property(QColor)` props and re-applies on every theme repaint** — the clean way to theme QPainter widgets (radios, charts, rainbow buttons) with zero Python styling code.
- **.ui property ORDER matters for range widgets**: uic emits `setProperty` in XML order, so a `value` authored before `minimum`/`maximum` gets clamped by the widget's ctor-default range (a RulerPicker height of 178 became 120). Author `minimum`/`maximum`/`step` BEFORE `value` in the .ui. For QCustomRangeSlider: min/max first, then `upperValue`, then `lowerValue` (each setter clamps against the current other bound).
- **"Half-themed app" failure signature**: when theme seeding fails (stale pre-identity QSettings), `copyMissingVariablesFromOtherThemes` still copies your `Other-variables` onto the predefined theme — so custom hues render over the built-in white/#00bcff base. If an app shows YOUR accents on the WRONG base palette, it's the boot-order/theme-seeding bug, not scss.
- **Concurrent agents sharing one MCP scratch session-id get responses crossed** — use a per-agent session file, or the race-free lint CLI (`python3 -m Custom_Widgets.lint --root <repo> <path>`). Correct MCP lint scoping is `project=<repo>` + `paths=["examples/PySide6/<App>"]`; `summary.files` counts files WITH findings (0 = clean).
- **Dark-theme token derivation always darkens `BACKGROUND_2..6` relative to `BG_1`** — for the "cards lighter than window" look, put the CARD colour in `Background-color` (BG_1 = card) and paint the window/centralwidget with `$COLOR_BACKGROUND_2`.
- **`themeEngine.toggleTheme(dark="X", light="Y")` is the clean two-theme toggle** for per-app theme names (replaces hand-rolled QSettings flips in demos).
- **QCustomKbd keycap QSS padding**: the token 8px side padding clips cap text ("Ctrl") when the row is width-tight — use 4px side padding in scss for keycaps.
- **NULL-ICON TRAP**: `theme-icons:` QIcons/QPixmaps created in `setupUi` are permanently null when the search path isn't registered yet (the theme engine registers it during `loadJsonStyle` — too late — and the failed lookup is cached). Fix: `QDir.addSearchPath("theme-icons", "<app>/Qss/icons")` at module import in main.py. Note `applyIcons` cannot repair `QCustomQPushButton` entries (no key in its widget_classes table).
- **QCustomSlideMenu / QMainWindow json-styles sections use the NEW dict format** — the ancient list-of-dicts format in old demos crashes the current loader.
- **Shipped feather icons are black-stroked and `applyCompiledSass(generateIcons=False)` never recolors them** — on dark headers give icon buttons a lighter chip background (theme Other-variable) instead of expecting recolored icons.
- **QCustomSlideMenu regained `"auto"` sizing (2026-08-01)** (= content sizeHint) in calculateEndWidth/Height + getters, with real expand/collapse state tracking (`_animatingExpand`, `_menuOpen`); int and `"parent"` paths unchanged.
- **Code-side data colours: use `themeEngine.themeColor("NAME")`** to read a theme `Other-variable` — no `json.load` of style.json needed; re-apply on `onThemeChanged` and the hues flip with the theme.
- **scss string concat works for string qproperties**: `qproperty-iconPath: $PATH_RESOURCES + 'feather/send.svg';` — theme-recoloured icons with zero Python `setIcon` calls.
- **QCustomSocialButton `brand` set from a .ui property does not apply the brand's default caption** (ctor seeds text first; setBrand only fills empty text) — set the `text` property explicitly per button in the .ui.
- **Designer-authored children can't live inside a promoted container widget (e.g. QCustomCard) in the .ui** (uic would attach a second layout). Pattern: author the content as a sibling holder widget, then `card.addWidget(self.ui.holder)` in code — it reparents cleanly.
- **Never name app themes "Light"/"Dark"**: `createNewTheme` merges by name into the PREDEFINED engine themes (keeps `predefined=True`), so the boot fallback finds no non-predefined theme and the app runs the built-in look. App-specific theme names are load-bearing, not cosmetic.
- **QCustomQToolTip auto-closes after the filter duration (default 1500ms) and its paintEvent early-returns while closing** — a grab during fade-out shows children but no bubble; grab before the duration elapses.
- **QCustomTipOverlay sets Qt.Popup flags AFTER reparenting** (parent() set but isWindow()=True) — it is absent from window grabs BY DESIGN; verify with a widget grab.
- **/tmp/app-verify is shared between concurrent agents** (deleted/recreated mid-run) — write verification PNGs to a private directory.
- **THEME persists across runs (INIT-THEME-SET), so toggle-test results ALTERNATE between runs** — it looks exactly like "lost signal connections" (receivers()==1 but 'nothing happens'). Delete `~/.config/Custom Widgets/<App>.conf` for deterministic screenshots before blaming the wiring.
- **Generated `_styles.scss` puts a visible border on QScrollArea** — add `border: none` by objectName for borderless demo scrolls.
- **Promotability traps**: widgets whose first ctor arg is NOT `parent` (QCustomSpinner takes `lineWidth`, QFlowProgressBar takes the steps list) break `setupUi`'s positional parent when promoted in a .ui — use a holder layout + build in code. The four loader widgets take colours ONLY via ctor → feed them from a ChartPalette section in style.json. QCustomChipGroup's `closable`/`selectable` are ctor-only flags too — seed chips in code via `addChip(...)`.
- **The icons-qrc gate is vacuous in this fleet**: zero example .ui files use qrc iconsets — icons ride the `theme-icons:` SEARCH PATH (registered from `Qss/icons/` at QCustomTheme.py:770); the per-app `_icons.qrc` is a generated tooling artifact. Verify icon refs by resolving `theme-icons:<p>` against `<App>/Qss/icons/<p>` on disk. Fleet norm: the full 4475-icon generated set (empty/partial sets silently degrade UIs — generate via `themeEngine.generateNewIcons()`).
- **Headless runs never persist settings** (the survey runner exits via `os._exit`, QSettings never flush). To prove a `Default-Theme` really applies, run with a fresh `XDG_CONFIG_HOME` — the normal env is contaminated by the shared pre-identity conf.
- **Running any app regenerates `Qss/scss/_variables.scss` + `generated-files/css/main.css` to the machine's active theme** — modified entries for those files in `git status` after verification runs are benign artifact churn.
- **Generated `_styles.scss` out-specifics bare tab rules** (`QTabBar::tab:top:selected` ships there) — scope tab styling under the tab widget's ID (`#controlTabs QTabBar::tab`, `#controlTabs::pane`, `#controlTabs::tab-bar`); ID specificity always wins.
- **Qt QSS attribute-existence selectors (`[prop]`) are unreliable** — always enumerate values (`[tileKind="color"], [tileKind="gradient"], …`).
- **`QCustomFlowLayoutOrder` pins listed widgets even against runtime reordering** — for demos that shuffle/reorder, expose `orderJsonPath` as a toggle (empty string restores insertion order); unlisted widgets keep insertion order after the pinned ones.
- **Arbitrary runtime colours can't be tokenised** — replace "random hex" with a random pick from an enumerable theme palette (`$TILE_1..8` Other-variables) so randomness stays theme-consistent and lint-clean.
- **Painted knob/thumb colours need their own Other-variable** (`$KNOB`): `$COLOR_TEXT_1` goes near-black in light themes — caught only by inspecting the light-theme screenshot.
- **`QCustomQLabel` icons go through `qproperty-pixmap`** (labels have no icon property); per-name dynamic property + one scss rule per icon name is the clean data-driven-icon pattern. When icons are referenced only from scss, the engine registers `theme-icons:` itself during `applyCompiledSass` — no manual `QDir.addSearchPath` needed.
- **Tab titles need `&&` for a literal ampersand (mnemonic parsing); QLabel text does NOT** — `&&` renders doubled there.
- **The boot THEME fallback must filter to the app's OWN themes**: `[t for t in themeEngine.themes if not getattr(t,'predefined',False)]` — "Light"/"Dark" are ALWAYS in `themeEngine.themes`, so a membership test against all themes keeps a stale built-in name and the app compiles half-styled with the default #00bcff accent.
- **Other-variables accept `"rgba(r, g, b, 0.16)"` strings** (qtsass converts to Qt-safe %). NEVER 8-digit hex in scss — CSS reads #RRGGBBAA, Qt reads #AARRGGBB.
- **Lint baseline fingerprints are (rule+path+symbol+stripped line)** — editing a grandfathered file is safe only if offending lines stay byte-identical; NEW files get zero grace (no unicode arrows/moons/stars anywhere, including .ui strings — use feather arrow-up-right/-down-right pixmaps for delta arrows).
- **QCustomStatCard `delta` is NOT a Designer property** (only label/value/caption/trend) — a delta entry in a .ui is silently inert; call `setDelta()` in code.
- **QCustomTableToolbar's pill row min-width propagates through QScrollArea** and shoves content off-window — set `hsizetype=Ignored` on the toolbar in the .ui (pills then compress/elide gracefully).
- **QCustomProgressRing is fully colourable from scss** (`qproperty-ringColor/trackColor/textColor`) — zero Python.
- **QCustomSegmentedControl children are `QPushButton#segmentButton` with `[seg="first"/"last"]` props** for end-radius styling; guard the `currentChanged` slot against no-op re-selection when syncing index on theme change.
- **The svg-icon test class was order-dependent on global THEME state** (it inherited whatever an earlier test left; a colourless "Emerald" from the task-menu test made `generateNewIcons` resolve an empty colour and silently skip — masked for months because another test accidentally repaired the state first). Fixed with an autouse pinned-theme fixture in tests/test_svg_icons.py. Rule: any test whose fixture calls icon generation must pin `THEME` (+ `theme._theme`) itself, and `generateNewIcons` silently no-ops when the current theme's icons colour resolves empty — check `currentTheme.icons_color` before blaming the generator.
- **Tests must NEVER import a converted example app's main.py in-process**: module import runs `setProjectRoot(__file__)` (re-points the process-global project root) and construction runs the full boot (identity switch + theme registration) — it silently broke 16 icon-generation tests. Test compiled forms instead (`src.ui_X` with the app dir on sys.path — see tests/test_glasshome_example.py / test_release_starter_app.py), and evict cached `src` packages from sys.modules before/after (every example ships a package literally named `src`). Full app boot belongs to the headless survey runner (subprocess).
- **The pre-identity QSettings theme bug is FIXED at the library level (2026-08-01)**: `configure_settings` now applies the style.json `AppSettings` identity to QCoreApplication BEFORE any QSettings read; a persisted `THEME` only outranks `Default-Theme` when it names a theme the file actually defines; and `currentTheme`'s last-resort fallback prefers the declared default, then any custom theme, before the legacy name-"Light" guess. Regression: `tests/test_pre_identity_theme_default.py` + end-to-end repro (polluted `Unknown Organization/main.py.conf` → app still boots its Dark default). The per-app boot-order pre-set in examples remains as belt-and-braces.
- **QCustomButtonGroup.orientation setter FIXED (2026-08-01)** — it now genuinely swaps the layout at runtime (buttons/order/margins/spacing/selection preserved), so .ui-promoted groups can be horizontal. Same commit fixed `addButton(button_id=None)` crashing on the nonexistent `QButtonGroup.count()` (auto-ids now `len(buttons())`). Regression tests: `tests/test_button_group_orientation.py`.
- **design_lint flags hex fallback literals in Python** (`pal.get("k", "#hex")`) — index the palette with `[]` instead.
- **qtsass cannot parse the full Qt gradient syntax** (`qlineargradient(spread:pad, x1:0, …)`) — the scss compile fails and the app silently runs UNSTYLED native gray. The short form (`qlineargradient(x1:…, stop:0 $VAR, stop:1 $VAR)` as used in SmartHomeDashboard's chrome.scss) compiles; when in doubt use flat `$TOKENS` and verify the app is actually styled.
- **QSS selectors on layout names never match** (`#someLayout QPushButton` — layouts aren't widgets); select on container widget objectNames. Also a freshly copied `_variables.scss` lacks your custom Other-variables until a correctly-registered theme regenerates it — don't debug missing `$VARS` in scss before confirming the theme actually loaded.
- **Hand-written .ui: numeric layout props MUST be `<number>`-wrapped** — `<property name="spacing">20</property>` with bare text silently compiles to 0 (margins/spacing vanish, no warning).
- **QSS specificity**: `#container QPushButton` (1,0,1) beats `#myButton` (1,0,0) — per-widget overrides inside a styled container need the container prefix (`#container #myButton`), including their `[state=…]` variants.
- **`_styles.scss` paints QLabel backgrounds and styles QStackedWidget white** — add `QLabel { background: transparent }` and explicit transparent rules for stacked widgets/pages or container chrome gets masked.
- **QtLocation: never reassign `Plugin.name`/`Map.plugin` on a live Map — segfault** (write-once QML). Provider choice must exist before engine load (`facade.setTileProvider(...)` before `loadDefaultEngine()`); fixed 2026-08-01 in `Custom_Widgets/map/_qtlocation.py` (per-provider materialised QML; live `setProvider` warns-and-refuses). `itemsoverlay` is the deterministic offline provider; `CW_MAPVIEW_ONLINE=1` opts into OSM tiles.
- **`QCustomHeatmap.setData()` restored 2026-08-01** as a backward-compat alias for `setValues`.

### QSettings writes are expensive — write-if-changed only (fixed 2026-08-01)
An app boot was issuing ~47 `QSettings.setValue` calls (161 QSettings constructions): the theming code re-asserted `ICONS-COLOR`/`THEME`/`GENERATED-ICONS-COLOR` once per component / per `applyIcons` call. Every write marks the settings dirty and costs a `QLockFile` + `fdatasync` round-trip (0.1–0.3s on a loaded filesystem) at QSettings destruction — component-heavy apps (AuroraChat, GlassHome, FinanceDashboard, CashFlowDashboard, CheckBoxDashboard, QCustomMapView) took >40s to reach `app.exec()` and looked like hangs. Fix: `_setSettingIfChanged()` in `Custom_Widgets/theming/QCustomTheme.py` guards the five hot sites — a settings write must compare-before-write. If an app "hangs" on boot with no output, count `QSettings.setValue` calls before suspecting anything else.
