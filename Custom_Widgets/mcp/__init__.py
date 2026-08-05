"""Custom Widgets MCP — agent control of Qt Designer + the project workflow.

Friendly entry points for humans and agents. Mount it WITHOUT `--project-dir`
so it stays per-session and dir-agnostic — the default project is the cwd
(repo root), and every tool takes a `project` arg to target any folder
(absolute used verbatim, relative resolved against the default):

    Custom_Widgets-mcp             # console script (installed)
    python -m Custom_Widgets.mcp   # module form (any env)

Register with Claude Code once, or let the repo's .mcp.json auto-mount it:

    claude mcp add custom-widgets -- Custom_Widgets-mcp

Pinning `--project-dir <example>` is discouraged: it bakes one session's
working folder into shared config and collides with other sessions. Pass
`project=` per call instead (or move the default live with
designer_open_workspace).

RULE #1: read the agent guide (``AGENT_GUIDE`` / the ``customwidgets://agent-guide``
resource) BEFORE any task, and drive the whole build/run/observe loop through the
MCP tools — never ad-hoc shell.
"""
from Custom_Widgets.mcp.guide import AGENT_GUIDE, RULE1
from Custom_Widgets.mcp.server import main, mcp

__all__ = ["main", "mcp", "AGENT_GUIDE", "RULE1"]
