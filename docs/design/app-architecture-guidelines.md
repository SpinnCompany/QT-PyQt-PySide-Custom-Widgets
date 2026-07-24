# App architecture guidelines — building Custom_Widgets apps the right way

Companion to [`design-rules.md`](design-rules.md) (which covers the *visual*
rules the linter enforces). This page covers the **architectural** rules for
building a real application with Custom_Widgets. They are conventions, not
lint-enforced — but they are how every reference app in `examples/PySide6/`
(AuroraChat, FinanceDashboard, AuroraDeckPro, CryptoDashboard) is built, and how
new apps should be built.

The one-line summary: **the interface is data + Designer forms + QSS + custom
widgets; Python is only the logic that drives them.**

---

## 1. Component-based UI — be very granular for complex UIs

Split the interface into **many small component `.ui` files**, one per logical
container **and** sub-container — not a couple of big monolithic forms. When in
doubt, split finer.

- Each region (sidebar, user card, list panel, thread, thread header, composer,
  profile, media panel, …) is its own `ComponentName.ui` whose root is a
  `QCustomComponent`.
- Compose them with `QCustomComponentContainer` — set its `filePath` property to
  `ui/ChildComponent.ui`. Containers nest arbitrarily.
- The shell forms (`MainWindow.ui`, a workspace form) become thin layouts of
  containers.

**Why.** Small forms are easy to maintain and to open/edit in Designer; each
component is independently reusable, hot-reloadable and testable. (A large
custom-widget form is also what tends to crash Designer on open — see §6.)

```
MainWindow  →  SidebarComponent(→UserCard) + Chat(→ChatsList, Thread(→Header,
Composer), Profile(→MediaPanel))
```

## 2. Maximize Designer properties — Python is for logic only

Expose and set **every configurable thing** as a typed Designer `@Property` on
the widget, and set it **in the `.ui`** — not from Python.

- When you build a custom widget, add its config as Designer qproperties first
  (text, counts, colours, sizes, variants, list items). Then the form — and a
  human in Designer — can configure it without touching code.
- Static / design-time data (labels, captions, icon roles, colours, sizes, tab
  items, sample rows) belongs in the `.ui` or the JSON theme, **not** in Python.
- The manager (`GuiFunctions`) is for LOGIC: signals/slots, async workers,
  live/dynamic data (network results, presence), navigation. Before setting a
  visual attribute in Python, ask "can this be a Designer property or a QSS
  rule?" — fall back to Python only when it genuinely can't.

If you find yourself adding `hasattr`-guarded `setX()` calls, that is a smell —
add the real Designer property instead (the `QCustomSegmentedControl` tabs were
invisible for exactly this reason: a `setItems` that never existed).

## 3. Colours and icons come from QSS, not Python

- Colours: app QSS via `objectName` / role selectors and design tokens; painted
  widgets expose `QColor` qproperties set from QSS (`qproperty-*`). Never
  `setStyleSheet` on a widget or its children — it blocks the theme engine's
  re-polish. Persist styles the sanctioned way (`project_write_style` →
  `Qss/scss/*.scss`, `@import`-ed from `defaultStyle.scss`).
- Icons: `qproperty-icon: url(theme-icons:icons/<set>/<name>.svg)` in QSS — the
  theme engine auto-recolours them on theme change. Never `setIcon`/`setPixmap`
  in code (and never re-`setIcon` per theme).

## 4. The manager reaches widgets by objectName

In a deeply-nested component tree, do **not** thread `container.component.child`
chains through the manager. Give every widget a globally-unique `objectName` and
resolve it with `window.findChild(QWidget, "name")`. Gate wiring on readiness
(poll until the required widgets exist) because components load asynchronously.
This decouples the manager from the exact nesting and survives re-layouts.

## 5. Theme boot re-assert for async component trees

Boot applies a default theme first; when the themed widgets (esp. a
`QCustomThemeList`) live in asynchronously-loaded components, the **persisted**
theme is not re-applied after they finish loading, so a persisted-dark app can
render light. Once the deepest themed sub-component exists, re-assert the
persisted theme **once**: `themeEngine.setTheme(themeEngine.theme)`. (A "light
boot" is often the app correctly applying a persisted *light* theme — verify the
persisted value before treating it as a bug.)

## 6. Reuse before you build — containers, not new widgets

Before writing a new widget, check whether an existing one composed into a
**container** already does the job. The clearest example: a chat message
**bubble** is a container — inline images, videos, files and link previews are
just `bubble.setBodyWidget(<existing widget>)` plus a new message *kind* in the
data, **not** new widget classes:

| inline content | reused widget |
| --- | --- |
| image / album | `QCustomMediaGrid` → tap → `QCustomImageViewer` |
| video | `QCustomVideoPlayer` |
| file | `QCustomFileCard` |
| URL preview | `QCustomLinkPreview` |

Only build a new widget when it has **genuinely new painting or interaction**
that no existing widget + container expresses. (This is also why the library
grows deliberately — see [`build-progress.md`](build-progress.md).)

## 7. The dev loop: all components open, live reload, observe the running app

Do the whole build/observe loop through the Custom_Widgets MCP so every edit is
observable with live reload:

- Run the app with the dev-server supervisor; saving a form regenerates
  `src/ui_*.py` and hot-restarts, saving `.scss` live-reloads styles.
- Author new forms with `designer_new_form_xml`; edit existing ones by reading
  the form XML, transforming it, and pushing it back with `designer_set_form_xml`
  (**target must already be open** in Designer, else it writes to the active
  form). Screenshot the **running app** after each change — it is the
  always-visible artifact.
- Do **not** open a large custom-widget form with `new_window=True` — it
  segfaults Designer. Small component forms are safe; this is another reason to
  keep forms small (§1).

---

### The forms pipeline in one line

`ui/*.ui` → `Custom_Widgets --convert-ui` → `src/ui_*.py`; `json-styles/` themes;
`Qss/scss/$TOKENS`; `gui/` managers + workers. See
[`dashboard-widgets.md`](dashboard-widgets.md) and the reference apps under
`examples/PySide6/`.
