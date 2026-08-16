"""T2 security: shared socket auth helpers, zip-slip guard in the iconify
fetcher, and QML injection escaping in the QtLocation facade."""
import os
import zipfile

import pytest


def test_socket_auth_token_round_trip(monkeypatch, tmp_path):
    from Custom_Widgets.tools import socket_auth

    cache = str(tmp_path / "cache")
    monkeypatch.setenv("XDG_CACHE_HOME", cache)
    name = "customwidgets-designer-abc123"

    assert socket_auth.read_token(name) is None
    token = socket_auth.write_token(name)
    assert len(token) == 32
    assert socket_auth.read_token(name) == token

    # the file is private to the owning user
    mode = os.stat(socket_auth.token_path(name)).st_mode & 0o777
    assert mode == 0o600

    socket_auth.remove_token(name)
    assert socket_auth.read_token(name) is None
    socket_auth.remove_token(name)  # idempotent


def test_socket_auth_line_parsing():
    from Custom_Widgets.tools import socket_auth

    token = "deadbeef"
    assert socket_auth.parse_auth_line("CWTOKEN deadbeef", token) is True
    assert socket_auth.parse_auth_line("CWTOKEN wrong", token) is False
    assert socket_auth.parse_auth_line("", token) is False
    assert socket_auth.parse_auth_line("CWTOKEN deadbeef", "") is False


def test_zip_slip_is_rejected(tmp_path):
    """A zip whose member escapes the extraction dir must raise, not write."""
    from Custom_Widgets.iconify.fetch import Fetcher

    evil = tmp_path / "evil.zip"
    with zipfile.ZipFile(str(evil), "w") as zf:
        zf.writestr("../pwned.txt", "owned")
        zf.writestr("ok/file.svg", "<svg/>")

    target = tmp_path / "install"
    with pytest.raises(ValueError):
        Fetcher.installZipFile(str(evil), str(target))
    assert not (tmp_path / "pwned.txt").exists()


def test_zip_slip_absolute_member_is_rejected(tmp_path):
    from Custom_Widgets.iconify.fetch import Fetcher

    evil = tmp_path / "abs.zip"
    with zipfile.ZipFile(str(evil), "w") as zf:
        zf.writestr("/etc/pwned.svg", "<svg/>")

    target = tmp_path / "install2"
    with pytest.raises(ValueError):
        Fetcher.installZipFile(str(evil), str(target))
    assert not os.path.exists("/etc/pwned.svg")


def test_qml_plugin_parameter_escaping(monkeypatch, tmp_path):
    """Values are QML-string-escaped and hostile keys are dropped, so an
    option value cannot break out of the PluginParameter literal."""
    from Custom_Widgets.map import _qtlocation

    captured = {}

    class FakeComponent:
        def __init__(self, engine):
            captured["engine"] = engine

        def setData(self, qml, url):
            captured["qml"] = qml.decode("utf-8")

        def create(self):
            captured["plugin"] = object()
            return captured["plugin"]

    import qtpy.QtQml
    monkeypatch.setattr(qtpy.QtQml, "QQmlComponent", FakeComponent)

    class FakeView:
        def engine(self):
            return "engine"

    class FakeRoot:
        def property(self, name):
            return "osm"

    engine = _qtlocation.QtLocationEngine.__new__(_qtlocation.QtLocationEngine)
    engine._view = FakeView()
    engine._root = FakeRoot()
    engine._call = lambda *a, **k: None

    engine._applyPluginParameters({
        "osm.mapping.custom.host": 'https://tiles.example.com/"x"\\y',
        "evil;break": "nope",
        "key\ninject": "nope",
        "good.key": 'a"b\\c',
    })
    qml = captured["qml"]
    assert 'value: "https://tiles.example.com/\\"x\\"\\\\y"' in qml
    assert 'value: "a\\"b\\\\c"' in qml
    assert "evil;break" not in qml
    assert "inject" not in qml
