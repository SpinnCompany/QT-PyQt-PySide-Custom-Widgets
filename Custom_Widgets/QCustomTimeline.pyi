# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomTimeline(QWidget):
    lineColor: Any
    dotColor: Any
    def __init__(self, parent = ...) -> None: ...
    def addItem(self, title, time = ..., description = ..., color = ...): ...
    def setItems(self, items) -> None: ...
    def count(self): ...
