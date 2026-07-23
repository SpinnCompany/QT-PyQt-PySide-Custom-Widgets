"""Custom Widgets MCP — agent control of Qt Designer + the project workflow.

Friendly entry points for humans and agents:

    Custom_Widgets-mcp --project-dir .        # console script (installed)
    python -m Custom_Widgets.mcp --project-dir .   # module form (any env)

Register with Claude Code once, or let the repo's .mcp.json auto-mount it:

    claude mcp add custom-widgets -- Custom_Widgets-mcp --project-dir .

RULE #1: read the agent guide (``AGENT_GUIDE`` / the ``customwidgets://agent-guide``
resource) BEFORE any task, and drive the whole build/run/observe loop through the
MCP tools — never ad-hoc shell.
"""
from Custom_Widgets.mcp.guide import AGENT_GUIDE, RULE1
from Custom_Widgets.mcp.server import main, mcp

__all__ = ["main", "mcp", "AGENT_GUIDE", "RULE1"]
