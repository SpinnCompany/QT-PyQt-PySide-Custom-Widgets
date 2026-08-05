"""Tests for the in-app control server (observe + navigate a running app).

The dispatch logic is exercised directly against real widgets; one raw-socket
round-trip proves the transport (same-thread QLocalServer, spun via
processEvents - Qt objects must not live on short-lived Python threads).
"""
import json
import socket
import time

import pytest


@pytest.fixture
def scene(qapp):
    """A main window with named widgets and a click counter."""
    from qtpy.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit

    win = QMainWindow()
    win.setObjectName("mainWin")
    win.setWindowTitle("Test App")
    central = QWidget()
    win.setCentralWidget(central)
    lay = QVBoxLayout(central)

    clicks = {"n": 0}
    btn = QPushButton("OK")
    btn.setObjectName("okBtn")
    btn.clicked.connect(lambda: clicks.__setitem__("n", clicks["n"] + 1))
    edit = QLineEdit()
    edit.setObjectName("nameEdit")
    lay.addWidget(btn)
    lay.addWidget(edit)
    win.resize(240, 160)
    win.show()
    qapp.processEvents()
    yield win, btn, edit, clicks
    win.close()


@pytest.fixture
def server(qapp, tmp_path):
    from Custom_Widgets.AppControl import AppControlServer
    srv = AppControlServer(project_dir=str(tmp_path))
    assert srv.isListening()
    yield srv
    srv.close()
    qapp.processEvents()


def test_ping_and_list_windows(server, scene):
    assert server._dispatch({"method": "ping"})["result"] == "pong"
    wins = server._dispatch({"method": "listWindows"})["result"]
    names = {w["objectName"] for w in wins}
    assert "mainWin" in names


def test_object_tree_and_find(server, scene):
    tree = server._dispatch({"method": "objectTree", "window": "active"})["result"]
    flat = json.dumps(tree)
    assert "okBtn" in flat and "nameEdit" in flat

    hits = server._dispatch({"method": "find", "query": "okBtn", "by": "name"})["result"]
    assert any(h["objectName"] == "okBtn" for h in hits)
    by_text = server._dispatch({"method": "find", "query": "OK", "by": "text"})["result"]
    assert any(h["objectName"] == "okBtn" for h in by_text)


def test_screenshot_returns_png(server, scene):
    reply = server._dispatch({"method": "screenshot", "target": "active"})
    assert reply["result"].startswith("iVBOR")  # PNG base64 header


def test_click_button_increments(server, scene):
    _, _, _, clicks = scene
    reply = server._dispatch({"method": "click", "widget": "okBtn"})
    assert reply["result"] == "ok"
    assert clicks["n"] == 1


def test_set_text_and_property_and_invoke(server, scene):
    _, btn, edit, _ = scene
    assert server._dispatch({"method": "setText", "widget": "nameEdit",
                             "text": "hello"})["result"] == "ok"
    assert edit.text() == "hello"

    assert server._dispatch({"method": "setProperty", "widget": "okBtn",
                             "property": "variant", "value": "primary"})["result"] == "ok"
    assert btn.property("variant") == "primary"

    assert server._dispatch({"method": "invoke", "widget": "nameEdit",
                             "slot": "clear"})["result"] == "ok"
    assert edit.text() == ""


def test_unknown_widget_and_method(server, scene):
    assert "error" in server._dispatch({"method": "click", "widget": "nope"})
    assert "error" in server._dispatch({"method": "bogus"})


def test_socket_roundtrip_ping(qapp, server):
    """Prove the newline-JSON transport over the real QLocalServer socket."""
    path = server._server.fullServerName()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.setblocking(False)
    try:
        try:
            sock.connect(path)
        except BlockingIOError:
            pass
        deadline = time.time() + 2
        while time.time() < deadline:
            qapp.processEvents(); time.sleep(0.01)
            try:
                sock.connect(path)
                break
            except (BlockingIOError, OSError):
                pass
        sock.sendall(b'{"method": "ping"}\n')
        buf = b""
        deadline = time.time() + 3
        while time.time() < deadline and b"\n" not in buf:
            qapp.processEvents()
            try:
                buf += sock.recv(4096)
            except BlockingIOError:
                time.sleep(0.01)
        assert b"pong" in buf
    finally:
        sock.close()


def test_maybe_start_gated_on_env(qapp, tmp_path, monkeypatch):
    from Custom_Widgets import AppControl
    monkeypatch.setattr(AppControl, "_server_singleton", None)
    monkeypatch.delenv("CUSTOM_WIDGETS_APP_CONTROL", raising=False)
    assert AppControl.maybe_start_app_control(str(tmp_path)) is None
    monkeypatch.setenv("CUSTOM_WIDGETS_APP_CONTROL", "1")
    srv = AppControl.maybe_start_app_control(str(tmp_path))
    assert srv is not None and srv.isListening()
    srv.close()
    qapp.processEvents()
    monkeypatch.setattr(AppControl, "_server_singleton", None)
