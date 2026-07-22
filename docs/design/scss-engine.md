# Future feature: modern SCSS engine (qtsass replacement)

**Status:** Proposed / not started
**Owner:** TBD
**Created:** 2026-07-22

## Summary

Replace our dependency on [`qtsass`](https://github.com/spyder-ide/qtsass) with a
vendored, modernized SCSS→QSS compiler built on **Dart Sass** instead of the
deprecated **LibSass**. This unlocks real modern SCSS (module system, `sass:*`
built-ins, source maps, useful errors) and lets us extend the Qt-specific layer
(gradient functions, compile-time icon recoloring, palette sync, a QSS linter).

## Motivation

We currently depend on `qtsass` (see `setup.py` → `install_requires`), which is
used in `Custom_Widgets/Qss/SassCompiler.py` via `qtsass.compile_filename`.

qtsass is small and does its job, but it is built on **LibSass**, which the Sass
team **officially deprecated in 2020** and froze at roughly the Sass 3.5 spec.
The limitation people hit ("not fully supporting real SCSS") is caused by
LibSass, *not* by qtsass's Qt layer. No amount of forking the Qt layer fixes it.

What LibSass can never give us:

- `@use` / `@forward` — the module system (we're stuck on global `@import`)
- Built-in modules: `sass:math`, `sass:color`, `sass:map`, `sass:string`, `sass:list`
- Modern `math.div()` (the `/`-as-division deprecation)
- First-class maps ergonomics, improved `@each`
- Source maps and error messages with file/line/column spans

qtsass upstream is effectively maintenance-only (recent commits are CI/test
housekeeping, no feature work), so an engine-swap upstream is unlikely to land.
It is MIT-licensed and ~7 small files, so vendoring/forking is clean and fits how
we already vendor `Custom_Widgets/Qss/colorsystem.py` and the theme engine.

## What qtsass actually is (so we know what to port)

- `conformers.py` — three regex transforms that are the *entire* QSS-awareness:
  `NotConformer` (`:!` selectors), `QLinearGradientConformer`,
  `QRadialGradientConformer`.
- `functions.py` — four custom Sass functions: `rgba`, `rgba_from_color`,
  `qlineargradient`, `qradialgradient`.
- Everything else delegates to `import sass` (LibSass).

Porting the conformers is trivial (pre/post text passes). Porting the functions
requires that the new engine support **custom-function callbacks into Python**.

## Engine options

The Sass team's only supported implementation is **Dart Sass**. How we consume
it from Python is the real decision:

| Option | Modern SCSS | Custom Qt functions | Packaging |
|---|---|---|---|
| **Dart Sass — embedded protocol** | ✅ full | ✅ yes (callback API) | ⚠️ ships a binary |
| **Dart Sass — `sass` CLI subprocess** | ✅ full | ❌ no callbacks | ⚠️ ships a binary |
| **LibSass (`import sass`, today)** | ❌ 3.5-era | ✅ yes | ✅ pure-Python wheel |

There is **no pure-Python modern Sass compiler** — nobody has reimplemented the
current spec in Python, so a "modern SCSS + pip-only, no binary" option does not
exist.

### Recommendation: Dart Sass via the embedded protocol

`sass-embedded` runs a long-lived Dart subprocess spoken to over a
protobuf/stdio protocol. Keep one warm process and call `compileString()`
repeatedly (no per-call startup cost). Python client:
[`sass-embedded`](https://pypi.org/project/sass-embedded/), or drive the
protocol directly (it's small).

Only this option gives us **both** modern SCSS **and** the custom-function API our
Qt layer depends on. The CLI subprocess option is rejected because it cannot call
back into Python — our `qlineargradient`, `icon()`, and `qpalette()` functions
would all break.

**Open tradeoff to decide before starting:** the embedded compiler ships a
~5–10 MB Dart binary per platform (download-on-first-run or bundled). If a
pure-`pip install` with no external binary is non-negotiable, we stay on LibSass
and this feature is not achievable. This decision gates everything below.

## Proposed work

### Phase 1 — engine swap (highest leverage)

- Vendor qtsass into `Custom_Widgets/Qss/` (drop the `qtsass` dependency from `setup.py`).
- Re-implement `compile_filename` on top of a single warm `sass-embedded` process.
- Preserve the existing conformers as pre/post passes.
- Register the existing `qlineargradient` / `qradialgradient` as custom functions.
- Add source-map output and surface real error spans.
- A/B the new path against the current LibSass output to confirm QSS parity.

### Phase 2 — extend the Qt layer

New custom functions:

- `qconicalgradient()` — the one Qt gradient qtsass is missing.
- `qpalette(role)` — pull colors from the running `QPalette` so themes derive
  from the live app instead of hardcoded hex.
- `icon(path, $color)` — recolor an SVG at compile time, return `url(...)`. We
  already do this at runtime in a `Worker` in `SassCompiler.py`; a compile-time
  function folds icon theming into the stylesheet.
- `dpi()` / `px()` — HiDPI scaling helpers.

QSS validation / linting (Qt silently ignores unsupported CSS, so surfacing it
saves real debugging):

- Warn on properties Qt drops: `box-shadow`, `transition`, `transform`, `flex`,
  `display`, `cursor`, `z-index`, etc.
- Warn on selectors Qt's limited engine can't parse (`>` edge cases, `+`/`~`,
  attribute selectors).
- Strip/warn on `!important` (Qt ignores it).

Theming pipeline (where this library benefits most):

- Design-token map → auto-generate light/dark variants.
- **Emit a `QPalette` alongside the QSS.** We already hand-build a palette in
  `SassCompiler.py`; formalizing it as a compiler output keeps native-drawn
  widgets (menus, tooltips, standard dialogs) in sync with the sheet.
- In-process hot reload — hot-swap `app.setStyleSheet` on file change (qtsass
  already has a `watchers/` dir to build on).

## Risks / considerations

- **Binary packaging** is the main risk (see open tradeoff above).
- **QSS output parity** with the current LibSass path must be verified before
  cutover — Dart Sass may emit color/whitespace differently; conformers/emitters
  may need adjustment.
- **Clean break**: per project convention, no backward-compat shim — document the
  migration in the Docs repo when this ships.

## References

- qtsass source: https://github.com/spyder-ide/qtsass
- Dart Sass: https://sass-lang.com/dart-sass/
- LibSass deprecation: https://sass-lang.com/blog/libsass-is-deprecated/
- Embedded protocol: https://github.com/sass/sass/blob/main/spec/embedded-protocol.md
