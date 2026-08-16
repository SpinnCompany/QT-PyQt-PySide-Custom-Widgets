"""In-app control server: lets Designer / the MCP OBSERVE and NAVIGATE a
running Custom_Widgets application.

The running app is a separate process from Designer (Run launches it under the
dev server, which sets ``CUSTOM_WIDGETS_APP_CONTROL=1``). This server runs
INSIDE that app process - so it can grab real screenshots, walk the live widget
tree, and synthesize clicks - and exposes it over a per-project QLocalServer
socket. The protocol mirrors the Designer bridge: newline-delimited JSON.

Methods: ping, listWindows, screenshot, objectTree, find, click, setProperty,
setText, invoke.

Started idempotently by ``QAppSettings.updateAppSettings`` via
``maybe_start_app_control`` (only when the env flag is set, so production apps
are unaffected). Talk to it with :class:`AppControlClient`.
"""
import base64
import hashlib
import json
import os

from qtpy.QtCore import QObject, QBuffer, QIODevice, QPointF, QEvent, Qt
from qtpy.QtGui import QMouseEvent
from qtpy.QtNetwork import QLocalServer, QLocalSocket
from qtpy.QtWidgets import QApplication, QWidget, QAbstractButton

from Custom_Widgets.Project import projectRoot
from Custom_Widgets.Log import *
from Custom_Widgets.tools.socket_auth import (write_token, read_token,
                                              remove_token, auth_line,
                                              parse_auth_line)

_server_singleton = None


def appControlServerName(project_dir=None):
    """Per-project socket name, distinct from the Designer bridge's."""
    root = os.path.abspath(project_dir or projectRoot())
    digest = hashlib.sha1(root.encode("utf-8")).hexdigest()[:12]
    return f"customwidgets-app-{digest}"


def start_app_control(project_dir=None):
    """Start (once) the in-app control server. Returns the server or None."""
    global _server_singleton
    if _server_singleton is not None:
        return _server_singleton
    try:
        _server_singleton = AppControlServer(project_dir=project_dir)
    except Exception as e:
        logDebug(f"App control: failed to start: {e}")
        _server_singleton = None
    return _server_singleton


def maybe_start_app_control(project_dir=None):
    """Start the control server only when opted in via
    ``CUSTOM_WIDGETS_APP_CONTROL`` (the dev server sets it for Run'd apps), so
    ordinary/production launches are untouched."""
    if os.environ.get("CUSTOM_WIDGETS_APP_CONTROL", "") not in ("1", "true", "True"):
        return None
    return start_app_control(project_dir)


