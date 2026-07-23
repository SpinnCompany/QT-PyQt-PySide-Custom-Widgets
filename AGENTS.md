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
3. [`.claude/skills/custom-widgets-demo/SKILL.md`](.claude/skills/custom-widgets-demo/SKILL.md)
   — token-widget demo pattern, verified widget signatures, and gotchas.

## The golden path (all through MCP tools)

```
designer_launch → designer_open_files / designer_new_form_xml   # build forms, VISIBLE in Designer
designer_qss_window(open) → project_write_style                 # style in the QSS editor, VISIBLE
designer_run_app → app_screenshot / app_click / app_object_tree # run + observe the REAL app
designer_stop_app → designer_quit                               # tear down cleanly
```

## Where things live

| Path | What |
| --- | --- |
| [`Custom_Widgets/mcp/`](Custom_Widgets/mcp/) | MCP server (`server.py`), agent guide (`guide.py`), `python -m` entry |
| [`Custom_Widgets/DesignerBridge.py`](Custom_Widgets/DesignerBridge.py) | live link that runs inside Qt Designer + the app |
| `Custom_Widgets/` | the widget library (import `from Custom_Widgets.QCustom… import …`) |
| `examples/PySide6/` | runnable examples / showcases |
| `.claude/skills/` | Claude Code skills for this repo |

**If a capability is missing, add it to the MCP** — don't work around it in a shell.
