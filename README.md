# QT PyQt PySide Custom Widgets

[![GitHub](https://img.shields.io/github/license/SpinnCompany/QT-PyQt-PySide-Custom-Widgets?logo=Github)](https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets/blob/master/LICENSE)
[![GitHub top language](https://img.shields.io/github/languages/top/SpinnCompany/QT-PyQt-PySide-Custom-Widgets?logo=github)](https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets)
[![GitHub issues](https://img.shields.io/github/issues/SpinnCompany/QT-PyQt-PySide-Custom-Widgets?logo=github)](https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets/issues)

## Repository Migration Notice

This repository has been forked and is now actively maintained at:

**New Repository**: [SpinnCompany/QT-PyQt-PySide-Custom-Widgets](https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets)

### Changes
- **New Maintainer**: Now actively maintained by SpinnCompany
- **Continuous Updates**: Regular maintenance, bug fixes, and new features
- **Improved Accessibility**: Resolved previous access limitations

This repository is the project's permanent home; the original KhamisiKibet repository is no longer accessible. All development continues here.

## Overview

Custom widgets for QT Desktop Applications designed to simplify UI development. These widgets can be used in QT Designer and imported to PySide code.

![Custom Widgets Art](https://github.com/SpinnCompany/Docs-QT-PyQt-PySide-Custom-Widgets/blob/main/images/custom_widgets_art.png?raw=true)

## Installation

**First time installation:**
```
pip install QT-PyQt-PySide-Custom-Widgets
```

**Upgrade to latest version:**
```
pip install --upgrade QT-PyQt-PySide-Custom-Widgets
```

**Optional extras** (niche widgets pull their heavier stacks on demand):
```
pip install "QT-PyQt-PySide-Custom-Widgets[qr]"       # QCustomQRGenerator
pip install "QT-PyQt-PySide-Custom-Widgets[map]"      # QCustomMapView (QtLocation)
pip install "QT-PyQt-PySide-Custom-Widgets[acrylic]"  # AcrylicEffect blur
pip install "QT-PyQt-PySide-Custom-Widgets[loaders]"  # QCustomPerlinLoader
pip install "QT-PyQt-PySide-Custom-Widgets[mcp]"      # the Custom_Widgets MCP server
pip install "QT-PyQt-PySide-Custom-Widgets[all]"      # everything above
```

## Quick Links

- **Documentation**: [spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/)
- **GitHub Pages**: [spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/)
- **Main Module**: [github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets](https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets)

## Usage

Please read the required [project structure](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets) and important updates [here](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets) before proceeding.

The examples folder contains code examples for testing and learning about the custom widgets.

![QCustomArcLoader GIF](https://github.com/SpinnCompany/Docs-QT-PyQt-PySide-Custom-Widgets/raw/main/images/24-modern-ui.gif)

## Documentation Resources

- **Full Documentation & Examples**: [spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/)
- **Video Tutorials**: [YouTube Playlist](https://www.youtube.com/watch?v=21Qt9p_F7Ts&list=PLJ8t3BKaQLhPKj9Mx08WAwvz7TGskefbK)
- **Widget Gallery**: [spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/Widgets/QCustomQMainWindow](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/Widgets/QCustomQMainWindow)

## Support

If you find this project valuable and would like to contribute to its development and maintenance, you can support us on [Patreon](https://www.patreon.com/c/spinntv).

## Contributors

Thanks to all the [contributors](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets) involved in the development of the project!

<a href="https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=SpinnCompany/QT-PyQt-PySide-Custom-Widgets" />
</a>

*Made with [contrib.rocks](https://contrib.rocks).*

## App Gallery

View a collection of modern GUIs made using the custom widgets module: [View Gallery](https://spinncompany.github.io/Docs-QT-PyQt-PySide-Custom-Widgets/gallery)

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