class AppControlServer(QObject):
    """QLocalServer inside the running app; answers observe/navigate requests."""

    def __init__(self, parent=None, project_dir=None):
        super().__init__(parent)
        self._sockets = []
        name = appControlServerName(project_dir)
        QLocalServer.removeServer(name)  # clear a stale socket from a crash
        self._socket_name = name
        self._server = QLocalServer(self)
        if not self._server.listen(name):
            raise RuntimeError(
                f"cannot listen on {name}: {self._server.errorString()}")
        try:
            # Only the owning user may connect; a token is still required as
            # the first line (see socket_auth).
            self._server.setSocketOptions(QLocalServer.UserAccessOption)
        except Exception as e:
            logDebug(f"App control: socket options not applied: {e}")
        self.token = write_token(name)
        self._server.newConnection.connect(self._onNewConnection)
        logInfo(f"App control: listening on {name} (pid {os.getpid()})")

    def isListening(self):
        return self._server.isListening()

    def close(self):
        """Disconnect clients and stop listening (clean teardown - avoids a
        lingering socket firing signals into deleted objects)."""
        for sock in list(self._sockets):
            try:
                sock.disconnected.disconnect()
                sock.readyRead.disconnect()
            except (RuntimeError, TypeError):
                pass
            try:
                sock.abort()
                sock.deleteLater()
            except RuntimeError:
                pass
        self._sockets.clear()
        try:
            self._server.close()
        except RuntimeError:
            pass
        remove_token(self._socket_name)

    # -- connection plumbing (line-based, mirrors DesignerBridge) -------
    def _onNewConnection(self):
        while self._server.hasPendingConnections():
            sock = self._server.nextPendingConnection()
            sock._authorized = False
            sock.readyRead.connect(lambda s=sock: self._onReadyRead(s))
            sock.disconnected.connect(lambda s=sock: self._dropSocket(s))
            self._sockets.append(sock)

    def _dropSocket(self, sock):
        if sock in self._sockets:
            self._sockets.remove(sock)
        try:
            sock.deleteLater()
        except RuntimeError:
            pass  # C++ side already gone

    def _onReadyRead(self, sock):
        while sock.canReadLine():
            raw = bytes(sock.readLine()).decode("utf-8", errors="ignore").strip()
            if not raw:
                continue
            if not getattr(sock, "_authorized", False):
                if parse_auth_line(raw, self.token):
                    sock._authorized = True
                else:
                    logWarning("App control: rejecting unauthenticated "
                               "connection")
                    sock.abort()
                    self._dropSocket(sock)
                    return
                continue
            try:
                reply = self._dispatch(json.loads(raw))
            except Exception as e:
                reply = {"error": f"{type(e).__name__}: {e}"}
            try:
                sock.write((json.dumps(reply) + "\n").encode("utf-8"))
                sock.flush()
            except Exception:
                pass

    # -- dispatch ------------------------------------------------------
    def _dispatch(self, message):
        method = str(message.get("method", ""))
        logDebug(f"App control received: {method}")
        if method == "ping":
            return {"result": "pong", "pid": os.getpid()}
        if method == "listWindows":
            return {"result": self._listWindows()}
        if method == "screenshot":
            return self._screenshot(str(message.get("target", "active")))
        if method == "objectTree":
            return self._objectTree(str(message.get("window", "")))
        if method == "find":
            return {"result": self._find(str(message.get("query", "")),
                                        str(message.get("by", "any")))}
        if method == "click":
            return self._click(str(message.get("widget", "")))
        if method == "setProperty":
            return self._setProperty(str(message.get("widget", "")),
                                     str(message.get("property", "")),
                                     message.get("value"))
        if method == "setText":
            return self._setText(str(message.get("widget", "")),
                                 str(message.get("text", "")))
        if method == "invoke":
            return self._invoke(str(message.get("widget", "")),
                                str(message.get("slot", "")))
        if method == "window":
            return self._window(message)
        if method == "quit":
            from qtpy.QtCore import QTimer
            QTimer.singleShot(50, QApplication.quit)  # let the reply flush first
            return {"result": "ok", "quitting": True}
        return {"error": f"unknown method '{method}'"}

    # -- helpers -------------------------------------------------------
    @staticmethod
    def _windows():
        """Real top-level windows of the app (skip Qt-internal popups)."""
        app = QApplication.instance()
        if app is None:
            return []
        out = []
        for w in app.topLevelWidgets():
            if not w.isWindow() or not w.isVisible():
                continue
            if w.objectName().startswith("qt_"):
                continue
            out.append(w)
        return out

    def _resolveWindow(self, target):
        wins = self._windows()
        if not wins:
            return None
        if target in ("", "active"):
            app = QApplication.instance()
            active = app.activeWindow() if app else None
            return active if active in wins else wins[0]
        if target == "main":
            for w in wins:
                if w.inherits("QMainWindow"):
                    return w
            return wins[0]
        for w in wins:  # by objectName
            if w.objectName() == target:
                return w
        return None

    def _find_widget(self, name):
        """First widget (prefer visible) whose objectName == name."""
        app = QApplication.instance()
        if app is None or not name:
            return None
        matches = [w for w in app.allWidgets() if w.objectName() == name]
        for w in matches:
            if w.isVisible():
                return w
        return matches[0] if matches else None

    @staticmethod
    def _grab_b64(widget):
        pixmap = widget.grab()
        buf = QBuffer()
        buf.open(QIODevice.WriteOnly)
        pixmap.save(buf, "PNG")
        return base64.b64encode(bytes(buf.data())).decode("ascii")

    @staticmethod
    def _widget_text(w):
        for attr in ("text", "title", "windowTitle", "currentText"):
            fn = getattr(w, attr, None)
            if callable(fn):
                try:
                    val = fn()
                    if val:
                        return str(val)
                except Exception:
                    pass
        return ""

    # -- methods -------------------------------------------------------
    def _listWindows(self):
        app = QApplication.instance()
        active = app.activeWindow() if app else None
        out = []
        for w in self._windows():
            g = w.geometry()
            out.append({
                "objectName": w.objectName(),
                "class": type(w).__name__,
                "title": w.windowTitle(),
                "geometry": [g.x(), g.y(), g.width(), g.height()],
                "active": w is active,
            })
        return out

    def _screenshot(self, target):
        win = self._resolveWindow(target)
        if win is None:
            return {"error": f"no window matching '{target}'"}
        return {"result": self._grab_b64(win),
                "window": win.objectName() or type(win).__name__}

    def _objectTree(self, window):
        win = self._resolveWindow(window or "active")
        if win is None:
            return {"error": "no window"}

        def node(w):
            g = w.geometry()
            info = {
                "class": type(w).__name__,
                "objectName": w.objectName(),
                "geometry": [g.x(), g.y(), g.width(), g.height()],
                "visible": w.isVisible(),
                "enabled": w.isEnabled(),
            }
            text = self._widget_text(w)
            if text:
                info["text"] = text[:80]
            children = [node(c) for c in w.findChildren(
                QWidget, options=Qt.FindDirectChildrenOnly)]
            if children:
                info["children"] = children
            return info

        return {"result": {"window": win.objectName() or type(win).__name__,
                            "tree": node(win)}}

    def _find(self, query, by):
        app = QApplication.instance()
        if app is None:
            return []
        q = query.lower()
        out = []
        for w in app.allWidgets():
            name = w.objectName()
            if name.startswith("qt_"):
                continue
            text = self._widget_text(w)
            hit = ((by in ("any", "name") and q in name.lower() and name) or
                   (by in ("any", "text") and q in text.lower() and text) or
                   (by in ("any", "class") and q in type(w).__name__.lower()))
            if hit:
                out.append({"objectName": name, "class": type(w).__name__,
                            "text": text[:60], "visible": w.isVisible()})
            if len(out) >= 50:
                break
        return out

    def _click(self, name):
        w = self._find_widget(name)
        if w is None:
            return {"error": f"no widget named '{name}' (see find/objectTree)"}
        try:
            if isinstance(w, QAbstractButton):
                w.click()
                return {"result": "ok", "clicked": name, "via": "click()"}
            center = QPointF(w.rect().center())
            for etype in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease):
                ev = QMouseEvent(etype, center, Qt.LeftButton, Qt.LeftButton,
                                 Qt.NoModifier)
                QApplication.sendEvent(w, ev)
            return {"result": "ok", "clicked": name, "via": "mouse"}
        except Exception as e:
            return {"error": f"click failed: {e}"}

    def _setProperty(self, name, prop, value):
        w = self._find_widget(name)
        if w is None:
            return {"error": f"no widget named '{name}'"}
        try:
            w.setProperty(prop, value)
            w.style().unpolish(w)
            w.style().polish(w)
            return {"result": "ok", "widget": name, "property": prop}
        except Exception as e:
            return {"error": f"setProperty failed: {e}"}

    def _setText(self, name, text):
        w = self._find_widget(name)
        if w is None:
            return {"error": f"no widget named '{name}'"}
        setter = getattr(w, "setText", None) or getattr(w, "setPlainText", None)
        if setter is None:
            return {"error": f"'{name}' has no setText/setPlainText"}
        try:
            setter(text)
            return {"result": "ok", "widget": name}
        except Exception as e:
            return {"error": f"setText failed: {e}"}

    def _window(self, message):
        """Move / resize / raise a top-level window, or list screens. Actions:
        move{x,y}, geometry{x,y,width,height}, maximize, normal, raise,
        toPrimary (move onto the primary screen), screens. Useful when a
        multi-monitor compositor parks the window on an off-screen output."""
        action = str(message.get("action", "raise"))
        app = QApplication.instance()
        if action == "screens":
            return {"result": [
                {"name": s.name(),
                 "geometry": [s.geometry().x(), s.geometry().y(),
                              s.geometry().width(), s.geometry().height()],
                 "primary": s is app.primaryScreen()} for s in app.screens()]}
        win = self._resolveWindow(str(message.get("target", "active")))
        if win is None:
            return {"error": "no window"}
        try:
            if action == "move":
                win.showNormal()
                win.move(int(message.get("x", 0)), int(message.get("y", 0)))
            elif action == "geometry":
                win.showNormal()
                win.setGeometry(int(message.get("x", 0)), int(message.get("y", 0)),
                                int(message.get("width", 900)),
                                int(message.get("height", 600)))
            elif action == "toPrimary":
                ps = app.primaryScreen()
                g = ps.geometry()
                win.showNormal()
                win.move(g.x() + 80, g.y() + 60)
            elif action == "maximize":
                win.showMaximized()
            elif action == "normal":
                win.showNormal()
            win.raise_()
            win.activateWindow()
            g = win.geometry()
            return {"result": "ok",
                    "geometry": [g.x(), g.y(), g.width(), g.height()]}
        except Exception as e:
            return {"error": f"window failed: {e}"}

    def _invoke(self, name, slot):
        w = self._find_widget(name)
        if w is None:
            return {"error": f"no widget named '{name}'"}
        fn = getattr(w, slot, None)
        if not callable(fn):
            return {"error": f"'{name}' has no callable '{slot}'"}
        try:
            fn()
            return {"result": "ok", "widget": name, "slot": slot}
        except Exception as e:
            return {"error": f"invoke failed: {e}"}


class AppControlClient:
    """Talks to a running app's control server. Fails fast/quietly when the
    app (or its control server) isn't up."""

    def __init__(self, project_dir=None, timeout_ms=500):
        self._name = appControlServerName(project_dir)
        self._timeout = timeout_ms

    def request(self, message, reply_timeout_ms=10000):
        token = read_token(self._name)
        if not token:
            return None
        sock = QLocalSocket()
        sock.connectToServer(self._name)
        if not sock.waitForConnected(self._timeout):
            return None
        try:
            sock.write(auth_line(token))
            sock.write((json.dumps(message) + "\n").encode("utf-8"))
            sock.flush()
            buf = b""
            while b"\n" not in buf:
                if not sock.waitForReadyRead(reply_timeout_ms):
                    return None
                buf += bytes(sock.readAll())
            return json.loads(buf.split(b"\n")[0].decode("utf-8"))
        finally:
            sock.disconnectFromServer()

    def isReachable(self, timeout_ms=1000):
        return (self.request({"method": "ping"},
                             reply_timeout_ms=timeout_ms) or {}).get("result") == "pong"
