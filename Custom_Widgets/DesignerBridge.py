########################################################################
## DESIGNER BRIDGE
##
## Live link between a running Custom_Widgets app and Qt Designer,
## modeled on the "Designer Control Plugin" from
## https://github.com/PyQt5/QtDesignerPlugins (C++/Qt5, WebSocket).
##
## Here the server runs INSIDE Qt Designer (started by the Custom_Widgets
## Designer plugins, see Plugins/register.py) as a QLocalServer, and the
## app connects as a short-lived client to push theme events, so open
## forms recolor/restyle live instead of requiring a manual reopen.
##
## Protocol: newline-delimited JSON, one object per line.
##   {"method": "ping"}                           -> {"result": "pong"}
##   {"method": "refreshIcons", "color": "#..."}  -> clear pixmap caches and
##                                                   repolish open forms
##   {"method": "setStyleSheet", "qss": "..."}    -> style open form previews
##   {"method": "reloadForms"}                    -> reload unmodified forms
##                                                   from disk
########################################################################
import hashlib
import json
import os

from qtpy.QtCore import QObject, QDir
from qtpy.QtGui import QPixmapCache
from qtpy.QtNetwork import QLocalServer, QLocalSocket
from qtpy.QtWidgets import QApplication, QWidget

from Custom_Widgets.Log import *

_bridge_server = None


def bridgeServerName(project_dir=None):
    """Server name unique per project folder, identical for the app and a
    Designer launched from that folder (Custom_Widgets --start-designer)."""
    project_dir = os.path.abspath(project_dir or os.getcwd())
    digest = hashlib.sha1(project_dir.encode("utf-8")).hexdigest()[:12]
    return f"customwidgets-designer-{digest}"


def startDesignerBridge(project_dir=None):
    """Start (once) the bridge server inside Qt Designer."""
    global _bridge_server
    if _bridge_server is None:
        _bridge_server = DesignerBridgeServer(project_dir=project_dir)
    return _bridge_server


class DesignerBridgeServer(QObject):
    """Runs inside Qt Designer's process."""

    def __init__(self, parent=None, project_dir=None):
        super().__init__(parent)
        self._project_dir = os.path.abspath(project_dir or os.getcwd())
        self._sockets = []

        # Themed url(theme-icons:...) references resolve inside Designer too
        QDir.addSearchPath('theme-icons', os.path.join(self._project_dir, 'Qss/icons/'))

        name = bridgeServerName(self._project_dir)
        QLocalServer.removeServer(name)  # clear a stale socket from a crash
        self._server = QLocalServer(self)
        if self._server.listen(name):
            self._server.newConnection.connect(self._onNewConnection)
            logInfo(f"Designer bridge listening on '{name}'")
        else:
            logWarning(f"Designer bridge could not listen on '{name}': "
                       f"{self._server.errorString()}")

    def isListening(self):
        return self._server.isListening()

    ####################################################################
    ## TRANSPORT
    ####################################################################
    def _onNewConnection(self):
        while self._server.hasPendingConnections():
            sock = self._server.nextPendingConnection()
            sock.readyRead.connect(lambda s=sock: self._onReadyRead(s))
            sock.disconnected.connect(lambda s=sock: self._dropSocket(s))
            self._sockets.append(sock)

    def _dropSocket(self, sock):
        if sock in self._sockets:
            self._sockets.remove(sock)
        sock.deleteLater()

    def _onReadyRead(self, sock):
        while sock.canReadLine():
            raw = bytes(sock.readLine()).decode("utf-8", errors="ignore").strip()
            if not raw:
                continue
            try:
                message = json.loads(raw)
                reply = self._dispatch(message)
            except Exception as e:
                reply = {"error": str(e)}
            try:
                sock.write((json.dumps(reply) + "\n").encode("utf-8"))
                sock.flush()
            except Exception as e:
                logDebug(f"Designer bridge reply failed: {e}")

    def _dispatch(self, message):
        method = str(message.get("method", ""))
        logDebug(f"Designer bridge received: {method}")
        if method == "ping":
            return {"result": "pong"}
        if method == "refreshIcons":
            self._refreshIcons()
            return {"result": "ok"}
        if method == "setStyleSheet":
            self._setStyleSheet(str(message.get("qss", "")))
            return {"result": "ok"}
        if method == "reloadForms":
            return {"result": "ok", "reloaded": self._reloadForms()}
        return {"error": f"unknown method '{method}'"}

    ####################################################################
    ## DESIGNER ACTIONS
    ####################################################################
    def _formWindows(self):
        """Open QDesignerFormWindowInterface instances (empty outside
        Designer, which keeps the server harmless in tests)."""
        try:
            from qtpy.QtDesigner import QDesignerFormWindowInterface
        except Exception:
            return []
        app = QApplication.instance()
        if app is None:
            return []
        return [w for w in app.allWidgets()
                if isinstance(w, QDesignerFormWindowInterface)]

    def _repolish(self, root):
        widgets = [root] + root.findChildren(QWidget)
        for widget in widgets:
            style = widget.style()
            style.unpolish(widget)
            style.polish(widget)
            widget.update()

    def _refreshIcons(self):
        """The shared icon set was rewritten in place - drop cached pixmaps
        so Designer re-reads the svg files, then repaint open forms."""
        QPixmapCache.clear()
        for fw in self._formWindows():
            container = fw.mainContainer()
            if container is not None:
                self._repolish(container)
        logInfo("Designer bridge: icon caches refreshed")

    def _setStyleSheet(self, qss):
        """Paint open form previews with the app's compiled theme."""
        for fw in self._formWindows():
            container = fw.mainContainer()
            if container is not None:
                container.setStyleSheet(qss)
                self._repolish(container)
        logInfo("Designer bridge: theme stylesheet applied to open forms")

    def _reloadForms(self):
        """Reload open, UNMODIFIED forms from disk (never touches dirty
        forms, so user edits are safe)."""
        reloaded = []
        for fw in self._formWindows():
            try:
                if fw.isDirty():
                    continue
                path = fw.fileName()
                if path and os.path.exists(path):
                    with open(path, encoding="utf-8") as f:
                        fw.setContents(f.read())
                    reloaded.append(os.path.basename(path))
            except Exception as e:
                logDebug(f"Designer bridge: reload failed for form: {e}")
        return reloaded


class DesignerBridgeClient:
    """Used by the running app. Fire-and-forget; every call fails silently
    when Designer (or the bridge) is not running."""

    def __init__(self, project_dir=None, timeout_ms=200):
        self._name = bridgeServerName(project_dir)
        self._timeout = timeout_ms

    def send(self, message):
        """Deliver one message. Returns True when the bridge accepted it."""
        try:
            sock = QLocalSocket()
            sock.connectToServer(self._name)
            if not sock.waitForConnected(self._timeout):
                return False
            sock.write((json.dumps(message) + "\n").encode("utf-8"))
            sock.flush()
            sock.waitForBytesWritten(self._timeout)
            sock.disconnectFromServer()
            return True
        except Exception as e:
            logDebug(f"Designer bridge send skipped: {e}")
            return False

    def notifyThemeChanged(self, color=None, qss=""):
        """Tell Designer the shared icon set was regenerated; optionally
        push the compiled theme stylesheet onto open form previews."""
        delivered = self.send({"method": "refreshIcons", "color": color})
        if delivered and qss:
            self.send({"method": "setStyleSheet", "qss": qss})
        return delivered
