# Session report — 2026-07-24 (AuroraChat: component-based messenger + media/messaging widgets)

Everything is **local-only** (no push, per the no-push-until-commercial-ready
rule). Work landed on branch `feat/tiering-manifest` in two commits:

- `081d9ce5` — AuroraChat app (granular component split) + media/messaging widgets + framework fixes
- `dec399d8` — inline chat media + URL previews

`examples/PySide6/AuroraChat` is now the canonical reference for a **component-based,
Designer-first** Custom_Widgets application. Its per-app state lives in
`examples/PySide6/AuroraChat/SESSION_HANDOFF.md`; this doc is the durable,
project-level record of what was built and — more importantly — what was learned.

## What shipped

**The app.** A single-window messenger reproducing a light-Messenger + dark
"PRO/credits" reference from one codebase, rebuilt from two monolithic forms into
**ten** small component `.ui` files composed with `QCustomComponentContainer`:

```
MainWindow
├─ SidebarComponent          └─ UserCardComponent
└─ ChatComponent
   ├─ ChatsListComponent
   ├─ ThreadComponent        ├─ ThreadHeaderComponent
   │                         └─ ComposerComponent
   └─ ProfileComponent       └─ MediaPanelComponent  (Media grid · Files · Links)
```

`gui/GuiFunctions.py` is pure LOGIC: it reaches widgets by (globally-unique)
`objectName` via `findChild`, with readiness gating, so it is decoupled from how
deeply the components nest. No `container.component` chains.

**New library widgets** (registered, `.pyi` stubbed, all Designer-promotable):

- Media: `QCustomImageViewer` (modal lightbox overlay), `QCustomVideoPlayer`
  (poster + simulated scrubber), `QCustomFileCard` (ext badge + download),
  `QCustomLinkPreview` (thumb + title + domain).
- Messaging: `QCustomMessageStatus` (painted sent/delivered/read ticks),
  `QCustomReactionBar` (interactive emoji reaction chips + add button).
- Extensions: `QCustomChatBubble.setMetaWidget`/`setReactionBar`/`setBodyPadding`;
  `QCustomChatThread` renders per-message status/reactions/inline-media and
  exposes reaction + inline-media signals; `QCustomSegmentedControl` gained a
  `segments` Designer property; `QCustomMediaGrid.pixmaps()` + `setImageAt` now
  tracks stored pixmaps.

**Inline chat media + URL previews** — media and link previews render *inside*
message bubbles by embedding the existing widgets via `setBodyWidget()`; **no new
widget classes were needed** (see the reuse principle below).

## Discoveries & fixes

### 1. Dark-theme render bug (framework) — root-caused and fixed
`QCustomTheme.applyCompiledSass` built the window `QPalette` from
`COLOR_BACKGROUND_1` **before** `createVariables()` refreshed the active theme's
colours, so dark themes painted big container panels with the stale *light*
palette while only widgets with an explicit QSS background flipped. Fix: run
`createVariables()` first. Verified dark on runtime switch and fresh boot.

### 2. Boot theme re-assert for async component trees
Once the profile's `QCustomThemeList` and the big panels moved into
deeply-nested, asynchronously-loaded components, the persisted theme was no
longer re-applied after they finished loading — a persisted-dark app rendered
light. Fix (app-side, standard pattern): once the deepest themed sub-component
(`themeList`) exists, re-assert the persisted theme **once** —
`themeEngine.setTheme(themeEngine.theme)`. Runtime `setTheme` fully re-applies
palette + QSS, so this deterministically paints the persisted theme on boot.

Corollary: a "light boot" is usually the app faithfully applying a persisted
*light* theme, not a bug — confirm the persisted value before chasing it.
`QCustomThemeList` does not re-sync its displayed name when the theme is set
programmatically (cosmetic; its dropdown can disagree with the applied theme).

### 3. The invisible-tabs bug
`QCustomSegmentedControl`'s API was `setSegments`, not `setItems`. A manager
called `setItems` guarded by `hasattr`, which silently no-op'd, so the tabs were
**always empty/invisible**. Fixed by adding a `segments` Designer property so the
tabs are defined in the `.ui` (and a `setItems` alias). Lesson: a `hasattr`-guarded
call hides API-drift as a silent visual bug; prefer a real Designer property.

### 4. Designer MCP gotchas (reconfirmed / new)
- `designer_open_files(new_window=True)` on a **large custom-widget form**
  segfaults Designer (the known custom-widget open crash). Author small forms
  with `designer_new_form_xml`; edit existing ones via get-XML → transform →
  `designer_set_form_xml`; observe via the RUNNING app. Small component forms are
  far less crash-prone than a monolith — another argument for granularity.
- `designer_set_form_xml(file=…)` only targets a form that is **already open** in
  Designer; otherwise it writes to the *active* form (this silently overwrote one
  component with another's XML). Always `designer_open_files` the target first.

## Rules crystallised this session

Promoted to durable guidelines in
[`app-architecture-guidelines.md`](app-architecture-guidelines.md):

1. **Component-based, very granular for complex UIs** — many small component
   `.ui` files (one per container *and* sub-container), never a few monoliths.
2. **Designer-first properties** — expose/set every configurable thing as a
   Designer qproperty in the `.ui`; Python is for LOGIC only, fall back to it
   only when a property genuinely can't express it.
3. **All components open + live reload** — the standard build/observe loop; watch
   the running app hot-reload each edit (the reason for the MCP-enforcement rule).
4. **Reuse before you build** — the message bubble is a *container*; inline
   content types are data + `setBodyWidget`, not new widgets. Only build a new
   widget when it has genuinely new painting/interaction.
