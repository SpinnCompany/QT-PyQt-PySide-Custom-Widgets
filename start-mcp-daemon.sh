#!/usr/bin/env bash
# Start the Custom_Widgets MCP server as a shared HTTP daemon.
# Kill with: pkill -f "Custom_Widgets.mcp.*--transport http"
set -eu
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
exec .venv/bin/python -m Custom_Widgets.mcp --transport http --port 8765