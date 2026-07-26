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

9. ICONS: file from Designer/QSS url, COLOUR from iconColor (never setIcon in
   Python). Set the icon FILE the normal way — in the .ui (Designer `icon`/
   iconset) for design-time preview AND at runtime from QSS with the path
   variable (a .ui iconset alone can be blank at runtime — setupUi builds the
   QIcon before the `theme-icons` search path is registered — so the QSS url is
   what reliably renders it):
       #saveBtn { qproperty-icon: url($PATH_RESOURCES+'material_design/save.svg'); }
   ($PATH_RESOURCES = `theme-icons:icons/`.) Then set the icon COLOUR from QSS:
   QCustomQPushButton / QCustomSidebarButton TINT that icon to `qproperty-iconColor`
   (resting) and `qproperty-iconColorActive` (while CHECKED), so a SELECTED button's
   icon turns accent and the colour tracks the theme — no Python, no iconName:
       #navHome { qproperty-icon: url($PATH_RESOURCES+'feather/home.svg');
                  qproperty-iconColor: $muted;
                  qproperty-iconColorActive: $accent; }   /* checked icon -> accent */
   The active colour is a BASE-rule property (iconColorActive) the button swaps to
   on toggle — NOT a `:checked { qproperty-iconColor }` rule, because Qt does not
   re-apply qproperty-* from a pseudo-state selector on state change. Set iconSize
   in the .ui. (Leave iconColor unset to just show the plain themed icon.)

10. NEST QSS PER COMPONENT, keyed by the component's objectName. Don't scatter
    flat global `#childObjectName` rules — wrap each component's chrome in a block
    selected by the component root's objectName and NEST the child rules inside,
    one self-contained block per .ui component:
        #CanvasComponent   { #canvasFrame { background-color: $COLOR_BACKGROUND_1; } }
        #ThoughtsComponent { #thoughtsTitle { color: $COLOR_TEXT_2; } QCustomCodeEditor { … } }
        #topBar            { #exportBtn { …; &:hover { … } } }
    `&` for state/pseudo. The component root objectName is the .ui <class>/root
    name (e.g. CanvasComponent) and matches the loaded root widget at runtime.

11. EVERY CUSTOM WIDGET YOU CREATE EXPOSES ITS CONFIG TO DESIGNER. Every
    configurable thing (colours, sizes, counts, text, enums, toggles) is a typed
    `@Property` AND is listed in `DESIGNER_CUSTOM_PROPS = [{name,kind,group}]`
    (and `__catalog__` for the MCP). `@Property(QColor/int/str/bool)` auto-appears
    in Designer's property editor; DESIGNER_CUSTOM_PROPS gives the Custom-Properties
    dock its typed editors. No widget ships with config reachable only from Python
    — if it's tweakable, it's a Designer property. (Inherently dynamic data — a
    node graph's nodes/edges, a table's rows — is set via a method, not a property.)

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
                            borderless fill + big radius, or a PAINTED glow/bloom
                            or shadow shape (theme-aware, no waiver), for depth.
  * large-icon    [warning] large images belong on a QPixmap, not a QIcon —
                            setIconSize(QSize(N,N)) with a LITERAL N>=40 is
                            flagged (QIcon caps + softens when scaled up). Use
                            QLabel.setPixmap / QPainter.drawPixmap at 2x; keep
                            setIcon for small (<=~22px) button glyphs. Suppress a
                            deliberate case with `# allow-large-icon: <reason>`.

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

