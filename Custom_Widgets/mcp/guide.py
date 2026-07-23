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
`custom-widgets` MCP (`claude mcp add custom-widgets -- Custom_Widgets-mcp
--project-dir .`, or the repo's .mcp.json auto-mounts it) — do not fall back
to a shell.
========================================================================

"""


_BODY = """\
Custom Widgets MCP — operating guide for agents.

You are driving a Qt Designer + Custom_Widgets project for a user who is
WATCHING and LEARNING. Make your work visible and teachable — never edit
silently in the background when the user could watch instead.

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

== BUILDING PROFESSIONAL SCREENS (how real Custom_Widgets apps are structured) ==

USE THE CUSTOM WIDGETS — that is the whole point of the library; do NOT default
to plain Qt when a Custom_Widgets class fits. Go-to classes: QCustomSidebar +
QCustomSidebarButton (icon + labelText) and QCustomSidebarLabel for nav;
QCustomComponent as the root of every embeddable screen; QCustomQStackedWidget
for animated page routing; QCustomThemeList / QCustomThemeDarkLightToggle for
live theme switching (no code); QCustomCheckBox, QCustomQPushButton (variant),
QCustomFlowWidget (responsive wrap), QCustomHorizontalSeparator /
QCustomVerticalSeparator, QCustomQProgressBar, QCustomQDialog. Prefer per-<item>
alignment + size policies over QSpacerItem/separators wherever the layout can
express the gap that way — reach for a spacer only when alignment cannot.

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
