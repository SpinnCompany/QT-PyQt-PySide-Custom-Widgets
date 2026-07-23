# Designer theming & QSS tooling

How themes and stylesheets are edited **inside Qt Designer** (the Custom
Widgets plugin), and the rules that keep it uniform.

## Ownership: the plugin, not the widgets

Design-time theming is owned by the **Designer plugin**, never by individual
widgets. The per-widget `liveCompileStylesheet` / `paintQtDesignerUI`
properties (and their `compileStylesheet` machinery) were removed from
`QCustomComponent` and `QCustomQMainWindow`. Runtime theming
(`loadJsonStyle` / `applyIcons` / `QSsFileMonitor`) is unchanged.

## The QSS / Theme Editor window

A standalone, movable, resizable, **undockable** window
(`DesignerTools.QssEditorWindow`, a `QMainWindow`) — not a dock. Opened from
the **🎨 QSS Editor** button in the Designer footer (or View menu). Layout:

- **Menu bar + top toolbar** — File (Open, New Style, Save, Close), Style
  (Check, Apply, Auto-compile toggle, Paint entire Designer). Shortcuts:
  Ctrl+O / Ctrl+N / Ctrl+S / Ctrl+Return / Ctrl+W.
- **Left: style-file list** — every `.scss`/`.qss`/`.css` in the project's
  `Qss/scss/` folder. 🔒 marks generated files, ✎ marks editable ones. Click
  to load.
- **Right: code editor** — syntax highlighting, property autocomplete,
  Tab/Shift+Tab indent, Ctrl+/ comment, Ctrl+D duplicate.

### Read-only (preview) files

Generated / system files open **read-only**: the editor is locked and Save is
disabled. These are:

    main.scss        # assembles the theme (@imports the below)
    _styles.scss     # library base widget styles
    _variables.scss  # the active theme's colour variables (regenerated on theme change)

Users edit **`defaultStyle.scss`** (overrides) and their own imported files.

### Uniformity: styles stay in `Qss/scss/`

Stylesheets must live in the project's `Qss/scss/` folder. This is enforced:

- **New Style** asks only for a *name*; any path typed is reduced to its
  basename, so the file always lands in `Qss/scss/` and is `@import`-ed into
  `defaultStyle.scss`. Reserved generated names are rejected.
- **Open** rejects any file chosen outside `Qss/scss/`.
- **Save** refuses to write outside `Qss/scss/` (defensive).

## Paint entire Designer

The **Paint entire Designer** toggle applies the **full current theme** as an
**application-level** stylesheet (`QApplication.setStyleSheet(css)`), so the
whole Designer — chrome and every open form — inherits it; unchecking clears
it. It compiles the full theme (`main.scss`, ~real CSS), not the (usually
empty) `defaultStyle.scss` buffer, and applies immediately (independent of the
Auto-compile option). Also reachable over the bridge:
`setStyleSheet` accepts an `entireApp` flag.

## Live apply

With **Auto-compile & apply on change** on, edits are compiled (qtsass,
resolving `@import`s and the theme `_variables.scss`) and pushed to the open
form previews via the Designer bridge (`_setStyleSheet`). Styles live in scss,
never inline in `.ui` files.

See also: [scss-engine.md](scss-engine.md).
