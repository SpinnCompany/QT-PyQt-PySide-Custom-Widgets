# SVG Icons Demo — real project layout

Manual test bed for the SVG theme-icon pipeline, structured like a real
Custom_Widgets project:

```
ui/            .ui files designed in Qt Designer (icons from ../Qss/icons/_icons.qrc)
src/           GENERATED Python (ui_*.py) - do not edit
generated-files/  GENERATED json/ui intermediates - do not edit
json-styles/   style.json (themes, icon color)
Qss/           GENERATED shared icon set + scss (created on first run)
main.py        imports src/ui_mainwindow.py, wires demo logic
```

## Workflow

```bash
# 1. Convert ui/ once (or after pulling changes)
Custom_Widgets --convert-ui ui --src-output-dir src

# 2. Run the app
python main.py

# 3. During development: live-regenerate on every Designer save
Custom_Widgets --monitor-ui ui --src-output-dir src   # separate terminal

# 4. Design with the same icons the app uses
Custom_Widgets --start-designer --plugins             # File > Open ui/mainwindow.ui
```

## What to check

1. **Theme switching** — top bar. ONE shared icon set (`Qss/icons/icons/`),
   recolored in place on every color change; the label reports the timing.
2. **`.ui` icons** — the save/settings/delete/material buttons and tab icons
   come from the qrc in Designer and are re-pointed to the shared set at
   runtime (via `generated-files/json` + `applyIcons`). They must recolor on
   every theme switch.
3. **QSS indicator icons** — checkbox/radio/combo/spinbox indicators load
   from the shared SVGs through the compiled stylesheet.
4. **Icon browser** — the shared set, filterable per pack.
5. **Icon color control** — `QtDesignerIconsColor` in
   `json-styles/style.json` is `"theme"` (icons follow the active theme).
   Set a hex color to pin ALL icons, or add `$ICONS_COLOR: #ff5722;` to
   `Qss/scss/defaultStyle.scss` to override from the stylesheet (highest
   precedence).
6. **Designer parity** — edit `ui/mainwindow.ui` in Designer (icons visible
   there too), save; with the monitor running, `src/` regenerates — restart
   the app to see your change.
