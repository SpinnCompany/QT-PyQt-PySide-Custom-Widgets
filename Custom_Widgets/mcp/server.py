########################################################################
## CUSTOM WIDGETS MCP SERVER
##
## Exposes the Qt Designer bridge and the project workflow to autonomous
## agents over the Model Context Protocol (stdio transport).
##
## Run from the project folder (the same folder the app and Designer run
## from - the bridge socket name is derived from it):
##
##     Custom_Widgets-mcp
##     Custom_Widgets-mcp --project-dir /path/to/project
##
## Register with Claude Code:
##
##     claude mcp add custom-widgets -- Custom_Widgets-mcp --project-dir .
##
## Requires the optional dependency:  pip install QT-PyQt-PySide-Custom-Widgets[mcp]
########################################################################
import argparse
import ast
import base64
import functools
import glob
import json
import os
from Custom_Widgets.Project import projectRoot
import subprocess
import sys

try:
    from mcp.server.fastmcp import FastMCP, Image
except ImportError:  # pragma: no cover
    sys.exit("The MCP server needs the 'mcp' package:\n"
             "    pip install QT-PyQt-PySide-Custom-Widgets[mcp]")

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
        "2. Claude Code skill: .claude/skills/custom-widgets-demo/SKILL.md —\n"
        "   the token-widget demo pattern, verified widget signatures, gotchas,\n"
        "   and the screenshot-verify workflow. Leads with 'MCP first'.\n"
        "3. Repo discovery: AGENTS.md at the repo root summarises how to work\n"
        "   here and how to mount this MCP.\n"
        "4. Build & run ONLY through this MCP's tools (designer_* / app_* /\n"
        "   designer_run_app). If a capability is missing, add it here.\n"
        "5. Before choosing/configuring a widget, read the catalog: the\n"
        "   widgets_catalog tool or customwidgets://catalog resource lists every\n"
        "   widget's props, allowed enum values, signals and tokens. Get exact\n"
        "   signatures with widget_signature, and preview any widget in isolation\n"
        "   with render_widget (both headless, no Designer needed).\n"
    )


@mcp.resource("customwidgets://catalog")
def catalog_resource() -> str:
    """Full machine-readable catalog of the Custom_Widgets widget library as
    JSON: every widget's module/class, each property with its type and allowed
    enum values, signals, the design tokens it honours, and whether it is
    Designer-droppable. Same data the widgets_catalog tool returns."""
    return json.dumps(_discover_widgets(), indent=2)


_PROJECT_DIR = projectRoot()
_qt_app = None


def _projectDir():
    return _PROJECT_DIR


def _client():
    """Bridge client bound to the project folder. QtNetwork needs a
    QCoreApplication in this process (no GUI)."""
    global _qt_app
    from qtpy.QtCore import QCoreApplication
    if _qt_app is None and QCoreApplication.instance() is None:
        _qt_app = QCoreApplication([])
    from Custom_Widgets.DesignerBridge import DesignerBridgeClient
    return DesignerBridgeClient(project_dir=_projectDir(), timeout_ms=500)


_NOT_RUNNING = ("Qt Designer is not reachable. Launch it with the "
                "designer_launch tool (or run `Custom_Widgets --start-designer "
                "--plugins` from the project folder '{dir}'), then retry.")


def _request(message, reply_timeout_ms=10000):
    reply = _client().request(message, reply_timeout_ms=reply_timeout_ms)
    if reply is None:
        raise RuntimeError(_NOT_RUNNING.format(dir=_projectDir()))
    if "error" in reply:
        raise RuntimeError(f"Designer reported: {reply['error']}")
    return reply


########################################################################
## STATUS / LIFECYCLE
########################################################################
@mcp.tool(annotations={"title": "Designer status", "readOnlyHint": True})
def designer_status() -> str:
    """Check whether Qt Designer (with the Custom_Widgets bridge) is running
    for this project, and report the project folder and bridge socket name."""
    from Custom_Widgets.DesignerBridge import bridgeServerName

    reachable = _client().request({"method": "ping"}, reply_timeout_ms=2000)
    return json.dumps({
        "project_dir": _projectDir(),
        "bridge_socket": bridgeServerName(_projectDir()),
        "designer_running": bool(reachable and reachable.get("result") == "pong"),
    }, indent=2)


