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
import subprocess
import sys

try:
    from mcp.server.fastmcp import FastMCP, Image
except ImportError:  # pragma: no cover
    sys.exit("The MCP server needs the 'mcp' package:\n"
             "    pip install QT-PyQt-PySide-Custom-Widgets[mcp]")

mcp = FastMCP("custom_widgets_mcp")

_PROJECT_DIR = os.getcwd()
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
def designer_open_files(files: list[str]) -> str:
    """Open one or more .ui files in the running Qt Designer. Paths may be
    relative to the project folder."""
    absolute = [f if os.path.isabs(f) else os.path.join(_projectDir(), f)
                for f in files]
    reply = _request({"method": "openFiles", "files": absolute})
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
    previous = os.getcwd()
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


def main():
    global _PROJECT_DIR
    parser = argparse.ArgumentParser(description="Custom Widgets MCP server")
    parser.add_argument("--project-dir", default=os.getcwd(),
                        help="Project folder (where Qss/, ui/ and json-styles/ live)")
    args = parser.parse_args()
    _PROJECT_DIR = os.path.abspath(args.project_dir)
    os.chdir(_PROJECT_DIR)
    mcp.run()


if __name__ == "__main__":
    main()
