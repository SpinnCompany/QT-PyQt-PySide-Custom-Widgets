"""ReleaseStarterApp — smoke-check the compiled form.

Deliberately does NOT import the app's main.py: since the forms-pipeline
rebuild (2026-08-01) importing it runs setProjectRoot + the identity/boot
globals, which would leak process-wide state into the suite (it broke the
icon-generation tests once). Full app boot is covered by the headless
survey runner in a subprocess; here we assert the compiled artifact.
"""
import os
import sys

import pytest
from qtpy.QtWidgets import QMainWindow

_APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "examples", "PySide6", "ReleaseStarterApp")


@pytest.fixture()
def starter_path():
    if not os.path.isdir(os.path.join(_APP, "src")):
        pytest.skip("ReleaseStarterApp example not built")
    # Every example ships a package literally named "src" — evict any cached
    # one (e.g. GlassHome's from an earlier test) so ours resolves fresh,
    # and clean up after ourselves for the same reason.
    def _evict():
        for name in [m for m in sys.modules if m == "src" or m.startswith("src.")]:
            del sys.modules[name]
    _evict()
    sys.path.insert(0, _APP)
    yield
    sys.path.remove(_APP)
    _evict()


def test_release_starter_form_compiles_and_titles(qapp, starter_path):
    from src.ui_MainWindow import Ui_MainWindow

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    assert window.windowTitle() == "Custom Widgets Release Starter"
