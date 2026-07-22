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
import sys

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
        if method == "openFiles":
            return {"result": "ok", "opened": self.openFiles(message.get("files", []))}
        if method == "closeFiles":
            return {"result": "ok",
                    "closed": self._closeFiles(message.get("files", []),
                                               bool(message.get("all", False)))}
        if method == "getObjectInfos":
            return {"result": self._objectInfos()}
        if method == "getUiCode":
            return self._uiCode(str(message.get("type", "xml")))
        if method == "getScreenShot":
            return self._screenShot(str(message.get("type", "current")))
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

    def _formWindowManager(self):
        """The form window manager, reachable through any open form."""
        for fw in self._formWindows():
            try:
                return fw.core().formWindowManager()
            except Exception:
                continue
        return None

    def openFiles(self, files):
        """Open .ui files in this Designer instance when the form window
        manager is reachable (any form already open); otherwise fall back
        to a new Designer process."""
        opened = []
        pending = []
        manager = self._formWindowManager()
        for path in files:
            path = os.path.abspath(str(path).replace("\\", "/"))
            if not os.path.exists(path):
                continue
            if manager is not None:
                try:
                    with open(path, encoding="utf-8") as f:
                        contents = f.read()
                    fw = manager.createFormWindow()
                    fw.setFileName(path)
                    fw.setContents(contents)
                    manager.setActiveFormWindow(fw)
                    fw.show()
                    opened.append(os.path.basename(path))
                    continue
                except Exception as e:
                    logDebug(f"Designer bridge: in-process open failed: {e}")
            pending.append(path)

        if pending:
            # No reachable manager (needs at least one open form) - fall back
            # to opening in a Designer window via the desktop shell
            from qtpy.QtCore import QProcess
            candidates = [
                os.path.join(os.path.dirname(sys.executable), 'pyside6-designer'),
                'pyside6-designer',
            ]
            if 'designer' in sys.executable.lower():
                candidates.insert(0, sys.executable)
            program = next((c for c in candidates
                            if os.path.sep not in c or os.path.exists(c)), candidates[-1])
            QProcess.startDetached(program, pending)
            opened.extend(os.path.basename(p) + " (new window)" for p in pending)
        return opened

    def _closeFiles(self, files, close_all=False):
        wanted = {os.path.abspath(str(f).replace("\\", "/")) for f in files}
        closed = []
        for fw in self._formWindows():
            try:
                path = os.path.abspath(fw.fileName() or "")
                if not close_all and path not in wanted:
                    continue
                # close the MDI subwindow / top level holding the form
                holder = fw.parentWidget()
                while holder is not None and not holder.inherits("QMdiSubWindow") \
                        and holder.parentWidget() is not None:
                    holder = holder.parentWidget()
                (holder or fw).close()
                closed.append(os.path.basename(path))
            except Exception as e:
                logDebug(f"Designer bridge: close failed: {e}")
        return closed

    def _objectInfos(self):
        """Widget tree of every open form: class, objectName, geometry."""
        def info(widget):
            geo = widget.geometry()
            return {
                "class": widget.metaObject().className(),
                "name": widget.objectName(),
                "geometry": [geo.x(), geo.y(), geo.width(), geo.height()],
                "children": [info(c) for c in widget.children()
                             if isinstance(c, QWidget)],
            }
        return [{"file": fw.fileName(), "tree": info(fw.mainContainer())}
                for fw in self._formWindows() if fw.mainContainer() is not None]

    def _uiCode(self, code_type):
        """Current (dirty-aware) contents of the active form, as ui XML or
        generated Python."""
        forms = self._formWindows()
        if not forms:
            return {"error": "no open forms"}
        fw = forms[0]
        try:
            manager = self._formWindowManager()
            if manager is not None and manager.activeFormWindow() is not None:
                fw = manager.activeFormWindow()
        except Exception:
            pass
        xml = fw.contents()
        if code_type in ("xml", "ui", ""):
            return {"result": xml, "file": fw.fileName()}
        if code_type in ("pyside6", "python", "py"):
            import subprocess
            import tempfile
            with tempfile.NamedTemporaryFile("w", suffix=".ui", delete=False,
                                             encoding="utf-8") as tmp:
                tmp.write(xml)
                tmp_path = tmp.name
            try:
                proc = subprocess.run(["pyside6-uic", tmp_path],
                                      capture_output=True, text=True, timeout=30)
                if proc.returncode != 0:
                    return {"error": proc.stderr[:2000]}
                return {"result": proc.stdout, "file": fw.fileName()}
            finally:
                os.unlink(tmp_path)
        return {"error": f"unknown code type '{code_type}'"}

    def _screenShot(self, shot_type):
        """Base64 PNG of the active form ('current'), every form ('all') or
        the Designer main window ('main')."""
        import base64
        from qtpy.QtCore import QBuffer, QIODevice

        def grab_b64(widget):
            pixmap = widget.grab()
            buffer = QBuffer()
            buffer.open(QIODevice.WriteOnly)
            pixmap.save(buffer, "PNG")
            return base64.b64encode(bytes(buffer.data())).decode("ascii")

        app = QApplication.instance()
        if shot_type == "main":
            windows = [w for w in (app.topLevelWidgets() if app else [])
                       if w.inherits("QMainWindow") and w.isVisible()]
            if not windows:
                return {"error": "no main window"}
            return {"result": grab_b64(windows[0])}

        forms = [fw for fw in self._formWindows() if fw.mainContainer() is not None]
        if not forms:
            return {"error": "no open forms"}
        if shot_type == "all":
            return {"result": [{"file": fw.fileName(),
                                "png": grab_b64(fw.mainContainer())} for fw in forms]}
        return {"result": grab_b64(forms[0].mainContainer()), "file": forms[0].fileName()}


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

    def request(self, message, reply_timeout_ms=10000):
        """Send one message and wait for the JSON reply. Returns the reply
        dict, or None when Designer/the bridge is not running."""
        try:
            sock = QLocalSocket()
            sock.connectToServer(self._name)
            if not sock.waitForConnected(self._timeout):
                return None
            sock.write((json.dumps(message) + "\n").encode("utf-8"))
            sock.flush()
            sock.waitForBytesWritten(self._timeout)

            import time
            buffer = b""
            deadline = time.monotonic() + (reply_timeout_ms / 1000.0)
            while time.monotonic() < deadline and b"\n" not in buffer:
                if sock.waitForReadyRead(200):
                    buffer += bytes(sock.readAll())
            sock.disconnectFromServer()
            if b"\n" not in buffer:
                return None
            return json.loads(buffer.split(b"\n")[0].decode("utf-8"))
        except Exception as e:
            logDebug(f"Designer bridge request failed: {e}")
            return None
