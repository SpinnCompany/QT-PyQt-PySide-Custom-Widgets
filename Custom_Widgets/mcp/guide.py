"""Agent operating guide for the Custom Widgets MCP.

Shipped WITH the MCP as the server `instructions`, the
`customwidgets://agent-guide` resource, and the AGENT_GUIDE symbol.
RULE #1 is hoisted to the very top so every agent meets it first.
"""
RULE1 = """\
========================================================================
 START HERE — RULE #1 (highest priority, read before anything else)
========================================================================
Before ANY task in a Custom_Widgets project:
  1. MOUNT this MCP (you are reading its guide, so you have) and keep using it.
  2. READ this whole guide + the customwidgets://skills resource FIRST.
  3. Do the ENTIRE build/run/observe loop THROUGH these tools — never via
     ad-hoc `python`/shell. Shell is only for bootstrapping Designer or the
     dev server. If a capability is missing, ADD it to this MCP.
If you cannot reach these tools, STOP and ask the user to mount the
`custom-widgets` MCP (`claude mcp add custom-widgets -- Custom_Widgets-mcp`,
or the repo's .mcp.json auto-mounts it) — do not fall back to a shell.
========================================================================

========================================================================
 RULE #2 — TARGET A PROJECT PER CALL, NEVER BAKE ONE IN
========================================================================
This server is PER-SESSION and DIR-AGNOSTIC. Do NOT pin it to a project
with `--project-dir` — that bakes one session's working folder into shared
config and collides with other sessions. Instead:
  - Mount it WITHOUT `--project-dir`. The default project is then the repo
    root (the server's cwd); it is only a fallback for calls that omit
    `project`.
  - Pass `project="/abs/path/to/examples/PySide6/<Project>"` on EVERY tool
    call. Absolute paths are used verbatim; relative paths resolve against
    the default. This is how one server drives any example/project.
  - Pass an `agent` name on mutating calls so ownership shows in
    workspaces_status. Call workspaces_status FIRST to see who is driving.
  - To move the session default at runtime (instead of remounting), use
    designer_open_workspace — do not edit .mcp.json mid-session.
========================================================================

"""


