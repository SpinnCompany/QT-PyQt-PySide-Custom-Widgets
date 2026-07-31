########################################################################
## DEV SERVER - `Custom_Widgets --dev`
##
## One command, everything hot - the web-style dev loop for Qt apps:
##
##   Custom_Widgets --dev              # runs ./main.py under supervision
##   Custom_Widgets --dev app.py       # or any entry script
##
## The supervisor runs the app as a subprocess and watches the project:
##   .ui change    -> regenerate src/ui_*.py (+ metadata json) -> restart
##   .py change    -> restart the app
##   .scss/.json   -> nothing here: the app itself live-reloads styles via
##                    QSsFileMonitor when LiveCompileQss is enabled - the
##                    supervisor just logs the event (and restarts if the
##                    app opted out of live compile? no - keep it simple).
##
## The child process gets CUSTOM_WIDGETS_PROJECT_ROOT so the app resolves
## the project root correctly no matter where the dev command ran from.
## Polling (0.5s) rather than QFileSystemWatcher: no QApplication needed
## in the supervisor, identical behavior on every platform.
########################################################################
import os
import signal
import subprocess
import sys
import time

from Custom_Widgets.Log import *
from Custom_Widgets.Project import projectRoot

POLL_INTERVAL = 0.5

# Directories never worth scanning
_SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules",
              "generated-files", ".claude"}

# What we watch, and what a change means
_RESTART_SUFFIXES = (".py",)
_CONVERT_SUFFIXES = (".ui",)
_STYLE_SUFFIXES = (".scss", ".json")


def _scan(root):
    """path -> mtime snapshot of everything we care about."""
    snapshot = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
        for name in filenames:
            if name.endswith(_RESTART_SUFFIXES + _CONVERT_SUFFIXES
                             + _STYLE_SUFFIXES):
                path = os.path.join(dirpath, name)
                try:
                    snapshot[path] = os.stat(path).st_mtime
                except OSError:
                    pass
    return snapshot


def _under(path, folder):
    try:
        return os.path.abspath(path).startswith(os.path.abspath(folder) + os.sep)
    except Exception:
        return False


def _classify(changed, generated_dir):
    """Split changed paths into buckets.

    - ui_files    : *.ui (regenerate the compiled .py)
    - source_py   : hand-written *.py OUTSIDE the generated dir (main.py, app
                    modules) -> full restart
    - gen_py      : generated *.py INSIDE the generated dir (src/ui_*.py) ->
                    the running app's component loaders hot-reload these in
                    place; never a restart trigger on their own
    - style_files : *.scss / *.json -> the app live-reloads
    """
    ui_files = [p for p in changed if p.endswith(_CONVERT_SUFFIXES)]
    style_files = [p for p in changed if p.endswith(_STYLE_SUFFIXES)]
    gen_py = [p for p in changed if p.endswith(_RESTART_SUFFIXES)
              and _under(p, generated_dir)]
    source_py = [p for p in changed if p.endswith(_RESTART_SUFFIXES)
                 and not _under(p, generated_dir)]
    return ui_files, source_py, style_files, gen_py


