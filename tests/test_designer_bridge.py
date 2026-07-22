"""Tests for the Designer bridge (QLocalServer inside Qt Designer, app as
client). The server runs harmlessly outside Designer (no form windows), so
the whole protocol is testable offscreen.

The test client talks plain unix sockets (QLocalServer's fullServerName is
a socket path on Linux) - Qt objects must not live on short-lived Python
threads, that crashes at teardown.
"""
import json
import socket
import time

import pytest


def _spin(qapp, seconds=0.3):
    deadline = time.time() + seconds
    while time.time() < deadline:
        qapp.processEvents()
        time.sleep(0.01)


def _request(qapp, server, payload, timeout=5.0):
    """Send one JSON line over a raw unix socket and read the reply while
    spinning the (same-thread) server's event loop."""
    path = server._server.fullServerName()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.setblocking(False)
    try:
        try:
            sock.connect(path)
        except BlockingIOError:
            pass
        _spin(qapp, 0.05)
        sock.sendall((json.dumps(payload) + "\n").encode())

        buf = b""
        deadline = time.time() + timeout
        while time.time() < deadline and b"\n" not in buf:
            qapp.processEvents()
            try:
                chunk = sock.recv(65536)
                if chunk:
                    buf += chunk
            except BlockingIOError:
                time.sleep(0.01)
        assert b"\n" in buf, f"no reply for {payload}"
        return json.loads(buf.split(b"\n")[0].decode())
    finally:
        sock.close()


@pytest.fixture
def bridge(qapp, project_dir):
    from Custom_Widgets.DesignerBridge import DesignerBridgeServer

    server = DesignerBridgeServer(project_dir=str(project_dir))
    assert server.isListening()
    yield server
    server._server.close()
    _spin(qapp, 0.05)


def test_server_name_is_per_project():
    from Custom_Widgets.DesignerBridge import bridgeServerName

    a = bridgeServerName("/tmp/project-a")
    b = bridgeServerName("/tmp/project-b")
    assert a != b
    assert a == bridgeServerName("/tmp/project-a")


def test_ping_roundtrip(qapp, bridge):
    assert _request(qapp, bridge, {"method": "ping"}) == {"result": "pong"}


def test_refresh_and_stylesheet_ok_without_forms(qapp, bridge):
    assert _request(qapp, bridge, {"method": "refreshIcons", "color": "#123456"}) == {"result": "ok"}
    assert _request(qapp, bridge, {"method": "setStyleSheet", "qss": "QWidget{}"}) == {"result": "ok"}
    assert _request(qapp, bridge, {"method": "reloadForms"})["result"] == "ok"


def test_unknown_method_reports_error(qapp, bridge):
    assert "error" in _request(qapp, bridge, {"method": "nope"})


def test_client_fails_silently_without_server(qapp, tmp_path):
    from Custom_Widgets.DesignerBridge import DesignerBridgeClient

    client = DesignerBridgeClient(project_dir=str(tmp_path / "nowhere"))
    start = time.time()
    assert client.send({"method": "ping"}) is False
    assert client.notifyThemeChanged(color="#fff", qss="x") is False
    # must not hang the caller (theme changes run through this)
    assert time.time() - start < 3


def test_client_delivers_to_server(qapp, bridge, project_dir):
    """The real client runs on the app's main thread; on unix the connect
    succeeds at OS level without the server's loop spinning."""
    from Custom_Widgets.DesignerBridge import DesignerBridgeClient

    client = DesignerBridgeClient(project_dir=str(project_dir), timeout_ms=2000)
    assert client.notifyThemeChanged(color="#abc", qss="QWidget{}") is True
    _spin(qapp, 0.2)  # let the server consume the messages