- AIM PREMIUM & CREATIVE — NO CEILING. A new widget should be the BEST version you
  can imagine, not the minimum that works. There is explicitly NO LIMIT on
  creativity, usability, scalability, styling, or modernization — push every one
  as far as it goes. Ship instrument-grade, skeuomorphic-MODERN finishes where
  they delight (beveled metal rims, domed faces, brass ticks, metallic caps — see
  QCustomCompassDial; neon glow, gradients, depth), rich interactivity
  (hover/zoom/search/drag/animate), and enough orthogonal knobs to bend to any
  brand. A plain flat version is a fine baseline, but a PREMIUM CREATIVE variant
  is always welcome — add it as a NEW widget (a `Dial`/`Pro`/styled sibling),
  never by downgrading a shipped one. There is no "too fancy" here — only
  "not painted / not themed / not maintainable / doesn't scale", which the
  conventions already prevent. Match the reference, then ask "what's the more
  delightful version?" and build THAT.
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
- EXHAUST THE VARIATION SPACE UP FRONT — don't build the one look a single
  reference shows and stop. As you design a widget, enumerate EVERY plausible way
  a designer might want it and expose each as an opt-in knob (defaulting to the
  look you already ship). For a painted primitive ask: can the SHAPE change
  (arc <-> full circle <-> semicircle via startAngle/spanAngle)? can the SCALE be
  shown as ticks AND/OR a dotted guide ring AND/OR numeric labels, independently?
  can the CENTRE hold a value + unit, centred, and be overridden? can the ACTIVE
  element be emphasised (the leading tick longer/brighter, the reached point
  marked)? can the ends be ROUNDED or flat (arc "border radius")? do value changes
  ANIMATE? can every COLOUR, WIDTH, GAP, RADIUS, COUNT and ANGLE (start / span /
  offset) be set? Ship the knobs even when the immediate demo uses one combination
  — flexibility is the product, and the next reference will want a different
  combination. WORKED EXAMPLE: QCustomRadialGauge is ONE widget that flexes to
  needle-speedometer, semicircle threat gauge, radial-tick timer, full-circle dial
  and countdown via gaugeStyle + startAngle/spanAngle (any start point / full
  circle) + zones/gradient + roundedCaps + animated/animationDuration + showGuide
  (dashed inner scale, both styles) + scaleLabelEvery (numeric scale labels) +
  emphasizeActiveTick + centerText/centerSuffix — not five separate gauge classes.
- DEPTH: SHADOWS, GLOW & BLUR ARE PART OF THE LOOK. Modern references use
  elevation and neon glow, not flat outlines — add them where they add depth (a
  glowing active arc/bar, a soft drop shadow under a raised card, a blurred
  frosted panel). PREFER PAINTED depth so it recolours with the theme and stays
  crisp at any DPI: a GLOW = re-stroke the value shape a few times at growing
  width + falling alpha (a cheap bloom that reads like a Gaussian blur); a SHADOW
  = an offset dark shape or a radial-gradient falloff; a FROSTED panel = a
  pre-blurred backdrop pixmap. Expose them as opt-in knobs (glow / glowStrength /
  glowRadius, shadowColor / shadowBlur / shadowOffset) defaulting OFF so existing
  looks are untouched. QGraphicsDropShadowEffect / QGraphicsBlurEffect are fine
  for genuine elevation but (a) trip the `drop-shadow` lint rule unless justified
  with a trailing `# allow-shadow: <reason>`, and (b) do NOT theme-flip on their
  own — recolour them on theme change. WORKED EXAMPLE: QCustomRadialGauge `glow`
  paints a theme-aware neon halo behind the value arc / lit ticks via the
  re-stroke bloom — no effect object, no lint waiver, flips colour with the zone.
