# Modernization roadmap: closing the gap with modern UI toolkits

**Status:** Proposed / not started
**Owner:** TBD
**Created:** 2026-07-22

## Summary

A gap analysis of QT-PyQt-PySide-Custom-Widgets against what modern web, mobile,
and desktop UI toolkits (shadcn/ui, MUI, Ant Design, Chakra, Flutter/Material 3,
SwiftUI, Jetpack Compose) treat as table stakes — plus two strategic threads the
project is uniquely positioned to own: **running/developing from the web** and an
**agent-native MCP** workflow (dev → preview → test → build).

This is an internal implementation roadmap for the code repo. User-facing docs
live in the separate Docusaurus repo.

## What we already ship (baseline)

Strong, distinctive coverage today:

- Theming via JSON/QSS (`JSonStyles`, `QCustomTheme`), dark/light toggle
- Animated stacked widgets, slide menus, sidebar/navigation system
- Charts (`QCustomCharts`), progress bars, loading indicators
- Modals, tooltips, tip overlays, badges, avatars, tag edit, emoji picker, QR
- Code editor with syntax highlighting/themes
- Window effects: acrylic / blur (Mica-style)
- Qt Designer integration + plugins + a Designer-bridge **MCP server** (21 tools)
- Project scaffolding / `.ui`→`src` conversion, SCSS pipeline (see scss-engine.md)

## Gap analysis

### 1. Component library completeness
Missing workhorse components that every serious app needs (ranked by demand):

- **DataTable / DataGrid** — sortable, filterable, paginated, **virtualized**
  (recycled rows for 100k+), inline edit, column resize/reorder, selection.
  *Single biggest gap.*
- **Date / time / calendar pickers** and **range pickers**
- **Combobox / autocomplete** (searchable select) and **Command palette (⌘K)**
- **Toast / snackbar** system (non-blocking, queued — sibling to existing modals)
- **Tabs, Accordion, Tree view, Breadcrumbs, Stepper/Wizard, Drawer, Popover,
  Context menu**
- **Skeleton loaders** (content-shaped placeholders vs. spinners)
- **File dropzone, rating, color picker, rich-text editor, carousel, timeline,
  empty-state**

### 2. Variants, sizes, and design tokens
The core reason modern kits feel consistent and ours feels bespoke:

- **Variant + size props on every component**: `variant="primary|secondary|ghost|
  outline|destructive"`, `size="sm|md|lg"`. Replaces per-instance QSS with a
  consistent API. *Highest ergonomic leverage.*
- **Design tokens**: semantic scales for spacing, radius, typography, elevation,
  and *semantic* colors (`surface`, `on-surface`, `muted`, `accent`) — not raw
  hex. Reference: Material 3 + Tailwind token model. Makes theming composable.

### 3. Reactivity / data binding
Every modern toolkit is declarative + reactive; Qt Widgets is imperative. Add a
**lightweight binding layer**: bind a widget property to an observable/model and
auto-update. Highest-leverage *differentiator* — no Qt widget library does this
well. Does not require abandoning Qt Widgets.

### 4. Forms & validation
No form-state story (React Hook Form / Formik / Zod equivalent): field binding,
validation rules, error display, dirty/touched tracking, submit handling.

### 5. Accessibility (a11y)
Largely absent across Qt custom-widget libs — a real differentiator if nailed:
keyboard nav & focus order, visible focus rings, `QAccessible` roles for screen
readers, `prefers-reduced-motion`, high-contrast theme. Increasingly a
compliance/procurement requirement.

### 6. Responsive & adaptive layout
No responsive system. Add **breakpoint-aware containers** (collapse sidebar under
a width, reflow grids), first-class **high-DPI / multi-monitor** correctness, and
**touch gesture** support.

### 7. Motion system
Beyond `QPropertyAnimation`: **spring/physics presets, state-transition
animations, page transitions, micro-interactions**, exposed declaratively
(`animate="fade|slide|spring"`). Reference: Framer Motion, SwiftUI.

### 8. Developer experience & tooling
- **Hot reload** for QSS/JSON *and* layout (extend `FileMonitor` into true live reload)
- **CLI that adds components on demand** (shadcn model: `add datatable`) rather
  than one monolith import
- **Interactive component playground / gallery** (Storybook-equivalent) with
  copy-paste snippets — major adoption driver (see Web thread below)
- **Starter templates**: dashboard, settings app, CRUD admin

