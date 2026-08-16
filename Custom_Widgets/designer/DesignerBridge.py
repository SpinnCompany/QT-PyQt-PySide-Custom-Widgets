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

from qtpy.QtCore import QObject, QDir, Qt
from qtpy.QtGui import QPixmapCache
from qtpy.QtNetwork import QLocalServer, QLocalSocket
from qtpy.QtWidgets import QApplication, QWidget

from Custom_Widgets.Project import projectRoot
from Custom_Widgets.Log import *
from Custom_Widgets.tools.socket_auth import (write_token, read_token,
                                              remove_token, auth_line,
                                              parse_auth_line)

_bridge_server = None
_form_editor_core = None  # QDesignerFormEditorInterface, captured at plugin init
_core_listeners = []      # callbacks run once the core is captured


def setFormEditorCore(core):
    """Called by the core-capture plugin when Designer initializes it.
    This is the only supported way to reach the form window manager (the
    core is internal C++, not in the widget tree)."""
    global _form_editor_core
    _form_editor_core = core
    logDebug("Designer bridge: form editor core captured")
    for callback in list(_core_listeners):
        try:
            callback(core)
        except Exception as e:
            logException(e, message="Designer bridge: core listener failed")


def addCoreListener(callback):
    """Run `callback(core)` when the form-editor core is captured (or now, if
    it already has been). Lets plugin registrars install Designer extensions
    that need the core, without racing its asynchronous capture."""
    _core_listeners.append(callback)
    if _form_editor_core is not None:
        try:
            callback(_form_editor_core)
        except Exception as e:
            logException(e, message="Designer bridge: core listener failed")


def registerCoreCapture():
    """Register a hidden custom-widget plugin whose sole job is to receive
    the QDesignerFormEditorInterface via initialize(core). Call from the
    Designer plugin registrars."""
    try:
        # Import the registration helpers from the concrete binding. qtpy's
        # `from PySide6.QtDesigner import *` shim drops QPyDesignerCustom-
        # WidgetCollection inside Designer's embedded interpreter, so reach
        # for PySide6 (then PyQt) directly, matching how the registrars do.
        try:
            from PySide6.QtDesigner import (QDesignerCustomWidgetInterface,
                                            QPyDesignerCustomWidgetCollection)
        except ImportError:
            from qtpy.QtDesigner import (QDesignerCustomWidgetInterface,
                                         QPyDesignerCustomWidgetCollection)
        from qtpy.QtWidgets import QWidget

        class _CoreCapturePlugin(QDesignerCustomWidgetInterface):
            def initialize(self, core):
                setFormEditorCore(core)

            def isInitialized(self):
                return _form_editor_core is not None

            def createWidget(self, parent):
                return QWidget(parent)

            def name(self):
                return "CustomWidgetsCoreCapture"

            def group(self):
                return "Custom Widgets (internal)"

            def toolTip(self):
                return ""

            def whatsThis(self):
                return ""

            def includeFile(self):
                return ""

            def isContainer(self):
                return False

            def icon(self):
                from qtpy.QtGui import QIcon
                return QIcon()

            def domXml(self):
                # empty -> hidden from the widget box
                return ""

        QPyDesignerCustomWidgetCollection.addCustomWidget(_CoreCapturePlugin())
    except Exception as e:
        logException(e, message="Designer bridge: core-capture registration failed")


def formEditorCore():
    return _form_editor_core


