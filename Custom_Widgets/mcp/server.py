########################################################################
## CUSTOM WIDGETS MCP SERVER
##
## Exposes the Qt Designer bridge and the project workflow to autonomous
## agents over the Model Context Protocol (stdio transport).
##
## Per-session and dir-agnostic: the default project is the cwd (repo root)
## and every tool takes a `project` arg to target any folder. Prefer mounting
## WITHOUT --project-dir; pass project= per call. --project-dir only moves the
## fallback default and should not pin a specific example in shared config:
##
##     Custom_Widgets-mcp
##     Custom_Widgets-mcp --project-dir /path/to/project   # optional: move default
##
## Register with Claude Code:
##
##     claude mcp add custom-widgets -- Custom_Widgets-mcp
##
## Requires the optional dependency:  pip install QT-PyQt-PySide-Custom-Widgets[mcp]
########################################################################
import argparse
import base64
import functools
import glob
import json
import os
from Custom_Widgets.Project import projectRoot
import subprocess
import sys
import threading
import traceback

try:
    from mcp.server.fastmcp import FastMCP, Image
except ImportError as exc:  # pragma: no cover
    # Raise, never sys.exit: SystemExit at import time kills whatever is
    # importing us (pytest collection dies with an INTERNALERROR). The
    # __main__ entry turns this into the friendly CLI message. This also
    # fires when an old 'mcp' (< 1.2, no fastmcp) is installed.
    raise ImportError(
        "The MCP server needs the 'mcp' package (>=1.9,<2 - 2.0 removed "
        "mcp.server.fastmcp):\n"
        "    pip install 'QT-PyQt-PySide-Custom-Widgets[mcp]'") from exc
try:
    from mcp.server.fastmcp.exceptions import ToolError
except ImportError:  # pragma: no cover
    ToolError = RuntimeError

########################################################################
## AGENT OPERATING GUIDE
##
## Shipped WITH the MCP (as server `instructions` and the
## `customwidgets://agent-guide` resource) so any agent pointed at the
## Custom Widgets MCP inherits how to work here: make changes VISIBLE and
## TEACHABLE, because the user is watching and learning.
########################################################################
from Custom_Widgets.mcp.guide import AGENT_GUIDE  # noqa: E402

mcp = FastMCP("custom_widgets_mcp", instructions=AGENT_GUIDE)


########################################################################
## UNIFORM STRUCTURED ERRORS
##
## Every tool failure reaches the agent as the SAME parseable JSON shape:
##   {"error": {"kind": "<machine-readable>", "message": "...",
##              "hint": "<what to do>", "details": {...}}}
## `_fail(kind, message, ...)` raises it; the `_tool` decorator (used in place
## of `@mcp.tool`) also converts any UNEXPECTED exception into the same envelope
## with kind="internal" (+ a traceback tail), so no tool ever emits an ad-hoc
## error string. FastMCP marks the result isError and forwards str(exc) verbatim.
########################################################################
class _ToolFailure(Exception):
    """An expected, classified tool failure. str() is the JSON envelope."""
    def __init__(self, kind, message, hint=None, details=None):
        error = {"kind": kind, "message": message}
        if hint:
            error["hint"] = hint
        if details is not None:
            error["details"] = details
        self.envelope = {"error": error}
        super().__init__(json.dumps(self.envelope))


def _fail(kind, message, hint=None, details=None):
    """Raise a uniform structured tool error."""
    raise _ToolFailure(kind, message, hint=hint, details=details)


def _tool(*args, **kwargs):
    """Drop-in for @mcp.tool that guarantees uniform structured errors: expected
    _ToolFailure passes through as its JSON envelope; anything unexpected becomes
    an {"error":{"kind":"internal",...}} envelope instead of a bare string."""
    register = mcp.tool(*args, **kwargs)

    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            try:
                return fn(*a, **kw)
            except _ToolFailure as exc:
                raise ToolError(str(exc))
            except ToolError:
                raise
            except Exception as exc:  # noqa: BLE001 - normalise everything
                env = {"error": {
                    "kind": "internal",
                    "message": str(exc) or type(exc).__name__,
                    "details": {"traceback": traceback.format_exc()[-1200:]}}}
                raise ToolError(json.dumps(env))
        return register(wrapper)

    return decorate


@mcp.resource("customwidgets://agent-guide")
def agent_guide() -> str:
    """How to work in this project so the user can watch and learn: edit forms
    in Designer, edit QSS in the QSS editor, run + observe the real app, keep
    components separate. Read this before building or editing GUIs here."""
    return AGENT_GUIDE


@mcp.resource("customwidgets://skills")
def skills() -> str:
    """Pointers to the shipped skills/knowledge an agent should read before
    building here. Referenced by RULE #1 in the agent guide."""
    return (
        "Custom Widgets — agent skills & knowledge\n"
        "=========================================\n"
        "1. Read customwidgets://agent-guide FIRST (RULE #1).\n"
        "2. Claude Code skills (.claude/skills/):\n"
        "   custom-widgets-app/SKILL.md — the FORMS PIPELINE for real apps\n"
        "   (.ui + compiled src/ + json-styles + scss $TOKENS + managers);\n"
        "   custom-widgets-demo/SKILL.md — the quick pure-code token demo\n"
        "   pattern, verified widget signatures, gotchas, screenshot-verify.\n"
        "3. Repo discovery: AGENTS.md at the repo root summarises how to work\n"
        "   here and how to mount this MCP.\n"
        "4. Build & run ONLY through this MCP's tools (designer_* / app_* /\n"
        "   designer_run_app). If a capability is missing, add it here.\n"
        "5. Before choosing/configuring a widget, read the catalog: the\n"
        "   widgets_catalog tool or customwidgets://catalog resource lists every\n"
        "   widget's props, allowed enum values, signals and tokens. Get exact\n"
        "   signatures with widget_signature, and preview any widget in isolation\n"
        "   with render_widget (both headless, no Designer needed).\n"
        "6. On failure, every tool returns a uniform JSON error:\n"
        "   {\"error\": {\"kind\", \"message\", \"hint\", \"details\"}}. Read `kind`\n"
        "   to branch (e.g. designer_not_running, app_not_running, bridge_error,\n"
        "   unknown_widget, invalid_argument, render_failed, internal) and follow\n"
        "   `hint`. Don't retry verbatim on a *_not_running kind — act on the hint.\n"
    )


@mcp.resource("customwidgets://catalog")
def catalog_resource() -> str:
    """Full machine-readable catalog of the Custom_Widgets widget library as
    JSON: every widget's module/class, each property with its type and allowed
    enum values, signals, the design tokens it honours, and whether it is
    Designer-droppable. Same data the widgets_catalog tool returns."""
    return json.dumps(catalog.discover_widgets(), indent=2)


_PROJECT_DIR = projectRoot()
_qt_app = None

# Designers this server launched: pid -> (project_dir, Popen). Lets
# designer_quit kill exactly the processes it owns instead of a /proc sweep
# (which is kept only as a fallback for other sessions' Designers).
_LAUNCHED_DESIGNERS = {}
_LAUNCHED_DESIGNERS_LOCK = threading.Lock()

