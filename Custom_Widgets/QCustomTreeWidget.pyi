# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTreeWidget
from typing import Any, ClassVar


class QCustomTreeWidget(QTreeWidget):
    variant: str
    sizeVariant: str
    def __init__(self, parent = ...) -> None: ...
    def setItems(self, items, headers = ...) -> None: ...