class DevServer:
    def __init__(self, script=None, project_dir=None, qt_binding="PySide6",
                 src_output_dir="src"):
        self.root = os.path.abspath(project_dir or projectRoot())
        self.script = os.path.abspath(script or os.path.join(self.root, "main.py"))
        self.qt_binding = qt_binding
        self.src_output_dir = src_output_dir
        self.child = None

    # ------------------------------------------------------------------
    def start_app(self):
        env = os.environ.copy()
        env["CUSTOM_WIDGETS_PROJECT_ROOT"] = self.root
        env.setdefault("QT_API", self.qt_binding.lower())
        # Let Designer / the MCP observe and navigate this running app (the
        # in-app control server starts only when this flag is set).
        env["CUSTOM_WIDGETS_APP_CONTROL"] = "1"
        logInfo(f"dev: starting {os.path.relpath(self.script, self.root)}")
        self.child = subprocess.Popen([sys.executable, self.script],
                                      cwd=self.root, env=env)

    def stop_app(self):
        if self.child is None or self.child.poll() is not None:
            return
        self.child.terminate()
        try:
            self.child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.child.kill()
            self.child.wait()

    def restart_app(self, reason):
        logInfo(f"dev: restarting app ({reason})")
        self.stop_app()
        self.start_app()

    def _entryForms(self):
        """Base names of .ui forms whose compiled ``ui_<base>`` module is
        imported by the entry script. These build the main window / top-level
        UI, whose widgets the app's own code holds references to - rebuilding
        them in place would orphan those connections, so a change to one of
        them triggers a full restart. Every OTHER form is assumed to be loaded
        via a component loader and hot-reloads in place.
        """
        try:
            import re
            text = open(self.script, encoding="utf-8").read()
            # If the app opts into main-window hot reload, it rebuilds every
            # form in place - nothing needs a restart.
            if "enable_hot_reload" in text:
                return set()
            # Only IMPORTED ui_<name> modules count as entry forms - matching a
            # bare string would false-positive on a component's filePath (e.g.
            # container.filePath = "src/ui_card.py"), which is hot-reloadable.
            return set(re.findall(
                r"(?:from|import)\s+[\w.]*\bui_([A-Za-z0-9_]+)", text))
        except Exception:
            return set()

    def convert_ui(self, ui_file):
        """Regenerate src/ui_*.py + metadata for one changed .ui file."""
        try:
            from Custom_Widgets.FileMonitor import start_ui_conversion
            start_ui_conversion(ui_file, qt_binding=self.qt_binding,
                                src_output_dir=self.src_output_dir)
        except Exception as e:
            logException(e, message=f"dev: conversion failed for {ui_file}")

    # ------------------------------------------------------------------
    def run(self):
        if not os.path.isfile(self.script):
            logError(f"dev: entry script not found: {self.script}")
            logError("dev: pass one explicitly: Custom_Widgets --dev path/to/main.py")
            return 1

        logInfo(" " + "=" * 60)
        logInfo(" CUSTOM WIDGETS DEV SERVER")
        logInfo(f" project : {self.root}")
        logInfo(f" app     : {self.script}")
        logInfo(" watching: *.ui (regenerate -> app hot-reloads component "
                "forms)  main-window/*.py (restart)  *.scss/*.json (live)")
        logInfo(" " + "=" * 60)

        generated_dir = os.path.abspath(os.path.join(self.root, self.src_output_dir))
        entry_forms = self._entryForms()

        # A supervisor killed with SIGTERM (e.g. Designer's Stop button via
        # QProcess.terminate) must still tear down the child app - route it
        # through KeyboardInterrupt so the finally block runs.
        def _on_sigterm(signum, frame):
            raise KeyboardInterrupt

        try:
            signal.signal(signal.SIGTERM, _on_sigterm)
        except (ValueError, OSError):
            pass  # non-main thread or unsupported platform

        snapshot = _scan(self.root)
        self.start_app()
        try:
            while True:
                time.sleep(POLL_INTERVAL)

                # surface app exit (crash or user closed the window)
                if self.child is not None and self.child.poll() is not None:
                    code = self.child.returncode
                    if code not in (0, -signal.SIGTERM):
                        logWarning(f"dev: app exited with code {code} - "
                                   "waiting for a file change to relaunch")
                    else:
                        logInfo("dev: app closed - waiting for a file change "
                                "to relaunch (Ctrl+C to quit)")
                    self.child = None

                current = _scan(self.root)
                changed = [p for p, m in current.items()
                           if snapshot.get(p) != m]
                changed += [p for p in snapshot if p not in current]  # deleted
                snapshot = current
                if not changed:
                    continue

                ui_files, source_py, style_files, gen_py = _classify(
                    changed, generated_dir)

                for path in style_files:
                    logInfo(f"dev: style changed: "
                            f"{os.path.relpath(path, self.root)} "
                            "(live-reloaded by the app)")

                # Regenerate the compiled .py for every changed .ui. A form
                # imported by the entry script builds the main window and needs
                # a restart; any other form hot-reloads in the running app.
                restart_ui = []
                for path in ui_files:
                    base = os.path.splitext(os.path.basename(path))[0]
                    is_entry = base in entry_forms
                    logInfo(f"dev: ui changed: {os.path.relpath(path, self.root)}"
                            + (" -> restart (main-window form)" if is_entry
                               else " -> app hot-reloads component form"))
                    self.convert_ui(path)
                    if is_entry:
                        restart_ui.append(path)

                for path in gen_py:
                    logDebug(f"dev: generated {os.path.relpath(path, self.root)} "
                             "(hot-reload target)")

                # Hand-written source or an entry (main-window) form -> restart.
                # main.py itself changing also re-reads the entry-form list.
                if source_py:
                    entry_forms = self._entryForms()
                restart_paths = source_py + restart_ui
                if restart_paths:
                    reason = ", ".join(os.path.relpath(p, self.root)
                                       for p in restart_paths[:3])
                    if self.child is None:
                        self.start_app()
                    else:
                        self.restart_app(reason)
                    snapshot = _scan(self.root)  # swallow regenerated files
                elif self.child is None and (ui_files or gen_py):
                    # App was closed and a form changed - bring it back fresh.
                    self.start_app()
                    snapshot = _scan(self.root)
        except KeyboardInterrupt:
            logInfo("dev: shutting down")
        finally:
            self.stop_app()
        return 0


def run_dev(script=None, project_dir=None, qt_binding="PySide6",
            src_output_dir="src"):
    return DevServer(script=script, project_dir=project_dir,
                     qt_binding=qt_binding,
                     src_output_dir=src_output_dir).run()
