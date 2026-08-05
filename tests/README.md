# Test Suite

Run the tests **before every commit and release**.

## Setup (one venv, PySide6)

The suite is tested locally with **PySide6** in a single project venv:

```bash
python -m venv .venv
.venv/bin/pip install -e . PySide6 pytest
```

## Run

```bash
.venv/bin/python -m pytest
```

The suite runs headless (`QT_QPA_PLATFORM=offscreen` is set by `conftest.py`),
so it works in CI and over ssh.

## Interactive UI tests

`examples/` contains runnable demo apps for testing widgets and the SVG theme
icons visually (theme switching, icon rendering, Designer parity):

```bash
.venv/bin/python examples/svg_icons_demo.py
```

## What is covered

- `tests/test_svg_icons.py` — the SVG theme-icon pipeline: generation and
  recoloring for a theme color, skip-if-exists behavior, the 24×24 Qt Designer
  set and its `.qrc`, `QIcon`/search-path rendering through Qt's SVG plugin,
  absence of the legacy cairosvg/PNG pipeline, and an end-to-end
  `applyCompiledSass` run (scss → css with `.svg` references + icon sets).