def bridgeServerName(project_dir=None):
    """Server name unique per project folder, identical for the app and a
    Designer launched from that folder (Custom_Widgets --start-designer)."""
    project_dir = os.path.abspath(project_dir or projectRoot())
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
        self._project_dir = os.path.abspath(project_dir or projectRoot())
        self._sockets = []

        # Themed url(theme-icons:...) references resolve inside Designer too
        QDir.addSearchPath('theme-icons', os.path.join(self._project_dir, 'Qss/icons/'))

        name = bridgeServerName(self._project_dir)
        QLocalServer.removeServer(name)  # clear a stale socket from a crash
        self._socket_name = name
        self._server = QLocalServer(self)
        if self._server.listen(name):
            try:
                # Only the owning user may connect; a token is still required
                # as the first line (see socket_auth).
                self._server.setSocketOptions(QLocalServer.UserAccessOption)
            except Exception as e:
                logDebug(f"Designer bridge: socket options not applied: {e}")
            self.token = write_token(name)
            self._server.newConnection.connect(self._onNewConnection)
            logInfo(f"Designer bridge listening on '{name}'")
        else:
            logWarning(f"Designer bridge could not listen on '{name}': "
                       f"{self._server.errorString()}")

    def isListening(self):
        return self._server.isListening()

    def rebindProject(self, project_dir):
        """Re-point the bridge at another project: new socket name (derived
        from the project path) and themed-icon search path. Used by the
        Designer workspace switcher."""
        self._project_dir = os.path.abspath(project_dir)
        QDir.addSearchPath('theme-icons',
                           os.path.join(self._project_dir, 'Qss/icons/'))
        name = bridgeServerName(self._project_dir)
        self._server.close()
        remove_token(self._socket_name)
        QLocalServer.removeServer(name)
        self._socket_name = name
        if self._server.listen(name):
            try:
                self._server.setSocketOptions(QLocalServer.UserAccessOption)
            except Exception as e:
                logDebug(f"Designer bridge: socket options not applied: {e}")
            self.token = write_token(name)
            logInfo(f"Designer bridge re-bound to '{name}'")
        else:
            logWarning(f"Designer bridge could not re-bind to '{name}': "
                       f"{self._server.errorString()}")

    ####################################################################
    ## TRANSPORT
    ####################################################################
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
            pass

    def close(self):
        """Stop listening and drop the auth token (clean teardown)."""
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

    def _onReadyRead(self, sock):
        while sock.canReadLine():
            raw = bytes(sock.readLine()).decode("utf-8", errors="ignore").strip()
            if not raw:
                continue
            if not getattr(sock, "_authorized", False):
                if parse_auth_line(raw, self.token):
                    sock._authorized = True
                else:
                    logWarning("Designer bridge: rejecting unauthenticated "
                               "connection")
                    sock.abort()
                    self._dropSocket(sock)
                    return
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
            self._setStyleSheet(str(message.get("qss", "")),
                                bool(message.get("entireApp", False)))
            return {"result": "ok"}
        if method == "reloadForms":
            return {"result": "ok", "reloaded": self._reloadForms()}
        if method == "openFiles":
            return {"result": "ok",
                    "opened": self.openFiles(message.get("files", []),
                                             new_process=bool(message.get("newWindow", False)))}
        if method == "newForm":
            return self._newForm(message.get("name", "untitled"),
                                 template=message.get("template"),
                                 folder=message.get("folder"),
                                 open_after=bool(message.get("open", True)))
        if method == "listTemplates":
            from Custom_Widgets.DesignerTools import FORM_TEMPLATES
            return {"result": list(FORM_TEMPLATES)}
        if method == "closeFiles":
            return {"result": "ok",
                    "closed": self._closeFiles(message.get("files", []),
                                               bool(message.get("all", False)))}
        if method == "getObjectInfos":
            return {"result": self._objectInfos()}
        if method == "getUiCode":
            return self._uiCode(str(message.get("type", "xml")))
        if method == "setFormXml":
            return self._setFormXml(message)
        if method == "newFormXml":
            return self._newFormXml(message)
        if method == "getScreenShot":
            return self._screenShot(str(message.get("type", "current")))
        if method == "getDocks":
            return {"result": self._getDocks()}
        if method == "setDock":
            return self._setDock(message)
        if method == "getDialogs":
            return {"result": self._getDialogs()}
        if method == "dismissDialog":
            return self._dismissDialog(str(message.get("match", "")),
                                       str(message.get("button", "")))
        if method == "getActions":
            return {"result": self._getActions()}
        if method == "triggerAction":
            return self._triggerAction(str(message.get("action", "")))
        if method == "setWidgetProperty":
            return self._setWidgetProperty(str(message.get("widget", "")),
                                           str(message.get("property", "")),
                                           message.get("value"))
        if method == "openWorkspace":
            try:
                from Custom_Widgets.DesignerTools import switchWorkspace
                ok = switchWorkspace(str(message.get("path", "")))
                return {"result": "ok" if ok else "failed"}
            except Exception as e:
                return {"error": f"openWorkspace failed: {e}"}
        if method == "runApp":
            return self._runApp("start")
        if method == "stopApp":
            return self._runApp("stop")
        if method == "restartApp":
            return self._runApp("restart")
        if method == "appStatus":
            return self._runApp("status")
        if method == "appLogs":
            return self._runApp("logs", int(message.get("lines", 100)))
        if method == "qssWindow":
            return self._qssWindow(message)
        if method == "designerWindow":
            return self._designerWindow(message)
        if method == "quit":
            from qtpy.QtCore import QTimer
            # Mark open forms clean so Designer doesn't pop a modal
            # "Save changes before exiting?" that blocks the quit — forms are
            # persisted explicitly (setFormXml save=True / Designer save).
            dirty = []
            for fw in self._formWindows():
                try:
                    if fw.isDirty():
                        dirty.append(os.path.basename(fw.fileName() or "form"))
                    fw.setDirty(False)
                except Exception:
                    pass
            # Flush this reply before tearing Designer down.
            QTimer.singleShot(80, lambda: (QApplication.quit()
                                           if QApplication.instance() else None))
            return {"result": "ok", "quitting": True,
                    "had_unsaved": dirty}
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

    def _setStyleSheet(self, qss, entire_app=False):
        """Paint open form previews with the app's compiled theme. When
        entire_app is True, ALSO set it as an application-level stylesheet so
        the whole Designer - chrome and every open form - inherits it (pass an
        empty qss with entire_app=True to clear that app-wide paint)."""
        if entire_app:
            app = QApplication.instance()
            if app is not None:
                app.setStyleSheet(qss)
            logInfo("Designer bridge: theme stylesheet applied to entire "
                    "Designer app (forms inherit)")
        for fw in self._formWindows():
            container = fw.mainContainer()
            if container is not None:
                container.setStyleSheet(qss)
                self._repolish(container)
        if not entire_app:
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

    def _formEditorCore(self):
        """The QDesignerFormEditorInterface - captured at plugin init, or
        reached through an open form."""
        if _form_editor_core is not None:
            return _form_editor_core
        for fw in self._formWindows():
            try:
                return fw.core()
            except Exception as e:
                logDebug(f"Designer bridge: core() via form failed: {e}")
        return None

    def _formWindowManager(self):
        core = self._formEditorCore()
        if core is None:
            logDebug("Designer bridge: form editor core unavailable")
            return None
        try:
            return core.formWindowManager()
        except Exception as e:
            logDebug(f"Designer bridge: formWindowManager() failed: {e}")
            return None

    def _noteInWorkspace(self, path):
        try:
            from Custom_Widgets.DesignerTools import WorkspaceDock
            WorkspaceDock.noteFile(path)
        except Exception:
            pass

    @staticmethod
    def _uiHasCustomWidgets(path):
        """True if the .ui declares any <customwidget> (a promoted/plugin
        widget). Best-effort: on any read/parse error, assume True so we take
        the safe (non-drop) open route."""
        try:
            import xml.etree.ElementTree as _ET
            root = _ET.parse(path).getroot()
            return root.find(".//customwidgets/customwidget") is not None
        except Exception:
            return True

    def _openViaDropEvent(self, path):
        """Open a .ui VISIBLY in THIS Designer instance by synthesizing a
        file-drop onto its main window - the one route into the workbench
        that PySide6 doesn't wall off (QDesignerWorkbench handles url drops
        exactly like File > Open). Returns True when Designer accepted it.

        Refuses forms that contain custom widgets: building a custom (Python)
        widget while a synthetic drop is delivered crashes shiboken's wrapper
        allocation, whether the drop is sent synchronously or from a clean
        event-loop tick (both confirmed via faulthandler -
        WidgetFactory::createCustomWidget -> SbkObject_tp_new -> SIGSEGV).
        Returning False routes such forms to the captured-core open path
        (_openViaCore), which builds the form through Designer's normal
        form-window API and is safe."""
        if self._uiHasCustomWidgets(os.path.abspath(path)):
            return False
        try:
            from qtpy.QtCore import QMimeData, QUrl, QPointF, QPoint
            from qtpy.QtGui import QDropEvent, QDragEnterEvent
            from qtpy.QtWidgets import QMainWindow, QMdiArea

            app = QApplication.instance()
            targets = []
            for window in (app.topLevelWidgets() if app else []):
                if isinstance(window, QMainWindow) and window.isVisible():
                    for mdi in window.findChildren(QMdiArea):
                        targets.append(mdi.viewport())
                        targets.append(mdi)
                    targets.append(window)
            mime = QMimeData()
            mime.setUrls([QUrl.fromLocalFile(path)])
            for target in targets:
                if not target.acceptDrops():
                    continue
                center = QPoint(target.width() // 2, target.height() // 2)
                enter = QDragEnterEvent(center, Qt.CopyAction, mime,
                                        Qt.LeftButton, Qt.NoModifier)
                QApplication.sendEvent(target, enter)
                if not enter.isAccepted():
                    continue
                drop = QDropEvent(QPointF(center), Qt.CopyAction, mime,
                                  Qt.LeftButton, Qt.NoModifier)
                QApplication.sendEvent(target, drop)
                if drop.isAccepted():
                    return True
        except Exception as e:
            logDebug(f"Designer bridge: drop-open failed: {e}")
        return False

    def openFiles(self, files, new_process=False):
        """Open .ui files.

        Default (new_process=False): first try a synthetic file-drop onto
        this Designer's window - that opens the form VISIBLY in the current
        instance (editable, tabbed into the workspace). If Designer refuses
        the drop, fall back to creating the form invisibly via the captured
        core (fully bridge-manipulable: getObjectInfos, getUiCode,
        setWidgetProperty, getScreenShot).

        new_process=True: force a separate Designer window instead."""
        opened = []
        pending = []
        manager = None if new_process else self._formWindowManager()

        for path in files:
            path = os.path.abspath(str(path).replace("\\", "/"))
            if not os.path.exists(path):
                continue
            # Dedupe: if this file is already open, reveal that form window
            # instead of opening a second copy (a duplicate form window makes
            # getScreenShot/setWidgetProperty ambiguous about which instance).
            if not new_process:
                existing = self._findOpenForm(path)
                if existing is not None:
                    self._revealFormWindow(existing)
                    self._noteInWorkspace(path)
                    opened.append(os.path.basename(path))
                    continue
            if not new_process and self._openViaDropEvent(path):
                self._noteInWorkspace(path)
                opened.append(os.path.basename(path))
                continue
            if manager is not None:
                try:
                    with open(path, encoding="utf-8") as f:
                        contents = f.read()
                    fw = manager.createFormWindow()
                    fw.setFileName(path)
                    fw.setContents(contents)
                    manager.addFormWindow(fw)
                    # Ask Designer's workbench to surface the form: make it the
                    # active form window (this is what File>Open does after
                    # reading a form), then reveal its MDI subwindow if the
                    # workbench wrapped it in one. Guarded - Designer internals
                    # are fragile.
                    self._revealFormWindow(fw)
                    self._noteInWorkspace(path)
                    opened.append(os.path.basename(path))
                    continue
                except Exception as e:
                    logDebug(f"Designer bridge: in-process open failed: {e}")
            pending.append(path)

        if pending:
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
            suffix = " (new window)" if new_process else " (new process - in-process open unavailable)"
            opened.extend(os.path.basename(p) + suffix for p in pending)
        return opened

    def _findOpenForm(self, path):
        """Return an already-open form window whose file is ``path`` (absolute
        match), or None. Used to dedupe openFiles."""
        target = os.path.normpath(os.path.abspath(path))
        for fw in self._formWindows():
            try:
                fn = fw.fileName()
            except Exception:
                continue
            if fn and os.path.normpath(os.path.abspath(fn)) == target:
                return fw
        return None

    def _activeForm(self):
        """The form window the workbench considers active (what the user/bridge
        last focused), if it has a main container - else None. This is what
        'current' screenshots and property edits should target."""
        try:
            manager = self._formWindowManager()
            if manager is not None:
                fw = manager.activeFormWindow()
                if fw is not None and fw.mainContainer() is not None:
                    return fw
        except Exception as e:
            logDebug(f"Designer bridge: activeFormWindow failed: {e}")
        return None

    def _revealFormWindow(self, fw):
        """Best-effort: make a captured-core form window visible in the
        Designer workbench. Tries setActiveFormWindow, then reveals the
        QMdiSubWindow the workbench may have created to host it."""
        manager = self._formWindowManager()
        try:
            if manager is not None:
                manager.setActiveFormWindow(fw)
        except Exception as e:
            logDebug(f"Designer bridge: setActiveFormWindow failed: {e}")
        try:
            from qtpy.QtWidgets import QMdiSubWindow, QMdiArea, QMainWindow
            app = QApplication.instance()
            widgets = app.allWidgets() if app else []

            # 1) If the workbench already wrapped fw in a QMdiSubWindow, reveal it.
            for sub in widgets:
                if not isinstance(sub, QMdiSubWindow):
                    continue
                w = sub.widget()
                if w is fw or (w is not None and fw in w.findChildren(type(fw))):
                    sub.show(); sub.raise_()
                    if sub.mdiArea() is not None:
                        sub.mdiArea().setActiveSubWindow(sub)
                    return True

            # 2) It didn't (PySide6 doesn't drive the workbench for forms added
            #    via the API). Host the already-built form in the main MDI area
            #    ourselves. fw's widgets are already constructed, so this only
            #    reparents - it does NOT rebuild custom widgets, so it avoids
            #    the shiboken create-crash.
            mdis = [w for w in widgets if isinstance(w, QMdiArea) and w.isVisible()]
            # Prefer the MDI area inside the largest visible main window (the
            # Designer workbench canvas).
            mdis.sort(key=lambda m: m.width() * m.height(), reverse=True)
            if mdis:
                sub = mdis[0].addSubWindow(fw)
                fw.show()
                # Size the subwindow to the form so small forms show their
                # content, not just a title bar. Fall back to a sane default.
                hint = fw.sizeHint()
                w = max(fw.width(), hint.width(), 320)
                h = max(fw.height(), hint.height(), 240)
                sub.resize(w + 16, h + 40)
                sub.show(); sub.raise_()
                mdis[0].setActiveSubWindow(sub)
                return True
        except Exception as e:
            logDebug(f"Designer bridge: reveal MDI subwindow failed: {e}")
        return False

    def _newForm(self, name, template=None, folder=None, open_after=True):
        """Create a new .ui form from a template and (optionally) open it in
        THIS Designer instance. Headless equivalent of the Workspace
        'New Form...' action, so the MCP can create forms autonomously.

        template: a key of DesignerTools.FORM_TEMPLATES (None -> the first,
        the blank icons-prewired form). folder: destination dir (defaults to
        the workspace folder, else <project>/ui). Returns the created path."""
        try:
            from Custom_Widgets.DesignerTools import FORM_TEMPLATES, WorkspaceDock
            from Custom_Widgets.Project import projectRoot

            base = "".join(c if c.isalnum() or c in "-_" else "_"
                           for c in str(name).strip()) or "untitled"

            tmpl_key = template if template is not None else next(iter(FORM_TEMPLATES))
            if tmpl_key not in FORM_TEMPLATES:
                return {"error": f"unknown template {template!r}; choose one of "
                                 f"{list(FORM_TEMPLATES)}"}
            builder = FORM_TEMPLATES[tmpl_key]

            project_dir = os.path.abspath(projectRoot())
            dock = WorkspaceDock._instance
            if folder:
                dest_folder = os.path.abspath(folder)
            elif dock is not None:
                dest_folder = dock._folder
            else:
                ui_dir = os.path.join(project_dir, "ui")
                dest_folder = ui_dir if os.path.isdir(ui_dir) else project_dir

            if builder is None:
                # Blank icons-prewired form -> ProjectMaker writes <cwd>/ui/<base>.ui
                from Custom_Widgets.ProjectMaker import create_ui_file
                prev = os.getcwd()
                os.chdir(project_dir)
                try:
                    create_ui_file(base)
                finally:
                    os.chdir(prev)
                path = os.path.join(project_dir, "ui", base + ".ui")
            else:
                os.makedirs(dest_folder, exist_ok=True)
                path = os.path.join(dest_folder, base + ".ui")
                if os.path.exists(path):
                    return {"error": f"{path} already exists"}
                with open(path, "w", encoding="utf-8") as f:
                    f.write(builder(base))

            if not os.path.exists(path):
                return {"error": f"form was not created at {path}"}

            if dock is not None:
                try:
                    WorkspaceDock.noteFile(path)
                    dock.refresh()
                except Exception as e:
                    logDebug(f"Designer bridge: workspace refresh failed: {e}")

            opened = self.openFiles([path], new_process=False) if open_after else []
            return {"result": "ok", "path": path, "template": tmpl_key,
                    "opened": opened}
        except Exception as e:
            return {"error": f"newForm failed: {e}"}

    def _ensureIconResources(self, xml):
        """If a form uses icons (<iconset>) but doesn't link the project's
        icons resource, inject the <resources> include so icons resolve -
        every form that requires icons must be linked to Qss/icons/_icons.qrc
        (mirrors what `Custom_Widgets --new-ui` sets up)."""
        if "<iconset" not in xml or "_icons.qrc" in xml:
            return xml
        qrc = os.path.join(projectRoot(), "Qss", "icons", "_icons.qrc")
        if not os.path.isfile(qrc):
            return xml
        include = '<include location="../Qss/icons/_icons.qrc"/>'
        if "<resources/>" in xml:
            return xml.replace("<resources/>",
                               f"<resources>{include}</resources>", 1)
        if "<resources>" in xml:
            return xml.replace("<resources>", f"<resources>{include}", 1)
        return xml.replace("</ui>", f" <resources>{include}</resources>\n</ui>", 1)

    def _resolveFormForXml(self, message):
        """Pick the form to (re)build: an explicit file (basename or path), else
        the active form, else the single open form."""
        target = message.get("file")
        if target:
            fw = self._findOpenForm(target)
            if fw is not None:
                return fw
            base = os.path.basename(str(target))
            for fw in self._formWindows():
                if os.path.basename(fw.fileName() or "") == base:
                    return fw
        active = self._activeForm()
        if active is not None:
            return active
        forms = [fw for fw in self._formWindows() if fw.mainContainer() is not None]
        return forms[0] if len(forms) == 1 else None

    def _setFormXml(self, message):
        """Replace a form's .ui XML contents LIVE in Designer (fw.setContents),
        so an agent can build/edit a form over MCP and watch it re-render.
        Targets the active form (or one named by `file`); optionally saves it to
        disk. Marks the form dirty otherwise (persist with save=true)."""
        xml = str(message.get("xml", ""))
        if "<ui" not in xml:
            return {"error": "xml must be a Qt Designer .ui document (<ui …>)"}
        xml = self._ensureIconResources(xml)
        fw = self._resolveFormForXml(message)
        if fw is None:
            return {"error": "no target form open (open/create one, or pass file)"}
        try:
            fw.setContents(xml)
        except Exception as e:
            return {"error": f"setContents failed: {e}"}
        saved = None
        if bool(message.get("save", False)):
            saved = self._saveForm(fw, xml)
        try:
            self._repolish(fw.mainContainer())
        except Exception:
            pass
        return {"result": "ok", "file": fw.fileName(), "saved": saved}

    def _newFormXml(self, message):
        """Create a NEW form from .ui XML and open it live in Designer. Writes
        <ui>/<name>.ui when save (default True), so it can be compiled + run."""
        xml = str(message.get("xml", ""))
        if "<ui" not in xml:
            return {"error": "xml must be a Qt Designer .ui document (<ui …>)"}
        xml = self._ensureIconResources(xml)
        name = "".join(c if c.isalnum() or c in "-_" else "_"
                       for c in str(message.get("name", "untitled")).strip()) or "untitled"
        project_dir = os.path.abspath(projectRoot())
        folder = message.get("folder")
        if folder:
            dest = os.path.abspath(folder)
        else:
            ui_dir = os.path.join(project_dir, "ui")
            dest = ui_dir if os.path.isdir(ui_dir) else project_dir
        path = os.path.join(dest, name + ".ui")
        if bool(message.get("save", True)):
            try:
                os.makedirs(dest, exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(xml)
            except Exception as e:
                return {"error": f"could not write {path}: {e}"}
            opened = self.openFiles([path], new_process=False)
            self._noteInWorkspace(path)
            return {"result": "ok", "path": path, "opened": opened}
        # In-memory only: create a form window and set its contents.
        manager = self._formWindowManager()
        if manager is None:
            return {"error": "no form window manager"}
        try:
            fw = manager.createFormWindow()
            fw.setContents(xml)
            manager.addFormWindow(fw)
            self._revealFormWindow(fw)
            return {"result": "ok", "path": None, "opened": [name]}
        except Exception as e:
            return {"error": f"newFormXml failed: {e}"}

    def _saveForm(self, fw, xml=None):
        """Persist a form window to its .ui file. Falls back to writing the
        provided xml if the form has a filename but Designer's save is
        unavailable."""
        path = fw.fileName()
        if not path:
            return None
        try:
            content = xml if xml is not None else self._uiCode("xml").get("result", "")
            if content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                try:
                    fw.setDirty(False)
                except Exception:
                    pass
                return path
        except Exception as e:
            logDebug(f"Designer bridge: save form failed: {e}")
        return None

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
        # 'current' -> the ACTIVE form window (what the user is looking at),
        # not merely the first one found (they can differ when several forms
        # are open).
        current = self._activeForm() or forms[0]
        return {"result": grab_b64(current.mainContainer()), "file": current.fileName()}


    def _runApp(self, action, lines=100):
        """Drive the project's app via the Designer Run controller
        (DesignerTools.RunController): start/stop/restart/status/logs."""
        try:
            from Custom_Widgets.DesignerTools import RunController
            runner = RunController._instance
            if runner is None:
                return {"error": "run controller not installed "
                                 "(Designer tools missing?)"}
            if action == "start":
                ok = runner.start()
                return {"result": "ok" if ok else "failed",
                        "running": runner.isRunning(),
                        "script": runner.script()}
            if action == "stop":
                runner.stop()
                return {"result": "ok", "running": runner.isRunning()}
            if action == "restart":
                runner.restart()
                return {"result": "ok", "running": runner.isRunning()}
            if action == "status":
                return {"result": {"running": runner.isRunning(),
                                   "script": runner.script(),
                                   "available": runner.available()}}
            if action == "logs":
                return {"result": runner.appLogs(lines)}
            return {"error": f"unknown app action '{action}'"}
        except Exception as e:
            return {"error": f"runApp failed: {e}"}

    def _qssWindow(self, message):
        """Drive the standalone QSS / Theme editor window.

        The editor is a floating top-level window (not a dock), so the dock,
        screenshot and action helpers can't reach it. This exposes it over the
        bridge so the whole QSS / theming surface is MCP-verifiable. Actions:

          open       - show + raise the window (openFloating)
          close      - hide the window
          status     - {open, paintEntireDesigner, currentFile, objectName}
          paint      - set the 'Paint entire Designer' toggle to message['enabled']
          screenshot - base64 PNG of the window (grab it as-is; 'open' first)
        """
        action = str(message.get("action", "status"))
        try:
            from Custom_Widgets.DesignerTools import _tools
        except Exception as e:
            return {"error": f"Designer tools unavailable: {e}"}
        win = _tools.get("qss")
        if win is None:
            return {"error": "QSS editor window not installed "
                             "(Designer tools missing?)"}
        try:
            if action == "open":
                win.openFloating()
                return {"result": "ok", "open": win.isVisible()}
            if action == "load":
                path = str(message.get("file", ""))
                if not path:
                    return {"error": "load requires 'file'"}
                win.showFile(path, content=message.get("content"))
                return {"result": "ok", "file": path, "open": win.isVisible()}
            if action == "close":
                win.close()
                return {"result": "ok", "open": win.isVisible()}
            if action == "paint":
                enabled = bool(message.get("enabled", True))
                act = win._repaintDesigner
                if act.isChecked() != enabled:
                    act.setChecked(enabled)  # fires _applyPaintDesigner once
                else:
                    win._applyPaintDesigner()  # force (re)apply; state unchanged
                return {"result": "ok",
                        "paintEntireDesigner": act.isChecked()}
            if action == "status":
                return {"result": {
                    "open": win.isVisible(),
                    "paintEntireDesigner": win._repaintDesigner.isChecked(),
                    "currentFile": os.path.basename(getattr(win, "_path", "") or ""),
                    "objectName": win.objectName(),
                }}
            if action == "screenshot":
                import base64
                from qtpy.QtCore import QBuffer, QIODevice
                pixmap = win.grab()
                buffer = QBuffer()
                buffer.open(QIODevice.WriteOnly)
                pixmap.save(buffer, "PNG")
                return {"result": base64.b64encode(
                    bytes(buffer.data())).decode("ascii")}
            return {"error": f"unknown qss action '{action}'"}
        except Exception as e:
            return {"error": f"qssWindow '{action}' failed: {e}"}

    ####################################################################
    ## WINDOW MANAGEMENT (panes, dialogs, actions, properties)
    ####################################################################
    _DOCK_AREAS = {"left": 1, "right": 2, "top": 4, "bottom": 8}

    def _designerWindow(self, message):
        """Move / raise the Designer main window, or list screens. Same actions
        as the app's window control: move{x,y}, geometry{x,y,width,height},
        toPrimary, maximize, normal, raise, screens. Handy when a multi-monitor
        compositor parks Designer on an off-screen output."""
        action = str(message.get("action", "raise"))
        app = QApplication.instance()
        if action == "screens":
            return {"result": [
                {"name": s.name(),
                 "geometry": [s.geometry().x(), s.geometry().y(),
                              s.geometry().width(), s.geometry().height()],
                 "primary": s is app.primaryScreen()} for s in (app.screens() if app else [])]}
        win = self._mainWindow()
        if win is None:
            return {"error": "no designer main window"}
        try:
            if action == "move":
                win.showNormal()
                win.move(int(message.get("x", 0)), int(message.get("y", 0)))
            elif action == "geometry":
                win.showNormal()
                win.setGeometry(int(message.get("x", 0)), int(message.get("y", 0)),
                                int(message.get("width", 1100)),
                                int(message.get("height", 750)))
            elif action == "toPrimary":
                g = app.primaryScreen().geometry()
                win.showNormal()
                win.move(g.x() + 40, g.y() + 40)
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
            return {"error": f"designerWindow failed: {e}"}

    def _mainWindows(self):
        """All visible QMainWindows - in Designer's multi-window mode every
        tool window is one, so dock/action lookups aggregate over them."""
        from qtpy.QtWidgets import QMainWindow
        app = QApplication.instance()
        return [w for w in (app.topLevelWidgets() if app else [])
                if isinstance(w, QMainWindow) and w.isVisible()]

    def _mainWindow(self):
        windows = self._mainWindows()
        for window in windows:  # prefer the one carrying the menu bar
            menu_bar = window.menuBar()
            if menu_bar is not None and menu_bar.actions():
                return window
        return windows[0] if windows else None

    def _getDocks(self):
        """Every dock pane of the Designer main window."""
        from qtpy.QtWidgets import QDockWidget
        area_names = {v: k for k, v in self._DOCK_AREAS.items()}
        docks = []
        for window in self._mainWindows():
            for dock in window.findChildren(QDockWidget):
                area = window.dockWidgetArea(dock)
                docks.append({
                    "objectName": dock.objectName(),
                    "title": dock.windowTitle(),
                    "visible": dock.isVisible(),
                    "floating": dock.isFloating(),
                    "area": area_names.get(getattr(area, "value", area), "none"),
                })
        return docks

    def _setDock(self, message):
        """Arrange a dock pane: visibility, area (left/right/top/bottom),
        floating. Matched by objectName or title substring."""
        from qtpy.QtCore import Qt
        from qtpy.QtWidgets import QDockWidget
        needle = str(message.get("dock", "")).lower()
        pairs = [(window, dock) for window in self._mainWindows()
                 for dock in window.findChildren(QDockWidget)]
        if not pairs:
            return {"error": "no main window"}
        for window, dock in pairs:
            if needle in dock.objectName().lower() or needle in dock.windowTitle().lower():
                if "visible" in message:
                    dock.setVisible(bool(message["visible"]))
                if "floating" in message:
                    dock.setFloating(bool(message["floating"]))
                area = str(message.get("area", ""))
                if area in self._DOCK_AREAS:
                    window.addDockWidget(Qt.DockWidgetArea(self._DOCK_AREAS[area]), dock)
                if message.get("raise", False):
                    dock.raise_()
                return {"result": "ok", "dock": dock.objectName() or dock.windowTitle()}
        return {"error": f"no dock matching '{needle}' "
                         f"(see getDocks for available panes)"}

    def _openDialogs(self):
        from qtpy.QtWidgets import QDialog
        app = QApplication.instance()
        return [w for w in (app.topLevelWidgets() if app else [])
                if isinstance(w, QDialog) and w.isVisible()]

    def _getDialogs(self):
        """Visible dialogs / popups / prompts / error boxes: class, title,
        message text and available buttons."""
        from qtpy.QtWidgets import QLabel, QPushButton
        dialogs = []
        for dialog in self._openDialogs():
            labels = [l.text() for l in dialog.findChildren(QLabel) if l.text()]
            buttons = [b.text().replace("&", "") for b in dialog.findChildren(QPushButton)]
            dialogs.append({
                "class": dialog.metaObject().className(),
                "title": dialog.windowTitle(),
                "text": " | ".join(labels)[:300],
                "buttons": buttons,
                "modal": dialog.isModal(),
            })
        return dialogs

    def _dismissDialog(self, match, button=""):
        """Close a dialog matched by title/class substring (empty match =
        first open dialog). With `button`, click that button instead of
        rejecting - e.g. answer a save prompt with 'Don't Save'."""
        from qtpy.QtWidgets import QPushButton
        match = match.lower()
        for dialog in self._openDialogs():
            haystack = (dialog.windowTitle() + " " + dialog.metaObject().className()).lower()
            if match and match not in haystack:
                continue
            if button:
                for btn in dialog.findChildren(QPushButton):
                    if button.lower() in btn.text().replace("&", "").lower():
                        btn.click()
                        return {"result": "ok", "clicked": btn.text().replace("&", ""),
                                "dialog": dialog.windowTitle()}
                return {"error": f"dialog '{dialog.windowTitle()}' has no "
                                 f"button matching '{button}'"}
            dialog.reject()
            return {"result": "ok", "dismissed": dialog.windowTitle()
                                                 or dialog.metaObject().className()}
        return {"error": "no matching open dialog (see getDialogs)"}

    def _allActions(self):
        """Actions from every top-level widget - Designer's action tree is
        not necessarily parented to a visible QMainWindow (multi-window
        mode, native menu bars)."""
        from qtpy.QtGui import QAction as _QAction  # Qt6
        app = QApplication.instance()
        if app is None:
            return []
        actions = []
        seen = set()
        for root in app.topLevelWidgets():
            found = list(root.findChildren(_QAction))
            try:
                found += list(root.actions())
            except Exception:
                pass
            for action in found:
                try:  # Designer deletes actions dynamically - skip dead wrappers
                    if id(action) not in seen and action.text():
                        seen.add(id(action))
                        actions.append(action)
                except RuntimeError:
                    continue
        return actions

    def _getActions(self):
        """Every action of Designer's menus/toolbars - trigger any of them
        with triggerAction (Save, Save All, Preview, Close, ...)."""
        infos = []
        for a in self._allActions():
            try:
                infos.append({"objectName": a.objectName(),
                              "text": a.text().replace("&", ""),
                              "shortcut": a.shortcut().toString(),
                              "enabled": a.isEnabled()})
            except RuntimeError:
                continue
        return infos

    def _triggerAction(self, wanted):
        wanted_l = wanted.lower()
        for action in self._allActions():
            try:
                matched = wanted_l in (action.objectName().lower(),
                                       action.text().replace("&", "").lower())
                if not matched:
                    continue
                if not action.isEnabled():
                    return {"error": f"action '{wanted}' is currently disabled"}
                action.trigger()
                return {"result": "ok", "triggered": action.text().replace("&", "")}
            except RuntimeError:
                continue
        return {"error": f"no action matching '{wanted}' (see getActions)"}

    def _setWidgetProperty(self, widget_name, prop, value):
        """Set a property on a widget of the ACTIVE form through the form
        cursor - goes through Designer's undo stack and marks the form
        dirty, exactly like a manual edit (persisted on save)."""
        if prop == "styleSheet":
            return {"error": "Project rule: no inline styles in ui files. "
                             "Persist styles in Qss/scss/defaultStyle.scss "
                             "(or a file it imports) using an objectName "
                             "selector like #" + (widget_name or "widgetName") +
                             " { ... }. For an ephemeral preview use the "
                             "setStyleSheet method instead."}
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
        container = fw.mainContainer()
        if container is None:
            return {"error": "form has no main container"}
        target = container if container.objectName() == widget_name else None
        if target is None:
            for child in container.findChildren(QWidget):
                if child.objectName() == widget_name:
                    target = child
                    break
        if target is None:
            return {"error": f"no widget named '{widget_name}' in the active "
                             f"form (see getObjectInfos)"}
        try:
            cursor = fw.cursor()
            cursor.setWidgetProperty(target, prop, value)
            return {"result": "ok", "widget": widget_name, "property": prop}
        except Exception as e:
            return {"error": f"setWidgetProperty failed: {e}"}


class DesignerBridgeClient:
    """Used by the running app. Fire-and-forget; every call fails silently
    when Designer (or the bridge) is not running."""

    def __init__(self, project_dir=None, timeout_ms=200):
        self._name = bridgeServerName(project_dir)
        self._timeout = timeout_ms

    def send(self, message):
        """Deliver one message. Returns True when the bridge accepted it."""
        try:
            token = read_token(self._name)
            if not token:
                return False
            sock = QLocalSocket()
            sock.connectToServer(self._name)
            if not sock.waitForConnected(self._timeout):
                return False
            sock.write(auth_line(token))
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
            token = read_token(self._name)
            if not token:
                return None
            sock = QLocalSocket()
            sock.connectToServer(self._name)
            if not sock.waitForConnected(self._timeout):
                return None
            sock.write(auth_line(token))
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
