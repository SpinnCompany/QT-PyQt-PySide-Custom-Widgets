# Custom Widgets design rules

This is the **canonical source of truth** for the project's *visual* rules — the
ones a type checker or pyflakes will never catch. They are enforced mechanically
by the shipped linter (`Custom_Widgets.lint`) so they hold **always**: in this
repo, in CI, in pre-commit, on every Claude Code / AI-agent edit, and in
downstream apps built with the library.

> The rule definitions live in code at
> [`Custom_Widgets/lint/rules.py`](../../Custom_Widgets/lint/rules.py). This page
> is the human-readable spec; keep the two in sync when you add or change a rule.

## The rules

| id | severity | what it forbids |
| --- | --- | --- |
| `glyph-icons` | **error** (fails CI / blocks the edit hook) | A unicode glyph used as an icon in UI text |
| `hardcoded-hex` | warning | A raw `#rrggbb` colour buried in chrome |
| `drop-shadow` | warning | `QGraphicsDropShadowEffect` with no justification |
| `large-icon` | warning | A large image pushed through `setIconSize(QSize(N,N))` (N≥40) instead of a `QPixmap` |

### `glyph-icons` — real icons only, never unicode-glyph "icons"

Never use a pictographic glyph as an icon in button/label text — no `◑ ◉ ▤ ◈ ⚙
≡ ✦ ➤ ✓ ✕ ↗ ＋ ％` and no emoji. They **don't recolour** on theme switch,
**vanish** when an icon-rail collapses to icon-only, and **render
inconsistently** across fonts and platforms.

Use a **real icon asset** instead:

- a **themed SVG** via QSS `qproperty-icon: url(theme-icons:icons/<set>/<name>.svg)`
  or `widget.setIcon(...)` (recolours on theme, survives rail collapse), or
- a **painted `QPixmap`** you recolour per theme — see the `_icon(...)` helper in
  [`examples/PySide6/AuroraJobsTable/main.py`](../../examples/PySide6/AuroraJobsTable/main.py),
  which paints the rail, header, `＋ Add job` and theme-toggle icons as vectors
  and re-tints them from the token roles on every theme change.

The linter scans **string literals** in `.py` and text in `.ui` (module/class/
function docstrings and code comments are ignored), so prose that merely *names*
a glyph is fine — only glyphs that would render in the UI are flagged.

