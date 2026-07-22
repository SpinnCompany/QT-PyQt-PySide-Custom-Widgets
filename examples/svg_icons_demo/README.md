# SVG Icons Demo — interactive test app

Manual test bed for the SVG theme-icon pipeline. Run it whenever you change
theming or icon code, before commits and releases (alongside `pytest`).

## Run

```bash
.venv/bin/python examples/svg_icons_demo/main.py
```

(Any environment with the package + PySide6 works; the app chdirs into its own
folder so all generated files stay here.)

## What to check

1. **Theme switching** — pick a theme in the top bar (`Demo Dark`,
   `Demo Light`, `Emerald`, plus built-in `Light`/`Dark`). The label reports
   how long icon generation took; with the SVG pipeline it should be
   milliseconds, not minutes.
2. **QSS indicator icons** (left panel) — checkbox/radio/combo/spinbox
   indicators are loaded from the generated SVGs through the compiled theme
   stylesheet. They must recolor with every theme.
3. **Icon browser** (right panel) — every generated SVG of the active theme,
   filterable per icon pack. Check color and vector sharpness.
4. **Qt Designer parity** — after running the app once (this generates
   `Qss/icons/` and `_icons.qrc`), open the test form in Designer:

   ```bash
   pyside6-designer designer_test.ui
   ```

   The buttons and pixmap label must show the same SVG icons the app uses.