- MAKE IT INTERACTIVE, AND USE CUSTOM (NOT NATIVE) TOOLTIPS. A static painted
  chart is a first draft; the product is the interactive one. Where a reference
  shows affordances — zoom (± control / wheel / drag-pan / double-click reset),
  SEARCH (dim non-matches, highlight matches), HOVER feedback (grow / glow / a
  detail popup), click/select — BUILD them in, don't ship a picture. And NEVER
  use the OS tooltip (`QWidget.setToolTip()` / `QToolTip`) for rich hover info in
  a modern UI: it renders an unthemed native box that clashes with the design.
  We have modern widgets — PAINT a custom tooltip card (rounded, category dot +
  label + value) or reuse `QCustomPopover` / `QCustomToast`, styled like the app,
  so the hover detail looks like it belongs. WORKED EXAMPLE: QCustomBubbleChart
  ships a painted tooltip card + hover grow/glow + wheel/± zoom + drag-pan +
  `setSearchQuery` dimming + a painted zoom/search control — not `setToolTip`.
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
  `stubgen` (it imports each module) + the live app. (d) FLEX-SIZE the paint, do
  NOT hardcode fractions of the widget. A painted widget that stacks content
  (e.g. an arc + a big value + a status badge, or a chart + axis labels) must
  SOLVE for the primary dimension so the WHOLE stack fits the box at any size —
  `r = min(width_limit, (height - pad) / (top_extent + reserved_below))` — and
  scale fonts/sub-elements off that solved size. Fixed fractions like
  `cy = 0.6*h; fontsize = 0.3*r` look fine at the size you tested and then CLIP
  (badge cut off) or overlap (value under the hub) when the widget is larger,
  shorter or wider. Reserve explicit room for every stacked element (including
  outside labels above and the value/badge below) and verify at BIG, SHORT and
  WIDE sizes, not one. Overlap check: keep a min-clearance between a moving part
  (needle hub) and text (`center_y >= hub + gap + fontHeight/2`). (e) CALCULATE
  TEXT SIZE TO FIT — painted text must never overflow its container OR get
  truncated. MEASURE the string with `QFontMetrics.horizontalAdvance()` against
  the available width and scale the FONT down to fit
  (`font.setPointSizeF(pt * maxW / adv)` when `adv > maxW`); don't pick a fixed
  point size and hope, and don't just paint into a too-small rect (it clips). A
  centre readout of variable-length strings (a compass "N" vs "SSW", a value "9"
  vs "1234") must shrink for the long ones — QCustomCompass fits its 16-point
  readout to the hub this way. Elide (`fm.elidedText`) ONLY when truncation is the
  intended design (a bubble label, a list cell), never as a substitute for
  sizing the box or the font.
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
- ABSOLUTE RULE (user-stated): ALL styling comes from QSS/SCSS files. In Python
  you may ONLY setProperty (incl. custom-widget Qt properties like
  card.scrimColor, btn.iconColor), style().polish()/unpolish(), and CONTENT
  (setText). NEVER setStyleSheet(...) anywhere — not the window, a region
  container, a code-built row, or a child. Standard-widget chrome (bg/border/
  radius/font, :hover/:checked/[prop]) go in chrome.scss by objectName; painted
  custom widgets get colours from their Qt properties; dynamic-created widgets
  get setObjectName + a dynamic prop (setProperty("muted",True)) styled by the
  GLOBAL app QSS (which cascades to them — a per-region container setStyleSheet
  is banned). The MAIN GOAL of Custom_Widgets is to ELIMINATE/REDUCE user GUI
  code: the framework does the work, the manager just feeds DATA + wires signals.
- ICONS/PIXMAPS/SIZES ARE SET IN THE .ui (Designer); dynamic aspects (colour) via
  a widget property or QSS. Prefer the QSS-recolour icon widgets:
  QCustomQPushButton and QCustomQLabel take `iconName` (feather/material name or
  .svg path, set in the .ui) + `iconSize` (.ui) and recolour the SVG to a QSS
  `iconColor` property — which, unlike the single-colour `theme-icons:` path,
  follows ANY token AND state selectors: `#navHome{qproperty-iconColor:$muted}` /
  `#navHome:checked{qproperty-iconColor:$accent}`. Zero Python icon code.
- KNOWN GAP: `qproperty-*` colours (painted-widget colours, icon colours) do NOT
  reliably re-apply on a LIVE theme switch (the app can hold a stale compiled
  stylesheet). Until the theme engine fully re-applies + unpolish/polishes the
  tree on switch, either reapply those colours via setProperty on
  onThemeChangeComplete (allowed) or force a full repolish there.
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

