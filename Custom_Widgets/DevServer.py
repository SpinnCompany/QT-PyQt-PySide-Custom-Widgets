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


def _classify(changed):
    """Split changed paths into (ui_files, restart_needed, style_files)."""
    ui_files = [p for p in changed if p.endswith(_CONVERT_SUFFIXES)]
    py_files = [p for p in changed if p.endswith(_RESTART_SUFFIXES)]
    style_files = [p for p in changed if p.endswith(_STYLE_SUFFIXES)]
    return ui_files, py_files, style_files


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
        logInfo(" watching: *.ui (regenerate+restart)  *.py (restart)  "
                "*.scss/*.json (app live-reloads)")
        logInfo(" " + "=" * 60)

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

                ui_files, py_files, style_files = _classify(changed)
                for path in style_files:
                    logInfo(f"dev: style changed: "
                            f"{os.path.relpath(path, self.root)} "
                            "(live-reloaded by the app)")
                for path in ui_files:
                    logInfo(f"dev: ui changed: {os.path.relpath(path, self.root)}")
                    self.convert_ui(path)
                # a .ui conversion rewrites src/*.py, which the NEXT scan
                # would catch - restart once now instead
                if ui_files or py_files:
                    reason = ", ".join(os.path.relpath(p, self.root)
                                       for p in (ui_files + py_files)[:3])
                    if self.child is None:
                        self.start_app()
                    else:
                        self.restart_app(reason)
                    # swallow the regenerated-file changes from this action
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
