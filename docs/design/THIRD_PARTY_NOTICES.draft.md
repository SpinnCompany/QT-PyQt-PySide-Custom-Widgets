# Third-Party Notices

> **⚠️ DRAFT — inventory for review, not yet authoritative.**
> Licenses marked **(verify)** are the commonly-known license for that component
> and must be confirmed against the actual bundled files / upstream before this
> goes live. This draft has not been reviewed by counsel. When complete, promote
> to `/THIRD_PARTY_NOTICES`.
>
> **Two items below require action before an LGPL relicense / commercial launch —
> see "⚠ Action required" at the end.**

Custom Widgets incorporates and/or depends on third-party software, icons, fonts,
and other materials. This file lists them and their licenses. Where components are
**bundled** (distributed inside this package), their attributions and license
texts must ship with the distribution.

## A. Qt bindings (not bundled — installed separately by the user)

Custom Widgets uses Qt via `qtpy` and works with **PySide6** or **PyQt6**. These
are the user's responsibility to license; see `LICENSING.md` §5.

| Component | Vendor | License |
|---|---|---|
| PySide6 (Qt for Python) | The Qt Company | LGPLv3 / commercial |
| PyQt6 | Riverbank Computing | GPLv3 / commercial |
| Qt libraries | The Qt Company | LGPLv3 / GPLv3 / commercial |

"Qt" is a trademark of The Qt Company Ltd. This project is independent and
unaffiliated.

## B. Python runtime dependencies (installed via pip, not bundled)

Declared in package metadata. Licenses below are the well-known license for each —
**(verify)** against the installed `*.dist-info` before publishing.

| Package | License (verify) | Notes |
|---|---|---|
| qtpy | MIT | Qt binding abstraction |
| qtsass | MIT | SCSS→QSS compilation |
| matplotlib | Matplotlib (BSD-style/PSF) | Charts |
| scipy | BSD-3-Clause | Numerics |
| Pillow | HPND (MIT-CMU / "PIL") | Imaging |
| lxml | BSD-3-Clause | XML/.ui parsing |
| watchdog | Apache-2.0 | File monitoring (live reload) |
| rich | MIT | Console output |
| termcolor | MIT | Colored logs |
| qrcode (>=8.0) | BSD-3-Clause | QR generator widget |
| perlin_noise | MIT (verify) | Perlin loader |
| colorthief | MIT/BSD (verify) | Palette extraction |
| kids-cache (kids.cache) | BSD/other (verify) | Caching |
| mock | BSD-3-Clause | (should be test-only — see action items) |
| setuptools | MIT | Packaging |
| mcp | MIT | Optional extra `[mcp]` — MCP server |

> Regenerate this table with a tool such as `pip-licenses --format=markdown
> --with-urls` against the *declared* runtime deps (exclude the full transitive
> venv, which includes test/build-only packages like uvicorn, starlette,
> pydantic, pytest, etc.).

## C. Bundled / vendored source code (distributed inside this package)

These carry upstream attributions and **must retain them**; verify each upstream
license is compatible with the planned **LGPLv3** core.

| File / module | Origin (from in-file attribution) | License |
|---|---|---|
| `Custom_Widgets/BlurWindow.py` | Adapted from GWSL-Source `blur.py`, zhiyiYo, and digsby `vista.py` | **(verify — mixed sources, possible GPL)** ⚠ |
| `Custom_Widgets/AnalogGaugeWidget.py` | Stefan Holstein; inspired by PyQt4 analog-clock example | (verify — likely MIT) |
| `Custom_Widgets/iconify/` | Vendored `iconify` icon-rendering engine | (verify — likely MIT) |
| `Custom_Widgets/ProgressIndicator.py` | Classic QProgressIndicator pattern (commonly attributed to Morgan Leborgne) | (verify — likely MIT) |
| `Custom_Widgets/LoadingIndicators/` | Appears original (`QCustom*`) | Project (LGPL after relicense) |

## D. Bundled icon sets (`Custom_Widgets/Qss/icons/`)

| Set | Count | License | Attribution requirement |
|---|---|---|---|
| Material Design Icons | ~2,123 | Apache-2.0 (verify exact set) | Include Apache-2.0 + NOTICE |
| **Font Awesome (Free)** | ~2,037 | Icons **CC BY 4.0**, fonts **SIL OFL 1.1**, code MIT | **CC BY 4.0 requires visible attribution** ⚠ |
| Feather | ~315 | MIT | Include MIT + copyright |

## E. Bundled fonts

| Font | License | Status |
|---|---|---|
| Rosario (incl. variable) | SIL Open Font License 1.1 | ✅ OK to bundle with OFL text + attribution |
| **Product Sans** (all weights) | **Proprietary — Google brand font** | 🚫 **NOT licensed for redistribution — must remove** |

## F. Bundled themes / syntax (`CodeEditorThemes/`, `CodeEditorSyntax/`)

Color schemes named after well-known editor themes (Monokai, One Dark/Light,
Zenburn, Oceanic) plus syntax definitions (`python.json`, `cpp.json`). Color
schemes are generally low/unprotectable, but **verify attribution** for any
scheme derived from a specifically-licensed source (e.g. One Dark = MIT; Zenburn
has its own terms). Syntax files appear original.

---

## ⚠ Action required (surfaced by this audit)

1. **Product Sans font — remove/replace (highest priority).** Product Sans is
   Google's proprietary corporate typeface and is **not licensed for
   redistribution**. Bundling it is very likely a license violation. **Replace**
   with an OFL alternative (e.g. Google Sans is *also* proprietary — use an open
   substitute such as a Grotesk/Neo-Grotesque OFL font) or remove it and reference
   a system font. Do this **before** any commercial distribution.

2. **`BlurWindow.py` license provenance — verify (LGPL-compatibility risk).** It's
   adapted from multiple upstreams, at least one of which (GWSL) may be
   copyleft/GPL. If any source is GPL, bundling it in an **LGPLv3** core is a
   conflict. Confirm each upstream's license; rewrite/replace the module if it's
   GPL-derived.

3. **Font Awesome attribution — ensure present.** CC BY 4.0 requires visible
   attribution to Font Awesome. Add it to the docs/about screen and this file's
   published version, or switch those icons to a set with no attribution
   requirement.

4. **`mock` as a runtime dependency — likely wrong.** `mock` is a testing library;
   it should be a test/dev extra, not a runtime `Requires-Dist`. Verify and move
   it to `extras_require`/dev deps.

5. **Confirm all (verify) licenses** against installed `dist-info` and upstream,
   and generate the license-text bundle (`licenses/` directory) that the LGPL and
   the bundled MIT/Apache/OFL/CC components require to ship with the distribution.

## How this file is maintained

- Runtime deps: regenerate with `pip-licenses` against declared deps only.
- Bundled code/assets: update whenever a vendored file, icon set, or font is added
  or changed. Every bundled component must have its license recorded here **and**
  its license text included in the distribution.
