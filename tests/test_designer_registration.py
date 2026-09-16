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
    statements AND the loop-variable batches (e.g. `for _ctr, _cont in
    ((QCustomTabWidget, True), (QCustomAccordion, False))` registers the class
    under the loop variable, and `for _pw in (QCustomPagination,
    QCustomSegmentedControl):` under `_pw`)."""
    import ast
    src = open(REGISTER, encoding="utf-8").read()
    tree = ast.parse(src)
    module_of = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module \
                and node.module.startswith("Custom_Widgets"):
            for alias in node.names:
                module_of[alias.asname or alias.name] = node.module
    loop_bindings = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.For) or not isinstance(node.iter, ast.Tuple):
            continue
        targets = node.target.elts if isinstance(node.target, ast.Tuple) else [node.target]
        vars_ = [t.id for t in targets if isinstance(t, ast.Name)]
        for elt in node.iter.elts:
            if isinstance(elt, ast.Tuple) and elt.elts and isinstance(elt.elts[0], ast.Name):
                for v in vars_:
                    loop_bindings.setdefault(v, set()).add(elt.elts[0].id)
            elif isinstance(elt, ast.Name):
                for v in vars_:
                    loop_bindings.setdefault(v, set()).add(elt.id)
    seen = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if not (isinstance(f, ast.Attribute) and f.attr == "registerCustomWidget"
                and node.args and isinstance(node.args[0], ast.Name)):
            continue
        name = node.args[0].id
        for cls in loop_bindings.get(name, {name}):
            if cls in module_of and (module_of[cls], cls) not in seen:
                seen.append((module_of[cls], cls))
    return seen


REGISTRATIONS = _registrations()


def _registration_icon_args():
    """icon= argument text per REGISTERED CLASS, e.g. {"QCustomBadge":
    ["_iconFor(QCustomBadge)"]}. Registrations may pass a loop variable
    (`registerCustomWidget(_nw, ..., icon=...)`) that batches several classes,
    so the icon arg is attributed to every class the variable binds."""
    import ast
    src = open(REGISTER, encoding="utf-8").read()
    tree = ast.parse(src)
    loop_bindings = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.For) or not isinstance(node.iter, ast.Tuple):
            continue
        targets = node.target.elts if isinstance(node.target, ast.Tuple) else [node.target]
        vars_ = [t.id for t in targets if isinstance(t, ast.Name)]
        for elt in node.iter.elts:
            if isinstance(elt, ast.Tuple) and elt.elts and isinstance(elt.elts[0], ast.Name):
                for v in vars_:
                    loop_bindings.setdefault(v, set()).add(elt.elts[0].id)
            elif isinstance(elt, ast.Name):
                for v in vars_:
                    loop_bindings.setdefault(v, set()).add(elt.id)
    out = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if not (isinstance(f, ast.Attribute) and f.attr == "registerCustomWidget"
                and node.args and isinstance(node.args[0], ast.Name)):
            continue
        icon = None
        for kw in node.keywords:
            if kw.arg == "icon":
                icon = ast.get_source_segment(src, kw.value)
        names = loop_bindings.get(node.args[0].id, {node.args[0].id})
        for n in names:
            out.setdefault(n, []).append(icon)
    return out


def test_designer_register_file_is_parsed():
    assert len(REGISTRATIONS) >= 90, "parsing register.py found too few widgets"


def _class_source_declares(module, name, attr):
    """True if the registered class's source file assigns `attr` (AST-only, no
    import/instantiation). Resolves the file by scanning Custom_Widgets for a
    class with `name` — widgets live in `widgets/<group>/` since the 2026-07-31
    regrouping, so the flat `module` path may not match the file on disk."""
    import ast

    widget_root = os.path.join(REPO, "Custom_Widgets")
    for root, _dirs, files in os.walk(widget_root):
        if "__pycache__" in root:
            continue
        for fn in files:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            try:
                tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
            except (OSError, SyntaxError):
                continue
            for node in tree.body:
                if not isinstance(node, ast.ClassDef) or node.name != name:
                    continue
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign):
                        for tgt in stmt.targets:
                            if isinstance(tgt, ast.Name) and tgt.id == attr:
                                return True
    return False


def _is_pro_stub(name):
    """True when the free package only carries a Pro placeholder for `name`.

    register.py still names the Pro widgets — the registration is guarded and
    lights up once the Pro wheel is installed — so the parse-based
    REGISTRATIONS list includes them either way. Their source here is a stub
    with no Designer metadata, which is correct rather than a rule violation.
    """
    import os
    for base, _dirs, files in os.walk(os.path.join(REPO, "Custom_Widgets")):
        if "__pycache__" in base:
            continue
        if name + ".py" in files:
            with open(os.path.join(base, name + ".py"), encoding="utf-8") as fh:
                return "_PRO_MODULE" in fh.read()
    return False


@pytest.mark.parametrize("module,name", REGISTRATIONS)
def test_every_registered_widget_declares_designer_custom_props(module, name):
    """Rule #11: every widget Designer registers declares DESIGNER_CUSTOM_PROPS
    (an explicit {name, kind, group} spec) so the Custom Properties dock lists
    its custom properties with typed editors. A widget may declare an EMPTY
    list when its config is delivered via methods / Qt-native properties, but
    the attribute must exist — otherwise the dock (and the right-click task
    menu) silently degrades for that widget."""
    if _is_pro_stub(name):
        pytest.skip("%s ships in Custom Widgets Pro; the free package keeps a "
                    "stub so Designer .ui files still resolve" % name)
    assert _class_source_declares(module, name, "DESIGNER_CUSTOM_PROPS"), (
        "%s is registered in Designer but does not declare "
        "DESIGNER_CUSTOM_PROPS (Custom Properties dock contract, rule #11)" % name)


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