from Custom_Widgets.mcp.workspace import ProjectRegistry  # noqa: E402
from Custom_Widgets.mcp import catalog  # noqa: E402

########################################################################
## PER-PROJECT SERIALIZATION
##
## Every tool takes an optional `project` (a folder, absolute or relative to the
## session default; blank = the default, which is the cwd / repo root unless
## moved with designer_open_workspace) and an optional `agent` tag.
## Bridge/app access for a project is funnelled through ONE worker thread
## (ProjectRegistry -> ProjectWorker), so multiple MCP clients sharing this
## server - e.g. several sessions over the HTTP transport - can never interleave
## commands against the same Designer/app. Different projects run in parallel;
## the same project is strictly FIFO. The default follows _PROJECT_DIR live, so
## --project-dir, designer_open_workspace and the test monkeypatch all apply.
########################################################################
REGISTRY = ProjectRegistry(lambda: _PROJECT_DIR)

# os.chdir is process-global; serialize the few tools that must chdir so
# concurrent clients (shared transport) don't yank each other's cwd.
_CWD_LOCK = threading.Lock()


def _projectDir():
    return _PROJECT_DIR


def _resolve(project=None):
    """Resolve a per-call `project` argument to an absolute project dir."""
    return REGISTRY.resolve(project)


def _client(project_dir=None):
    """Bridge client bound to a project folder (defaults to the session's
    project). QtNetwork needs a QCoreApplication in this process (no GUI)."""
    global _qt_app
    from qtpy.QtCore import QCoreApplication
    if _qt_app is None and QCoreApplication.instance() is None:
        _qt_app = QCoreApplication([])
    from Custom_Widgets.DesignerBridge import DesignerBridgeClient
    return DesignerBridgeClient(project_dir=project_dir or _projectDir(),
                                timeout_ms=500)


_NOT_RUNNING = ("Qt Designer is not reachable. Launch it with the "
                "designer_launch tool (or run `Custom_Widgets --start-designer "
                "--plugins` from the project folder '{dir}'), then retry.")


def _request(message, project=None, owner=None, reply_timeout_ms=10000):
    """Send a bridge request, SERIALIZED through the target project's worker so
    concurrent MCP clients never interleave against one Designer instance."""
    project_dir = _resolve(project)

    def call():
        reply = _client(project_dir).request(message,
                                              reply_timeout_ms=reply_timeout_ms)
        if reply is None:
            _fail("designer_not_running", _NOT_RUNNING.format(dir=project_dir),
                  hint="Call designer_launch, wait ~5s, then retry (check "
                       "designer_status).")
        if "error" in reply:
            _fail("bridge_error", "Designer reported: %s" % reply["error"],
                  details={"method": message.get("method")})
        return reply

    return REGISTRY.worker(project_dir).submit(
        call, owner=owner, label=message.get("method"))


########################################################################
## STATUS / LIFECYCLE
########################################################################
@_tool(annotations={"title": "Designer status", "readOnlyHint": True})
def designer_status(project: str = "") -> str:
    """Check whether Qt Designer (with the Custom_Widgets bridge) is running
    for this project, and report the project folder and bridge socket name.
    `project` targets another project folder (absolute, or relative to the
    session default); blank uses the default. Read-only ping - not queued."""
    from Custom_Widgets.DesignerBridge import bridgeServerName
    project_dir = _resolve(project)
    reachable = _client(project_dir).request({"method": "ping"}, reply_timeout_ms=2000)
    return json.dumps({
        "project_dir": project_dir,
        "bridge_socket": bridgeServerName(project_dir),
        "designer_running": bool(reachable and reachable.get("result") == "pong"),
    }, indent=2)


@_tool(annotations={"title": "Workspaces status (multi-project / multi-agent)",
                    "readOnlyHint": True})
def workspaces_status(project: str = "") -> str:
    """Discovery for multi-project / multi-agent work: for every project this
    server has touched (plus the default and an optional `project`), report
    whether its Designer and app are live and the state of its serialization
    queue - depth, busy, and the in-flight command's owner/label. Use it to see
    who is driving what before starting, and to pick a free project.

    Liveness is probed directly (not queued), so this never blocks behind
    queued work. Returns JSON: {default, projects:[{project_dir, bridge_socket,
    designer_running, app_running, queue_depth, busy, current}]}."""
    from Custom_Widgets.DesignerBridge import bridgeServerName
    dirs = set(REGISTRY.known())
    dirs.add(REGISTRY.default_dir())
    if project:
        dirs.add(_resolve(project))
    queue_stats = REGISTRY.statuses()
    projects = []
    for d in sorted(dirs):
        try:
            ping = _client(d).request({"method": "ping"}, reply_timeout_ms=1000)
            designer = bool(ping and ping.get("result") == "pong")
        except Exception:
            designer = False
        try:
            app_up = _app_client(d).isReachable(timeout_ms=1000)
        except Exception:
            app_up = False
        q = queue_stats.get(d, {"queue_depth": 0, "busy": False, "current": None})
        projects.append({
            "project_dir": d,
            "bridge_socket": bridgeServerName(d),
            "designer_running": designer,
            "app_running": app_up,
            "queue_depth": q["queue_depth"],
            "busy": q["busy"],
            "current": q["current"],
        })
    return json.dumps({"default": REGISTRY.default_dir(), "projects": projects},
                      indent=2)


@_tool(annotations={"title": "Switch Designer workspace / project folder"})
def designer_open_workspace(path: str) -> str:
    """Re-point the RUNNING Designer AND this MCP at another Custom_Widgets
    project folder in the same session: its workspace listing, QSS editor, theme
    list, Run target and the bridge socket all follow. `path` is absolute or
    relative to the current project dir. Use this instead of remounting the MCP
    when you need to work on a different project mid-session. After it returns,
    designer_status should report the new project_dir.

    NB: the bridge rebinds its socket during the switch, so this MCP's client is
    re-pointed at the new socket here too; a dropped reply to this call does not
    mean the switch failed - confirm with designer_status."""
    global _PROJECT_DIR
    target = os.path.abspath(os.path.join(_projectDir(), path))
    if not os.path.isdir(target):
        _fail("invalid_argument", "not a folder: %s" % target,
              hint="Pass a path to an existing Custom_Widgets project folder.")
    try:
        reply = _request({"method": "openWorkspace", "path": target})
        switched = reply.get("result")
    except (_ToolFailure, RuntimeError):
        # The bridge closes/rebinds its socket as part of the switch, which can
        # drop the reply to this very request (surfacing as a designer_not_running
        # _ToolFailure); the switch itself still happens.
        switched = "unknown (verify with designer_status)"
    # Keep the MCP's client (which derives the socket name from the project dir)
    # aligned with the bridge's new socket.
    _PROJECT_DIR = target
    try:
        from Custom_Widgets.Project import setProjectRoot
        setProjectRoot(target)
    except Exception:
        pass
    try:
        os.chdir(target)
    except OSError:
        pass
    from Custom_Widgets.DesignerBridge import bridgeServerName
    return json.dumps({"project_dir": target,
                       "bridge_socket": bridgeServerName(target),
                       "switched": switched}, indent=2)