### 9. Native OS integration
System tray + native notifications, OS dark-mode auto-follow, taskbar/dock badges
& progress, native menus. Extend existing acrylic/blur into a coherent "native
feel" layer.

### 10. Distribution & i18n
- **Packaging / auto-update** recipes + an updater widget (the thing Electron
  makes easy and Python makes hard)
- **i18n / RTL** support (translation hooks, mirrored layouts)

## Strategic thread A — Run & develop from the web

Three viable paths, different maturity:

1. **Qt for WebAssembly** (compile to browser via Emscripten; PySide6 WASM wheels
   are **experimental**). Limits: single-threaded default, large download, one
   top-level window, constrained clipboard/fs/native. **Best near-term use: docs
   playground / widget gallery / shareable demos** — "try the widgets in your
   browser," like shadcn's site. Ties into Gap #8.
2. **Server-side render + stream** (noVNC/VNC or WebRTC frame streamer). Runs the
   *real* full stack today; heavier to operate. Good for cloud/agent preview and
   "run from web" without a WASM rebuild.
3. **Browser-based development** — cloud IDE editing the project while the app
   renders via (1) or (2). This is where MCP plugs in (Thread B).

Out of scope: NiceGUI/Streamlit "Python-to-web" are *different frameworks*, not
our Qt widgets — only relevant if we ever want a separate web target.

## Strategic thread B — Agent-native MCP (dev → preview → test → build)

Today's MCP server (21 tools) targets **Qt Designer + scaffolding only**. To
support *full agent development*, add tool families that target the **running
app** and the **build pipeline**:

- **Runtime preview**: launch the *compiled app* (not just Designer), screenshot
  it, read stdout/logs — real-app feedback loop.
- **Interaction / testing**: click/type/assert on the running app (pytest-qt
  style), widget-state queries, **visual-regression snapshots**.
- **Build / package**: PyInstaller/Nuitka packaging, wheel build, **WASM build**
  for the playground (Thread A).
- **Component-catalog introspection**: machine-readable registry so an agent can
  query available widgets + their variants/props/slots (depends on Gap #2) and
  assemble UIs correctly.
- **Theme / token tools**: read/write design tokens, generate & preview a theme
  (depends on Gap #2).

Outcome: an agent can scaffold → build UI → theme → preview → test → package
end-to-end. Almost no GUI toolkit is designed for this — a genuine differentiator.

## Suggested priority order

Top 5 to move the needle first:

1. **DataTable (virtualized) + Combobox + Toast + Date picker** — closes the
   "can I build a real app?" gap (Gap #1).
2. **Variant/size API + design tokens** — instant modern consistency; unblocks
   MCP catalog + theme tools (Gap #2).
3. **Reactive binding layer** — unique differentiator (Gap #3).
4. **Forms + validation** (Gap #4).
5. **Accessibility baseline + hot reload** — compliance win + DX win (Gaps #5, #8).

Parallel strategic bets, both high-differentiation and mutually reinforcing:

- **A:** WASM playground for the docs/gallery.
- **B:** Extend MCP to runtime preview + testing + build.

## Decisions (2026-07-22)

Locked via planning quiz:

- **First deep-dive:** variant/size + tokens → see `variant-token-system.md`.
- **Token format:** clean-break new schema (no compat shim over the old flat
  4-color theme model).
- **Token model:** hybrid — Tailwind-like primitives + Material-3-like semantic roles.
- **Variant mechanism:** Qt dynamic properties + QSS attribute selectors
  (Designer-editable, runtime hot-swappable).
- **Pilot scope:** `QCustomQPushButton` first, then template the rest.
- **Catalog:** machine-readable catalog hooks included from day one (for MCP).
- **Binding layer:** minimal in-house observable + `bind()` on Qt signals/props;
  deferred behind tokens/components.
- **Web/WASM:** docs playground / gallery only, not a supported deploy target.
- **MCP:** extend the existing 21-tool Designer bridge to runtime preview +
  testing + build; deferred behind the token work.

## Open questions (still unresolved)

- Token file split: primitives (shipped) vs semantic (per-project override)?
- Old `Accent-color` themes: one-shot migration script vs full re-authoring?
- SCSS `token()` function vs plain SCSS variables — decide with scss-engine.md.
- MCP testing: build on pytest-qt, or a custom interaction bridge like the
  existing Designer bridge?
