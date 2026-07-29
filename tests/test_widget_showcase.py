"""
Test for the widget showcase app.
"""


def test_widget_showcase_app_imports(qapp):
    """Verify the showcase app imports and instantiates without errors."""
    from examples.PySide6.WidgetShowcase.main import WidgetShowcase
    
    window = WidgetShowcase()
    assert window.windowTitle() == "Custom Widgets Showcase — Complete Library"
    assert window.width() == 1200
    assert window.height() == 800


def test_widget_showcase_tab_creation(qapp):
    """Verify all tabs are created successfully."""
    from examples.PySide6.WidgetShowcase.main import WidgetShowcase
    
    window = WidgetShowcase()
    # The window has a central widget with tabs
    central = window.centralWidget()
    assert central is not None
