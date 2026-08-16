"""Tests for the Designer bridge (QLocalServer inside Qt Designer, app as
client). The server runs harmlessly outside Designer (no form windows), so
the whole protocol is testable offscreen.

The test client talks plain unix sockets (QLocalServer's fullServerName is
a socket path on Linux) - Qt objects must not live on short-lived Python
threads, that crashes at teardown.
"""
import json
import os
import socket
import time

import pytest


def _spin(qapp, seconds=0.3):
    deadline = time.time() + seconds
    while time.time() < deadline:
        qapp.processEvents()
        time.sleep(0.01)


def _request(qapp, server, payload, timeout=5.0, token=None):
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
        if token is None:
            token = getattr(server, "token", None)
        if token:
            sock.sendall(("CWTOKEN " + token + "\n").encode())
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
    server.close()
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


def test_qss_window_error_when_not_installed(qapp, bridge, monkeypatch):
    """Outside Designer the QSS editor window isn't installed, so the bridge
    reports an actionable error rather than crashing."""
    from Custom_Widgets import DesignerTools

    monkeypatch.setattr(DesignerTools, "_tools", {}, raising=False)
    reply = _request(qapp, bridge, {"method": "qssWindow", "action": "status"})
    assert "error" in reply and "not installed" in reply["error"]


@pytest.fixture
def fake_qss_window(qapp, monkeypatch):
    """Inject a stand-in QSS editor window into DesignerTools._tools so the
    bridge's qssWindow driver can be exercised offscreen (the real window is a
    heavy top-level tied to a project's Qss/scss tree)."""
    from qtpy.QtGui import QAction
    from qtpy.QtWidgets import QWidget
    from Custom_Widgets import DesignerTools

    class _FakeQss(QWidget):
        def __init__(self):
            super().__init__()
            self.setObjectName("customWidgetsQssWindow")
            self._path = "/proj/Qss/scss/defaultStyle.scss"
            self.painted = None
            self._repaintDesigner = QAction(self)
            self._repaintDesigner.setCheckable(True)
            # mirror the real window: toggling applies/clears the paint
            self._repaintDesigner.toggled.connect(self._applyPaintDesigner)

        def openFloating(self):
            self.show()

        def _applyPaintDesigner(self, *_):
            self.painted = self._repaintDesigner.isChecked()

    fake = _FakeQss()
    monkeypatch.setattr(DesignerTools, "_tools", {"qss": fake}, raising=False)
    yield fake
    fake.close()


def test_qss_window_open_status_and_screenshot(qapp, bridge, fake_qss_window):
    status = _request(qapp, bridge,
                      {"method": "qssWindow", "action": "status"})["result"]
    assert status["open"] is False
    assert status["paintEntireDesigner"] is False
    assert status["currentFile"] == "defaultStyle.scss"
    assert status["objectName"] == "customWidgetsQssWindow"

    opened = _request(qapp, bridge, {"method": "qssWindow", "action": "open"})
    assert opened["result"] == "ok" and opened["open"] is True

    shot = _request(qapp, bridge, {"method": "qssWindow", "action": "screenshot"})
    assert isinstance(shot["result"], str) and len(shot["result"]) > 0

    closed = _request(qapp, bridge, {"method": "qssWindow", "action": "close"})
    assert closed["open"] is False


def test_qss_window_paint_entire_designer_toggle(qapp, bridge, fake_qss_window):
    # turn it on: the toggle fires and the paint is applied
    on = _request(qapp, bridge,
                  {"method": "qssWindow", "action": "paint", "enabled": True})
    assert on["result"] == "ok" and on["paintEntireDesigner"] is True
    assert fake_qss_window.painted is True

    # re-applying the same state still forces an apply (no silent no-op)
    fake_qss_window.painted = None
    again = _request(qapp, bridge,
                     {"method": "qssWindow", "action": "paint", "enabled": True})
    assert again["paintEntireDesigner"] is True
    assert fake_qss_window.painted is True

    off = _request(qapp, bridge,
                   {"method": "qssWindow", "action": "paint", "enabled": False})
    assert off["paintEntireDesigner"] is False
    assert fake_qss_window.painted is False


def test_qss_window_unknown_action(qapp, bridge, fake_qss_window):
    reply = _request(qapp, bridge, {"method": "qssWindow", "action": "bogus"})
    assert "error" in reply and "unknown qss action" in reply["error"]


def test_unauthenticated_connection_is_rejected(qapp, bridge):
    """A raw socket that does NOT present the auth token first must never get
    a reply (the server aborts the connection)."""
    path = bridge._server.fullServerName()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.setblocking(False)
    try:
        try:
            sock.connect(path)
        except BlockingIOError:
            pass
        _spin(qapp, 0.05)
        sock.sendall(b'{"method": "ping"}\n')
        buf = b""
        deadline = time.time() + 2
        while time.time() < deadline and b"\n" not in buf:
            qapp.processEvents()
            try:
                chunk = sock.recv(4096)
                if chunk:
                    buf += chunk
            except BlockingIOError:
                time.sleep(0.01)
        assert b"pong" not in buf
    finally:
        sock.close()


def test_wrong_token_is_rejected(qapp, bridge):
    with pytest.raises(AssertionError):
        _request(qapp, bridge, {"method": "ping"}, token="deadbeef")


def test_no_token_file_means_client_fails_closed(qapp, tmp_path):
    """A client for a socket whose token file is absent fails closed - it must
    not even attempt a connection, so a spoofed pre-listen server is never
    talked to."""
    from Custom_Widgets.DesignerBridge import DesignerBridgeClient
    from Custom_Widgets.tools import socket_auth

    client = DesignerBridgeClient(project_dir=str(tmp_path / "ghost"))
    path = socket_auth.token_path(client._name)
    if os.path.exists(path):  # paranoia: nothing should have created it
        os.remove(path)
    start = time.time()
    assert client.send({"method": "ping"}) is False
    assert client.request({"method": "ping"}) is None
    assert time.time() - start < 3
