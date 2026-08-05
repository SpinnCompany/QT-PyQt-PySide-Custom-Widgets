# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomBreadcrumbs(QWidget):
    itemClicked: ClassVar[Signal]
    def __init__(self, parent = ..., separator = ...) -> None: ...
    def setItems(self, items) -> None: ...
    def items(self): ...
