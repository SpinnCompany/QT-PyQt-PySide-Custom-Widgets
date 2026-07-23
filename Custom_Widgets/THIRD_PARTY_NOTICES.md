# Third-Party Notices

`QT-PyQt-PySide-Custom-Widgets` incorporates and/or depends on third-party
software, icons, and fonts. This file lists them and their licenses. The license
texts for the **bundled** assets ship alongside this file in
[`licenses/`](licenses/); each icon set also carries a `LICENSE.txt` in its own
directory.

_Last reviewed: 2026-07-23. Licenses marked **(confirm)** are the well-known
license for that component and should be reconfirmed against the upstream before
a formal legal sign-off; they are not believed to pose a redistribution issue._

## A. Qt bindings (not bundled — installed separately by the user)

Uses Qt via `qtpy` with **PySide6** or **PyQt6**. These are the user's
responsibility to license (see `LICENSING.md`).

| Component | Vendor | License |
|---|---|---|
| PySide6 (Qt for Python) | The Qt Company | LGPLv3 / commercial |
| PyQt6 | Riverbank Computing | GPLv3 / commercial |
| Qt libraries | The Qt Company | LGPLv3 / GPLv3 / commercial |

"Qt" is a trademark of The Qt Company Ltd. This project is independent and
unaffiliated.

## B. Python runtime dependencies (installed via pip, not bundled)

**Core** dependencies (`pyproject.toml [project.dependencies]`) — licenses
verified against the installed `*.dist-info` on 2026-07-23:

| Package | License | Notes |
|---|---|---|
| qtpy | MIT | Qt binding abstraction |
| qtsass | MIT | SCSS→QSS compilation |
| termcolor | MIT | Coloured logs |
| lxml | BSD-3-Clause | XML / `.ui` parsing |
| rich | MIT | Console output |
| kids-cache (`kids.cache`) | BSD (BSD-3-Clause) | Caching |

**Optional** dependencies (installed only with the matching extra) — confirm at
release with `pip-licenses` against the extra actually shipped:

| Package | Extra | License (confirm) |
|---|---|---|
| qrcode (>=8.0), Pillow | `qr` | BSD-3-Clause; Pillow = HPND (MIT-CMU) |
| numpy, colorthief, Pillow | `acrylic` | BSD-3-Clause; colorthief = MIT/BSD |
| scipy | `acrylic-hq` | BSD-3-Clause |
| perlin_noise | `loaders` | MIT |
| mcp | `mcp` | MIT |

## C. Bundled / vendored source code

| File / module | Origin | License |
|---|---|---|
| `Custom_Widgets/BlurWindow.py` | **Original project code** (clean-room, 2026-07-23; rewritten from the documented OS APIs) | Project license |
| `Custom_Widgets/LoadingIndicators/` | Original (`QCustom*`) | Project license |
| `Custom_Widgets/AnalogGaugeWidget.py` | Stefan Holstein; inspired by the PyQt analog-clock example | MIT (confirm) |
| `Custom_Widgets/iconify/` | Vendored `iconify` icon-rendering engine | MIT (confirm) |
| `Custom_Widgets/ProgressIndicator.py` | Classic QProgressIndicator pattern (Morgan Leborgne) | MIT (confirm) |

## D. Bundled icon sets (`Custom_Widgets/Qss/icons/`)

License texts in [`licenses/`](licenses/); a `LICENSE.txt` also sits in each set's
directory.

| Set | Approx. count | License |
|---|---|---|
| Material Design Icons | ~2,123 | Apache-2.0 — [`Apache-2.0.txt`](licenses/Apache-2.0.txt) |
| Font Awesome (Free) | ~2,037 | Icons **CC BY 4.0** — [`CC-BY-4.0.txt`](licenses/CC-BY-4.0.txt); fonts SIL OFL 1.1; code MIT |
| Feather | ~315 | MIT — [`Feather-MIT.txt`](licenses/Feather-MIT.txt) |

## E. Bundled fonts (`Custom_Widgets/Qss/fonts/`)

| Font | License | Notes |
|---|---|---|
| Rosario (incl. variable) | SIL OFL 1.1 — [`OFL-1.1.txt`](licenses/OFL-1.1.txt) | The only bundled app font, loaded by `QCustomTheme.loadAppFont()`. Reserved Font Name "Rosario". |

> Product Sans (Google's proprietary font) was **removed** on 2026-07-23 — it was
> bundled but never loaded.

## F. Bundled themes / syntax (`CodeEditorThemes/`, `CodeEditorSyntax/`)

Colour schemes named after well-known editor themes (Monokai, One Dark/Light,
Zenburn, Oceanic) plus syntax definitions. Colour schemes are generally
low/unprotectable; confirm attribution for any scheme derived from a specifically
licensed source (e.g. One Dark = MIT). Syntax files appear original.

---

## Required attributions

- **Font Awesome Free** — Icons © Fonticons, Inc., licensed under **CC BY 4.0**
  (<https://fontawesome.com>). Icons may have been recoloured/resized for use as
  themed Qt icons.
- **Material Design Icons** — © Google and contributors, **Apache-2.0**.
- **Feather** — © 2013-2017 Cole Bemis, **MIT**.
- **Rosario** — © The Rosario Project Authors, **SIL OFL 1.1** (Reserved Font
  Name "Rosario").

These attributions are also shown in the project `README.md` (Credits) so they
are visible without opening the package.

## Maintenance

- Runtime deps: regenerate section B with `pip-licenses` against the declared
  deps (not the full transitive venv) before each release.
- Bundled assets: whenever an icon set, font, or vendored module is added or
  changed, record it here **and** add its license text to `licenses/`.
