"""Plugins/register.py must run to its last line and register every free
widget, with or without Custom Widgets Pro installed.

test_designer_registration.py checks each registration in isolation by
parsing register.py; it never executes the file, so it cannot see control
flow that stops the script partway. That gap let 2.6.0 ship a Designer
palette of 14 widgets to every free user (GitHub issue #2). The tier split
turned 22 widgets into Pro stubs whose attribute access raises ImportError
without Pro, and register.py mapped each one to None. The first of them,
QCustomRichTextEditor, sat in a loop whose error handler formatted
`_iw.__name__`: that raised AttributeError from inside its own `except`,
nothing above it caught the error, and Designer kept only what had
registered by then. Two batch `try` blocks also dropped six chat and two
media widgets that are free, because a Pro import earlier in the same block
failed first.

These tests execute register.py the way PySide6's Designer loader does - in
a fresh interpreter, as a script with SEPARATE globals and locals dicts -
against a recording stand-in for QPyDesignerCustomWidgetCollection: once
with Pro absent, once with a fake Pro installed. The fresh interpreter
matters: importing a chart submodule first, as other tests do, rebinds the
package attribute register.py imports the chart class from.
"""
import builtins
import glob
import json
import logging
import os
import re
import subprocess
import sys
import types

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(REPO, "Custom_Widgets", "Plugins", "register.py")
_RESULT = "REGISTER-RESULT:"


def _proStubs():
    """{widget name: Pro module path} for every Pro stub in the free package."""
    stubs = {}
    pattern = os.path.join(REPO, "Custom_Widgets", "widgets", "**", "*.py")
    for path in glob.glob(pattern, recursive=True):
        with open(path, encoding="utf-8") as fh:
            match = re.search(r'^_PRO_MODULE = "([\w.]+)"$', fh.read(), re.M)
        if match:
            stubs[os.path.basename(path)[:-3]] = match.group(1)
    return stubs


PRO = _proStubs()


class _Collection:
    """Records what register.py hands to QPyDesignerCustomWidgetCollection."""

    def __init__(self):
        self.widgets = {}
        self.plugins = []

    def registerCustomWidget(self, cls, **kwargs):
        self.widgets[cls.__name__] = kwargs

    def addCustomWidget(self, plugin):
        self.plugins.append(plugin)


class _Records(logging.Handler):
    """Keeps every record that reaches the root logger."""

    def __init__(self):
        super().__init__(logging.DEBUG)
        self.records = []

    def emit(self, record):
        self.records.append(record)


def _fakeProModule(path, name):
    module = types.ModuleType(path)
    setattr(module, name, type(name, (), {
        "WIDGET_MODULE": "Custom_Widgets." + name,
        "WIDGET_TOOLTIP": name,
        "WIDGET_DOM_XML": '<ui language="c++"><widget class="%s" name="w"/></ui>' % name,
        "WIDGET_ICON": "",
    }))
    return module


def _childMain(path, proInstalled):
    """Runs in the child interpreter: execute register.py, print the outcome."""
    import faulthandler
    import importlib

    import PySide6
    from qtpy.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])  # noqa: F841 (kept alive)

    # Pro present as fakes at exactly the paths the stubs forward to, or
    # absent even on a machine that has it installed.
    if proInstalled:
        for name, modPath in PRO.items():
            sys.modules[modPath] = _fakeProModule(modPath, name)
    else:
        sys.modules["custom_widgets_pro"] = None

    # PySide6 creates its classes lazily, so they are not in the real
    # module's __dict__ until first use: forward instead of copying.
    collection = _Collection()
    real = importlib.import_module("PySide6.QtDesigner")
    designer = types.ModuleType("PySide6.QtDesigner")
    designer.__getattr__ = lambda name: getattr(real, name)
    designer.QPyDesignerCustomWidgetCollection = collection
    sys.modules["PySide6.QtDesigner"] = designer
    PySide6.QtDesigner = designer

    # setupLogger would replace the root handlers this run reads from, and
    # the script enables faulthandler on a log file; neither is under test.
    importlib.import_module("Custom_Widgets.Log").setupLogger = lambda *a, **k: None
    faulthandler.enable = lambda *a, **k: None

    records = _Records()
    root = logging.getLogger()
    root.addHandler(records)
    root.setLevel(logging.INFO)
    with open(path, encoding="utf-8") as fh:
        code = compile(fh.read(), path, "exec")
    exec(code, {"__builtins__": builtins, "__name__": "__main__", "__file__": path}, {})

    print(_RESULT + json.dumps({
        "widgets": list(collection.widgets),
        "plugins": len(collection.plugins),
        "info": [r.getMessage() for r in records.records if r.levelno == logging.INFO],
        "errors": [r.getMessage() for r in records.records if r.levelno >= logging.ERROR],
    }))


def _runRegister(home, proInstalled):
    """Execute register.py in a fresh interpreter, as Designer does."""
    env = dict(os.environ, HOME=str(home), XDG_DATA_HOME=str(home),
               QT_QPA_PLATFORM="offscreen", QT_API="pyside6",
               PYTHONPATH=os.pathsep.join(
                   p for p in (REPO, os.environ.get("PYTHONPATH")) if p))
    proc = subprocess.run(
        [sys.executable, os.path.abspath(__file__), REGISTER,
         "pro" if proInstalled else "free"],
        cwd=REPO, env=env, capture_output=True, text=True, timeout=600)
    line = next((l for l in proc.stdout.splitlines() if l.startswith(_RESULT)), None)
    assert line, "register.py did not run to its end:\n%s" % (
        proc.stderr[-4000:] or proc.stdout[-4000:])
    return json.loads(line[len(_RESULT):])


def test_pro_stubs_are_discovered():
    assert len(PRO) >= 20, "found only %d Pro stubs; the scan is broken" % len(PRO)


def test_register_runs_to_the_end_without_pro(tmp_path):
    run = _runRegister(tmp_path, proInstalled=False)
    registered = set(run["widgets"])
    assert not registered & set(PRO), (
        "Pro widgets registered without Pro: %s" % sorted(registered & set(PRO)))
    assert len(registered) >= 100, (
        "only %d widgets registered; register.py stopped early" % len(registered))
    assert not run["errors"], "registration errors without Pro: %s" % run["errors"]
    summary = [m for m in run["info"] if all(name in m for name in PRO)]
    assert len(summary) == 1, (
        "absent Pro widgets should be reported in exactly one info line, got %r"
        % summary)


def test_free_palette_is_the_full_palette_minus_pro(tmp_path):
    full = _runRegister(tmp_path / "pro", proInstalled=True)
    free = _runRegister(tmp_path / "free", proInstalled=False)
    assert not full["errors"], "registration errors with Pro: %s" % full["errors"]
    assert set(PRO) <= set(full["widgets"]), (
        "Pro widgets missing with Pro installed: %s"
        % sorted(set(PRO) - set(full["widgets"])))
    lost = sorted(set(full["widgets"]) - set(PRO) - set(free["widgets"]))
    assert not lost, "free widgets that only register when Pro is installed: %s" % lost


if __name__ == "__main__":
    _childMain(sys.argv[1], sys.argv[2] == "pro")
