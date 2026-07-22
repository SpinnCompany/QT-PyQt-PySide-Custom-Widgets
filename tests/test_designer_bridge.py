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


def test_extended_protocol_without_forms(qapp, bridge):
    """The reference-parity methods respond sanely outside Designer."""
    assert _request(qapp, bridge, {"method": "getObjectInfos"})["result"] == []
    assert "error" in _request(qapp, bridge, {"method": "getUiCode", "type": "xml"})
    assert "error" in _request(qapp, bridge, {"method": "getScreenShot", "type": "current"})
    reply = _request(qapp, bridge, {"method": "closeFiles", "all": True})
    assert reply == {"result": "ok", "closed": []}


def test_open_files_ignores_missing(qapp, bridge, project_dir):
    reply = _request(qapp, bridge, {"method": "openFiles",
                                    "files": [str(project_dir / "missing.ui")]})
    assert reply == {"result": "ok", "opened": []}


def test_screenshot_main_window(qapp, bridge):
    """'main' grabs any visible QMainWindow - create one for the test."""
    from qtpy.QtWidgets import QMainWindow

    window = QMainWindow()
    window.resize(120, 80)
    window.show()
    _spin(qapp, 0.1)
    try:
        reply = _request(qapp, bridge, {"method": "getScreenShot", "type": "main"})
        assert isinstance(reply.get("result"), str) and len(reply["result"]) > 100
    finally:
        window.close()


@pytest.fixture
def fake_designer_window(qapp):
    """A QMainWindow with a menu bar, dock, action and dialog - stands in
    for Designer's main window in the window-management methods."""
    from qtpy.QtCore import Qt
    from qtpy.QtGui import QAction
    from qtpy.QtWidgets import QDialog, QDockWidget, QLabel, QMainWindow, QPushButton, QVBoxLayout

    window = QMainWindow()
    window.menuBar().addMenu("File")
    dock = QDockWidget("Property Editor", window)
    dock.setObjectName("propertyEditorDock")
    window.addDockWidget(Qt.LeftDockWidgetArea, dock)

    fired = []
    action = QAction("Save Form", window)
    action.setObjectName("actionSave")
    action.triggered.connect(lambda: fired.append("save"))
    window.addAction(action)

    dialog = QDialog(window)
    dialog.setWindowTitle("New Form")
    layout = QVBoxLayout(dialog)
    layout.addWidget(QLabel("Choose a template"))
    close_btn = QPushButton("&Close")
    close_btn.clicked.connect(dialog.reject)
    layout.addWidget(close_btn)

    window.show()
    dialog.show()
    _spin(qapp, 0.1)
    yield window, dialog, fired
    dialog.close()
    window.close()


def test_docks_listed_and_arranged(qapp, bridge, fake_designer_window):
    docks = _request(qapp, bridge, {"method": "getDocks"})["result"]
    assert any(d["objectName"] == "propertyEditorDock" and d["area"] == "left"
               for d in docks)

    reply = _request(qapp, bridge, {"method": "setDock", "dock": "property",
                                    "area": "right", "visible": True})
    assert reply["result"] == "ok"
    docks = _request(qapp, bridge, {"method": "getDocks"})["result"]
    assert any(d["objectName"] == "propertyEditorDock" and d["area"] == "right"
               for d in docks)


def test_dialogs_listed_and_dismissed(qapp, bridge, fake_designer_window):
    _, dialog, _ = fake_designer_window
    dialogs = _request(qapp, bridge, {"method": "getDialogs"})["result"]
    match = [d for d in dialogs if d["title"] == "New Form"]
    assert match and "Choose a template" in match[0]["text"]
    assert "Close" in match[0]["buttons"]

    reply = _request(qapp, bridge, {"method": "dismissDialog",
                                    "match": "new form", "button": "Close"})
    assert reply["result"] == "ok" and reply["clicked"] == "Close"
    _spin(qapp, 0.05)
    assert not dialog.isVisible()


def test_actions_listed_and_triggered(qapp, bridge, fake_designer_window):
    _, _, fired = fake_designer_window
    actions = _request(qapp, bridge, {"method": "getActions"})["result"]
    assert any(a["text"] == "Save Form" for a in actions)

    reply = _request(qapp, bridge, {"method": "triggerAction", "action": "save form"})
    assert reply["result"] == "ok"
    _spin(qapp, 0.05)
    assert fired == ["save"]


def test_stylesheet_property_refused_by_project_rule(qapp, bridge):
    reply = _request(qapp, bridge, {"method": "setWidgetProperty",
                                    "widget": "saveBtn",
                                    "property": "styleSheet", "value": "x"})
    assert "defaultStyle.scss" in reply["error"]


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
