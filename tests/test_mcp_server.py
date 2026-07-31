"""Tests for the Custom Widgets MCP server (agent control of Qt Designer).

Tool functions are called directly (FastMCP registers but does not wrap
them); the live Designer path is covered by the bridge tests plus manual
verification - here we cover registration, project tools and the
actionable-error path when Designer is not running.
"""
import asyncio
import json
import os

import pytest

mcp_sdk = pytest.importorskip("mcp", reason="mcp extra not installed")

from Custom_Widgets.mcp import server as McpServer  # noqa: E402
from Custom_Widgets.mcp.workspace import ProjectRegistry, ProjectWorker  # noqa: E402

try:  # tool failures surface as FastMCP's ToolError (not a RuntimeError subclass
    from mcp.server.fastmcp.exceptions import ToolError
    _TOOL_ERR = (RuntimeError, ToolError)
except ImportError:  # pragma: no cover - older/newer mcp without this module
    _TOOL_ERR = (RuntimeError,)


@pytest.fixture
def mcp_project(tmp_path, monkeypatch):
    monkeypatch.setattr(McpServer, "_PROJECT_DIR", str(tmp_path))
    return tmp_path


def test_expected_tools_registered():
    # Driven with asyncio.run rather than @pytest.mark.asyncio: this is the
    # only coroutine in the suite and it takes no async fixtures, so requiring
    # the pytest-asyncio plugin for it means this test errors out wherever the
    # plugin is absent — which includes any PEP 668 externally-managed Python,
    # where installing it is blocked.
    tools = {t.name for t in asyncio.run(McpServer.mcp.list_tools())}
    expected = {
        "designer_status", "designer_launch", "designer_open_files",
        "designer_close_files", "designer_reload_forms",
        "designer_screenshot", "designer_get_ui_code",
        "designer_get_object_info", "designer_set_stylesheet",
        "designer_refresh_icons", "project_list_ui_files",
        "project_new_ui", "project_convert_ui",
        "designer_list_docks", "designer_arrange_dock",
        "designer_list_dialogs", "designer_dismiss_dialog",
        "designer_list_actions", "designer_trigger_action",
        "designer_set_widget_property", "project_write_style",
        "designer_qss_window", "designer_qss_screenshot",
        "app_status", "app_list_windows", "app_screenshot", "app_object_tree",
        "app_find", "app_click", "app_set_text", "app_set_property", "app_invoke",
        "app_window", "designer_window",
        "designer_set_form_xml", "designer_new_form_xml", "designer_quit",
        "workspaces_status",
    }
    assert expected <= tools


def test_status_reports_not_running(qapp, mcp_project):
    status = json.loads(McpServer.designer_status())
    assert status["designer_running"] is False
    assert status["project_dir"] == str(mcp_project)
    assert status["bridge_socket"].startswith("customwidgets-designer-")


def test_designer_tools_raise_actionable_error(qapp, mcp_project):
    with pytest.raises(_TOOL_ERR, match="designer_launch"):
        McpServer.designer_refresh_icons()


def test_project_new_ui_and_listing(qapp, mcp_project):
    created = McpServer.project_new_ui("AgentForm")
    assert created == os.path.join("ui", "AgentForm.ui")
    files = json.loads(McpServer.project_list_ui_files())
    assert files == ["ui/AgentForm.ui"]
    content = (mcp_project / "ui" / "AgentForm.ui").read_text(encoding="utf-8")
    assert "_icons.qrc" in content

    with pytest.raises(_TOOL_ERR, match="already exists"):
        McpServer.project_new_ui("AgentForm")


def test_project_write_style_appends_to_default(qapp, mcp_project):
    result = McpServer.project_write_style("#saveBtn { padding: 6px; }")
    assert "defaultStyle.scss" in result
    content = (mcp_project / "Qss" / "scss" / "defaultStyle.scss").read_text(encoding="utf-8")
    assert "#saveBtn { padding: 6px; }" in content


