"""Every widget Qt Designer registers must survive Designer's construction.

Designer instantiates a dropped widget as `Class(parent)` — a single
positional argument and nothing else. Two 2.3.3 regressions shipped because
nothing exercised that contract:

- QCustomSpinner / QFlowProgressBar have a first positional arg that is NOT a
  parent (`lineWidth` / `strDetailList`), so `Class(parent)` silently bound the
  parent to that slot, left the widget unparented, and crashed in paintEvent.
  They were unregistered and waived in the tiering manifest (2026-08-16).
- QCustomEmbeddedWindow raised `ValueError: empty range in randint(0, -N)` on
  any form smaller than its minimum size.

These tests parse `Plugins/register.py` (importing it would require a running
Designer) and reproduce both halves of the contract: construct + paint, and
palette-icon resolution. The construct test would have caught all three bugs.
"""
import importlib
import os
import re

import pytest

from qtpy.QtWidgets import QWidget

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(REPO, "Custom_Widgets", "Plugins", "register.py")


def _registrations():
    """(module, class) pairs for every `registerCustomWidget(<Class>, ...)` in
    register.py, resolved through the same-file `from Custom_Widgets... import`
    statements."""
    src = open(REGISTER, encoding="utf-8").read()
    module_of = dict((m.group(2), m.group(1))
                     for m in re.finditer(r'from (Custom_Widgets\.[\w.]+) import (\w+)', src))
    seen = []
    for m in re.finditer(r'registerCustomWidget\(\s*(\w+),', src):
        name = m.group(1)
        if name in module_of and (module_of[name], name) not in seen:
            seen.append((module_of[name], name))
    return seen


REGISTRATIONS = _registrations()


def _registration_icon_args():
    """icon= argument text for every registration, e.g. "_iconFor(QCustomBadge)"."""
    src = open(REGISTER, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'registerCustomWidget\(\s*(\w+),([^)]*)\)', src, re.S):
        name = m.group(1)
        icon = re.search(r'icon=(\S+)', m.group(2))
        out.setdefault(name, []).append(icon.group(1) if icon else None)
    return out


def test_designer_register_file_is_parsed():
    assert len(REGISTRATIONS) >= 90, "parsing register.py found too few widgets"


def _resolve_class(module, name):
    """The registered class, immune to import-order shadowing.

    register.py imports the charts from the package
    (`from Custom_Widgets.QCustomCharts import QCustomLineChart`), so `module`
    may be the package. Importing a chart submodule earlier in the suite then
    shadows the package's re-exported class with the submodule object
    (Python binds submodules as package attributes), so getattr can return a
    module. Resolve through the same-named submodule as a fallback.
    """
    mod = importlib.import_module(module)
    cls = getattr(mod, name, None)
    if cls is None or not isinstance(cls, type):
        cls = getattr(importlib.import_module("%s.%s" % (module, name)), name)
    return cls


@pytest.mark.parametrize("module,name", REGISTRATIONS)
def test_designer_can_construct_with_a_positional_parent(qapp, module, name):
    """Designer's `createWidget(parent)` contract: Class(parent) must build a
    parented, paintable widget."""
    try:
        cls = _resolve_class(module, name)
    except (ImportError, ModuleNotFoundError) as e:
        pytest.skip("optional dependency missing: %s" % e)
    parent = QWidget()
    try:
        widget = cls(parent)
    except ImportError as e:
        pytest.skip("ctor needs an optional dependency: %s" % e)
    assert isinstance(widget, QWidget), "%s built a %s" % (name, type(widget).__name__)
    # The exact 2.3.3 regression: the parent was bound to a non-parent ctor
    # slot, leaving the widget unparented.
    assert widget.parent() is parent, (
        "%s did not adopt the positional parent (parent=%s)"
        % (name, type(widget.parent()).__name__))
    # Paint must not blow up (the spinner/flow crash only appeared at paint
    # time, not construction).
    widget.grab()
    parent.deleteLater()


@pytest.mark.parametrize("module,name", REGISTRATIONS)
def test_designer_palette_icon_resolves(qapp, module, name):
    """The icon passed to Designer must be `_iconFor(cls)` (absolute + existing),
    never a bare relative path Designer resolves against its own cwd."""
    icon_args = _registration_icon_args().get(name)
    assert icon_args, "registration for %s not parsed" % name
    for icon in icon_args:
        if icon is None:
            continue
        assert icon.startswith("_iconFor("), (
            "%s passes a raw icon path to Designer: %s" % (name, icon))
    try:
        cls = _resolve_class(module, name)
    except (ImportError, ModuleNotFoundError):
        pytest.skip("module not importable")
    declared = getattr(cls, "WIDGET_ICON", "") or ""
    if not declared:
        return  # no icon declared; Designer draws its placeholder
    from Custom_Widgets._resources import packageDir
    if not os.path.isabs(declared):
        declared = os.path.normpath(os.path.join(packageDir(), declared))
    assert os.path.isfile(declared), (
        "%s WIDGET_ICON does not resolve: %s" % (name, declared))