_BODY = """\
Custom Widgets MCP — operating guide for agents.

You are driving a Qt Designer + Custom_Widgets project for a user who is
WATCHING and LEARNING. Make your work visible and teachable — never edit
silently in the background when the user could watch instead.

== RULE #0 — THE FORMS PIPELINE *IS* THE PRODUCT (don't ship a pure-code app) ==
For any production-shaped build (app, dashboard, multi-page tool), the deliverable
is the maintainable pipeline: `.ui` forms -> compiled `src/ui_*.py`
(Custom_Widgets --convert-ui) + `json-styles/style.json` CustomThemes + `Qss/scss`
`$TOKENS` + a `GuiFunctions` orchestrator with per-page Managers and background
workers. A single hand-built `main.py` full of hard-coded hex is a FAILURE even if
it renders correctly — it throws away theming, Designer, and maintainability.
Switch themes BY NAME (`themeEngine.setTheme("<Custom Theme>")`), never the generic
Light/Dark toggle (it can't match a custom theme name). Colour charts from a
`ChartPalette` you read out of style.json so hues flip with the theme. Mirror the
examples/PySide6/AuroraDeckPro + WinningDashboard_CorrectArchitecture layouts.
Known traps: Qt QColor hex is `#AARRGGBB` (a faint white is "#14ffffff"); token
widgets (QCustomBadge…) need applyDesignTokens OR inline styling under
loadJsonStyle; a QtCharts pie collapses to a hairline in small panels — use the
painted QCustomDonut; wire the sidebar toggle once (or via toggleButtonName).

== WORKFLOW ==

1. BUILD AND RUN EVERYTHING VIA MCP. Do the whole loop — create/convert forms,
   run, observe, navigate — through these tools, not ad-hoc shell. Use Bash
   only to bootstrap Designer / the dev server. If a capability is missing, it
   should be ADDED to this MCP, not worked around.

2. SHOW FORM EDITS IN DESIGNER. When you create or edit a form (.ui), open it
   in Qt Designer and reveal THAT form so the user sees the change:
   designer_launch (if not running) -> designer_open_files([form]) -> edit via
   designer_set_widget_property, or build layouts/widgets by pushing .ui XML
   with designer_set_form_xml / designer_new_form_xml (Designer re-renders live)
   -> designer_screenshot to confirm. Do not hand-edit .ui files silently.

3. EDIT QSS/THEME IN THE QSS EDITOR. When changing styles or the theme, open
   the QSS/Theme editor so the user sees the stylesheet and learns to do it
   themselves: designer_qss_window(action='open') -> persist styles with
   project_write_style (it STREAMS the edited .scss live into the editor so the
   user watches it change) -> preview with designer_set_stylesheet and/or
   designer_qss_window(action='paint', enabled=true) -> designer_qss_screenshot.
   Never put styleSheet properties in .ui files.

4. RUN THE APP VIA DESIGNER'S RUN ONLY. To observe the running app, start it
   with designer_run_app (Designer's Run controller) — do NOT launch the app
   any other way. Then observe/navigate it: app_screenshot, app_object_tree,
   app_find, app_click, app_set_text, app_set_property, app_invoke. Stop with
   designer_stop_app; read output with designer_app_logs.

5. COMPONENTS ARE SEPARATE + HOT-RELOADED. Build reusable component forms on
   their own and embed them via a QCustomComponentContainer whose filePath
   points at the compiled component. Edit a component on its own and it
   hot-reloads in place in the running app.

6. KEEP RUNS VISIBLE, BUT DON'T MANAGE WINDOWS. Runs should produce real
   windows the user can watch. Do NOT focus, raise, move, or place windows —
   leave all window management to the user.

7. TEAR DOWN CLEANLY VIA MCP. To close Designer use designer_quit (marks forms
   clean so no "save changes?" prompt blocks exit — it reports had_unsaved_forms
   — then force-kills a hung instance) and designer_stop_app for the app — never
   leave orphaned windows/processes, and don't kill by shell pattern (it can
   match your own commands). Launch at most ONE Designer at a time. On startup
   Designer's blocking dialogs (New Form picker, recover-last-session prompt)
   are auto-dismissed. CLOSE the QSS editor when done with it
   (designer_qss_window(action='close')) — don't leave it floating.

8. LINK ICONS TO THE QRC. Every form that uses icons must reference the icons
   resource(s) via <resources> (Qss/icons/_icons.qrc, and the app's own
   assets qrc). The form-construction tools inject the icons qrc automatically
   when a form uses <iconset>; if you author .ui another way, include it.

== MULTI-PROJECT / MULTI-AGENT ==

Every tool takes an optional `project` (a folder — absolute, used verbatim; or
relative, resolved against the session default) and mutating tools take an
optional `agent` tag. The session default is the server's cwd (the repo root)
unless moved with designer_open_workspace; it is a FALLBACK only, so name your
project explicitly rather than relying on it. Do NOT mount with `--project-dir`
pinned to one example (see RULE #2) — it baffles other sessions. Different
projects are fully isolated (separate Designer/app sockets) and run in parallel;
the SAME project is serialized — a per-project queue funnels all bridge/app
commands so concurrent sessions/agents can never interleave against one
Designer/app. So:
  - To work on any example, pass project="/abs/examples/PySide6/Foo" (or a path
    relative to the repo root, e.g. project="examples/PySide6/Foo").
  - Call workspaces_status FIRST when others may be active: it lists each
    project's designer_running / app_running / queue_depth / busy / current
    owner, so you can pick a free project and see who is driving what. Pass an
    `agent` name on your mutating calls so that ownership shows up there.
  - Two agents on ONE project still share its single Designer/app (one at a
    time via the queue) — prefer giving each agent its OWN project folder.
  - designer_quit affects only THIS project by default; all_projects=True also
    kills Designers other agents are using and is refused without
    confirm='all-projects'.
For several sessions to share one server (and thus one queue per project), run
it once as a shared daemon: `Custom_Widgets-mcp --transport http --port 8765`
and point each .mcp.json at http://127.0.0.1:8765/mcp. Plain stdio (the default)
is one client per process and needs none of this.

== DESIGN RULES (ENFORCED — run design_lint) ==

The library ships a design-rule linter (Custom_Widgets.lint) that enforces the
VISUAL rules a type checker can't see. It runs automatically on every file edit
(project hook) and in CI/pre-commit; call the design_lint tool yourself before
you consider a screen done. Rules (full text: docs/design/design-rules.md):

  * glyph-icons   [error]   NEVER use a unicode glyph as an icon in button/label
                            text — geometric shapes, dingbats, arrows, emoji,
                            fullwidth symbols (a half-filled circle, a fullwidth
                            plus, a gear, a sparkle, a checkmark, and the like).
                            They don't recolour on theme, vanish when a rail
                            collapses, and render differently per font/OS. Use a
                            REAL icon — a themed SVG (qproperty-icon:
                            url(theme-icons:icons/<set>/<name>.svg) / setIcon) or
                            a painted QPixmap you recolour per theme (see
                            examples/PySide6/AuroraJobsTable `_icon`).
  * hardcoded-hex [warning] don't bury #rrggbb in chrome — drive colour from
                            token roles / a named ALL-CAPS palette constant so it
                            flips with the theme.
  * drop-shadow   [warning] no QGraphicsDropShadowEffect unless justified with a
                            trailing `# allow-shadow: <reason>`; prefer a
                            borderless fill + big radius for depth.

A NEW glyph-icons error will block the edit hook — fix it or, for a genuine false
positive, add `# noqa: <rule-id>`. Add/adjust rules in Custom_Widgets/lint/rules.py.

== BUILDING PROFESSIONAL SCREENS (how real Custom_Widgets apps are structured) ==

USE THE CUSTOM WIDGETS — that is the whole point of the library; do NOT default
to plain Qt when a Custom_Widgets class fits. To find the right one and how to
configure it, read the CATALOG first (widgets_catalog tool, or the
customwidgets://catalog resource): it lists every widget with its properties,
allowed enum values (variant/sizeVariant/...), signals and design tokens — so you
never guess a property name or value. For exact constructor/method signatures
call widget_signature (a live-generated .pyi — base class, signals, typed props,
every public method), since qtpy hides these from normal introspection. Preview
any widget in isolation with render_widget (headless offscreen PNG, no
Designer/app needed) before wiring it into a form. For HOW to wire it up, search
the bundled recipes with search_examples (e.g. "sidebar navigation with stacked
pages") and open the top hit. Go-to classes: QCustomSidebar +
QCustomSidebarButton (icon + labelText) and QCustomSidebarLabel for nav;
QCustomComponent as the root of every embeddable screen; QCustomQStackedWidget
for animated page routing; QCustomThemeList / QCustomThemeDarkLightToggle for
live theme switching (no code); QCustomCheckBox, QCustomQPushButton (variant),
QCustomFlowWidget (responsive wrap), QCustomHorizontalSeparator /
QCustomVerticalSeparator, QCustomQProgressBar, QCustomQDialog. Prefer per-<item>
alignment + size policies over QSpacerItem/separators wherever the layout can
express the gap that way — reach for a spacer only when alignment cannot.

== DESIGN FIDELITY: WIDGETS ARE FULLY CUSTOMIZABLE ==

Treat every Custom_Widget like an HTML element + CSS: it must be flexible enough
to reproduce an ARBITRARY design reference pixel-for-pixel. Widgets are NOT
tight or one-look — the library's whole value is that a developer can bend a
widget to any brand or mockup.

- When matching a reference image, diff it ELEMENT-BY-ELEMENT (alignment, font
  weight/size hierarchy, glyphs, colours, affordances like sort carets / gears /
  carets), not with a "looks close" glance and not on green tests alone. Own
  every gap you find.
- If the widget can't hit some detail, the fix is to ADD THE HOOK to the widget,
  not to accept the limitation or call it close enough. Expose it as an opt-in
  setter/Property that DEFAULTS TO THE CURRENT behaviour (never break existing
  looks) and, for colours, that can track the active theme. Prefer many small
  orthogonal knobs over a single "style" enum. Then EXTEND THIS MCP / the widget,
  and note the new knob in the catalog.
- PROMOTE, DON'T HAND-PAINT. When a design needs a data surface NO existing
  widget covers, BUILD a real widget (painted; WIDGET_* metadata + a __catalog__
  entry + typed @Property inputs, e.g. a `valuesCsv`-style string), register it,
  stub it, THEN use it — never leave a hand-painted surface living in a Manager /
  GuiFunctions. Anything hand-rolled in GuiFunctions is the signal for a missing
  widget. Widget-authoring gotchas: (a) do NOT give a method and a @Property the
  same name — the Property shadows the method, so `w.count()` throws "int object
  is not callable"; expose the read via the Property only. (b) Use real
  `QFontMetrics.height()` (not the point size) to size a painted label band or the
  text clips at the bottom edge. (c) A new `QCustom*.py` only appears in
  widgets_catalog / render_widget after a SERVER RESTART (the catalog is
  lru-cached per process) — until you restart, validate the new widget with
  `stubgen` (it imports each module) + the live app.
- Reference: QCustomDataTable exposes per-column `align`, twoline subtitle
  scale/weight, kebab colour + status-dot size, and opt-in header affordances
  (persistent per-column sort carets, select caret, actions gear) — enough to
  match a real SaaS "Jobs" table exactly (examples/PySide6/AuroraJobsTable).
- Verify rendering with a PIXEL PROBE (render_widget / grab -> toImage ->
  pixelColor) under a stable harness, never by eyeballing a downscaled shot.
  BUT offscreen != the real display: anything font/metric/style-sensitive (text
  metrics, delegate paint, pill/border-radius, hover/focus, native style) MUST be
  verified on the REAL running window via the MCP (designer_run_app ->
  app_screenshot) — offscreen grabs missed three real-display-only bugs (a
  pixel-sized-font subtitle collapse, square-instead-of-pill radius, a starved
  Stretch column). Use offscreen probes for colour/geometry; use the live window
  for anything the platform font/style engine touches, and keep a pytest probe
  that forces the failing condition so the bug stays reproducible headlessly.

COMPOSITION
- ONE top-level window: class QCustomQMainWindow (extends QMainWindow). Every
  other screen is a QCustomComponent (extends QWidget); modals are a root
  QCustomComponentContainer. Compose by placing a QCustomComponentContainer
  whose filePath property points at the COMPILED child (src/ui/ui_<Name>.py),
  previewComponent=false in production — never manually addWidget a child form.
- In Python reach an embedded component via container.component, chained for
  depth (parent.component.childContainer.component). Managers reference widgets
  by objectName, so objectNames are a stable public API — don't rename without
  updating code. Give every code-referenced widget a meaningful objectName.

NAVIGATION
- Route screens with a top-level QStackedWidget plus an inner ANIMATED
  QCustomQStackedWidget. Switch with setCurrentWidget(<pageWidget>), NEVER by
  index. Sidebar buttons call a navigateTo(name) that maps name -> page widget,
  switches, sets the active button, and lazy-inits the page.
- Track the ACTIVE page yourself and RE-ASSERT setChecked(True) on the active nav
  button whenever you repaint chrome — a theme switch or a sidebar collapse/expand
  can steal an autoExclusive checked state, so isChecked() is NOT trustworthy
  after one.
- QCustomSidebarButton auto-shows its labelText on expand and hides it on collapse
  — "no label when expanded" just means labelText was never set (set labelText,
  not text). Style it text-align:left + padding-left so the icon still centers when
  the rail is collapsed.

LAYOUT
- Zero the ROOT layout margins/spacing so components own their padding. Inside,
  use the spacing scale 0/10/16/20/24/40 (matches the SCSS tokens).
- Wrap tall pages in a QScrollArea (widgetResizable=true) over a zero-margin
  content layout. Drive responsiveness with size policies (Expanding for the
  flexible column, Preferred for fixed panels) + per-<item> alignment rather
  than spacers; pin sizes with minimum/maximum (16777215 = unbounded). Group
  cards with QFrame frameShape=StyledPanel + frameShadow=Raised.

CUSTOM WIDGETS & PROPERTIES
- ALL Custom_Widgets-specific properties use stdset="0" (dynamic props);
  standard Qt props (sizePolicy, minimumSize, text, icon) do not. Examples:
  QCustomSidebarButton uses labelText (not text) + textPrefixSpaces;
  QCustomSidebar has toggleButtonName/collapsedWidth/expandedWidth;
  QCustomQStackedWidget has slideTransition/transitionDirection/transitionTime;
  QCustomFlowWidget order is data-driven via orderJsonPath -> style.json
  QCustomFlowLayoutOrder. Declare every promoted widget in the form's
  <customwidgets> block (class/extends/header, <container>1 for containers).
- .ui custom-property order is NOT guaranteed against dependencies — a widget's
  activeIndex/selected prop can be applied BEFORE its count/data prop, so set
  index-dependent props from the Manager in code (after setCount/data), not in
  the .ui.

THEMING
- Keep colors/fonts/flow-order in json-styles/style.json (CustomThemes each
  with Background/Text/Accent/Icons colors + Other-variables incl. _R/_G/_B
  triples for rgba). The startup theme is the form's appTheme property.
  QCustomThemeList / QCustomThemeDarkLightToggle auto-switch themes (no code).
- App styles go in Qss/scss/defaultStyle.scss: objectName-nested selectors
  using $TOKENS ($COLOR_ACCENT_1, $COLOR_BACKGROUND_1, $SPACING_*, ...) with
  &:hover/&:pressed states. NEVER edit _variables.scss (generated) or
  _styles.scss (base), and never hard-code hex in .ui. Persist via
  project_write_style.
- ICONS/PIXMAPS ARE SET IN DESIGNER OR QSS, NEVER FROM PYTHON. Declare each icon
  in the .scss by objectName: `#navHome { qproperty-icon:
  url(theme-icons:icons/feather/home.svg); }` on an icon-bearing widget
  (QToolButton/QPushButton/QCustomSidebarButton, iconSize in the .ui). The
  `theme-icons:` search path recolours the asset to the theme's Icons-color
  automatically. On a theme switch Python ONLY re-polishes to reload the
  recoloured icons — `w.style().unpolish(w); w.style().polish(w)` — it must NOT
  call setIcon()/setPixmap(). (A QLabel pixmap you must use: set it in Designer
  with scaledContents.) Because icons take ONE Icons-color per theme, a rail that
  must stay dark in a light theme can't use theme-icons — make the rail a themed
  QCustomSidebar so the single Icons-color contrasts everywhere. This does NOT
  cover delegate/chart PAINT colours (DataTable setCellAccentColor, chart series):
  those come from theme roles in code and are reapplied on onThemeChangeComplete.
- DataTable/Toolbar in the pipeline: place them in the .ui (objectNames only) and
  configure DataTable COLUMNS + Toolbar STATUSES in the Manager in code (Designer
  can't set them, like chart series). Style the internal view via #dataTableView
  selectors. Row separators must come from the delegate
  (table.setRowSeparatorColor) — rich cells are custom-painted and miss a QSS
  ::item border, so some cells get a separator and some don't.

APP WIRING
- Boot order (each step guarded): setupUi -> loadJsonStyle(self, self.ui,
  jsonFiles={"json-styles/style.json"}) -> show() -> QAppSettings.updateApp
  Settings(self) -> app logic. Keep main.py minimal; put logic in a central
  orchestrator (a "GuiFunctions") holding one Manager(QObject) per screen and
  calling each manager.initialize(). A manager grabs container =
  ui.<x>ComponentContainer, component = container.component, and wires
  component.<child> signals + worker signals.
- Workers run in background and only emit Qt signals (Worker -> Signal -> GUI
  slot); never touch widgets from a worker. Toggle QSS state with
  setProperty(key,value) then style().unpolish()/polish() (camelCase signals:
  past-tense success, Failed/Changed suffixes).

FILE LAYOUT: ui/<Name>.ui (class <Name>) -> compiled src/ui/ui_<Name>.py
(class Ui_<Name>); generated-files/ holds intermediates; theme in
json-styles/style.json + Qss/.

The goal is not just to produce a GUI, but to let the user SEE and LEARN the
Custom_Widgets workflow.
"""

AGENT_GUIDE = RULE1 + _BODY
