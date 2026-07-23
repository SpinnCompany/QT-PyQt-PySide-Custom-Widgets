"""Type-check smoke test for the generated widget stubs — checked by MYPY, not
pytest (see [tool.mypy] in pyproject.toml).

It proves the `.pyi` stubs (Custom_Widgets/mcp/stubgen.py) actually drive type
resolution: inherited Qt API resolves only because each stub re-roots its base to
the concrete, typed PySide6 class, and own methods/signals/properties come from
the stub. If the generator regresses (e.g. a base stops re-rooting, or a method
signature changes), the calls below stop resolving and `mypy` fails in CI.

This file is intentionally error-free; there are no runtime assertions.
"""
from Custom_Widgets.QCustomBadge import QCustomBadge
from Custom_Widgets.QCustomSwitch import QCustomSwitch


def _exercise() -> None:
    badge = QCustomBadge("Hi")
    badge.setCount(5)                      # own method (from stub)
    badge.setStyleSheet("color: red")      # inherited QLabel -> only via typed base
    badge.setToolTip("a badge")            # inherited QWidget
    badge.move(10, 20)                     # inherited QWidget
    badge.clicked.connect(lambda: None)    # signal (from stub)

    switch = QCustomSwitch()
    switch.setEnabled(True)                # inherited QWidget
    switch.toggled.connect(lambda _: None)  # signal
    is_on: bool = switch.checked           # catalog-typed property
    del is_on
