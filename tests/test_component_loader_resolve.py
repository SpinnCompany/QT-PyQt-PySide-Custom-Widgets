"""Loader back-compat: a QCustomComponentContainer/Loader whose filePath still
points at a raw .ui is transparently resolved to the sibling compiled
ui_<stem>.py that `Custom_Widgets --convert-ui` produces. See
QCustomComponentLoader._resolve_ui_to_compiled.
"""
import os

import pytest


class _Resolver:
    """Calls the loader's path helper without constructing the QWidget.

    ``_resolve_ui_to_compiled`` is a pure path helper that never touches
    ``self``, so we invoke it unbound - avoiding a real QCustomComponentLoader
    (which would connect to the QCustomTheme singleton and leak state into
    later tests).
    """

    def _resolve_ui_to_compiled(self, filePath):
        from Custom_Widgets.QCustomComponentLoader import QCustomComponentLoader

        return QCustomComponentLoader._resolve_ui_to_compiled(self, filePath)


@pytest.fixture
def loader():
    return _Resolver()


def _make_ui(dirpath, stem="newtest"):
    os.makedirs(dirpath, exist_ok=True)
    ui = os.path.join(dirpath, f"{stem}.ui")
    with open(ui, "w") as f:
        f.write("<ui/>")
    return ui


def test_no_compiled_module_returns_none(loader, tmp_path):
    ui = _make_ui(os.path.join(tmp_path, "ui"))
    assert loader._resolve_ui_to_compiled(ui) is None


def test_resolves_compiled_alongside_ui(loader, tmp_path):
    ui_dir = os.path.join(tmp_path, "ui")
    ui = _make_ui(ui_dir)
    compiled = os.path.join(ui_dir, "ui_newtest.py")
    with open(compiled, "w") as f:
        f.write("# compiled")
    assert loader._resolve_ui_to_compiled(ui) == os.path.normpath(compiled)


def test_resolves_compiled_in_src_sibling(loader, tmp_path):
    # ui/newtest.ui  ->  src/ui_newtest.py (the default --convert-ui layout)
    ui = _make_ui(os.path.join(tmp_path, "ui"))
    src = os.path.join(tmp_path, "src")
    os.makedirs(src)
    compiled = os.path.join(src, "ui_newtest.py")
    with open(compiled, "w") as f:
        f.write("# compiled")
    assert loader._resolve_ui_to_compiled(ui) == os.path.normpath(compiled)


def test_plain_stem_py_alongside(loader, tmp_path):
    ui_dir = os.path.join(tmp_path, "ui")
    ui = _make_ui(ui_dir)
    compiled = os.path.join(ui_dir, "newtest.py")
    with open(compiled, "w") as f:
        f.write("# compiled")
    assert loader._resolve_ui_to_compiled(ui) == os.path.normpath(compiled)
