"""Enable ``python -m Custom_Widgets.mcp`` (portable across environments)."""
import sys

try:
    from Custom_Widgets.mcp.server import main
except ImportError as exc:
    # the missing-'mcp' guard in server.py — show its message, not a traceback
    sys.exit(str(exc))

if __name__ == "__main__":
    main()
