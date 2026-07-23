# Session handoff — 2026-07-24 (release prep: compile pipeline, tiering, hardening)

Everything is **local-only** (no push, per the no-push-until-commercial-ready
rule). Two feature branches carry this session's work.

## Branches

**Pro repo** `QT-PyQt-PySide-Custom-Widgets-Pro` — branch `feat/compile-pipeline`
- `build:` native **Cython compile pipeline** — `setup.py` compiles every module
  (incl. `__init__`), ships `packages=[]` so wheels carry **only `.so`, no
  source**. Real `[tool.cibuildwheel]` matrix + dormant `.github/workflows/
  wheels.yml` (manual/tag only, no sdist). Proven: cp314 wheel, clean-venv
  install, 86 tests pass compiled, `QCustomDataTablePro` renders. See `BUILD.md`.
- `feat(cli):` **`custom-widgets-pro` entitlement CLI** (status / activate /
  deactivate). Fixed an `activate()` bug (invalid `LicenseStatus` is falsy, so
  `last or …` swallowed the real reason). Verified against live Gumroad.

**Free core** `QT-PyQt-PySide-Custom-Widgets` — branch `feat/tiering-manifest`
- `docs:` **tiering & hardening manifest** + regenerable `tools/scan_widgets.py`
  (+ `.json` sidecar). The launch-gate artifact.
- `test:` **untested backlog 34 → 0** — `tests/test_qcustom_{chat,dataviz,misc}.py`
  (~40 widgets). Coverage 58% → 90%.
- Fixed `QCustomTagEdit` (was fully broken: undefined `QFlowLayout` +
  Qt6-removed `QPalette.Background`×4).
- `docs:` **ratified tiers** — everything free except 5 anchors (DataTable →
  DataTable Pro *locked*; 4 chart types → Charts Pro *candidate*). No Pro
  watchlist. Encoded in the scanner.
- `test/docs:` **security + stability pass** — `docs/design/security-review.md`
  (low-risk verdict) + `tests/test_widget_stability.py` (43 edge cases).

## Launch gate status (`docs/design/tiering-manifest.md`)

| Column | State |
|---|---|
| Tested | ✅ 0 untested user-facing; ~448 tests passing |
| Classified | ✅ tiers ratified & encoded (5 free→Pro · 84 free · 19 internal) |
| Secure | ✅ swept — low risk (no eval/exec/pickle/shell in widgets; one opt-in network widget) |
| Stable | 🟨 data widgets + charts locked down; **input/interactive + theme-switch sweep remain** |

Once Stable is green, the free/Pro split can **lock**, and the whole open-core
product ships at once (still counsel-gated on the separate LGPL relicense).

## Next steps
1. Edge-probe regression tests for input/interactive widgets (sliders, number,
   range, combo, date/time — out-of-range, inverted min>max, rapid toggle).
2. Theme-switch safety sweep (repolish light/dark across all widgets).
3. Then lock tiers; proceed to the legal/store/delivery launch tasks
   (see the `pro-sku-roadmap` / `commercial-product-decisions` notes).

## In flight / cautions
- A background session is fixing `QCustomCodeEditor.py` (invalid escape
  sequences + deprecated `setNamedColor`). **Do not edit that file** until it
  lands.
- Pre-existing uncommitted working-tree changes (icons, `register.py`,
  `QCustomEmojiPicker.py`) predate this session and are **not** ours — leave them.
