# Running the Custom Widgets MCP server

The repo ships an MCP server that lets an agent drive Qt Designer, run apps and
read the widget catalog. `.claude/skills/custom-widgets-demo` makes mounting it
a hard prerequisite, so it is worth knowing exactly how it is wired.

---

## Why it appears "not connected"

`.mcp.json` registers it over **HTTP**, not stdio:

```json
{
  "mcpServers": {
    "custom-widgets": { "type": "http", "url": "http://127.0.0.1:8765/mcp" }
  }
}
```

That is deliberate. `Custom_Widgets/mcp/server.py` describes it as a *shared
daemon*: several sessions and agents dial into one process, so cross-client
commands against a project are serialized by that project's worker. A stdio
server could not do that — each client would spawn its own isolated copy.

The consequence is the thing that bites:

> **An HTTP MCP server is never started by the client. The client only dials
> in.** If nothing is already listening on 8765, every session sees the server
> as unavailable, with no error explaining why.

Verified 2026-08-01: nothing was listening, the port was free, and starting the
daemon by hand bound it immediately and served fine. The server is not broken —
it simply was not running.

## Starting it

```bash
python -m Custom_Widgets.mcp --transport http --port 8765
```

Leave that running; agent sessions then connect automatically via `.mcp.json`.

Check it is up:

```bash
ss -ltn | grep 8765          # expect a LISTEN line on 127.0.0.1:8765
```

### Why not `Custom_Widgets-mcp`

`pyproject.toml` declares the console script:

```toml
[project.scripts]
Custom_Widgets-mcp = "Custom_Widgets.mcp:main"
```

but it only exists once the package is **installed** (`pip install -e .`). When
the repo is used straight from the source tree — as it is here — the script is
not on `PATH` and the documented command fails with `command not found`. Use
`python -m Custom_Widgets.mcp` in that case; it is the same entry point.

## Options

| Flag | Default | Notes |
|---|---|---|
| `--transport` | `stdio` | Must be `http` to match `.mcp.json` |
| `--host` | `127.0.0.1` | Loopback only |
| `--port` | `8765` | Must match `.mcp.json` |
| `--project-dir` | cwd | The server chdirs here and sets the project root |

Note the default transport is **stdio** while `.mcp.json` expects **http**, so
the flag is not optional. Starting it bare gives a working stdio server that no
client is configured to reach.

## Troubleshooting

- **Agent reports the server missing** — check the port first; the usual cause
  is that no daemon is running, not a config error.
- **`command not found: Custom_Widgets-mcp`** — the package is not installed;
  use `python -m Custom_Widgets.mcp`.
- **Port already in use** — a daemon is already up. That is the intended
  state; do not start a second one.
- **Started but agents still cannot see it** — confirm the transport is `http`
  and the port matches `.mcp.json`.

## What the server is for

Driving Designer and running apps: `designer_launch`, `designer_open_files`,
`designer_screenshot`, `designer_set_widget_property`, `app_*` control, plus
project helpers (`project_new_ui`, `project_convert_ui`, `project_write_style`)
and the widget catalog.

It has **no equivalent for library-level work** — editing widget source,
running pytest, generating `.pyi` stubs or regenerating the tiering manifest
are all ordinary shell tasks. The skill's "never fall back to a shell" rule is
aimed at building and running *apps*; it is not a claim that the MCP can run
the test suite.