> **Convention — custom-button icons recolour from QSS, not Python.**
> `QCustomQPushButton` and `QCustomSidebarButton` recolour their own SVG from two
> QSS properties: `qproperty-iconName` (a bundled feather/material name or a `.svg`
> path) + `qproperty-iconColor` (a token). Prefer this to `qproperty-icon:
> url(theme-icons:…)` on a custom button — it recolours on **theme** change and
> **previews in Qt Designer** (the setter renders the SVG immediately; Designer
> does not rewrite `theme-icons:` urls). Set `iconSize` in the `.ui`.
>
> The **checked/active** look uses the *separate* base-rule properties
> `qproperty-iconNameActive` / `qproperty-iconColorActive` — **not** a
> `:checked { qproperty-iconColor }` rule. Qt does **not** re-apply `qproperty-*`
> from a pseudo-state selector on state change, so a `:checked` qproperty never
> takes effect; the button swaps to the `*Active` values in code on toggle.
> ```scss
> #navHome { qproperty-iconName: "home";
>            qproperty-iconColor: $muted;
>            qproperty-iconColorActive: $accent; }   /* checked icon -> accent */
> #playBtn { qproperty-iconName: "play_arrow"; qproperty-iconNameActive: "pause"; }
> ```
> `theme-icons:` urls remain fine for `QLabel` pixmaps / plain widgets, but must be
> **unquoted** — `url(theme-icons:icons/…)`, never a quoted `url("…")` produced by an
> SCSS `$PATH_RESOURCES+'…'` concat (the engine's rewriter only matches unquoted).

### `hardcoded-hex` — colours come from token roles

Chrome colour should come from `tokens.role("surface"|"on-surface"|"primary"|…)`
(or a named palette constant) so it **flips with the theme**. A raw `#rrggbb`
inside a stylesheet string is a warning.

**Allowed:** an intentional data palette declared as ALL-CAPS module constants,
e.g. `GREEN = "#22c55e"` — semantic status hues deliberately kept out of the
theme roles. The linter recognises ALL-CAPS assignment targets and does not flag
them.

### `drop-shadow` — depth without shadows

The design bar is *"no drop shadows unless necessary"* (get depth from a
borderless fill a step off the canvas + a big corner radius). Constructing
`QGraphicsDropShadowEffect` or calling `setGraphicsEffect(...)` is a warning
unless the line carries a justification comment:

```python
card.setGraphicsEffect(QGraphicsDropShadowEffect(self))  # allow-shadow: hero KPI card
```

### `large-icon` — large images belong on a `QPixmap`, not a `QIcon`

`QIcon`/`setIcon` is for **small button glyphs**; it caps and softens when a
button scales it up (and can pick up disabled/greyscale modes). A **prominent or
large** image should be a **`QPixmap`** — `QLabel.setPixmap` (with
`setScaledContents`), or `QPainter.drawPixmap` inside a painted widget — rendered
at the real target size (2× for HiDPI) so it stays crisp.

The rule is deliberately **conservative**: it only fires on
`setIconSize(QSize(<int>, <int>))` where a **literal** dimension is `≥ 40`px.
Small button icons and any computed / variable size never trip it, so false
positives are minimal.

```python
btn.setIconSize(QSize(48, 48))   # warning: 48px QIcon → use a QLabel pixmap
lbl.setPixmap(pm)                # OK: a QLabel pixmap at the real size
btn.setIconSize(QSize(20, 20))   # OK: a small button glyph
btn.setIconSize(QSize(64, 64))   # allow-large-icon: deliberate, e.g. a themed action tile
```

## Running the linter

```bash
python -m Custom_Widgets.lint                 # scan configured paths
python -m Custom_Widgets.lint app/ ui/        # scan specific paths
Custom_Widgets-lint --strict                  # warnings fail too
Custom_Widgets-lint --list-rules              # describe every rule
Custom_Widgets-lint --format github           # CI annotations
```

From an AI agent driving the MCP: call the **`design_lint`** tool (read-only)
before considering a screen done.

### Suppressing a false positive

Add a trailing comment on the offending line:

```python
label.setText(SPECIAL)   # noqa: glyph-icons
label.setText(SPECIAL)   # cwlint: allow glyph-icons  (reason)
```

## Configuration

Per-project settings live under `[tool.custom_widgets_lint]` in `pyproject.toml`
(all optional — the defaults ship with the library):

```toml
[tool.custom_widgets_lint]
paths   = ["Custom_Widgets", "examples"]  # what to scan with no path args
ignore  = ["hardcoded-hex"]               # turn a rule off
select  = ["glyph-icons"]                 # or run ONLY these
strict  = true                            # warnings fail too
exclude = ["**/vendored/**"]              # extra path globs to skip
allow-glyphs = "✓✗"                       # codepoints that are NOT icons here

[tool.custom_widgets_lint.severity]
hardcoded-hex = "error"                   # promote a warning to an error
```

## Baseline (adopting on an existing codebase)

The repo carries `.custom_widgets_lint_baseline.json`, a set of *grandfathered*
violations that already existed when the linter landed. Only **new** violations
fail — the backlog is burned down over time. Fingerprints are line-independent,
so they survive edits elsewhere in a file but stop matching once the offending
line is actually fixed.

```bash
Custom_Widgets-lint --generate-baseline   # re-snapshot after intentional changes
Custom_Widgets-lint --no-baseline         # see the full backlog
```

## Where it's enforced

| Surface | Mechanism |
| --- | --- |
| Local edits by any agent/session | `.claude/settings.json` PostToolUse hook → [`.claude/hooks/design_lint_hook.py`](../../.claude/hooks/design_lint_hook.py) (blocks new `error`s) |
| Pre-commit | [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) local hook |
| CI | `design-lint` job in [`.github/workflows/tests.yml`](../../.github/workflows/tests.yml) |
| AI agents via MCP | the `design_lint` tool + the DESIGN RULES section of the MCP agent guide |
| Downstream apps | the linter ships in the wheel; users run it / wire their own hooks |

## Adding a rule

1. Implement `_check_myrule(ctx)` in `Custom_Widgets/lint/rules.py` and append a
   `Rule(...)` to `_ALL`. Nothing else changes — CLI, config, hook, CI and the
   MCP tool all pick it up from the registry.
2. Add a test to `tests/test_lint.py`.
3. Document it here and in the MCP guide (`Custom_Widgets/mcp/guide.py`).
