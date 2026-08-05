"""WidgetShowcase — smoke-check the compiled form.

Deliberately does NOT import the app's main.py: since the forms-pipeline
rebuild (2026-08-01) importing it runs setProjectRoot + boot globals, which
leaks process-wide state into the suite (see AGENTS.md). Full app boot is
covered by the headless survey runner in a subprocess; here we assert the
compiled artifact.
"""
import os
import sys

import pytest
from qtpy.QtWidgets import QMainWindow, QTabWidget

_APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "examples", "PySide6", "WidgetShowcase")


@pytest.fixture()
def showcase_path():
    if not os.path.isdir(os.path.join(_APP, "src")):
        pytest.skip("WidgetShowcase example not built")

    def _evict():
        for name in [m for m in sys.modules if m == "src" or m.startswith("src.")]:
            del sys.modules[name]
    _evict()
    sys.path.insert(0, _APP)
    yield
    sys.path.remove(_APP)
    _evict()


def test_widget_showcase_form_compiles_and_titles(qapp, showcase_path):
    from src.ui_MainWindow import Ui_MainWindow

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    assert window.windowTitle() == "Custom Widgets Showcase — Complete Library"


def test_widget_showcase_tabs(qapp, showcase_path):
    from src.ui_MainWindow import Ui_MainWindow

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    tabs = window.findChild(QTabWidget, "tabs")
    assert tabs is not None
    assert tabs.count() == 4
