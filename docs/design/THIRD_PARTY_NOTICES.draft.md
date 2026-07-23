# Third-Party Notices

> **⚠️ DRAFT — inventory for review, not yet authoritative.**
> Licenses marked **(verify)** are the commonly-known license for that component
> and must be confirmed against the actual bundled files / upstream before this
> goes live. This draft has not been reviewed by counsel. When complete, promote
> to `/THIRD_PARTY_NOTICES`.
>
> **Progress (2026-07-23): Product Sans removed; `mock` runtime-dep concern
> confirmed resolved; `BlurWindow.py` clean-room rewritten (provenance risk
> cleared). Remaining before an LGPL relicense / commercial launch: Font Awesome
> in-app attribution, on-Windows/macOS verification of the new blur code, and the
> license-text bundle — see "⚠ Action required" at the end.**

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
| ~~mock~~ | — | **Not a runtime dep** (verified 2026-07-23): absent from `pyproject.toml`; only `unittest.mock` is used, in tests. |
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
| `Custom_Widgets/BlurWindow.py` | **Original project code** (clean-room, 2026-07-23) | Project (LGPL after relicense). Rewritten from the documented OS APIs; no longer adapted from third-party sources — see action item 2. |
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
| Rosario (incl. variable) | SIL Open Font License 1.1 | ✅ OK to bundle with OFL text + attribution. This is the only bundled app font, loaded by `QCustomTheme.loadAppFont()`. |
| ~~Product Sans (all weights)~~ | ~~Proprietary — Google brand font~~ | ✅ **REMOVED** (2026-07-23). The 12 `.ttf` files under `Qss/fonts/google-sans-cufonfonts/` were deleted; they were bundled but never loaded (the theme already loaded Rosario). |

## F. Bundled themes / syntax (`CodeEditorThemes/`, `CodeEditorSyntax/`)

Color schemes named after well-known editor themes (Monokai, One Dark/Light,
Zenburn, Oceanic) plus syntax definitions (`python.json`, `cpp.json`). Color
schemes are generally low/unprotectable, but **verify attribution** for any
scheme derived from a specifically-licensed source (e.g. One Dark = MIT; Zenburn
has its own terms). Syntax files appear original.

---

## ⚠ Action required (surfaced by this audit)

Status legend: ✅ done · 🔬 investigated (decision/action pending) · ⏳ open.

1. ✅ **Product Sans font — REMOVED (2026-07-23).** The 12 proprietary `.ttf`
   files under `Custom_Widgets/Qss/fonts/google-sans-cufonfonts/` were deleted.
   They were bundled but **unused**: `QCustomTheme` already loaded the OFL
   **Rosario** font. The loader method was renamed `loadProductSansFont` →
   `loadAppFont` and its docstring/log strings corrected. Rosario (SIL OFL 1.1)
   remains the only bundled app font.

2. ✅ **`BlurWindow.py` — clean-room rewritten (2026-07-23).** The module was
   rewritten from scratch against the documented OS APIs (Windows DWM
   `DwmEnableBlurBehindWindow` / `DwmExtendFrameIntoClientArea` and the
   `user32.SetWindowCompositionAttribute` accent policy; macOS
   `NSVisualEffectView`; Linux KWin `_KDE_NET_WM_BLUR_BEHIND_REGION`). The
   third-party source-attribution header was removed and no upstream code is
   reproduced — the ctypes struct/constant definitions are OS ABI facts. The
   public API (`GlobalBlur`, `blur`, `Win7Blur`, `ExtendFrameIntoClientArea`,
   `BlurLinux`, `HEXtoRGBAint`, `MacBlur`) is preserved and now fails soft
   (returns `False`, never raises) off-platform. This removes the earlier
   provenance risk (the upstream sources were: GWSL "Modified MIT" — ambiguous;
   digsby PSF-derived — permissive; zhiyiYo — unlicensed blog).
   *Behaviour on Windows/macOS still needs on-target verification (rewrite done
   on Linux); the Linux import path + `HEXtoRGBAint` parity are tested.*

3. ⏳ **Font Awesome attribution — text added below; in-app placement pending.**
   The required CC BY 4.0 attribution now appears in §D and in the "Required
   attributions" block below (which ships once this file is promoted to
   `/THIRD_PARTY_NOTICES`). Still to do: surface it somewhere user-visible
   (About dialog / docs) or swap those icons for an attribution-free set.

4. ✅ **`mock` runtime dependency — already resolved.** The current
   `pyproject.toml` (v2.2.1) runtime deps are `qtpy, qtsass, termcolor, lxml,
   rich, kids-cache` — `mock` is **not** among them, and no runtime module
   imports it (only `unittest.mock` is used, in tests). Nothing to change; the
   draft table's "should be test-only" note stands corrected.

5. ⏳ **Confirm all (verify) licenses** against installed `dist-info` and upstream,
   and generate the license-text bundle (`licenses/` directory) that the LGPL and
   the bundled MIT/Apache/OFL/CC components require to ship with the distribution.

## Required attributions (must ship in the published notices)

- **Font Awesome Free** — icons under **CC BY 4.0**, fonts under **SIL OFL 1.1**,
  code under **MIT**. Attribution: *"Icons by Font Awesome — https://fontawesome.com,
  licensed under CC BY 4.0."* (Required by CC BY 4.0.)
- **Material Design Icons** — Apache-2.0; include the Apache-2.0 license text + NOTICE.
- **Feather** — MIT; include the MIT text + copyright.
- **Rosario** — SIL OFL 1.1; include the OFL text + reserved font name.

## How this file is maintained

- Runtime deps: regenerate with `pip-licenses` against declared deps only.
- Bundled code/assets: update whenever a vendored file, icon set, or font is added
  or changed. Every bundled component must have its license recorded here **and**
  its license text included in the distribution.