@_tool(annotations={"title": "Launch Qt Designer"})
def designer_launch(project: str = "") -> str:
    """Launch Qt Designer with the Custom_Widgets plugins, tool docks and
    control bridge, working in a project folder (`project`; blank = default).
    Returns immediately; give Designer a few seconds to start, then check
    designer_status."""
    proc = subprocess.Popen(
        [os.path.join(os.path.dirname(sys.executable), "Custom_Widgets"),
         "--start-designer", "--plugins"],
        cwd=_resolve(project), start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with _LAUNCHED_DESIGNERS_LOCK:
        _LAUNCHED_DESIGNERS[proc.pid] = (_resolve(project), proc)
    return "Designer launching (verify with designer_status in ~5s)"


def _kill_designer_processes(project_dir=None):
    """Force-kill Designer processes (optionally only those whose project is
    project_dir). Prefers processes this server actually launched (tracked by
    PID - no /proc walk), falling back to a /proc scan for Designers another
    agent/session or a manual run started. Robust against a hung Designer
    whose bridge won't answer."""
    import glob
    import signal
    killed = []
    target = os.path.abspath(project_dir) if project_dir else None

    # 1) Processes we launched and can identify exactly.
    with _LAUNCHED_DESIGNERS_LOCK:
        for pid, (pdir, proc) in list(_LAUNCHED_DESIGNERS.items()):
            if target and pdir != target:
                continue
            if proc.poll() is not None:
                del _LAUNCHED_DESIGNERS[pid]
                continue
            try:
                proc.kill()
                killed.append(pid)
            except OSError:
                pass
            del _LAUNCHED_DESIGNERS[pid]

    # 2) Fallback: Designers we didn't launch (other sessions, manual runs).
    #    Match both the real binary and our launcher script.
    for proc in glob.glob("/proc/[0-9]*"):
        pid = proc.rsplit("/", 1)[-1]
        try:
            with open(os.path.join(proc, "cmdline"), "rb") as f:
                cmd = f.read().replace(b"\x00", b" ").decode("utf-8", "ignore")
        except OSError:
            continue
        if "pyside6-designer" not in cmd and "--start-designer" not in cmd:
            continue
        if int(pid) in killed:
            continue
        if target:
            try:
                cwd = os.path.abspath(os.readlink(os.path.join(proc, "cwd")))
            except OSError:
                cwd = None
            if cwd is not None and cwd != target:
                continue
        try:
            os.kill(int(pid), signal.SIGKILL)
            killed.append(int(pid))
        except (ProcessLookupError, PermissionError, ValueError):
            pass
    return killed


@_tool(annotations={"title": "Quit Qt Designer", "destructiveHint": True})
def designer_quit(force: bool = True, all_projects: bool = False,
                  project: str = "", confirm: str = "") -> str:
    """Tear Designer down cleanly. Asks it to quit over the bridge first; if
    force (default) it then force-kills any lingering Designer process (a hung
    Designer won't answer the bridge). Kills only THIS project's Designer
    (`project`; blank = default) unless all_projects=True.

    all_projects=True also kills Designers other agents/sessions are using, so
    it is guarded: re-call with confirm='all-projects' to actually do it."""
    import time
    if all_projects and confirm != "all-projects":
        _fail("confirmation_required",
              "all_projects=True force-kills EVERY project's Designer, including "
              "ones other agents/sessions are driving.",
              hint="Re-call with confirm='all-projects' to proceed, or drop "
                   "all_projects to quit only this project's Designer.")
    project_dir = _resolve(project)
    clean = False
    had_unsaved = []
    try:
        reply = _client(project_dir).request({"method": "quit"},
                                             reply_timeout_ms=2000)
        clean = bool(reply and reply.get("result") == "ok")
        had_unsaved = (reply or {}).get("had_unsaved", []) or []
    except Exception:
        pass
    if clean:
        time.sleep(1.0)  # give it a moment to exit on its own
    killed = []
    if force:
        killed = _kill_designer_processes(None if all_projects else project_dir)
    return json.dumps({"clean_quit": clean, "force_killed": killed,
                       "had_unsaved_forms": had_unsaved,
                       "scope": "all_projects" if all_projects else project_dir})


########################################################################
## FORMS
########################################################################
@_tool(annotations={"title": "Open .ui files in Designer"})
def designer_open_files(files: list[str], new_window: bool = False,
                        project: str = "", agent: str = "") -> str:
    """Open one or more .ui files. Default: create the form in the running
    Designer process - you can then inspect it (designer_get_object_info,
    designer_get_ui_code), edit it (designer_set_widget_property) and see it
    (designer_screenshot), though it is not shown in Designer's visible
    workspace (a PySide6 limitation). Set new_window=True to launch a
    Designer window a human can see. Paths may be relative to the project.
    `project` targets another project folder; `agent` tags who is driving it."""
    base = _resolve(project)
    absolute = [f if os.path.isabs(f) else os.path.join(base, f) for f in files]
    reply = _request({"method": "openFiles", "files": absolute,
                      "newWindow": new_window}, project=project, owner=agent)
    return json.dumps(reply)


@_tool(annotations={"title": "List form templates", "readOnlyHint": True})
def designer_list_templates(project: str = "") -> str:
    """List the form templates available to designer_new_form (e.g. the blank
    icons-prewired form, dashboard, login, settings page)."""
    return json.dumps(_request({"method": "listTemplates"}, project=project))


@_tool(annotations={"title": "Create a new form in Designer"})
def designer_new_form(name: str, template: str = "", folder: str = "",
                      open_after: bool = True, project: str = "",
                      agent: str = "") -> str:
    """Create a new .ui form from a template and open it in the running
    Designer instance.

    name: the form/file base name (sanitized; '.ui' added automatically).
    template: one of designer_list_templates (empty -> the blank
    icons-prewired form). folder: destination directory (empty -> the
    workspace folder, else <project>/ui). open_after: also open it now.
    `project`/`agent`: target folder and owner tag. Returns the created path."""
    reply = _request({"method": "newForm", "name": name,
                      "template": template or None,
                      "folder": folder or None, "open": open_after},
                     project=project, owner=agent)
    return json.dumps(reply)


@_tool(annotations={"title": "Close forms in Designer", "destructiveHint": True})
def designer_close_files(files: list[str] = [], close_all: bool = False,
                         project: str = "", agent: str = "") -> str:
    """Close open forms in Qt Designer, by file path or all of them.
    Unsaved changes in closed forms may prompt the user in Designer."""
    base = _resolve(project)
    absolute = [f if os.path.isabs(f) else os.path.join(base, f) for f in files]
    reply = _request({"method": "closeFiles", "files": absolute, "all": close_all},
                     project=project, owner=agent)
    return json.dumps(reply)


@_tool(annotations={"title": "Reload forms from disk"})
def designer_reload_forms(project: str = "", agent: str = "") -> str:
    """Reload open, unmodified forms from disk. Use after editing a .ui
    file on disk so Designer shows the new content (dirty forms are left
    untouched so user edits are never lost)."""
    return json.dumps(_request({"method": "reloadForms"},
                               project=project, owner=agent))


########################################################################
## INSPECTION (agent eyes)
########################################################################
@_tool(annotations={"title": "Screenshot Designer", "readOnlyHint": True})
def designer_screenshot(target: str = "current", project: str = "") -> Image:
    """Take a screenshot inside Qt Designer. target='current' captures the
    active form preview, 'main' captures the whole Designer window. Use it
    to visually verify forms while editing .ui files."""
    reply = _request({"method": "getScreenShot", "type": target},
                     project=project, reply_timeout_ms=20000)
    data = reply["result"]
    if isinstance(data, list):  # 'all' - return the first form
        data = data[0]["png"] if data else ""
    return Image(data=base64.b64decode(data), format="png")


@_tool(annotations={"title": "Get form source code", "readOnlyHint": True})
def designer_get_ui_code(code_type: str = "xml", project: str = "") -> str:
    """Get the ACTIVE form's current contents (including unsaved edits).
    code_type='xml' returns the .ui XML; 'pyside6' returns the generated
    Python class (via uic)."""
    reply = _request({"method": "getUiCode", "type": code_type},
                     project=project, reply_timeout_ms=30000)
    return reply["result"]


@_tool(annotations={"title": "Build/replace a form from .ui XML (live)"})
def designer_set_form_xml(xml: str, file: str = "", save: bool = False,
                          project: str = "", agent: str = "") -> str:
    """Design a form by pushing its .ui XML into Designer LIVE — Designer
    re-renders it immediately so the user watches it take shape. Use this to
    add layouts and widgets an agent can't add via property edits alone: read
    the form with designer_get_ui_code, transform the XML (add QVBoxLayout/
    QHBoxLayout/QGridLayout/QFormLayout, widgets, spacing), then push it here.
    Build progressively (push, designer_screenshot, refine). Targets the active
    form, or one named by `file`. Pass save=true to write it to disk (needed
    before compiling + running). Keep styles in the QSS editor, not inline."""
    reply = _request({"method": "setFormXml", "xml": xml,
                      "file": file or None, "save": save},
                     project=project, owner=agent, reply_timeout_ms=20000)
    return json.dumps(reply)


@_tool(annotations={"title": "Create a new form from .ui XML (live)"})
def designer_new_form_xml(name: str, xml: str, folder: str = "",
                          save: bool = True, project: str = "",
                          agent: str = "") -> str:
    """Create a NEW form from .ui XML and open it live in Designer. Writes
    <ui>/<name>.ui by default so it can be compiled (project_convert_ui) and
    run (designer_run_app). Author professional layouts (nested box/grid/form
    layouts with margins + spacing) and iterate with designer_set_form_xml +
    designer_screenshot; style in the QSS editor."""
    reply = _request({"method": "newFormXml", "name": name, "xml": xml,
                      "folder": folder or None, "save": save},
                     project=project, owner=agent, reply_timeout_ms=20000)
    return json.dumps(reply)


@_tool(annotations={"title": "Get widget tree", "readOnlyHint": True})
def designer_get_object_info(project: str = "") -> str:
    """Widget tree of every open form: class names, object names and
    geometries as JSON. Useful to understand a form before editing it."""
    reply = _request({"method": "getObjectInfos"}, project=project)
    return json.dumps(reply["result"], indent=2)


########################################################################
## WIDGET CATALOG + HEADLESS RENDER  (agent knowledge; no Designer needed)
##
## These tools answer "which widget, configured how" and "what does it look
## like" WITHOUT a running Designer or app. The catalog is read straight from
## each widget's `__catalog__` (via AST, so importing/instantiating nothing) —
## the single implementation lives in catalog.py, shared with the stub
## generator and the launch-gate manifest. render_widget draws one widget
## offscreen in an isolated subprocess.
########################################################################
def _find_widget(name):
    info = catalog.find_widget(name)
    if info is None:
        _fail("unknown_widget",
              "no widget named %r" % name,
              hint="Call widgets_catalog() to list the available widgets.")
    return info


@_tool(annotations={"title": "Widget catalog (machine-readable API)",
                       "readOnlyHint": True})
def widgets_catalog(name: str = "", query: str = "") -> str:
    """Machine-readable catalog of the Custom_Widgets library so an agent can
    pick and configure a widget WITHOUT reading source.

      no args   -> compact list of every widget {name, summary, droppable}.
      query     -> filter that list by substring of name / summary / token.
      name      -> FULL detail for one widget: module + class (feed to
                   render_widget / imports), every property with its type and
                   allowed enum 'values' (feed to app_set_property /
                   designer_set_widget_property), signals, the design tokens it
                   honours, and whether it is Designer-droppable.
    """
    if name:
        return json.dumps(_find_widget(name), indent=2)
    items = sorted(catalog.discover_widgets().values(), key=lambda w: w["name"])
    if query:
        q = query.lower()
        items = [w for w in items
                 if q in w["name"].lower() or q in w["summary"].lower()
                 or any(q in t.lower() for t in w["tokens_used"])]
    compact = [{"name": w["name"], "summary": w["summary"],
                "droppable": w["droppable"]} for w in items]
    return json.dumps({"count": len(compact), "widgets": compact}, indent=2)


# Runs in a subprocess (offscreen Qt). Reads its spec from CW_RENDER_SPEC so we
# avoid quoting a JSON blob through `python -c`.
_RENDER_SCRIPT = r"""
import base64, importlib, json, os, sys
spec = json.loads(os.environ["CW_RENDER_SPEC"])
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QByteArray, QBuffer, QIODevice
app = QApplication.instance() or QApplication([])
if spec.get("theme", True):
    try:
        from Custom_Widgets.theming.tokens import applyDesignTokens
        applyDesignTokens(app, theme=spec.get("theme_name", "light"))
    except Exception:
        pass
mod = importlib.import_module(spec["module"])
widget = getattr(mod, spec["class"])()
for key, value in (spec.get("props") or {}).items():
    setter = "set" + key[:1].upper() + key[1:]
    try:
        getattr(widget, setter)(value) if hasattr(widget, setter) \
            else widget.setProperty(key, value)
    except Exception:
        widget.setProperty(key, value)
try:
    widget.style().unpolish(widget); widget.style().polish(widget)
except Exception:
    pass
w, h = int(spec.get("width") or 0), int(spec.get("height") or 0)
if w > 0 and h > 0:
    widget.resize(w, h)
else:
    widget.adjustSize()
    if widget.width() < 2 or widget.height() < 2:
        widget.resize(widget.sizeHint())
widget.ensurePolished()
app.processEvents()
ba = QByteArray()                 # keep alive: QBuffer holds it by pointer
buf = QBuffer(ba)
buf.open(QIODevice.WriteOnly)
widget.grab().save(buf, "PNG")
sys.stdout.write(base64.b64encode(bytes(ba)).decode("ascii"))
"""


@_tool(annotations={"title": "Render a widget headless (offscreen)",
                       "readOnlyHint": True})
def render_widget(name: str, props: dict = {}, width: int = 0, height: int = 0,
                  theme: bool = True, theme_name: str = "light",
                  project: str = "") -> Image:
    """Render ONE Custom_Widgets widget to a PNG headlessly — no Designer, no
    running app, no display (offscreen Qt). Use it to SEE and self-verify a
    widget in isolation while writing UI code.

    name        a widget from widgets_catalog (its name or class).
    props       {prop: value} applied after construction (setter or Qt
                property); use the enum 'values' from widgets_catalog, e.g.
                {"text": "Save", "variant": "primary", "sizeVariant": "lg"}.
    width/height  pixel size; 0 (default) uses the widget's own sizeHint.
    theme       apply the built token theme QSS so tokenized colours show.
    theme_name  'light' or 'dark'.

    The widget is constructed with default args in an isolated subprocess (a bad
    widget can't affect the server); configure it through props."""
    info = _find_widget(name)
    spec = {"module": info["module"], "class": info["class"],
            "props": props or {}, "width": width, "height": height,
            "theme": theme, "theme_name": theme_name}
    proc = subprocess.run(
        [sys.executable, "-c", _RENDER_SCRIPT],
        cwd=_resolve(project), capture_output=True, text=True, timeout=60,
        env={**os.environ, "QT_QPA_PLATFORM": "offscreen",
             "CW_RENDER_SPEC": json.dumps(spec)})
    data = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    if proc.returncode != 0 or not data:
        _fail("render_failed", "could not render %s" % info["name"],
              hint="Check the widget name/props against widgets_catalog.",
              details={"stderr": (proc.stderr or "no output")[-1500:]})
    return Image(data=base64.b64decode(data), format="png")


@_tool(annotations={"title": "Widget type signature (.pyi)", "readOnlyHint": True})
def widget_signature(name: str) -> str:
    """The PEP 484 type signature of one widget, generated LIVE from the real
    class (so it is never stale): its base class, signals, typed properties, and
    every public method with its parameters. Use it to call constructors/methods
    with the right names and arity — qtpy's dynamic imports otherwise hide these.
    The same generator writes the on-disk .pyi stubs (py.typed) that type-checkers
    and IDEs consume; regenerate those with `python -m Custom_Widgets.mcp.stubgen
    --write`."""
    import importlib
    from Custom_Widgets.mcp import stubgen
    info = _find_widget(name)
    cls = getattr(importlib.import_module(info["module"]), info["class"])
    prop_types = stubgen._catalog_props().get(info["class"], {})
    return stubgen.stub_for_class(cls, prop_types)


@_tool(annotations={"title": "Search examples & docs (recipes)",
                    "readOnlyHint": True})
def search_examples(query: str, k: int = 5, full: bool = False,
                    project: str = "") -> str:
    """Search the bundled example projects and the repo docs for task->code
    recipes — grounding for HOW to use the widgets, straight from real code
    instead of guesswork. Lexical (BM25) ranking; a query is natural language or
    keywords (e.g. "badge with a count", "dark/light theme toggle", "sidebar
    navigation with stacked pages").

    Returns the top-k matches as JSON: {path, kind (example|doc), title, line,
    score, excerpt}. Open the `path` for the full recipe (or pass full=true to
    inline each match's text). Covers examples/ + README/AGENTS.md, plus an
    external docs tree if CUSTOM_WIDGETS_DOCS_DIR is set; internal design docs
    are not indexed."""
    from Custom_Widgets.mcp import retrieval
    k = max(1, min(int(k), 20))
    hits = retrieval.search(query, k=k, project_dir=_resolve(project), full=full)
    return json.dumps({"query": query, "count": len(hits), "results": hits},
                      indent=2)


@_tool(annotations={"title": "Lint design rules (glyph icons / hex / shadows)",
                       "readOnlyHint": True})
def design_lint(paths: list[str] = [], select: str = "", ignore: str = "",
                strict: bool = False, use_baseline: bool = True,
                project: str = "") -> str:
    """Check .py/.ui sources against the Custom_Widgets DESIGN rules — the visual
    rules a type checker can't see. RUN THIS before you finish a screen (and it
    also runs automatically on every file edit via the project hook).

    Rules:
      glyph-icons   [error]   no unicode glyph (◑ ＋ ⚙ ✦ …) used as an icon —
                              use a real painted/SVG icon asset instead
      hardcoded-hex [warning] no raw #rrggbb in chrome — drive colour from token
                              roles / a named palette constant so it flips theme
      drop-shadow   [warning] no QGraphicsDropShadowEffect without a justifying
                              `# allow-shadow:` comment
      large-icon    [warning] large images belong on a QPixmap, not a QIcon —
                              setIconSize(QSize(N,N)) with literal N>=40 flagged
                              (`# allow-large-icon:` to justify)

    paths        files/dirs (default: the project's configured lint paths).
    select/ignore comma-separated rule ids to run-only / skip.
    strict       treat warnings as failures too.
    use_baseline apply the repo baseline so only NEW violations surface.

    Returns JSON {summary:{errors,warnings,failed}, findings:[...]}. `failed`
    true means fix the findings (or justify with `# noqa: <rule-id>`). Rules are
    defined in Custom_Widgets/lint/rules.py and documented in
    Custom_Widgets/lint/DESIGN_RULES.md."""
    from Custom_Widgets import lint as _lint
    root = _resolve(project)
    cfg = _lint.load_config(root)
    csv = lambda v: frozenset(t.strip() for t in v.split(",") if t.strip()) or None
    cfg = cfg.with_overrides(
        paths=tuple(paths) or None,
        select=csv(select) if select else None,
        ignore=csv(ignore) if ignore else None,
        strict=True if strict else None)
    base = _lint.baseline.load(_lint.baseline.default_path(root)) if use_baseline else None
    findings = _lint.lint_paths(cfg.paths or (root,), cfg, baseline=base)
    errors = [f for f in findings if f.severity == _lint.ERROR]
    warnings = [f for f in findings if f.severity != _lint.ERROR]
    failed = bool(errors) or (cfg.strict and bool(findings))
    return json.dumps({
        "summary": {"errors": len(errors), "warnings": len(warnings),
                    "failed": failed,
                    "files": len({f.path for f in findings})},
        "findings": [{"rule": f.rule, "path": f.path, "line": f.line,
                      "col": f.col, "severity": f.severity,
                      "message": f.message} for f in findings],
    }, indent=2)


########################################################################
## THEME / STYLING
########################################################################
@_tool(annotations={"title": "Style Designer forms"})
def designer_set_stylesheet(qss: str, project: str = "", agent: str = "") -> str:
    """Apply a stylesheet to all open form previews in Designer (live
    preview only - it does not modify the .ui files)."""
    _request({"method": "setStyleSheet", "qss": qss}, project=project, owner=agent)
    return "stylesheet applied to open forms"


@_tool(annotations={"title": "Refresh Designer icon caches"})
def designer_refresh_icons(project: str = "") -> str:
    """Clear Designer's pixmap caches and repaint open forms. Use after
    the shared icon set (Qss/icons/icons) was regenerated on disk."""
    _request({"method": "refreshIcons"}, project=project)
    return "icon caches refreshed"


@_tool(annotations={"title": "Drive the QSS / Theme editor window"})
def designer_qss_window(action: str = "status", enabled: bool = True,
                        project: str = "") -> str:
    """Drive the standalone QSS / Theme editor window - a floating top-level
    window the dock tools can't reach.

      action='open'    show + raise the window
      action='close'   hide it
      action='status'  report {open, paintEntireDesigner, currentFile}
      action='paint'   set 'Paint entire Designer' to `enabled` (applies the
                       full current theme app-wide, or clears it)

    Use designer_qss_screenshot to capture the window."""
    return json.dumps(_request({"method": "qssWindow",
                                "action": action, "enabled": enabled},
                               project=project))


@_tool(annotations={"title": "Move/raise the Designer window"})
def designer_window(action: str = "raise", x: int = 0, y: int = 0,
                    width: int = 1100, height: int = 750,
                    project: str = "") -> str:
    """Position the Designer main window (multi-monitor compositors often park
    it on an off-screen output). action='screens' lists monitors; 'toPrimary'
    moves Designer onto the primary screen; 'move'/'geometry' use x/y[/w/h];
    'maximize'/'normal'/'raise' as named."""
    return json.dumps(_request({"method": "designerWindow", "action": action,
                                "x": x, "y": y, "width": width, "height": height},
                               project=project))


@_tool(annotations={"title": "Screenshot the QSS editor window",
                       "readOnlyHint": True})
def designer_qss_screenshot(project: str = "") -> Image:
    """Screenshot the floating QSS / Theme editor window. Open it first with
    designer_qss_window(action='open')."""
    reply = _request({"method": "qssWindow", "action": "screenshot"},
                     project=project, reply_timeout_ms=20000)
    data = reply.get("result", "")
    if not data:
        _fail("no_screenshot",
              reply.get("error", "no QSS window screenshot data"),
              hint="Open it first with designer_qss_window(action='open').")
    return Image(data=base64.b64decode(data), format="png")


########################################################################
## APP RUN (the project's main.py under the dev server, inside Designer)
########################################################################
@_tool(annotations={"title": "Run the project app"})
def designer_run_app(project: str = "", agent: str = "") -> dict:
    """Start the project's main.py under the dev-server supervisor from
    inside Designer. While running, saving a form in Designer regenerates
    src/ui_*.py and hot-restarts the app. Output streams into Designer's
    Logs dock and is readable via designer_app_logs."""
    return _request({"method": "runApp"}, project=project, owner=agent)


@_tool(annotations={"title": "Stop the project app"})
def designer_stop_app(project: str = "", agent: str = "") -> dict:
    """Stop the app started with designer_run_app."""
    return _request({"method": "stopApp"}, project=project, owner=agent)


@_tool(annotations={"title": "Restart the project app"})
def designer_restart_app(project: str = "", agent: str = "") -> dict:
    """Restart the app started with designer_run_app."""
    return _request({"method": "restartApp"}, project=project, owner=agent)


@_tool(annotations={"title": "Project app status", "readOnlyHint": True})
def designer_app_status(project: str = "") -> dict:
    """Whether the project app is running, and which script it runs."""
    return _request({"method": "appStatus"}, project=project)


@_tool(annotations={"title": "Read project app output", "readOnlyHint": True})
def designer_app_logs(lines: int = 100, project: str = "") -> dict:
    """The last stdout/stderr lines of the running (or last-run) app -
    includes crash tracebacks."""
    return _request({"method": "appLogs", "lines": lines}, project=project)


########################################################################
## RUNNING-APP OBSERVE + NAVIGATE
##
## The running app is a separate process from Designer; when launched via
## designer_run_app the dev server starts an in-app control server that
## these tools talk to directly (no Designer round-trip). Use them to SEE
## the real app window and DRIVE it - screenshot, walk the widget tree,
## click buttons, set text/properties, invoke slots.
########################################################################
def _app_client(project_dir=None):
    global _qt_app
    from qtpy.QtCore import QCoreApplication
    if _qt_app is None and QCoreApplication.instance() is None:
        _qt_app = QCoreApplication([])
    from Custom_Widgets.AppControl import AppControlClient
    return AppControlClient(project_dir=project_dir or _projectDir(),
                            timeout_ms=500)


_APP_NOT_RUNNING = ("The project app is not reachable. Start it with "
                    "designer_run_app (it must run under the dev server so its "
                    "in-app control server is enabled), then retry.")


def _app_request(message, project=None, owner=None, reply_timeout_ms=15000):
    """Send a running-app control request, SERIALIZED through the target
    project's worker (shared with the Designer bridge for that project)."""
    project_dir = _resolve(project)

    def call():
        reply = _app_client(project_dir).request(
            message, reply_timeout_ms=reply_timeout_ms)
        if reply is None:
            _fail("app_not_running", _APP_NOT_RUNNING,
                  hint="Start the app with designer_run_app, then retry (check "
                       "app_status).")
        if "error" in reply:
            _fail("app_error", "App reported: %s" % reply["error"],
                  details={"method": message.get("method")})
        return reply

    return REGISTRY.worker(project_dir).submit(
        call, owner=owner, label="app:" + str(message.get("method")))


@_tool(annotations={"title": "Running app status", "readOnlyHint": True})
def app_status(project: str = "") -> str:
    """Whether the running app's control server is reachable (the app must be
    started with designer_run_app). Use before the other app_* tools.
    Read-only reachability probe - not queued."""
    reachable = _app_client(_resolve(project)).isReachable(timeout_ms=1500)
    return json.dumps({"app_reachable": reachable})


@_tool(annotations={"title": "List running-app windows", "readOnlyHint": True})
def app_list_windows(project: str = "") -> str:
    """List the running app's top-level windows (objectName, class, title,
    geometry, which is active)."""
    return json.dumps(_app_request({"method": "listWindows"},
                                   project=project)["result"], indent=2)


@_tool(annotations={"title": "Screenshot the running app", "readOnlyHint": True})
def app_screenshot(target: str = "active", project: str = "") -> Image:
    """Screenshot a window of the RUNNING app (not Designer). target='active'
    (default), 'main' (the QMainWindow), or a window objectName."""
    reply = _app_request({"method": "screenshot", "target": target},
                         project=project, reply_timeout_ms=20000)
    return Image(data=base64.b64decode(reply["result"]), format="png")


@_tool(annotations={"title": "Running app widget tree", "readOnlyHint": True})
def app_object_tree(window: str = "active", project: str = "") -> str:
    """The live widget tree of a running-app window: class, objectName,
    geometry, text, visible/enabled. Use it to find things to click/edit."""
    return json.dumps(_app_request({"method": "objectTree", "window": window},
                                   project=project)["result"], indent=2)


@_tool(annotations={"title": "Find widgets in the running app", "readOnlyHint": True})
def app_find(query: str, by: str = "any", project: str = "") -> str:
    """Find widgets in the running app by=name|text|class|any (substring,
    case-insensitive). Returns objectName, class, text, visibility."""
    return json.dumps(_app_request({"method": "find", "query": query, "by": by},
                                   project=project)["result"], indent=2)


@_tool(annotations={"title": "Click a widget in the running app"})
def app_click(widget: str, project: str = "", agent: str = "") -> str:
    """Click a widget in the running app by objectName (buttons via click();
    others via a synthesized mouse click). Navigate the live app this way."""
    return json.dumps(_app_request({"method": "click", "widget": widget},
                                   project=project, owner=agent))


@_tool(annotations={"title": "Set text in the running app"})
def app_set_text(widget: str, text: str, project: str = "", agent: str = "") -> str:
    """Set a widget's text in the running app by objectName (setText or
    setPlainText)."""
    return json.dumps(_app_request({"method": "setText", "widget": widget,
                                    "text": text}, project=project, owner=agent))


@_tool(annotations={"title": "Set a widget property in the running app"})
def app_set_property(widget: str, property_name: str, value,
                     project: str = "", agent: str = "") -> str:
    """Set a Qt property on a running-app widget by objectName (repolishes so
    QSS re-evaluates). E.g. set 'variant' on a themed button."""
    return json.dumps(_app_request({"method": "setProperty", "widget": widget,
                                    "property": property_name, "value": value},
                                   project=project, owner=agent))


@_tool(annotations={"title": "Invoke a slot in the running app"})
def app_invoke(widget: str, slot: str, project: str = "", agent: str = "") -> str:
    """Call a no-arg method/slot on a running-app widget by objectName (e.g.
    'showMaximized', 'clear', a custom slot)."""
    return json.dumps(_app_request({"method": "invoke", "widget": widget,
                                    "slot": slot}, project=project, owner=agent))


@_tool(annotations={"title": "Move/raise the running-app window"})
def app_window(action: str = "raise", x: int = 0, y: int = 0,
               width: int = 900, height: int = 600, target: str = "active",
               project: str = "", agent: str = "") -> str:
    """Position a running-app window (multi-monitor compositors often park it
    on an off-screen output). action='screens' lists monitors; 'toPrimary'
    moves the window onto the primary screen; 'move'/'geometry' use x/y[/w/h];
    'maximize'/'normal'/'raise' as named. Use app_screenshot after to verify."""
    return json.dumps(_app_request({"method": "window", "action": action,
                                    "x": x, "y": y, "width": width,
                                    "height": height, "target": target},
                                   project=project, owner=agent))


########################################################################
## WINDOW MANAGEMENT (panes, dialogs, actions)
########################################################################
@_tool(annotations={"title": "List Designer panes", "readOnlyHint": True})
def designer_list_docks(project: str = "") -> str:
    """List Designer's dock panes (Widget Box, Property Editor, Object
    Inspector, Custom Widgets docks...) with visibility, area and floating
    state."""
    return json.dumps(_request({"method": "getDocks"},
                               project=project)["result"], indent=2)


@_tool(annotations={"title": "Arrange a Designer pane"})
def designer_arrange_dock(dock: str, visible: bool = True, area: str = "",
                          floating: bool = False, raise_: bool = False,
                          project: str = "") -> str:
    """Arrange a Designer dock pane matched by name/title substring:
    show/hide it, move it to an area ('left'/'right'/'top'/'bottom'),
    float it, or raise it above tabbed siblings."""
    message = {"method": "setDock", "dock": dock, "visible": visible,
               "floating": floating, "raise": raise_}
    if area:
        message["area"] = area
    return json.dumps(_request(message, project=project))


@_tool(annotations={"title": "List open dialogs", "readOnlyHint": True})
def designer_list_dialogs(project: str = "") -> str:
    """List visible dialogs / popups / prompts / error boxes in Designer
    (e.g. the startup New Form dialog or a save prompt), with their title,
    message text and buttons. Check this when Designer seems blocked."""
    return json.dumps(_request({"method": "getDialogs"},
                               project=project)["result"], indent=2)


@_tool(annotations={"title": "Dismiss a dialog"})
def designer_dismiss_dialog(match: str = "", button: str = "",
                            project: str = "") -> str:
    """Close an open dialog matched by title/class substring (empty match =
    first open dialog). Pass button text to click a specific button
    instead, e.g. button='Don't Save' on a save prompt, or button='Close'
    on the startup New Form dialog."""
    return json.dumps(_request({"method": "dismissDialog",
                                "match": match, "button": button},
                               project=project))


@_tool(annotations={"title": "List Designer actions", "readOnlyHint": True})
def designer_list_actions(contains: str = "", project: str = "") -> str:
    """List Designer's menu/toolbar actions (Save, Save All, Preview,
    Close, ...). Optionally filter by substring. Trigger any of them with
    designer_trigger_action."""
    actions = _request({"method": "getActions"}, project=project)["result"]
    if contains:
        needle = contains.lower()
        actions = [a for a in actions
                   if needle in a["text"].lower() or needle in a["objectName"].lower()]
    return json.dumps(actions, indent=2)


@_tool(annotations={"title": "Trigger a Designer action"})
def designer_trigger_action(action: str, project: str = "", agent: str = "") -> str:
    """Trigger a Designer menu/toolbar action by text or objectName
    (e.g. 'Save Form', 'Save All', 'Preview'). Use it to save forms after
    edits."""
    return json.dumps(_request({"method": "triggerAction", "action": action},
                               project=project, owner=agent))


@_tool(annotations={"title": "Set a widget property (undoable)"})
def designer_set_widget_property(widget: str, property_name: str, value,
                                 project: str = "", agent: str = "") -> str:
    """Set a property on a widget of the ACTIVE form (matched by
    objectName) through Designer's undo stack, like a manual edit - e.g.
    text, geometry, toolTip, checked. NOTE: styleSheet is refused by
    project rule; persist styles with project_write_style instead."""
    return json.dumps(_request({"method": "setWidgetProperty", "widget": widget,
                                "property": property_name, "value": value},
                               project=project, owner=agent))


########################################################################
## PROJECT WORKFLOW
########################################################################
@_tool(annotations={"title": "List project .ui files", "readOnlyHint": True})
def project_list_ui_files(project: str = "") -> str:
    """List the .ui files of the project (excluding generated copies)."""
    base = _resolve(project)
    found = []
    skip = {".git", "__pycache__", "generated-files", "node_modules", "venv", ".venv"}
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in skip]
        for name in files:
            if name.lower().endswith(".ui") and not name.startswith("new_"):
                found.append(os.path.relpath(os.path.join(root, name), base))
    return json.dumps(sorted(found), indent=2)


