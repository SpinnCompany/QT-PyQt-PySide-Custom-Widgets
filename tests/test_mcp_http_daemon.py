"""MCP HTTP daemon: bearer-token auth and the non-loopback refusal.

The daemon (`python -m Custom_Widgets.mcp --transport http`) is the transport
sessions/agents actually use, so auth around it is release-blocking behaviour,
not a unit detail: it must reject unauthenticated requests with a 401, accept
the right bearer token, and refuse to bind a non-loopback host without one.
"""
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _daemon_env():
    env = dict(os.environ)
    env["QT_API"] = "pyside6"
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    env["PYTHONUNBUFFERED"] = "1"
    return env


def _request(port, path, token=None, timeout=5):
    url = "http://127.0.0.1:%d%s" % (port, path)
    req = urllib.request.Request(url)
    if token is not None:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except (urllib.error.URLError, ConnectionError, OSError):
        return None


def _wait_up(port, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        code = _request(port, "/mcp", timeout=2)
        if code is not None:
            return code
        time.sleep(0.5)
    return None


@pytest.fixture
def http_daemon():
    """Start a token-authed HTTP daemon on a free port; yield (port, token)."""
    port = _free_port()
    token = "daemon-test-token-%d" % os.getpid()
    proc = subprocess.Popen(
        [sys.executable, "-m", "Custom_Widgets.mcp", "--transport", "http",
         "--host", "127.0.0.1", "--port", str(port), "--token", token],
        cwd=REPO_ROOT, env=_daemon_env(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        _wait_up(port)
        yield port, token
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


def test_unauthenticated_request_is_rejected(http_daemon):
    port, _ = http_daemon
    assert _request(port, "/mcp", token=None) == 401


def test_wrong_token_is_rejected(http_daemon):
    port, _ = http_daemon
    assert _request(port, "/mcp", token="wrong-token") == 401


def test_correct_token_is_accepted(http_daemon):
    port, token = http_daemon
    # A valid token must get past the auth middleware; the endpoint itself may
    # then answer 200/405/400 — anything but the auth rejection.
    assert _request(port, "/mcp", token=token) != 401


def test_non_loopback_bind_without_token_is_refused():
    """Binding to a non-loopback host without a bearer token must not even
    start: the daemon exits with the refusal message."""
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "Custom_Widgets.mcp", "--transport", "http",
         "--host", "0.0.0.0", "--port", str(port)],
        cwd=REPO_ROOT, env=_daemon_env(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        pytest.fail("daemon did not refuse the non-loopback bind")
    assert proc.returncode != 0
    assert b"refusing to bind" in err


def test_daemon_with_token_serves_requests():
    port = _free_port()
    token = "bind-token"
    proc = subprocess.Popen(
        [sys.executable, "-m", "Custom_Widgets.mcp", "--transport", "http",
         "--host", "127.0.0.1", "--port", str(port), "--token", token],
        cwd=REPO_ROOT, env=_daemon_env(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        assert _wait_up(port) is not None
        assert _request(port, "/mcp", token=token) != 401
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()