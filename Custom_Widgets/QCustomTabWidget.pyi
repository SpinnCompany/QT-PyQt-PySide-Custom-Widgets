# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget
from typing import Any, ClassVar


class QCustomTabWidget(QTabWidget):
    addTabRequested: ClassVar[Signal]
    closableTabs: bool
    showAddButton: bool
    tabStyle: str
    sizeVariant: str
    def __init__(self, parent = ...) -> None: ...