== HARD-WON GOTCHAS (read before debugging layout / theme / previews) ==
- DIAGNOSE LAYOUT FROM REAL GEOMETRY, NOT SCREENSHOTS. A downscaled app_screenshot
  lies about spacing. When "icon almost touches the value" / rows look wrong, read
  the actual rects with app_object_tree and compute the gap
  (valueTop - (iconTop+iconH)). ROOT CAUSE pattern: a card in a scroll area whose
  total content exceeds the viewport gets PINNED to its `minimumSize` (the layout
  distributes minimums, not sizeHints), so a card min-height SMALLER than its
  content squeezes the rows until they OVERLAP. Raising the inner VBox `spacing`
  makes it WORSE (the card can't grow). FIX: raise the CARD's minimumSize height to
  fit margins+rows+spacings.
- native="true" QWidget CONTAINERS PAINT THE PALETTE BACKGROUND (a white box in a
  light theme / dark box in dark). Invisible on a matching card, but a visible box
  on a COLOURED surface (e.g. a % delta on a teal banner). FIX: make the holder
  transparent (`w.setStyleSheet("background:transparent")` +
  `w.setAttribute(Qt.WA_TranslucentBackground, True)`), or don't mark it native.
- THE SCSS ENGINE HAS NO `_R/_G/_B` rgba TRIPLES unless the active theme declares
  `Other-variables`. A stray `rgba($COLOR_ACCENT_1_R, …)` raises "Undefined
  variable" and silently FAILS THE WHOLE scss compile -> the app renders UNSTYLED
  (looks like the wrong/dark theme). For tints use base tokens
  ($COLOR_ACCENT_1 / $COLOR_BACKGROUND_3), or add Other-variables to the theme.
- TOP-LEVEL POPUPS (Qt.Popup, e.g. a QCustomMenu) are NOT captured by
  win.grab()/app_screenshot (grab only sees the main window tree). They ARE on the
  user's screen. Verify them with a headless `panel.grab()` pytest, not
  app_screenshot. A child-overlay modal (parented to the window) IS captured.
- SEED GUARDED DEMO DATA in a painted / data-driven widget's __init__ so it PREVIEWS
  in Designer + render_widget (an empty QCustomDivergingBarChart/CardStack/Menu
  paints nothing). The app replaces the seed the moment it calls setData()/setCards()
  — gate the manager's "build vs recolour" on a `_built` flag, and give the widget a
  clear()/clearContent() so seeds don't accumulate.
- A NEW QCustom*.py needs a DESIGNER restart (designer_quit -> designer_launch) to
  appear in the palette; render_widget/widgets_catalog usually pick it up without a
  full MCP restart — confirm with render_widget (no unknown_widget = available).
- MCP COLD-COMPILE TIMEOUT: on a cold .pyc cache the server can miss its connect
  handshake window and never mount. Pre-warm with `python -m compileall Custom_Widgets`
  then reconnect. Do NOT silently fall back to ad-hoc python/shell for build/run —
  that breaks RULE #1; if the MCP is unreachable, say so and get it mounted.
- PAINT AN AFFORDANCE, DON'T TYPE A GLYPH. A modal close "x" as button TEXT is a
  glyph-icons lint ERROR (blocks the edit). Paint the X in a tiny QPushButton
  subclass (recolours with the theme), or use a themed SVG icon.
- REMOTE FONTS: `json-styles Fonts.LoadFonts[]` accepts `{"name","url"}` (downloaded
  + cached by Utils.download_font; TTF/OTF only, NOT woff2) as well as `{"name","path"}`;
  `Fonts.DefaultFont` applies the family APP-WIDE. Use it to ship a brand/web font
  (e.g. Inter) — the bundled Rosario often fails to load and Qt falls back to a
  mono/system font, so the whole UI looks off until you set a real sans.

FILE LAYOUT: ui/<Name>.ui (class <Name>) -> compiled src/ui/ui_<Name>.py
(class Ui_<Name>); generated-files/ holds intermediates; theme in
json-styles/style.json + Qss/.

The goal is not just to produce a GUI, but to let the user SEE and LEARN the
Custom_Widgets workflow.
"""

AGENT_GUIDE = RULE1 + _BODY
