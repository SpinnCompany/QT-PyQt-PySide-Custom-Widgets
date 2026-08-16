"""Shared per-user socket authentication for the Designer bridge and the
in-app control server.

Both servers listen on per-project QLocalServer sockets whose names are a
deterministic hash of the project folder. A socket name alone gives ANY local
process (any user) the address, and a process can even pre-listen on the name
before the real server starts. Two layers close that down:

* ``QLocalServer.SocketOptions.UserAccessOption`` restricts connect() to the
  owning user (other users get EACCES on the socket file).
* A one-time token is written to a 0600 file under the user's cache dir
  (``~/.cache/customwidgets/<socket-name>.token``) by the server at listen
  time. Clients must present the token as the FIRST line of a connection;
  connections that don't are aborted. Because the file is only readable by
  the owning user, an unrelated same-user process would have to actively
  hunt for it — it no longer works to just guess the socket name.

Pure stdlib, no Qt — cheap to import from both control surfaces.
"""
import hashlib
import os
import secrets

TOKEN_PREFIX = "CWTOKEN "
_TOKEN_DIR = "customwidgets"


def _token_dir():
    cache = os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
    return os.path.join(cache, _TOKEN_DIR)


def token_path(socket_name):
    """Path of the token file for a socket name (hashed so odd characters in
    user-supplied names can't escape the token directory)."""
    digest = hashlib.sha1(socket_name.encode("utf-8")).hexdigest()[:16]
    return os.path.join(_token_dir(), f"{digest}.token")


def write_token(socket_name):
    """Create a fresh token for a socket and persist it 0600. Returns the
    token string. Idempotent — a later server on the same name overwrites."""
    path = token_path(socket_name)
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    token = secrets.token_hex(16)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, token.encode("utf-8"))
    finally:
        os.close(fd)
    return token


def read_token(socket_name):
    """Token for a socket, or None when no authorized server has written one."""
    path = token_path(socket_name)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read().strip() or None
    except (OSError, ValueError):
        return None


def remove_token(socket_name):
    """Drop a server's token file (best-effort)."""
    try:
        os.remove(token_path(socket_name))
    except OSError:
        pass


def auth_line(token):
    return (TOKEN_PREFIX + token + "\n").encode("utf-8")


def parse_auth_line(raw_line, token):
    """True when a first-line token matches the server's token."""
    if not raw_line or not token:
        return False
    return raw_line == TOKEN_PREFIX + token
