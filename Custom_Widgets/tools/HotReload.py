########################################################################
## MAIN-WINDOW HOT RELOAD
##
## enable_hot_reload(window, build) rebuilds a top-level window's UI in
## place whenever its compiled Ui_ module(s) change - no process restart.
##
## Unlike a component (a leaf form with no external references), the main
## window's widgets are wired to app code (signal connections). Rebuilding
## them would orphan those connections, so the app supplies a `build()`
## callable that re-runs setupUi AND re-connects signals; the helper calls
## it on every change. Window geometry is preserved across the rebuild.
##
##     class MainWindow(QMainWindow):
##         def build(self):
##             from src.ui_mainwindow import Ui_MainWindow   # inside build()
##             self.ui = Ui_MainWindow(); self.ui.setupUi(self)
##             self.ui.button.clicked.connect(self.on_click)
##
##         def __init__(self):
##             super().__init__()
##             enable_hot_reload(self, self.build)
########################################################################
import importlib
import os
import sys

from qtpy.QtCore import QFileSystemWatcher, QTimer

from Custom_Widgets.Project import projectRoot
from Custom_Widgets.Log import logInfo, logDebug, logError, logException


def enable_hot_reload(window, build, watch=None, src_dir=None):
    """Rebuild ``window``'s UI in place when its compiled Ui_ module(s) change.

    window : the top-level widget being (re)built by ``build``.
    build  : zero-arg callable that constructs the UI (setupUi + signal
             connections). Called once now, then again after each change to a
             watched compiled UI module. IMPORTANT: import the Ui_ class INSIDE
             ``build`` (e.g. ``from src.ui_mainwindow import Ui_MainWindow``)
             so the reloaded module is picked up.
    watch  : optional explicit list of .py files to watch. Default: the
             ui_*.py modules ``build`` imported (discovered after the first
             build), else every ui_*.py under ``src_dir``.
    src_dir: generated-source dir (default ``<projectRoot>/src``).

    Returns the QFileSystemWatcher (also stored on the window).
    """
    build()  # initial construction

    src_dir = os.path.abspath(src_dir or os.path.join(projectRoot(), "src"))
    files = [os.path.abspath(f) for f in watch] if watch \
        else _loaded_ui_modules(src_dir) or _ui_modules_on_disk(src_dir)

    watcher = QFileSystemWatcher(window)
    state = {"timer": None, "pending": set()}

    def arm():
        try:
            current = watcher.files()
            if current:
                watcher.removePaths(current)
            existing = [f for f in files if os.path.isfile(f)]
            if existing:
                watcher.addPaths(existing)
        except Exception as e:
            logDebug(f"Hot reload: watch arm failed: {e}")

    def on_changed(path):
        state["pending"].add(path)
        if state["timer"] is None:
            timer = QTimer(window)
            timer.setSingleShot(True)
            timer.timeout.connect(do_reload)
            state["timer"] = timer
        # Debounce - editors/converters save atomically (write + rename).
        state["timer"].start(150)

    def do_reload():
        changed = list(state["pending"])
        state["pending"].clear()
        for path in changed:
            _reload_module_for_file(path)
        try:
            geometry = window.saveGeometry()
            build()
            window.restoreGeometry(geometry)
            logInfo(f"Hot reload: rebuilt {type(window).__name__} "
                    f"({', '.join(os.path.basename(p) for p in changed)})")
        except Exception as e:
            # A partial write (mid-conversion) can raise - the next change
            # fires again once the file is whole.
            logError(f"Hot reload: rebuild failed: {e}")
            logException(e)
        arm()  # re-arm - atomic saves drop the watched path

    watcher.fileChanged.connect(on_changed)
    arm()

    # Keep references alive for the window's lifetime.
    window._hot_reload_watcher = watcher
    window._hot_reload_state = state
    return watcher


def _loaded_ui_modules(src_dir):
    """Files of already-imported ui_*.py modules living under src_dir."""
    found = []
    for mod in list(sys.modules.values()):
        path = getattr(mod, "__file__", None)
        if not path:
            continue
        try:
            path = os.path.abspath(path)
        except Exception:
            continue
        base = os.path.basename(path)
        if base.startswith("ui_") and base.endswith(".py") \
                and path.startswith(src_dir + os.sep):
            found.append(path)
    return found


def _ui_modules_on_disk(src_dir):
    try:
        return [os.path.join(src_dir, f) for f in os.listdir(src_dir)
                if f.startswith("ui_") and f.endswith(".py")]
    except Exception:
        return []


def _reload_module_for_file(path):
    """Reload the already-imported module whose __file__ is ``path`` so the
    next ``from ... import`` inside build() sees the fresh definitions."""
    target = os.path.abspath(path)
    for name, mod in list(sys.modules.items()):
        mod_file = getattr(mod, "__file__", None)
        if not mod_file:
            continue
        try:
            if os.path.abspath(mod_file) == target:
                importlib.reload(mod)
                return name
        except Exception as e:
            logDebug(f"Hot reload: reload of {name} failed: {e}")
    return None