@_tool(annotations={"title": "Create a new .ui form"})
def project_new_ui(name: str, project: str = "") -> str:
    """Create ui/<name>.ui pre-wired to the theme icons resource
    (Qss/icons/_icons.qrc), ready to design in Qt Designer."""
    base = _resolve(project)
    with _CWD_LOCK:  # create_ui_file relies on cwd; keep it process-safe
        previous = os.getcwd()
        os.chdir(base)
        try:
            from Custom_Widgets.ProjectMaker import create_ui_file
            path = create_ui_file(name)
            if path is None:
                _fail("already_exists", "ui/%s.ui already exists" % name,
                      hint="Pick another name or edit the existing form.")
            return os.path.relpath(path, base)
        finally:
            os.chdir(previous)


@_tool(annotations={"title": "Convert ui/ to Python sources"})
def project_convert_ui(ui_path: str = "ui", src_output_dir: str = "src",
                       project: str = "") -> str:
    """Convert the project's .ui files to Python (src/ui_*.py) plus the
    generated-files/ intermediates the theme engine needs. Run after
    editing .ui files (equivalent of `Custom_Widgets --convert-ui`)."""
    exe = os.path.join(os.path.dirname(sys.executable), "Custom_Widgets")
    proc = subprocess.run(
        [exe, "--convert-ui", ui_path, "--src-output-dir", src_output_dir],
        cwd=_resolve(project), capture_output=True, text=True, timeout=300,
        env={**os.environ, "QT_QPA_PLATFORM": os.environ.get("QT_QPA_PLATFORM", "offscreen")})
    if proc.returncode != 0:
        _fail("convert_failed", "ui-to-Python conversion failed",
              hint="Fix the .ui/scss error in the details, then retry.",
              details={"stderr": proc.stderr[-1500:]})
    generated = [line for line in proc.stdout.splitlines()
                 if "Python:" in line or "Completed" in line]
    return "\n".join(generated) or "converted"


