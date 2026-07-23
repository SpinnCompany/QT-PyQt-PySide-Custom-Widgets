"""Tests for the Custom Widgets MCP server (agent control of Qt Designer).

Tool functions are called directly (FastMCP registers but does not wrap
them); the live Designer path is covered by the bridge tests plus manual
verification - here we cover registration, project tools and the
actionable-error path when Designer is not running.
"""
import json
import os

import pytest

mcp_sdk = pytest.importorskip("mcp", reason="mcp extra not installed")

from Custom_Widgets.mcp import server as McpServer  # noqa: E402


@pytest.fixture
def mcp_project(tmp_path, monkeypatch):
    monkeypatch.setattr(McpServer, "_PROJECT_DIR", str(tmp_path))
    return tmp_path


@pytest.mark.asyncio
async def test_expected_tools_registered():
    tools = {t.name for t in await McpServer.mcp.list_tools()}
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
    }
    assert expected <= tools


def test_status_reports_not_running(qapp, mcp_project):
    status = json.loads(McpServer.designer_status())
    assert status["designer_running"] is False
    assert status["project_dir"] == str(mcp_project)
    assert status["bridge_socket"].startswith("customwidgets-designer-")


def test_designer_tools_raise_actionable_error(qapp, mcp_project):
    with pytest.raises(RuntimeError, match="designer_launch"):
        McpServer.designer_refresh_icons()


def test_project_new_ui_and_listing(qapp, mcp_project):
    created = McpServer.project_new_ui("AgentForm")
    assert created == os.path.join("ui", "AgentForm.ui")
    files = json.loads(McpServer.project_list_ui_files())
    assert files == ["ui/AgentForm.ui"]
    content = (mcp_project / "ui" / "AgentForm.ui").read_text(encoding="utf-8")
    assert "_icons.qrc" in content

    with pytest.raises(RuntimeError, match="already exists"):
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
