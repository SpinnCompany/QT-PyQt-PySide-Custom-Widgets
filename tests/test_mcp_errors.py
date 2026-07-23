"""Every MCP tool failure must reach the agent as the SAME structured JSON
envelope: {"error": {"kind", "message", "hint"?, "details"?}}.

FastMCP wraps a raised exception as ToolError("Error executing tool NAME: <msg>")
and forwards <msg> verbatim, so we assert the JSON body embedded in that message.
"""
import asyncio
import json

import pytest

pytest.importorskip("mcp")
from mcp.server.fastmcp.exceptions import ToolError  # noqa: E402

from Custom_Widgets.mcp import server  # noqa: E402


def _run(tool_name, args):
    """Invoke a tool through the real FastMCP path (arg validation + wrapper),
    returning the parsed error envelope. Fails if the tool did NOT error."""
    async def go():
        tool = server.mcp._tool_manager.get_tool(tool_name)
        try:
            await tool.run(args)
        except ToolError as exc:
            text = str(exc)
            return json.loads(text[text.index("{"):])
        return None
    return asyncio.run(go())


def _assert_shape(env, kind):
    assert env is not None, "tool did not raise"
    assert set(env) == {"error"}
    err = env["error"]
    assert err["kind"] == kind
    assert isinstance(err.get("message"), str) and err["message"]


def test_unknown_widget_is_structured():
    env = _run("widgets_catalog", {"name": "NoSuchWidget"})
    _assert_shape(env, "unknown_widget")
    assert "widgets_catalog" in env["error"]["hint"]


def test_widget_signature_unknown_is_structured():
    _assert_shape(_run("widget_signature", {"name": "Nope"}), "unknown_widget")


def test_designer_not_running_is_structured():
    # No Designer bridge in the test env -> uniform designer_not_running.
    env = _run("designer_get_object_info", {})
    _assert_shape(env, "designer_not_running")
    assert "hint" in env["error"]


def test_app_not_running_is_structured():
    env = _run("app_object_tree", {"window": "active"})
    _assert_shape(env, "app_not_running")


def test_unexpected_exception_becomes_internal(monkeypatch):
    def boom(_name):
        raise KeyError("surprise")
    monkeypatch.setattr(server, "_find_widget", boom)
    env = _run("widget_signature", {"name": "QCustomBadge"})
    _assert_shape(env, "internal")
    assert "traceback" in env["error"]["details"]
