"""Screen-reader surface for the custom-painted widgets.

Qt hands QAbstractButton / QSlider subclasses a correct role and checked state
for free, but the interactive widgets in this library mostly subclass plain
QWidget and paint their own chrome, so a screen reader announces them as an
anonymous pane. Each widget sets an accessible name (its text, tooltip, or a
sensible default) so assistive tech says something meaningful.

Qt 6.4+ dropped QWidget::setAccessibleRole entirely, so an explicit role is
best-effort: applied only when the running binding still supports it (Qt 5 /
older Qt 6). The name and description always apply.
"""
try:
    from qtpy.QtGui import QAccessible  # Qt 6
except ImportError:  # pragma: no cover - Qt 5
    from qtpy.QtWidgets import QAccessible  # type: ignore


def set_accessibility(widget, role=None, name="", description=""):
    """Assign role + optional name/description. Each part is guarded separately:
    a missing API on one binding must not stop the parts that exist, and a11y
    metadata must never be able to break a widget that otherwise works."""
    if role is not None and hasattr(widget, "setAccessibleRole"):
        try:
            widget.setAccessibleRole(role)
        except Exception:
            pass
    if name:
        try:
            widget.setAccessibleName(name)
        except Exception:
            pass
    if description:
        try:
            widget.setAccessibleDescription(description)
        except Exception:
            pass
    return widget