@_tool(annotations={"title": "Write project styles (scss)"})
def project_write_style(scss: str, file: str = "", project: str = "") -> str:
    """Persist custom styles the Custom_Widgets way: appended to
    Qss/scss/defaultStyle.scss, or written to a separate scss file that
    gets @import-ed into it (pass file='mystyles.scss'). Target widgets
    with objectName selectors, e.g. '#saveBtn { padding: 6px; }'. This is
    the ONLY sanctioned way to persist styles - never put styleSheet
    properties in .ui files. The edited .scss is streamed live into the QSS
    editor so the user watches it change. Styles apply on the next app run;
    for an instant Designer preview also call designer_set_stylesheet."""
    scss_dir = os.path.join(_resolve(project), "Qss", "scss")
    os.makedirs(scss_dir, exist_ok=True)
    default_path = os.path.join(scss_dir, "defaultStyle.scss")
    if not os.path.exists(default_path):
        with open(default_path, "w", encoding="utf-8") as f:
            f.write("// Project default styles (override theme styles)\n")

    if file:
        name = os.path.basename(file)
        if not name.endswith(".scss"):
            name += ".scss"
        edited = os.path.join(scss_dir, name)
        with open(edited, "w", encoding="utf-8") as f:
            f.write(scss.rstrip() + "\n")
        import_line = f"@import '{name[:-5]}';"
        with open(default_path, encoding="utf-8") as f:
            default_content = f.read()
        if import_line not in default_content:
            with open(default_path, "a", encoding="utf-8") as f:
                f.write(f"\n{import_line}\n")
        _show_style_in_editor(edited, project)
        return f"wrote Qss/scss/{name} and imported it from defaultStyle.scss"

    with open(default_path, "a", encoding="utf-8") as f:
        f.write("\n" + scss.rstrip() + "\n")
    _show_style_in_editor(default_path, project)
    return "appended to Qss/scss/defaultStyle.scss"