def test_project_write_style_separate_file_gets_imported(qapp, mcp_project):
    McpServer.project_write_style("#x { margin: 0; }", file="agent-styles")
    scss_dir = mcp_project / "Qss" / "scss"
    assert (scss_dir / "agent-styles.scss").read_text(encoding="utf-8").strip() == "#x { margin: 0; }"
    default = (scss_dir / "defaultStyle.scss").read_text(encoding="utf-8")
    assert "@import 'agent-styles';" in default
    # idempotent - no duplicate import
    McpServer.project_write_style("#x { margin: 1px; }", file="agent-styles")
    default = (scss_dir / "defaultStyle.scss").read_text(encoding="utf-8")
    assert default.count("@import 'agent-styles';") == 1


########################################################################
## MULTI-PROJECT / MULTI-AGENT HARDENING
########################################################################
def test_worker_serializes_same_project():
    """Concurrent submits to ONE project's worker never overlap (FIFO, one at a
    time), and results/exceptions propagate to the submitter."""
    import threading
    import time

    reg = ProjectRegistry(lambda: "/tmp/projA")
    worker = reg.worker(reg.resolve())
    active = {"n": 0, "max": 0}
    lock = threading.Lock()

    def job(i):
        with lock:
            active["n"] += 1
            active["max"] = max(active["max"], active["n"])
        time.sleep(0.02)
        with lock:
            active["n"] -= 1
        return i * i

    threads = [threading.Thread(target=lambda i=i: worker.submit(lambda: job(i)))
               for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert active["max"] == 1                      # never two at once
    assert worker.submit(lambda: 6 * 6) == 36      # result propagates
    with pytest.raises(ZeroDivisionError):         # exception propagates
        worker.submit(lambda: 1 / 0)


def test_resolve_and_distinct_workers_per_project(tmp_path):
    """Per-call project resolution: blank -> default, relative -> under default,
    absolute -> itself; distinct dirs get distinct serialization workers."""
    reg = ProjectRegistry(lambda: str(tmp_path))
    assert reg.resolve() == str(tmp_path)
    assert reg.resolve("examples/X") == os.path.join(str(tmp_path), "examples", "X")
    assert reg.resolve("/somewhere/else") == "/somewhere/else"
    assert reg.worker(reg.resolve("a")) is not reg.worker(reg.resolve("b"))
    assert reg.worker(reg.resolve("a")) is reg.worker(reg.resolve("a"))  # cached
    assert set(reg.known()) >= {reg.resolve("a"), reg.resolve("b")}


def test_server_request_routes_through_target_project_worker(qapp, mcp_project,
                                                             monkeypatch):
    """server._request funnels a call through the RESOLVED project's worker
    (not the default), so per-call project addressing reaches the right queue."""
    seen = {}

    def fake_client(project_dir=None):
        class _C:
            def request(self, message, reply_timeout_ms=0):
                seen["project_dir"] = project_dir
                return {"result": "ok"}
        return _C()

    monkeypatch.setattr(McpServer, "_client", fake_client)
    target = str(mcp_project / "examples" / "Jobs")
    reply = McpServer._request({"method": "ping"}, project=target)
    assert reply == {"result": "ok"}
    assert seen["project_dir"] == target          # routed to the named project
    assert target in McpServer.REGISTRY.known()   # its worker was created


def test_workspaces_status_shape(qapp, mcp_project):
    status = json.loads(McpServer.workspaces_status())
    assert status["default"] == str(mcp_project)
    assert isinstance(status["projects"], list) and status["projects"]
    entry = status["projects"][0]
    assert entry["designer_running"] is False and entry["app_running"] is False
    assert entry["queue_depth"] == 0 and entry["busy"] is False
    assert entry["bridge_socket"].startswith("customwidgets-designer-")


def test_designer_quit_all_projects_requires_confirmation(qapp, mcp_project):
    # Guard: nuking every project's Designer needs an explicit confirm token.
    with pytest.raises(_TOOL_ERR, match="confirmation_required|all_projects"):
        McpServer.designer_quit(all_projects=True)
    # This-project-only quit is unguarded (Designer just isn't running here).
    result = json.loads(McpServer.designer_quit(force=False))
    assert result["clean_quit"] is False
    assert result["scope"] == str(mcp_project)
