# Aurora Chat — a single-window messenger showcase

A polished, Dribbble-grade **chat / messenger** app built the correct
Custom_Widgets way (the forms pipeline, not a hand-built `main.py`). It
reproduces two real design references at once — a **light Messenger** look and a
**dark "PRO / credits"** look — from ONE codebase, flipped purely by switching
themes **by name**.

![light + dark](.)

## What it showcases

Three chat widgets were added to the library for this demo (they live in
`Custom_Widgets/`, so any project can use them and drop them in Qt Designer):

| Widget | Role |
| ------ | ---- |
| **QCustomChatListItem** | a conversation row — avatar + online dot, name, elided last-message preview, timestamp, unread-count badge, selected-pill + muted states, `clicked` signal |
| **QCustomChatBubble** | a message bubble — incoming/outgoing side (drives palette, tail corner & alignment), sender/time meta, credits-cost foot, natural width up to `maxBubbleWidth`, and `setBodyWidget()` to embed anything |
| **QCustomVoiceMessage** | a voice message — circular play/pause, painted scrubber waveform (`valuesCsv`), progress fill, duration; `playToggled` / `seeked` signals |

Plus existing widgets: **QCustomSidebar / QCustomSidebarButton** (nav rail),
**QCustomAvatar** (every avatar + status dot + profile ring),
**QCustomSegmentedControl** (Media/Files/Links), **QCustomQStackedWidget**,
**QCustomComponentContainer**, and the overhauled **QCustomEmojiPicker** (opens
from the input bar → inserts into the message box; category quick-nav, recently
used, and can refresh its emoji set online when the bundled one is outdated).

**Real media, not placeholders.** Avatars are real portraits from free no-key
providers (`randomuser.me`) and the media grid is real photos (`picsum.photos`),
loaded async + disk-cached via `gui/net.py`, with the initials/gradient kept as
the offline fallback.

Live touches: a background **presence worker** flips the header between
`Online` and `typing…` (Worker → Signal → GUI slot), conversation selection
re-routes the thread + profile panel, and the whole UI recolours on theme
switch.

## The pipeline (how it is built)

```
ui/*.ui  ->  compiled src/ui_*.py       (Custom_Widgets --convert-ui)
json-styles/style.json                  (Aurora Light / Aurora Dark themes + ChatPalette)
Qss/scss/chrome.scss                    ($TOKENS only — no hard-coded hex in chrome)
gui/GuiFunctions.py                     (orchestrator + ChatManager + presence worker)
```

- **Themes switch BY NAME** (`themeEngine.setTheme("Aurora Dark")`), never the
  generic light/dark toggle.
- **Chat surface colours** (bubbles, waveform, pills, online dot, credits) come
  from the token-driven `ChatPalette` in `style.json` and are applied in the
  manager, so they flip with the theme. Chrome (panels, fields, sidebar) is
  pure `$COLOR_*` tokens in `chrome.scss`.
- **Icons** are themed SVGs recoloured to the theme's Icons-color and repainted
  on theme change (never unicode glyphs).
- Repeating content (conversations, the thread, the media grid, profile
  actions) is **data-driven** from `gui/data.py`; the `.ui` holds only the
  structural containers by `objectName`.

## Run it (via the Custom Widgets MCP)

```bash
# 1. build the compiled forms
Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src
# 2. run
python main.py
```

Or drive the whole loop through the MCP: `project_convert_ui` →
`designer_run_app` → `app_screenshot`, and toggle themes with a click on
`themeToggle`.