def _show_style_in_editor(path, project=None):
    """Best-effort: open the just-edited .scss in Designer's QSS editor so the
    user sees the change live. No-op when Designer isn't running."""
    try:
        _client(_resolve(project)).request(
            {"method": "qssWindow", "action": "load", "file": path},
            reply_timeout_ms=2000)
    except Exception:
        pass


def _loopback_host(host):
    return host in ("127.0.0.1", "localhost", "::1")


def _enable_http_auth(token, host, port):
    """Require ``Authorization: Bearer <token>`` on every HTTP request. Uses
    the mcp SDK's native bearer middleware (token verifier + AuthSettings) so
    unauthenticated requests get a 401 instead of reaching the tool layer."""
    import hmac

    from mcp.server.auth.provider import AccessToken, TokenVerifier
    from mcp.server.auth.settings import AuthSettings
    from pydantic import AnyHttpUrl

    class _StaticTokenVerifier(TokenVerifier):
        def __init__(self, secret):
            self._secret = secret.encode("utf-8")

        async def verify_token(self, token):
            if hmac.compare_digest(token.encode("utf-8"), self._secret):
                return AccessToken(token=token, client_id="static", scopes=[])
            return None

    base = f"http://{host}:{port}"
    mcp._token_verifier = _StaticTokenVerifier(token)
    try:
        mcp.settings.auth = AuthSettings(
            issuer_url=AnyHttpUrl(base),
            resource_server_url=AnyHttpUrl(base),
        )
    except Exception:  # pragma: no cover - pydantic/URL edge cases
        pass
    print("MCP HTTP: bearer-token auth enabled", file=sys.stderr)


