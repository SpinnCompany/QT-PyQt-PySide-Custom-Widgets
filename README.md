# QT PyQt PySide Custom Widgets

[![PyPI](https://img.shields.io/pypi/v/QT-PyQt-PySide-Custom-Widgets?logo=pypi&logoColor=white)](https://pypi.org/project/QT-PyQt-PySide-Custom-Widgets/)
[![Python](https://img.shields.io/pypi/pyversions/QT-PyQt-PySide-Custom-Widgets?logo=python&logoColor=white)](https://pypi.org/project/QT-PyQt-PySide-Custom-Widgets/)
[![License](https://img.shields.io/github/license/SpinnCompany/QT-PyQt-PySide-Custom-Widgets?logo=github)](https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-customwidgets-blue)](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/)

**164 documented widgets for PySide6** — charts, data tables, gauges,
animated menus, window chrome, loaders and more. Every widget is
authorable in **Qt Designer**, themed through **design tokens** with
light/dark palettes, and documented with live screenshots generated
straight from the code.

![Custom Widgets Art](https://github.com/SpinnCompany/Docs-QT-PyQt-PySide-Custom-Widgets/blob/main/images/custom_widgets_art.png?raw=true)

## Installation

```bash
pip install QT-PyQt-PySide-Custom-Widgets[pyside6]   # first install, with Qt
pip install --upgrade QT-PyQt-PySide-Custom-Widgets
```

Requires Python **3.10+** (PySide6's own floor).

**You need a Qt binding.** The library reaches Qt through `qtpy` and does not
bundle a binding — that is what lets you use PySide6 *or* PyQt6, instead of
forcing a second ~200 MB Qt download on anyone who already has one. The
`[pyside6]` extra above installs it for you. Prefer PyQt6? `pip install PyQt6`
and set `QT_API=pyqt6`. Install without a binding and the first import tells
you exactly this, rather than raising a bare `QtBindingsNotFoundError`.

**Optional extras** (niche widgets pull their heavier stacks on demand):

```bash
pip install "QT-PyQt-PySide-Custom-Widgets[qr]"       # QCustomQRGenerator
pip install "QT-PyQt-PySide-Custom-Widgets[map]"      # QCustomMapView (QtLocation)
pip install "QT-PyQt-PySide-Custom-Widgets[acrylic]"  # AcrylicEffect blur
pip install "QT-PyQt-PySide-Custom-Widgets[loaders]"  # QCustomPerlinLoader
pip install "QT-PyQt-PySide-Custom-Widgets[mcp]"      # the Custom_Widgets MCP server
pip install "QT-PyQt-PySide-Custom-Widgets[all]"      # everything above
```

## Highlights

- **Painted chart family** — scatter, funnel, range bar, radial gauges,
  Sankey, candlestick, beeswarm, diverging bar, bubble, dot matrix,
  sparklines, donut and more; QPainter-native, crisp at any size.
- **`QCustomDataTable`** — rich cell renderers (two-line, status,
  currency, link), synthetic select/actions columns, sortable headers.
- **Chrome & motion** — custom title bars, hamburger and slide menus,
  animated stacked-widget transitions, flow layouts with animated reflow,
  progress and skeleton loaders, typewriter/sparkles/gradient text.
- **Design-token theming** — `applyDesignTokens` drives role-based QSS
  and light/dark palettes across the whole set.
- **Qt Designer first** — every widget and property can be authored
  visually; the examples ship with editable `.ui` files.
- **Typed** — full `.pyi` stubs, `py.typed`, mypy-clean.
- **MCP server** (`[mcp]` extra) — agent control of Qt Designer, live app
  observation, widget catalog/signature/render tools.
- **Design-rule linter** — `Custom_Widgets.lint` catches glyph icons,
  hardcoded hex colours, drop shadows and oversized icons.

## Usage

Read the required
[project structure](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/)
before starting — apps use a `ui/` + compiled `src/` + `Qss/` layout that
keeps Designer files, generated code and themes separate. The
[`examples/`](examples/) folder contains 82 complete apps built that way.

![QCustomArcLoader GIF](https://github.com/SpinnCompany/Docs-QT-PyQt-PySide-Custom-Widgets/raw/main/images/24-modern-ui.gif)

## Documentation

- **Docs & widget reference**: [spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/)
- **Widget gallery**: [164 widgets with screenshots](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/Widgets/QCustomQMainWindow)
- **App showcase**: [92 real apps](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/gallery)
- **Video tutorials**: [YouTube — SpinnTV](https://www.youtube.com/@SpinnTV)

## Pro & support

The free library is complete on its own and licensed **GPLv3**. For
commercial teams there is
[**Custom Widgets Pro**](https://pypi.org/project/QT-PyQt-PySide-Custom-Widgets-Pro/)
— starting with DataTable Pro (virtualization, server-side sort/filter,
grouping with aggregates, pivot, frozen columns, inline editing,
CSV/XLSX export) — plus twelve premium example applications. Plans at
[customwidgets.org/pricing](https://customwidgets.org/pricing/); active
[Patreon supporters](https://www.patreon.com/c/spinntv) get the same
entitlements. The Pro licence includes a written GPL additional
permission, so combining the core with Pro and your application does not
pull your application under the GPL.

## Contributors

Thanks to everyone involved in the development of the project!

<a href="https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=SpinnCompany/QT-PyQt-PySide-Custom-Widgets" />
</a>

*Made with [contrib.rocks](https://contrib.rocks).*

> **Note** — this repository is the project's permanent home. It was
> previously published from the KhamisiKibet account, which is no longer
> accessible; all development continues here under SpinnCompany.

## Credits & third-party assets

This package bundles third-party icon sets and a font. Full notices and the
license texts ship inside the package under
[`Custom_Widgets/THIRD_PARTY_NOTICES.md`](Custom_Widgets/THIRD_PARTY_NOTICES.md)
and [`Custom_Widgets/licenses/`](Custom_Widgets/licenses/).

- **Icons by [Font Awesome](https://fontawesome.com)** — Free icons licensed under
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (© Fonticons, Inc.);
  fonts under SIL OFL 1.1, code under MIT. Icons may be recoloured/resized.
- **[Material Design Icons](https://github.com/google/material-design-icons)** —
  Apache License 2.0 (© Google and contributors).
- **[Feather](https://github.com/feathericons/feather)** — MIT (© 2013-2017 Cole Bemis).
- **[Rosario](https://github.com/Omnibus-Type/Rosario)** — SIL Open Font License 1.1
  (the bundled UI font).
