# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomNumberCounter(QWidget):
    valueChanged: ClassVar[Signal]
    finished: ClassVar[Signal]
    displayValue: Any
    value: float
    prefix: str
    suffix: str
    decimals: int
    separator: str
    duration: int
    fontScale: float
    bold: bool
    alignment: str
    textColor: str
    def __init__(self, parent = ..., value = ..., prefix = ..., suffix = ...) -> None: ...
    def setValue(self, value, animate = ...) -> None: ...
    def displayedValue(self): ...
    def isAnimating(self): ...
    def reset(self, value = ...): ...
    def formattedText(self): ...
    def sizeHint(self): ...
    def minimumSizeHint(self): ...
    def paintEvent(self, e): ...
