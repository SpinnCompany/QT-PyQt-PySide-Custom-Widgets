import os
import sys

# Must be set before any Qt import so the suite runs headless (CI, ssh, etc.)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# Default binding for the suite. Override with e.g. `QT_API=pyqt5 pytest`.
os.environ.setdefault("QT_API", "pyside6")

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)


@pytest.fixture(scope="session")
def qapp():
    from qtpy.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    app.setOrganizationName("CustomWidgetsTests")
    app.setApplicationName("CustomWidgetsTests")
    return app


@pytest.fixture(scope="session")
def theme(qapp):
    """The QCustomTheme singleton. Session-scoped because the class only ever
    creates one instance per process."""
    from Custom_Widgets.QCustomTheme import QCustomTheme

    return QCustomTheme()


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    """A fresh working directory, since icon generation writes to cwd."""
    monkeypatch.chdir(tmp_path)
    return tmp_path
