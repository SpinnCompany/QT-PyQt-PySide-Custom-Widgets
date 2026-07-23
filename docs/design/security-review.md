# Widget Security & Stability Review

**2026-07-24.** The Stable/Secure half of the launch gate (see
`tiering-manifest.md`). Sweep of the free-core user-facing widgets for dangerous
sinks (security) and edge-input crashes (stability).

## Security — verdict: LOW RISK

Scanned every widget module for code-execution, deserialization, network, and
filesystem sinks.

| Vector | Result |
|---|---|
| `eval` / `exec` / `compile` / `__import__` | **none in any widget** |
| `os.system` / `subprocess` / `Popen` | only in **dev tooling** (Designer launch, uic/rcc/qtsass compile, DevServer, ProjectMaker) — never in a shipped widget; args are fixed tool names, not user input |
| `pickle` / `marshal` / unsafe `yaml.load` | **none** |
| Network | only `QCustomEmojiPicker` — and it is **safe by design**: `autoUpdate=False` (opt-in), offline-first with a **bundled** dataset, runs on a worker thread (no UI freeze), XDG cache path, parses with `json.loads` (not eval), single fixed GitHub gemoji URL |
| File writes / deletes | app-controlled and self-contained: annotation save (`QCustomAnnotationWidget`), emoji cache (XDG), QR temp-file cleanup (`os.remove` of its own temp), theme SCSS generation (infra) |
| QSS injection | `setStyleSheet` calls compose **style values** (dark/light/gradient/token), not user free-text; Qt QSS cannot execute code regardless |

**Notes (informational, low severity):**
- `QCustomAnnotationWidget` builds its output path from the annotated image's
  filename under a user-chosen project folder. It's a local desktop annotation
  tool (author == user), so path-traversal risk is informational only. If ever
  exposed to untrusted filenames, sanitize the basename.
- All `subprocess` sites are dev/build tooling, not shipped-app runtime. Out of
  scope for the widget security surface, but they run fixed executables
  (`pyside6-uic`, `rcc`, qtsass) — no shell string interpolation of user input.

## Stability — verdict: strong

Every user-facing widget constructs and paints (405-test suite). On top of that,
the painted **data** widgets were edge-probed and are now covered by permanent
regression tests (`tests/test_widget_stability.py`, 43 cases): each is fed
**empty / single / all-equal / all-zero / negative / huge** data and forced to
paint, catching the classic normalization crashes (divide-by-zero when
`max == min` or `total == 0`, empty indexing).

Covered: `QCustomSparkline`, `QCustomDonut`, `QCustomMiniBarChart`,
`QCustomAreaChart`, `QCustomLineChart`, `QCustomBarChart`, `QCustomPieChart`
(incl. the all-zero pie case), `AnalogGaugeWidget`. **All pass.**

- `QCustomBarChart.addSeries` raises a clear `ValueError("Invalid data format")`
  on a wrong data shape — intentional fail-fast validation, not a crash.
- Bug found & fixed during this pass: `QCustomTagEdit` was fully broken
  (undefined `QFlowLayout` + Qt6-removed `QPalette.Background`) — now fixed and
  tested.

## Remaining gate work
- Extend the edge-probe regression tests to input/interactive widgets (sliders,
  number input, range slider, combo, date/time) — feed out-of-range / inverted
  min-max / rapid-toggle and assert no crash.
- Theme-switch safety sweep (repolish on light/dark toggle across all widgets).
- Then the free/Pro split can lock (all four gate columns green).