def main():
    global _PROJECT_DIR
    parser = argparse.ArgumentParser(description="Custom Widgets MCP server")
    parser.add_argument("--project-dir", default=projectRoot(),
                        help="Optional: move the FALLBACK default project "
                             "folder (defaults to cwd / the repo root). Prefer "
                             "leaving this unset and targeting each folder via "
                             "the per-tool `project` argument — pinning a "
                             "specific example here bakes it into shared config "
                             "and collides with other sessions.")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio",
                        help="stdio (default): one client per process. http: a "
                             "single SHARED daemon many sessions/agents connect "
                             "to - the per-project queue then serializes them. "
                             "Point .mcp.json at http://<host>:<port>/mcp.")
    parser.add_argument("--host", default="127.0.0.1",
                        help="HTTP bind host (transport=http). Default 127.0.0.1.")
    parser.add_argument("--port", type=int, default=8765,
                        help="HTTP bind port (transport=http). Default 8765.")
    parser.add_argument(
        "--token", default=os.environ.get("CUSTOM_WIDGETS_MCP_TOKEN", ""),
        help="Bearer token HTTP clients must present (Authorization: Bearer "
             "<token>). Non-loopback binds REQUIRE one; the daemon refuses to "
             "start otherwise. Loopback works without it (matches existing "
             "configs), but set it when several machines/users can reach the "
             "port. Also read from CUSTOM_WIDGETS_MCP_TOKEN.")
    args = parser.parse_args()
    _PROJECT_DIR = os.path.abspath(args.project_dir)
    from Custom_Widgets.Project import setProjectRoot
    setProjectRoot(_PROJECT_DIR)
    os.chdir(_PROJECT_DIR)
    if args.transport == "http":
        # Shared daemon: several sessions/agents dial in over streamable HTTP;
        # cross-client commands to one project are serialized by its worker.
        if not _loopback_host(args.host) and not args.token:
            raise SystemExit(
                f"refusing to bind the MCP HTTP daemon to a non-loopback host "
                f"({args.host}) without a bearer token. Pass --token=... (or "
                f"set CUSTOM_WIDGETS_MCP_TOKEN) and put that token in the "
                f"client's Authorization header.")
        try:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
        except Exception:  # pragma: no cover - older FastMCP settings shape
            pass
        if args.token:
            _enable_http_auth(args.token, args.host, args.port)
        mcp.run(transport="streamable-http")
    else:
        mcp.run()


if __name__ == "__main__":
    main()
