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


def test_theme_change_completion_runs_on_the_main_thread(project_dir):
    """The `finished` connection that drives _themeChangeComplete must deliver
    on the GUI thread. It used to be a plain lambda (DirectConnection), so the
    completion ran on the icon worker's thread and mutated Qt GUI state (pixmap
    cache, stylesheet, full repolish walk, QLocalSocket I/O) off-thread.

    This exercises the REAL applyCompiledSass wiring in a subprocess: a full
    icon worker runs, and the completion wrapper records the thread it landed
    on. Runs in a subprocess because a revert to DirectConnection would crash
    or behave badly inside the pytest process itself.
    """
    result = subprocess.run(
        [sys.executable, "-c", AFFINITY_SCRIPT, REPO_ROOT],
        capture_output=True,
        text=True,
        timeout=180,
        cwd=str(project_dir),
    )
    assert result.returncode == 0, (
        f"affinity subprocess failed\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "OK" in result.stdout


def test_superseded_theme_generation_is_skipped(theme, qapp):
    """A completion for an old generation (a rapid toggle started a newer
    worker) must not re-apply the GUI."""
    theme._icon_generation = 5
    fired = []
    theme.onThemeChangeComplete.connect(lambda: fired.append(1))
    theme._themeChangeComplete(4)  # stale -> early return, no side effects
    assert fired == []
    theme._themeChangeComplete(5)  # current generation -> full completion
    assert len(fired) == 1


def test_get_theme_variable_value_is_memoized(theme, qapp, monkeypatch):
    """getThemeVariableValue ran createVariables (colour maths, an _variables.scss
    write, a stat) on EVERY lookup, and loadJsonStyle looks up several variables
    per widget. Only the first lookup after a theme change may recompute.

    createVariables is stubbed so the test does not depend on whatever theme the
    suite-wide singleton happens to be pointing at (an earlier test's QSettings
    THEME can resolve to a theme with empty colours and make the real
    createVariables raise)."""
    calls = []

    def fake_create():
        calls.append(1)
        theme._variable_mapping = {"COLOR_BACKGROUND_1": "white"}

    monkeypatch.setattr(theme, "createVariables", fake_create)
    theme._variables_cache_key = None
    v1 = theme.getThemeVariableValue("COLOR_BACKGROUND_1")
    v2 = theme.getThemeVariableValue("COLOR_BACKGROUND_1")
    assert v1 == v2 == "white"
    assert len(calls) == 1, "createVariables recomputed per lookup: %s" % calls


AFFINITY_SCRIPT = r"""
import os, sys, threading, time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_API", "pyside6")
sys.path.insert(0, sys.argv[1])

from qtpy.QtWidgets import QApplication

app = QApplication([])
app.setOrganizationName("CustomWidgetsTests")
app.setApplicationName("CustomWidgetsTests")

from Custom_Widgets.QCustomTheme import QCustomTheme

theme = QCustomTheme()
main_tid = threading.get_ident()
# A bare test project has no json-styles to seed `themesRead`; the flag just
# lets applyCompiledSass past its early return. Set it directly.
theme.themesRead = True

# Record which thread the completion actually lands on, then let the real
# completion body run (guarded to the current generation).
recorded = []
orig = theme._themeChangeComplete

def recording(gen=None):
    recorded.append((gen, threading.get_ident()))

theme._themeChangeComplete = recording

# This is the exact code path applyCompiledSass(generateIcons=True) takes:
# a Worker on the shared pool whose `finished` drives the completion.
theme.applyCompiledSass(generateIcons=True, paintEntireApp=False)

deadline = time.monotonic() + 120
while time.monotonic() < deadline and not recorded:
    app.processEvents()
    time.sleep(0.02)

theme.customWidgetsThreadpool.waitForDone(30000)

assert recorded, "theme-change completion was never delivered"
gen, tid = recorded[0]
assert tid == main_tid, (
    "completion %r ran on a worker thread (main=%r got=%r)"
    % (gen, main_tid, tid))
print("OK")
"""
