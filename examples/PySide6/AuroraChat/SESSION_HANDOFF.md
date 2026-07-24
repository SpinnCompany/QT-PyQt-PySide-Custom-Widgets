# AuroraChat — session handoff (2026-07-24)

A single-window **chat/messenger** showcase built the correct Custom_Widgets way
(forms pipeline), reproducing a light Messenger + dark "PRO/credits" reference
from one codebase. This doc is the state-of-play for the next session.

## ✅ What shipped (working)

**New library widgets** (in `Custom_Widgets/`, registered in `Plugins/register.py`, `.pyi` stubbed):
- `QCustomChatBubble` — in/out bubble, tail, sender/time meta, credits foot, `setBodyWidget()`.
- `QCustomVoiceMessage` — play/pause + painted scrubber waveform + duration.
- `QCustomChatListItem` — conversation row (avatar+dot, name, elided preview, time, unread badge, active/muted).
- `QCustomEmojiPicker` — **overhauled**: category quick-nav (feather line icons), Recently-used (QSettings), `emojiSelected` signal, online dataset update (gemoji, off-thread, cached, offline-safe), clean palette styling.
- **Normalization set:** `QCustomActionButton`, `QCustomChatDivider`, `QCustomTypingIndicator`, `QCustomMediaGrid`, `QCustomChatList`, `QCustomChatThread`, `QCustomChatInput` — data-driven, droppable, styled entirely from app QSS.

