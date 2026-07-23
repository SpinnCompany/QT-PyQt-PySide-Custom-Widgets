# Deck Pro — session handoff (2026-07-23)

Context for the next (MCP-mounted) session. Everything here is committed on
`feat/qcustom-datatable`; nothing is pushed (per the commit-locally rule).

## What happened this session
- Built a token-widget showcase, then established **RULE #1**: mount the
  `custom-widgets` MCP and read its knowledge/skills before any task; never
  develop/build/run a Custom_Widgets app via ad-hoc shell.
- Refactored the MCP into `Custom_Widgets/mcp/` (server.py + guide.py with the
  RULE #1 preamble hoisted), added `customwidgets://skills`, `python -m
  Custom_Widgets.mcp`, repo-root `.mcp.json` (auto-mount) and `AGENTS.md`.
- Wrote the Deck Pro rebuild plan.

## Commits
- `be7ad95` mcp: extract MCP into Custom_Widgets/mcp subpackage + agent discovery
- `921fb0e` examples: Aurora Command Deck token-widget showcase (single-page)
- `ccdc0a7` docs: Deck Pro MCP build plan

## State / where we parked
- The `custom-widgets` MCP could not be used **in that session** — an MCP only
  attaches at session startup, so a mid-session mount is impossible. Verified the
  server is healthy (44 tools, tests green) and the env runs Qt Designer
  (`designer`/`designer6`/`pyside6-designer` present, `DISPLAY=:1`, Qt GUI inits).
- **`examples/PySide6/AuroraCommandDeck/deck_pro.py` is an OFF-MCP draft** built
  before the rule — uncommitted, kept only as a content/layout reference. Do NOT
  ship it; rebuild via the MCP instead.

## Next session: do this
1. Mount confirmed (`/mcp` shows `custom-widgets`, ~44 tools).
2. Read `AGENTS.md` + `docs/design/deck-pro-build-plan.md` +
   `customwidgets://agent-guide` + `customwidgets://skills`.
3. Execute the build plan through the MCP: `designer_status` → `designer_launch`
   → theme-first → `MainWindow.ui` shell → 6 page components → `project_convert_ui`
   + wiring → `designer_run_app` + verify every page in both themes via `app_*` →
   clean teardown.
4. Surface any capability gap (widget without a Designer plugin, missing MCP tool)
   instead of shelling around it — add it to the MCP.
