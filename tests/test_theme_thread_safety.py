"""Regression tests for the QSettings deadlock in theme icon generation.

QSettings serializes access through a lock file. If a worker thread reads or
writes QSettings while the main thread is also using it, both threads can
block forever inside QSettings C code. applyCompiledSass therefore resolves
every settings-derived value on the main thread and passes plain values to
the icon worker; the worker-side chain (compileSassTheme -> generateNewIcons
and generateDesignerIcons) must never construct a QSettings object.
"""
import os
import subprocess
import sys
import threading

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def resolve_worker_kwargs(theme):
    """Resolve the settings-derived values on the main thread, exactly like
    applyCompiledSass does before starting the icon worker."""
    theme_info = theme.getCurrentThemeInfo()
    icons_color, icons_force = theme._resolveIconsColor(theme_info)
    return {
        "themeInfo": theme_info,
        "iconsColor": icons_color,
        "iconsForce": icons_force,
    }


def test_worker_path_never_touches_qsettings(theme, project_dir, monkeypatch):
    """Deterministic guard: run the full worker-side call chain on a non-main
    thread and record every QSettings construction in the module."""
    # The package __init__ rebinds the QCustomTheme attribute to the class, so
    # "import Custom_Widgets.QCustomTheme as qct" would grab the class here.
    import Custom_Widgets.QCustomTheme  # noqa: F401 - ensure module is loaded
    import Custom_Widgets.Log
    qct = sys.modules["Custom_Widgets.QCustomTheme"]
    log_mod = sys.modules["Custom_Widgets.Log"]

    offending = []
    real_qsettings = qct.QSettings

    class RecordingQSettings(real_qsettings):
        def __init__(self, *args, **kwargs):
            if threading.current_thread() is not threading.main_thread():
                offending.append(threading.current_thread().name)
            super().__init__(*args, **kwargs)

    monkeypatch.setattr(qct, "QSettings", RecordingQSettings)
    # The logging helpers read a QSettings-backed flag on every call and run
    # on worker threads too - they must use their cache, never QSettings
    monkeypatch.setattr(log_mod, "QSettings", RecordingQSettings)

    kwargs = resolve_worker_kwargs(theme)

    def worker():
        theme.compileSassTheme(None, **kwargs)

    t = threading.Thread(target=worker, name="icons-worker")
    t.start()
    t.join(timeout=120)

    assert not t.is_alive(), "icon worker did not finish (possible QSettings deadlock)"
    assert offending == [], f"QSettings constructed on worker thread(s): {offending}"


STRESS_SCRIPT = r"""
import os, sys, threading, time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_API", "pyside6")
sys.path.insert(0, sys.argv[1])

from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QApplication

app = QApplication([])
app.setOrganizationName("CustomWidgetsTests")
app.setApplicationName("CustomWidgetsTests")

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.WidgetsWorker import Worker

theme = QCustomTheme()

# Main thread resolves the settings-derived values, like applyCompiledSass.
theme_info = theme.getCurrentThemeInfo()
icons_color, icons_force = theme._resolveIconsColor(theme_info)

deadline = time.monotonic() + 3.0
done = threading.Event()

def spin(progress_callback):
    while time.monotonic() < deadline:
        theme.compileSassTheme(None, themeInfo=theme_info,
                               iconsColor=icons_color,
                               iconsForce=icons_force)
    done.set()

pool = QThreadPool()
pool.start(Worker(spin))

# Main thread hammers QSettings-backed calls while the worker generates icons.
while time.monotonic() < deadline:
    theme.getCurrentThemeInfo()

assert done.wait(timeout=60), "worker never finished"
assert pool.waitForDone(60000), "thread pool never drained"
print("OK")
"""


def test_main_thread_settings_access_during_icon_generation(project_dir):
    """The reported repro: the main thread calls getCurrentThemeInfo in a
    tight loop while the worker runs the icon-generation chain. Runs in a
    subprocess so a deadlock fails the test instead of hanging the suite."""
    result = subprocess.run(
        [sys.executable, "-c", STRESS_SCRIPT, REPO_ROOT],
        capture_output=True,
        text=True,
        timeout=90,
        cwd=str(project_dir),
    )
    assert result.returncode == 0, (
        f"stress subprocess failed (possible deadlock)\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "OK" in result.stdout