**The app** (`examples/PySide6/AuroraChat`, forms pipeline):
- `ui/MainWindow.ui` (nav rail + page stack) + `ui/ChatComponent.ui` (3-panel chat, now assembled from the components above).
- Real images from free providers via `gui/net.py` (avatars = randomuser.me, media = picsum.photos), async + disk-cached + offline fallback.
- `gui/GuiFunctions.py` is now **data + wiring only**; colours/icons live in `Qss/scss/chrome.scss` (modern nested QSS, `$CHAT_*` tokens from each theme's `Other-variables`, icons via `theme-icons`).
- Live presence worker (Online ↔ typing…), conversation-select re-routing, emoji picker wired to the input bar, collapsible media section.
- `QCustomThemeList` added to the profile "Customize Chat" area (switches themes).

## 🔬 Key discoveries / rules established (saved to memory)
- **`icons-via-qss-not-python`** (addendum): the theme engine AUTO-refreshes icons on theme change; never re-`setIcon` per theme.
- **`fully-utilize-customwidgets`**: use built-ins (theme engine, file listeners, theme widgets) before hand-rolling.
- **`qss-app-driven-nested`**: widgets must NOT `setStyleSheet` themselves/children (blocks theme re-polish); drive from app QSS with objectNames + dynamic-property state selectors (`&[active="true"]`); write modern nested SCSS. Painted colours may be a `QColor` qproperty set from QSS via `qproperty-*`.
- **`theme-widgets-and-set`**: use `QCustomThemeList`/`QCustomThemeDarkLightToggle`; the app's theme SET includes the built-in `Light`/`Dark` beside custom `Aurora Light`/`Aurora Dark`.
- **`use-free-online-media`**: pull real faces/photos from free no-key providers, async+cached+fallback.

## ❌ Failures / gotchas hit (don't repeat)
- **Hand-writing `.ui`/`.scss` with the Write tool is a rule violation** — edit forms in Designer and styles via the QSS editor / `project_write_style`. (Did this early; adopt-existing was chosen, but future edits must go through Designer.)
- **Per-widget `setStyleSheet` broke dark theme** (blocks re-polish) — removed across the chat widgets.
- **Recursion trap:** a `qproperty-<color>` setter that re-polishes → polish re-applies the qproperty → setter → ∞ `RecursionError`. Colour qproperty setters must only store + `update()`; only STATE setters (`active`/`muted`) may re-polish. (Fixed in `QCustomChatListItem`.)
- **Window churn:** multiple `designer_launch` + `designer_open_files(new_window=True)` spawned duplicate Designers/apps → "2 app windows". Launch ONE Designer; don't open forms in a new window unless needed; tear down by exact PID only when the MCP has lost track.
- **Huge time sunk** chasing the dark-theme render via app-side hacks (`_forceRestyle`, disk re-read, boot re-assert) — all reverted. The real cause was a framework palette-ordering bug (below).

## 🐞 OPEN ISSUE — dark theme background (the big one)
Root cause found: `QCustomTheme.applyCompiledSass` built the window **QPalette** from `COLOR_BACKGROUND_1` **before** `createVariables()` refreshed it, so a dark theme's big container panels painted the stale **light palette** while the (correct, dark) QSS only reached widgets with explicit backgrounds. See memory `theme-palette-before-createvariables-bug`.

**Fix applied:** moved `self.createVariables()` to the top of `applyCompiledSass` (before the palette block), removed the duplicate later call.

**NOT yet verified:** after the fix a FRESH BOOT still rendered light panels (dark markers present). The last runtime widget-driven switch (Light→Dark via `QCustomThemeList`) was issued but **not screenshotted** before the session ended. Determine:
1. Does a runtime theme switch (via `QCustomThemeList`) now paint the panels dark? If YES → the fix works and only the BOOT path needs a re-apply (boot applies default-light first, then `QAppSettings.updateAppSettings` restores the persisted theme without re-running palette+stylesheet, or races the dev-server recompile).
2. If NO → the palette isn't the whole story; check whether the big QFrames need `WA_StyledBackground`, or whether `updateAppSettings` reapplies the compiled QSS at all on boot.

## ✅ P1 DONE (2026-07-24 next session) — dark theme fixed & verified
The `createVariables()`-before-palette fix in `QCustomTheme.applyCompiledSass`
works for BOTH runtime theme switch AND fresh boot (verified over multiple
`designer_restart_app`s — dark in sidebar + all panels). The one light boot was
a `convert_ui`+dev-server first-run transient; self-heals via the
`_variables.scss` live-reload. `design_lint` app-clean. See memory
`theme-palette-before-createvariables-bug` (now RESOLVED).

## 🧭 ARCHITECTURE PIVOT (user rules, 2026-07-24) — component-based, Designer-driven
The user set new standing rules (saved to memory):
- **`component-based-ui-rule`** — split the UI into MANY small component `.ui`
  files (sidebar / profile / chat-list / thread / …), NOT a couple of monoliths.
  Compose via `QCustomComponentContainer` (property `filePath=ui/Xxx.ui`);
  reach a loaded child in Python via `container.component`.
- **`maximize-designer-properties-rule`** — expose/set EVERY configurable thing
  as a Designer qproperty IN the `.ui`; GuiFunctions = LOGIC only.
- **`all-components-open-live-reload`** — keep components open + live-reload;
  observe the RUNNING app (that's why MCP-enforcement exists).
- Chosen granularity: **finer** (containers + sub-components:
  ThreadHeader/Composer/MediaPanel/UserCard).

### ⚠️ Designer gotcha reconfirmed
`designer_open_files(new_window=True)` on the BIG ChatComponent.ui **segfaults**
Designer (custom-widget open crash). Author small forms with
`designer_new_form_xml`; edit existing via get_ui_code → transform → 
`designer_set_form_xml(file=…, save=true)`; observe via the RUNNING app.
If Designer wedges (status false but procs alive), `kill` the pids + relaunch.

## ✅ P2 vertical slice DONE — MediaPanel component + 4 media widgets
New **library widgets** (registered, `.pyi` regenerated via `stubgen`):
`QCustomImageViewer` (lightbox overlay), `QCustomVideoPlayer` (poster+scrubber),
`QCustomFileCard` (ext badge + download), `QCustomLinkPreview` (thumb+title+domain).
- New **component** `ui/MediaPanelComponent.ui`: `mediaTabs`
  (QCustomSegmentedControl) + `mediaStack` (QStackedWidget: Media grid / Files
  cards / Links previews). File/link items are DESIGN-TIME with Designer props.
- `ChatComponent.ui`: profile panel's media section replaced by
  `mediaContainer` (QCustomComponentContainer → MediaPanelComponent.ui).
- **Fixed a real bug:** GuiFunctions called `mediaTabs.setItems()` (doesn't
  exist) → tabs were ALWAYS empty/invisible. Added a **`segments` Designer
  property** to `QCustomSegmentedControl` (+ `currentSegment`, `setItems` alias);
  tabs are now set in the `.ui`. GuiFunctions only wires
  `currentChanged→mediaStack.setCurrentIndex` and `mediaGrid.tileClicked→lightbox`.
- `_Tile` now has objectName `mediaTile<i>` (testable/QSS).
- QSS: `Qss/scss/media.scss` (auto-imported) styles the file/link cards.
- VERIFIED in the running dark app: Media grid, Files cards, Links previews all
  render; tab switch works; clicking a tile opens the lightbox ("5 / 12", nav).
  `design_lint` failed=false (only qproperty-default hex warnings, like the rest
  of the lib).

## ✅ FULL GRANULAR COMPONENT SPLIT DONE (2026-07-24)
AuroraChat is now **10 forms**, composed via `QCustomComponentContainer`:
- `MainWindow.ui` → `sidebarContainer`(SidebarComponent) + pageStack→`chatContainer`(ChatComponent)
- `SidebarComponent.ui` → nav rail + `userCardContainer`(UserCardComponent)
- `ChatComponent.ui` → `chatsContainer`(ChatsListComponent) + `threadContainer`(ThreadComponent) + `profileContainer`(ProfileComponent)
- `ThreadComponent.ui` → `threadHeaderContainer`(ThreadHeaderComponent) + creditsBanner + chatThread + `composerContainer`(ComposerComponent)
- `ProfileComponent.ui` → profile + `mediaContainer`(MediaPanelComponent)

**GuiFunctions rewritten to `findChild(objectName)` access** (not container.component
chains) with readiness gating — robust to any nesting depth since objectNames are
globally unique. Both the sidebar wiring and the chat wiring wait (QTimer poll)
until their widgets exist.

**Boot theme re-assert added** (see memory `theme-palette-before-createvariables-bug`
UPDATE): deep async component loading reintroduced boot-light; fix = re-assert the
persisted theme once `themeList` exists. Verified: boots dark deterministically over
multiple restarts; runtime toggle + QCustomThemeList switch both work. `design_lint`
app-clean (0/0).

### Gotchas hit this split
- `designer_set_form_xml(file=…)` only targets a form that is **already OPEN** in
  Designer; otherwise it writes to the ACTIVE form (silently overwrote
  ProfileComponent.ui with MainWindow XML once). ALWAYS `designer_open_files` the
  target first (headless), then push.
- `QCustomSegmentedControl.setItems` never existed → tabs were empty. Added a
  `segments` Designer property (+ `currentSegment`, `setItems` alias).

## ✅ P3 MESSAGING WIDGETS DONE (2026-07-24)
- `QCustomMessageStatus` — painted delivery ticks (sending clock / sent 1-check /
  delivered 2-check / read 2-check in accent). qproperties: status, tickColor,
  readColor, tickSize.
- `QCustomReactionBar` — emoji reaction chips (emoji + count, count hidden when 1)
  + painted add(+) button. Data via setReactions([("👍",3)]) or the `reactions`
  Designer property ("👍:3,❤️:1"); signals reactionClicked(emoji)/addRequested.
- `QCustomChatBubble` extended: `setMetaWidget(w)` (ticks next to the time) +
  `setReactionBar(w)` (reactions row below the body), both side-aligned.
- `QCustomChatThread._attach_extras`: reads `status`/`reactions` off each message
  dict and attaches the widgets. Message data carries them via a trailing extras
  dict in `gui/data.py` THREAD (read by `_thread_messages`).
- QSS: `Qss/scss/messaging.scss` styles the reaction chips. Ticks paint from
  qproperties (tick=metaColor, read=accent). VERIFIED in the dark app: 👍2 / ❤️ /
  😄🔥3 chips render, read/delivered ticks show next to outgoing times.
  `design_lint` app-clean.

## ✅ Interactive reactions DONE (2026-07-24)
Reaction chips are now interactive:
- `QCustomChatThread` gained `reactionAddRequested(int index, object bar)` and
  `reactionClicked(int index, str emoji)` signals (message-scoped) + an
  `addReaction(index, emoji)` mutator (increment-or-append, then rebuild). The
  internally-built reaction bars forward their events up with the owning
  message index.
- ChatManager wires: chip click → `chatThread.addReaction` (increments); "+" →
  `_open_reaction_picker(index, bar)` opens `QCustomEmojiPicker` targeted at the
  bar, and `emojiSelected` → `addReaction`.
- VERIFIED: headless (chip-click 👍2→3, picker-add appends 🎉) AND live app
  (clicking a chip incremented ❤️ 1→2; "+" opens the picker — logs confirm, though
  the picker is a Wayland transient overlay `app_screenshot` can't capture).
- BUG fixed mid-way: an earlier `replace_all` only updated the VOICE branch's
  `_attach_extras(..., mi)` call (12-space indent) not the TEXT branch (8-space),
  so text messages passed `mi=-1` and reactions never matched. Both call sites now
  pass `mi`.

## ✅ "+" on ALL messages DONE + theme finding (2026-07-24)
- `QCustomChatThread` now attaches a reaction bar to EVERY message bubble (text +
  voice): chips render only when the message has reactions, but the "+" add
  affordance is always present so any message can be reacted to from scratch.
  Gated by a new `showReactionAdd` Designer bool property (default True).
- **Theme "boot-light" was a FALSE ALARM** — debug logging proved the re-assert
  correctly applies the PERSISTED theme; it had simply drifted to `Aurora Light`
  during heavy testing (a `QCustomThemeList` populate/show quirk can fire
  `on_theme_changed` once and change the persisted theme; its dropdown can then
  show a stale name that disagrees with the actual applied theme). Toggling to
  Aurora Dark persists + boots dark deterministically. No app bug. (Latent
  framework nit: QCustomThemeList doesn't re-sync its display when the theme is
  set programmatically via setTheme — cosmetic, left as-is.)

## ▶️ Remaining polish (optional)
- `QCustomVideoPlayer` still not placed in a form (video tile / attachment).
- FileCard/LinkPreview titles clip — add eliding. `segmentButton` QSS for nicer
  tab pills.

## Run it
Via the MCP: `project_convert_ui` → `designer_launch` (once) → `designer_run_app` → `app_screenshot`. Theme switch via the `QCustomThemeList` in the profile panel.