@mcp.tool(annotations={"title": "Switch Designer workspace / project folder"})
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
        raise RuntimeError("not a folder: %s" % target)
    try:
        reply = _request({"method": "openWorkspace", "path": target})
        switched = reply.get("result")
    except RuntimeError:
        # The bridge closes/rebinds its socket as part of the switch, which can
        # drop the reply to this very request; the switch itself still happens.
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


@mcp.tool(annotations={"title": "Launch Qt Designer"})
def designer_launch() -> str:
    """Launch Qt Designer with the Custom_Widgets plugins, tool docks and
    control bridge, working in this project folder. Returns immediately;
    give Designer a few seconds to start, then check designer_status."""
    subprocess.Popen(
        [os.path.join(os.path.dirname(sys.executable), "Custom_Widgets"),
         "--start-designer", "--plugins"],
        cwd=_projectDir(), start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return "Designer launching (verify with designer_status in ~5s)"


def _kill_designer_processes(project_dir=None):
    """Force-kill pyside6-designer processes (optionally only those whose cwd is
    project_dir). Robust against a hung Designer whose bridge won't answer."""
    import glob
    import signal
    killed = []
    target = os.path.abspath(project_dir) if project_dir else None
    for proc in glob.glob("/proc/[0-9]*"):
        pid = proc.rsplit("/", 1)[-1]
        try:
            with open(os.path.join(proc, "cmdline"), "rb") as f:
                cmd = f.read().replace(b"\x00", b" ").decode("utf-8", "ignore")
        except OSError:
            continue
        if "pyside6-designer" not in cmd:
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


@mcp.tool(annotations={"title": "Quit Qt Designer", "destructiveHint": True})
def designer_quit(force: bool = True, all_projects: bool = False) -> str:
    """Tear Designer down cleanly. Asks it to quit over the bridge first; if
    force (default) it then force-kills any lingering Designer process (a hung
    Designer won't answer the bridge). Kills only THIS project's Designer unless
    all_projects=True. Use this instead of leaving windows around."""
    import time
    clean = False
    had_unsaved = []
    try:
        reply = _client().request({"method": "quit"}, reply_timeout_ms=2000)
        clean = bool(reply and reply.get("result") == "ok")
        had_unsaved = (reply or {}).get("had_unsaved", []) or []
    except Exception:
        pass
    if clean:
        time.sleep(1.0)  # give it a moment to exit on its own
    killed = []
    if force:
        killed = _kill_designer_processes(
            None if all_projects else _projectDir())
    return json.dumps({"clean_quit": clean, "force_killed": killed,
                       "had_unsaved_forms": had_unsaved})


########################################################################
## FORMS
########################################################################
@mcp.tool(annotations={"title": "Open .ui files in Designer"})
def designer_open_files(files: list[str], new_window: bool = False) -> str:
    """Open one or more .ui files. Default: create the form in the running
    Designer process - you can then inspect it (designer_get_object_info,
    designer_get_ui_code), edit it (designer_set_widget_property) and see it
    (designer_screenshot), though it is not shown in Designer's visible
    workspace (a PySide6 limitation). Set new_window=True to launch a
    Designer window a human can see. Paths may be relative to the project."""
    absolute = [f if os.path.isabs(f) else os.path.join(_projectDir(), f)
                for f in files]
    reply = _request({"method": "openFiles", "files": absolute,
                      "newWindow": new_window})
    return json.dumps(reply)


@mcp.tool(annotations={"title": "List form templates", "readOnlyHint": True})
def designer_list_templates() -> str:
    """List the form templates available to designer_new_form (e.g. the blank
    icons-prewired form, dashboard, login, settings page)."""
    return json.dumps(_request({"method": "listTemplates"}))


@mcp.tool(annotations={"title": "Create a new form in Designer"})
def designer_new_form(name: str, template: str = "", folder: str = "",
                      open_after: bool = True) -> str:
    """Create a new .ui form from a template and open it in the running
    Designer instance.

    name: the form/file base name (sanitized; '.ui' added automatically).
    template: one of designer_list_templates (empty -> the blank
    icons-prewired form). folder: destination directory (empty -> the
    workspace folder, else <project>/ui). open_after: also open it now.
    Returns the created path."""
    reply = _request({"method": "newForm", "name": name,
                      "template": template or None,
                      "folder": folder or None, "open": open_after})
    return json.dumps(reply)


@mcp.tool(annotations={"title": "Close forms in Designer", "destructiveHint": True})
def designer_close_files(files: list[str] = [], close_all: bool = False) -> str:
    """Close open forms in Qt Designer, by file path or all of them.
    Unsaved changes in closed forms may prompt the user in Designer."""
    absolute = [f if os.path.isabs(f) else os.path.join(_projectDir(), f)
                for f in files]
    reply = _request({"method": "closeFiles", "files": absolute, "all": close_all})
    return json.dumps(reply)


@mcp.tool(annotations={"title": "Reload forms from disk"})
def designer_reload_forms() -> str:
    """Reload open, unmodified forms from disk. Use after editing a .ui
    file on disk so Designer shows the new content (dirty forms are left
    untouched so user edits are never lost)."""
    return json.dumps(_request({"method": "reloadForms"}))


########################################################################
## INSPECTION (agent eyes)
########################################################################
@mcp.tool(annotations={"title": "Screenshot Designer", "readOnlyHint": True})
def designer_screenshot(target: str = "current") -> Image:
    """Take a screenshot inside Qt Designer. target='current' captures the
    active form preview, 'main' captures the whole Designer window. Use it
    to visually verify forms while editing .ui files."""
    reply = _request({"method": "getScreenShot", "type": target},
                     reply_timeout_ms=20000)
    data = reply["result"]
    if isinstance(data, list):  # 'all' - return the first form
        data = data[0]["png"] if data else ""
    return Image(data=base64.b64decode(data), format="png")


@mcp.tool(annotations={"title": "Get form source code", "readOnlyHint": True})
def designer_get_ui_code(code_type: str = "xml") -> str:
    """Get the ACTIVE form's current contents (including unsaved edits).
    code_type='xml' returns the .ui XML; 'pyside6' returns the generated
    Python class (via uic)."""
    reply = _request({"method": "getUiCode", "type": code_type},
                     reply_timeout_ms=30000)
    return reply["result"]


@mcp.tool(annotations={"title": "Build/replace a form from .ui XML (live)"})
def designer_set_form_xml(xml: str, file: str = "", save: bool = False) -> str:
    """Design a form by pushing its .ui XML into Designer LIVE — Designer
    re-renders it immediately so the user watches it take shape. Use this to
    add layouts and widgets an agent can't add via property edits alone: read
    the form with designer_get_ui_code, transform the XML (add QVBoxLayout/
    QHBoxLayout/QGridLayout/QFormLayout, widgets, spacing), then push it here.
    Build progressively (push, designer_screenshot, refine). Targets the active
    form, or one named by `file`. Pass save=true to write it to disk (needed
    before compiling + running). Keep styles in the QSS editor, not inline."""
    reply = _request({"method": "setFormXml", "xml": xml,
                      "file": file or None, "save": save}, reply_timeout_ms=20000)
    return json.dumps(reply)


@mcp.tool(annotations={"title": "Create a new form from .ui XML (live)"})
def designer_new_form_xml(name: str, xml: str, folder: str = "",
                          save: bool = True) -> str:
    """Create a NEW form from .ui XML and open it live in Designer. Writes
    <ui>/<name>.ui by default so it can be compiled (project_convert_ui) and
    run (designer_run_app). Author professional layouts (nested box/grid/form
    layouts with margins + spacing) and iterate with designer_set_form_xml +
    designer_screenshot; style in the QSS editor."""
    reply = _request({"method": "newFormXml", "name": name, "xml": xml,
                      "folder": folder or None, "save": save}, reply_timeout_ms=20000)
    return json.dumps(reply)


@mcp.tool(annotations={"title": "Get widget tree", "readOnlyHint": True})
def designer_get_object_info() -> str:
    """Widget tree of every open form: class names, object names and
    geometries as JSON. Useful to understand a form before editing it."""
    reply = _request({"method": "getObjectInfos"})
    return json.dumps(reply["result"], indent=2)


########################################################################
## WIDGET CATALOG + HEADLESS RENDER  (agent knowledge; no Designer needed)
##
## These tools answer "which widget, configured how" and "what does it look
## like" WITHOUT a running Designer or app. The catalog is read straight from
## each widget's `__catalog__` (via AST, so importing/instantiating nothing);
## render_widget draws one widget offscreen in an isolated subprocess.
########################################################################
def _widgets_package_dir():
    import Custom_Widgets
    return os.path.dirname(Custom_Widgets.__file__)


def _ast_literal(node):
    try:
        return ast.literal_eval(node)
    except (ValueError, SyntaxError):
        return None


def _class_catalog(node, stem):
    """Extract a widget's catalog entry from its ClassDef, or None if the class
    declares no `__catalog__`."""
    catalog = None
    attrs = {}
    for stmt in node.body:
        if not isinstance(stmt, ast.Assign):
            continue
        for tgt in stmt.targets:
            if not isinstance(tgt, ast.Name):
                continue
            if tgt.id == "__catalog__":
                catalog = _ast_literal(stmt.value)
            elif tgt.id in ("WIDGET_MODULE", "WIDGET_TOOLTIP", "WIDGET_DOM_XML"):
                attrs[tgt.id] = _ast_literal(stmt.value)
    if not isinstance(catalog, dict):
        return None
    doc = ast.get_docstring(node)
    summary = (doc.strip().splitlines()[0] if doc
               else (attrs.get("WIDGET_TOOLTIP") or ""))
    return {
        "name": catalog.get("name") or node.name,
        "class": node.name,
        "module": attrs.get("WIDGET_MODULE") or "Custom_Widgets.%s" % stem,
        "summary": summary,
        "props": catalog.get("props", {}),
        "signals": catalog.get("signals", []),
        "tokens_used": catalog.get("tokens_used", []),
        "droppable": "WIDGET_DOM_XML" in attrs,
    }


@functools.lru_cache(maxsize=1)
def _discover_widgets():
    """Scan the Custom_Widgets package for widgets declaring `__catalog__` and
    return {name: entry}. Parsed via AST — nothing is imported or instantiated,
    so it's safe and fast in the headless server process."""
    out = {}
    for path in sorted(glob.glob(os.path.join(_widgets_package_dir(), "QCustom*.py"))):
        stem = os.path.splitext(os.path.basename(path))[0]
        try:
            with open(path, encoding="utf-8") as fh:
                tree = ast.parse(fh.read(), filename=path)
        except (OSError, SyntaxError):
            continue
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                entry = _class_catalog(node, stem)
                if entry:
                    out[entry["name"]] = entry
    return out


def _find_widget(name):
    widgets = _discover_widgets()
    info = widgets.get(name)
    if info is None:
        needle = name.lower()
        info = next((w for w in widgets.values()
                     if w["name"].lower() == needle or w["class"].lower() == needle),
                    None)
    if info is None:
        raise RuntimeError("no widget named %r; call widgets_catalog() to list them"
                           % name)
    return info


@mcp.tool(annotations={"title": "Widget catalog (machine-readable API)",
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
    items = sorted(_discover_widgets().values(), key=lambda w: w["name"])
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
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
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


@mcp.tool(annotations={"title": "Render a widget headless (offscreen)",
                       "readOnlyHint": True})
def render_widget(name: str, props: dict = {}, width: int = 0, height: int = 0,
                  theme: bool = True, theme_name: str = "light") -> Image:
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
        cwd=_projectDir(), capture_output=True, text=True, timeout=60,
        env={**os.environ, "QT_QPA_PLATFORM": "offscreen",
             "CW_RENDER_SPEC": json.dumps(spec)})
    data = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    if proc.returncode != 0 or not data:
        raise RuntimeError("render failed:\n%s" % (proc.stderr[-2000:] or "no output"))
    return Image(data=base64.b64decode(data), format="png")


@mcp.tool(annotations={"title": "Widget type signature (.pyi)", "readOnlyHint": True})
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


########################################################################
## THEME / STYLING
########################################################################
@mcp.tool(annotations={"title": "Style Designer forms"})
def designer_set_stylesheet(qss: str) -> str:
    """Apply a stylesheet to all open form previews in Designer (live
    preview only - it does not modify the .ui files)."""
    _request({"method": "setStyleSheet", "qss": qss})
    return "stylesheet applied to open forms"


@mcp.tool(annotations={"title": "Refresh Designer icon caches"})
def designer_refresh_icons() -> str:
    """Clear Designer's pixmap caches and repaint open forms. Use after
    the shared icon set (Qss/icons/icons) was regenerated on disk."""
    _request({"method": "refreshIcons"})
    return "icon caches refreshed"


@mcp.tool(annotations={"title": "Drive the QSS / Theme editor window"})
def designer_qss_window(action: str = "status", enabled: bool = True) -> str:
    """Drive the standalone QSS / Theme editor window - a floating top-level
    window the dock tools can't reach.

      action='open'    show + raise the window
      action='close'   hide it
      action='status'  report {open, paintEntireDesigner, currentFile}
      action='paint'   set 'Paint entire Designer' to `enabled` (applies the
                       full current theme app-wide, or clears it)

    Use designer_qss_screenshot to capture the window."""
    return json.dumps(_request({"method": "qssWindow",
                                "action": action, "enabled": enabled}))


@mcp.tool(annotations={"title": "Move/raise the Designer window"})
def designer_window(action: str = "raise", x: int = 0, y: int = 0,
                    width: int = 1100, height: int = 750) -> str:
    """Position the Designer main window (multi-monitor compositors often park
    it on an off-screen output). action='screens' lists monitors; 'toPrimary'
    moves Designer onto the primary screen; 'move'/'geometry' use x/y[/w/h];
    'maximize'/'normal'/'raise' as named."""
    return json.dumps(_request({"method": "designerWindow", "action": action,
                                "x": x, "y": y, "width": width, "height": height}))


@mcp.tool(annotations={"title": "Screenshot the QSS editor window",
                       "readOnlyHint": True})
def designer_qss_screenshot() -> Image:
    """Screenshot the floating QSS / Theme editor window. Open it first with
    designer_qss_window(action='open')."""
    reply = _request({"method": "qssWindow", "action": "screenshot"},
                     reply_timeout_ms=20000)
    data = reply.get("result", "")
    if not data:
        raise RuntimeError(reply.get("error", "no QSS window screenshot data"))
    return Image(data=base64.b64decode(data), format="png")


########################################################################
## APP RUN (the project's main.py under the dev server, inside Designer)
########################################################################
@mcp.tool(annotations={"title": "Run the project app"})
def designer_run_app() -> dict:
    """Start the project's main.py under the dev-server supervisor from
    inside Designer. While running, saving a form in Designer regenerates
    src/ui_*.py and hot-restarts the app. Output streams into Designer's
    Logs dock and is readable via designer_app_logs."""
    return _request({"method": "runApp"})


@mcp.tool(annotations={"title": "Stop the project app"})
def designer_stop_app() -> dict:
    """Stop the app started with designer_run_app."""
    return _request({"method": "stopApp"})


@mcp.tool(annotations={"title": "Restart the project app"})
def designer_restart_app() -> dict:
    """Restart the app started with designer_run_app."""
    return _request({"method": "restartApp"})


@mcp.tool(annotations={"title": "Project app status", "readOnlyHint": True})
def designer_app_status() -> dict:
    """Whether the project app is running, and which script it runs."""
    return _request({"method": "appStatus"})


@mcp.tool(annotations={"title": "Read project app output", "readOnlyHint": True})
def designer_app_logs(lines: int = 100) -> dict:
    """The last stdout/stderr lines of the running (or last-run) app -
    includes crash tracebacks."""
    return _request({"method": "appLogs", "lines": lines})


########################################################################
## RUNNING-APP OBSERVE + NAVIGATE
##
## The running app is a separate process from Designer; when launched via
## designer_run_app the dev server starts an in-app control server that
## these tools talk to directly (no Designer round-trip). Use them to SEE
## the real app window and DRIVE it - screenshot, walk the widget tree,
## click buttons, set text/properties, invoke slots.
########################################################################
def _app_client():
    global _qt_app
    from qtpy.QtCore import QCoreApplication
    if _qt_app is None and QCoreApplication.instance() is None:
        _qt_app = QCoreApplication([])
    from Custom_Widgets.AppControl import AppControlClient
    return AppControlClient(project_dir=_projectDir(), timeout_ms=500)


_APP_NOT_RUNNING = ("The project app is not reachable. Start it with "
                    "designer_run_app (it must run under the dev server so its "
                    "in-app control server is enabled), then retry.")


def _app_request(message, reply_timeout_ms=15000):
    reply = _app_client().request(message, reply_timeout_ms=reply_timeout_ms)
    if reply is None:
        raise RuntimeError(_APP_NOT_RUNNING)
    if "error" in reply:
        raise RuntimeError(f"App reported: {reply['error']}")
    return reply


@mcp.tool(annotations={"title": "Running app status", "readOnlyHint": True})
def app_status() -> str:
    """Whether the running app's control server is reachable (the app must be
    started with designer_run_app). Use before the other app_* tools."""
    reachable = _app_client().isReachable(timeout_ms=1500)
    return json.dumps({"app_reachable": reachable})


@mcp.tool(annotations={"title": "List running-app windows", "readOnlyHint": True})
def app_list_windows() -> str:
    """List the running app's top-level windows (objectName, class, title,
    geometry, which is active)."""
    return json.dumps(_app_request({"method": "listWindows"})["result"], indent=2)


@mcp.tool(annotations={"title": "Screenshot the running app", "readOnlyHint": True})
def app_screenshot(target: str = "active") -> Image:
    """Screenshot a window of the RUNNING app (not Designer). target='active'
    (default), 'main' (the QMainWindow), or a window objectName."""
    reply = _app_request({"method": "screenshot", "target": target},
                         reply_timeout_ms=20000)
    return Image(data=base64.b64decode(reply["result"]), format="png")


@mcp.tool(annotations={"title": "Running app widget tree", "readOnlyHint": True})
def app_object_tree(window: str = "active") -> str:
    """The live widget tree of a running-app window: class, objectName,
    geometry, text, visible/enabled. Use it to find things to click/edit."""
    return json.dumps(_app_request({"method": "objectTree", "window": window})["result"],
                      indent=2)


@mcp.tool(annotations={"title": "Find widgets in the running app", "readOnlyHint": True})
def app_find(query: str, by: str = "any") -> str:
    """Find widgets in the running app by=name|text|class|any (substring,
    case-insensitive). Returns objectName, class, text, visibility."""
    return json.dumps(_app_request({"method": "find", "query": query, "by": by})["result"],
                      indent=2)


@mcp.tool(annotations={"title": "Click a widget in the running app"})
def app_click(widget: str) -> str:
    """Click a widget in the running app by objectName (buttons via click();
    others via a synthesized mouse click). Navigate the live app this way."""
    return json.dumps(_app_request({"method": "click", "widget": widget}))


@mcp.tool(annotations={"title": "Set text in the running app"})
def app_set_text(widget: str, text: str) -> str:
    """Set a widget's text in the running app by objectName (setText or
    setPlainText)."""
    return json.dumps(_app_request({"method": "setText", "widget": widget, "text": text}))


@mcp.tool(annotations={"title": "Set a widget property in the running app"})
def app_set_property(widget: str, property_name: str, value) -> str:
    """Set a Qt property on a running-app widget by objectName (repolishes so
    QSS re-evaluates). E.g. set 'variant' on a themed button."""
    return json.dumps(_app_request({"method": "setProperty", "widget": widget,
                                    "property": property_name, "value": value}))


@mcp.tool(annotations={"title": "Invoke a slot in the running app"})
def app_invoke(widget: str, slot: str) -> str:
    """Call a no-arg method/slot on a running-app widget by objectName (e.g.
    'showMaximized', 'clear', a custom slot)."""
    return json.dumps(_app_request({"method": "invoke", "widget": widget, "slot": slot}))


@mcp.tool(annotations={"title": "Move/raise the running-app window"})
def app_window(action: str = "raise", x: int = 0, y: int = 0,
               width: int = 900, height: int = 600, target: str = "active") -> str:
    """Position a running-app window (multi-monitor compositors often park it
    on an off-screen output). action='screens' lists monitors; 'toPrimary'
    moves the window onto the primary screen; 'move'/'geometry' use x/y[/w/h];
    'maximize'/'normal'/'raise' as named. Use app_screenshot after to verify."""
    return json.dumps(_app_request({"method": "window", "action": action,
                                    "x": x, "y": y, "width": width,
                                    "height": height, "target": target}))


########################################################################
## WINDOW MANAGEMENT (panes, dialogs, actions)
########################################################################
@mcp.tool(annotations={"title": "List Designer panes", "readOnlyHint": True})
def designer_list_docks() -> str:
    """List Designer's dock panes (Widget Box, Property Editor, Object
    Inspector, Custom Widgets docks...) with visibility, area and floating
    state."""
    return json.dumps(_request({"method": "getDocks"})["result"], indent=2)


@mcp.tool(annotations={"title": "Arrange a Designer pane"})
def designer_arrange_dock(dock: str, visible: bool = True, area: str = "",
                          floating: bool = False, raise_: bool = False) -> str:
    """Arrange a Designer dock pane matched by name/title substring:
    show/hide it, move it to an area ('left'/'right'/'top'/'bottom'),
    float it, or raise it above tabbed siblings."""
    message = {"method": "setDock", "dock": dock, "visible": visible,
               "floating": floating, "raise": raise_}
    if area:
        message["area"] = area
    return json.dumps(_request(message))


@mcp.tool(annotations={"title": "List open dialogs", "readOnlyHint": True})
def designer_list_dialogs() -> str:
    """List visible dialogs / popups / prompts / error boxes in Designer
    (e.g. the startup New Form dialog or a save prompt), with their title,
    message text and buttons. Check this when Designer seems blocked."""
    return json.dumps(_request({"method": "getDialogs"})["result"], indent=2)


@mcp.tool(annotations={"title": "Dismiss a dialog"})
def designer_dismiss_dialog(match: str = "", button: str = "") -> str:
    """Close an open dialog matched by title/class substring (empty match =
    first open dialog). Pass button text to click a specific button
    instead, e.g. button='Don't Save' on a save prompt, or button='Close'
    on the startup New Form dialog."""
    return json.dumps(_request({"method": "dismissDialog",
                                "match": match, "button": button}))


@mcp.tool(annotations={"title": "List Designer actions", "readOnlyHint": True})
def designer_list_actions(contains: str = "") -> str:
    """List Designer's menu/toolbar actions (Save, Save All, Preview,
    Close, ...). Optionally filter by substring. Trigger any of them with
    designer_trigger_action."""
    actions = _request({"method": "getActions"})["result"]
    if contains:
        needle = contains.lower()
        actions = [a for a in actions
                   if needle in a["text"].lower() or needle in a["objectName"].lower()]
    return json.dumps(actions, indent=2)


@mcp.tool(annotations={"title": "Trigger a Designer action"})
def designer_trigger_action(action: str) -> str:
    """Trigger a Designer menu/toolbar action by text or objectName
    (e.g. 'Save Form', 'Save All', 'Preview'). Use it to save forms after
    edits."""
    return json.dumps(_request({"method": "triggerAction", "action": action}))


@mcp.tool(annotations={"title": "Set a widget property (undoable)"})
def designer_set_widget_property(widget: str, property_name: str, value) -> str:
    """Set a property on a widget of the ACTIVE form (matched by
    objectName) through Designer's undo stack, like a manual edit - e.g.
    text, geometry, toolTip, checked. NOTE: styleSheet is refused by
    project rule; persist styles with project_write_style instead."""
    return json.dumps(_request({"method": "setWidgetProperty", "widget": widget,
                                "property": property_name, "value": value}))


########################################################################
## PROJECT WORKFLOW
########################################################################
@mcp.tool(annotations={"title": "List project .ui files", "readOnlyHint": True})
def project_list_ui_files() -> str:
    """List the .ui files of the project (excluding generated copies)."""
    found = []
    skip = {".git", "__pycache__", "generated-files", "node_modules", "venv", ".venv"}
    for root, dirs, files in os.walk(_projectDir()):
        dirs[:] = [d for d in dirs if d not in skip]
        for name in files:
            if name.lower().endswith(".ui") and not name.startswith("new_"):
                found.append(os.path.relpath(os.path.join(root, name), _projectDir()))
    return json.dumps(sorted(found), indent=2)


@mcp.tool(annotations={"title": "Create a new .ui form"})
def project_new_ui(name: str) -> str:
    """Create ui/<name>.ui pre-wired to the theme icons resource
    (Qss/icons/_icons.qrc), ready to design in Qt Designer."""
    previous = projectRoot()
    os.chdir(_projectDir())
    try:
        from Custom_Widgets.ProjectMaker import create_ui_file
        path = create_ui_file(name)
        if path is None:
            raise RuntimeError(f"ui/{name}.ui already exists")
        return os.path.relpath(path, _projectDir())
    finally:
        os.chdir(previous)


@mcp.tool(annotations={"title": "Convert ui/ to Python sources"})
def project_convert_ui(ui_path: str = "ui", src_output_dir: str = "src") -> str:
    """Convert the project's .ui files to Python (src/ui_*.py) plus the
    generated-files/ intermediates the theme engine needs. Run after
    editing .ui files (equivalent of `Custom_Widgets --convert-ui`)."""
    exe = os.path.join(os.path.dirname(sys.executable), "Custom_Widgets")
    proc = subprocess.run(
        [exe, "--convert-ui", ui_path, "--src-output-dir", src_output_dir],
        cwd=_projectDir(), capture_output=True, text=True, timeout=300,
        env={**os.environ, "QT_QPA_PLATFORM": os.environ.get("QT_QPA_PLATFORM", "offscreen")})
    if proc.returncode != 0:
        raise RuntimeError(f"conversion failed:\n{proc.stderr[-2000:]}")
    generated = [line for line in proc.stdout.splitlines()
                 if "Python:" in line or "Completed" in line]
    return "\n".join(generated) or "converted"


@mcp.tool(annotations={"title": "Write project styles (scss)"})
def project_write_style(scss: str, file: str = "") -> str:
    """Persist custom styles the Custom_Widgets way: appended to
    Qss/scss/defaultStyle.scss, or written to a separate scss file that
    gets @import-ed into it (pass file='mystyles.scss'). Target widgets
    with objectName selectors, e.g. '#saveBtn { padding: 6px; }'. This is
    the ONLY sanctioned way to persist styles - never put styleSheet
    properties in .ui files. The edited .scss is streamed live into the QSS
    editor so the user watches it change. Styles apply on the next app run;
    for an instant Designer preview also call designer_set_stylesheet."""
    scss_dir = os.path.join(_projectDir(), "Qss", "scss")
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
        _show_style_in_editor(edited)
        return f"wrote Qss/scss/{name} and imported it from defaultStyle.scss"

    with open(default_path, "a", encoding="utf-8") as f:
        f.write("\n" + scss.rstrip() + "\n")
    _show_style_in_editor(default_path)
    return "appended to Qss/scss/defaultStyle.scss"


def _show_style_in_editor(path):
    """Best-effort: open the just-edited .scss in Designer's QSS editor so the
    user sees the change live. No-op when Designer isn't running."""
    try:
        _client().request({"method": "qssWindow", "action": "load", "file": path},
                          reply_timeout_ms=2000)
    except Exception:
        pass


def main():
    global _PROJECT_DIR
    parser = argparse.ArgumentParser(description="Custom Widgets MCP server")
    parser.add_argument("--project-dir", default=projectRoot(),
                        help="Project folder (where Qss/, ui/ and json-styles/ live)")
    args = parser.parse_args()
    _PROJECT_DIR = os.path.abspath(args.project_dir)
    from Custom_Widgets.Project import setProjectRoot
    setProjectRoot(_PROJECT_DIR)
    os.chdir(_PROJECT_DIR)
    mcp.run()


if __name__ == "__main__":
    main()
