# Agent guide — QT-PyQt-PySide Custom Widgets

> **⛔ RULE #1 (read before any task).** Work on this project **through the
> `custom-widgets` MCP**, not ad-hoc shell. Before starting: **mount the MCP,
> then read its agent guide + skills.** If you can't reach the MCP tools, STOP
> and ask the user to mount it — don't fall back to a raw `python`/Bash run.

## Mount the MCP (auto or manual)

- **Auto:** this repo ships [`.mcp.json`](.mcp.json) — Claude Code mounts the
  `custom-widgets` server on session start. Approve it when prompted.
- **Manual / other agents:**
  ```
  claude mcp add custom-widgets -- Custom_Widgets-mcp --project-dir .
  # or, environment-portable:
  python -m Custom_Widgets.mcp --project-dir .
  ```
  Requires the package installed with the MCP extra: `pip install -e .[mcp]`.

## Read these first (RULE #1 step 2)

1. `customwidgets://agent-guide` — the operating guide (also `AGENT_GUIDE` in
   [`Custom_Widgets/mcp/guide.py`](Custom_Widgets/mcp/guide.py)). It leads with
   RULE #1 and covers the visible-and-teachable workflow, how to build
   professional screens, theming, and app wiring.
2. `customwidgets://skills` — pointers to the shipped skills/knowledge.
3. Pick the RIGHT build skill:
   - [`.claude/skills/custom-widgets-app/SKILL.md`](.claude/skills/custom-widgets-app/SKILL.md)
     — **REAL apps / dashboards / multi-page tools**: the forms pipeline
     (`.ui` → compiled `src/` → `json-styles` themes → `Qss/scss` `$TOKENS` →
     GuiFunctions managers + workers). This is how production apps must be built.
   - [`.claude/skills/custom-widgets-demo/SKILL.md`](.claude/skills/custom-widgets-demo/SKILL.md)
     — the quick pure-code token demo only (a single styled `main.py`).

## ⭐ RULE #0 — the forms pipeline IS the product; don't ship a pure-code app

For any production-shaped build, the deliverable is `.ui` forms + `json-styles`
CustomThemes + `Qss/scss` `$TOKENS` + `GuiFunctions` managers/workers — NOT a
hand-built `main.py` with hard-coded hex. A code-only app that "looks right" is
still a failure for maintenance. Mirror `examples/PySide6/AuroraDeckPro` and
`examples/PySide6/WinningDashboard_CorrectArchitecture`. Compile forms with
`Custom_Widgets --convert-ui ui --qt-library PySide6 --src-output-dir src`.
Switch themes BY NAME (`themeEngine.setTheme("<Custom Theme>")`). Read the
custom-widgets-app skill for the full procedure and the hard-won gotchas
(Qt hex is `#AARRGGBB`; token widgets need inline styling under `loadJsonStyle`;
use `QCustomDonut` not a QChart pie in small panels; etc.).

## The golden path (all through MCP tools)

```
designer_launch → designer_open_files / designer_new_form_xml   # build forms, VISIBLE in Designer
designer_qss_window(open) → project_write_style                 # style in the QSS editor, VISIBLE
designer_run_app → app_screenshot / app_click / app_object_tree # run + observe the REAL app
designer_stop_app → designer_quit                               # tear down cleanly
```

## Design rules (enforced — not optional)

The library ships a design-rule linter (`Custom_Widgets.lint`) that enforces the
project's **visual** rules a type checker can't see. It runs automatically on
every file edit (a PostToolUse hook in [`.claude/settings.json`](.claude/settings.json)),
in pre-commit, and in CI — and is exposed to MCP agents as the `design_lint`
tool. Canonical spec: [`docs/design/design-rules.md`](docs/design/design-rules.md).

- **`glyph-icons` (error)** — never use a unicode glyph as an icon in UI text
  (no `◑ ＋ ⚙ ✦ ➤ ✓ ↗` / emoji). Use a real themed-SVG or painted icon that
  recolours per theme. A new violation **blocks the edit**.
- **`hardcoded-hex` (warning)** — drive chrome colour from token roles, not raw
  `#rrggbb` (ALL-CAPS palette constants are allowed).
- **`drop-shadow` (warning)** — no `QGraphicsDropShadowEffect` without a
  `# allow-shadow: <reason>` justification.

Run it yourself before finishing a screen: `python -m Custom_Widgets.lint`
(or the `design_lint` MCP tool). Pre-existing debt is grandfathered by
`.custom_widgets_lint_baseline.json`; only **new** violations fail. Suppress a
genuine false positive with `# noqa: <rule-id>`.

## Where things live

| Path | What |
| --- | --- |
| [`Custom_Widgets/mcp/`](Custom_Widgets/mcp/) | MCP server (`server.py`), agent guide (`guide.py`), `python -m` entry |
| [`Custom_Widgets/DesignerBridge.py`](Custom_Widgets/DesignerBridge.py) | live link that runs inside Qt Designer + the app |
| `Custom_Widgets/` | the widget library (import `from Custom_Widgets.QCustom… import …`) |
| `examples/PySide6/` | runnable examples / showcases |
| [`Custom_Widgets/lint/`](Custom_Widgets/lint/) | design-rule linter (rules in `rules.py`); spec in [`docs/design/design-rules.md`](docs/design/design-rules.md) |
| `.claude/skills/` | Claude Code skills for this repo |

**If a capability is missing, add it to the MCP** — don't work around it in a shell.
