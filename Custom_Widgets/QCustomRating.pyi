# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomRating(QWidget):
    valueChanged: ClassVar[Signal]
    maximum: int
    value: int
    readOnly: bool
    def __init__(self, parent = ..., maximum = ...) -> None: ...
    def mouseMoveEvent(self, e): ...
    def mousePressEvent(self, e): ...
    def leaveEvent(self, e): ...
    def setValue(self, v) -> None: ...
