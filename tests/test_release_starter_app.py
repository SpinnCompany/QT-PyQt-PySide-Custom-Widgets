from qtpy.QtWidgets import QApplication


def test_release_starter_app_imports(qapp):
    from examples.PySide6.ReleaseStarterApp.main import ReleaseStarterWindow

    window = ReleaseStarterWindow()
    assert window.windowTitle() == "Custom Widgets Release Starter"
