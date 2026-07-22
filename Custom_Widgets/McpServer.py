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
import base64
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

mcp = FastMCP("custom_widgets_mcp")

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


@mcp.tool(annotations={"title": "Get widget tree", "readOnlyHint": True})
def designer_get_object_info() -> str:
    """Widget tree of every open form: class names, object names and
    geometries as JSON. Useful to understand a form before editing it."""
    reply = _request({"method": "getObjectInfos"})
    return json.dumps(reply["result"], indent=2)


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
    properties in .ui files. Styles apply on the next app run; for an
    instant Designer preview also call designer_set_stylesheet."""
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
        with open(os.path.join(scss_dir, name), "w", encoding="utf-8") as f:
            f.write(scss.rstrip() + "\n")
        import_line = f"@import '{name[:-5]}';"
        with open(default_path, encoding="utf-8") as f:
            default_content = f.read()
        if import_line not in default_content:
            with open(default_path, "a", encoding="utf-8") as f:
                f.write(f"\n{import_line}\n")
        return f"wrote Qss/scss/{name} and imported it from defaultStyle.scss"

    with open(default_path, "a", encoding="utf-8") as f:
        f.write("\n" + scss.rstrip() + "\n")
    return "appended to Qss/scss/defaultStyle.scss"


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
