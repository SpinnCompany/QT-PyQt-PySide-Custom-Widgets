# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomRulerPicker(QWidget):
    valueChanged: ClassVar[Signal]
    value: float
    orientation: str
    minimum: float
    maximum: float
    step: float
    majorEvery: int
    centered: bool
    tickSpacing: float
    snap: bool
    unit: str
    showValue: bool
    tickColor: str
    majorTickColor: str
    indicatorColor: str
    labelColor: str
    valueColor: str
    def __init__(self, parent = ..., value = ..., minimum = ..., maximum = ..., step = ..., orientation = ...) -> None: ...
    def setValue(self, value) -> None: ...
    def setRange(self, minimum, maximum) -> None: ...
    def setUnit(self, unit) -> None: ...
    def paintEvent(self, e): ...
    def mousePressEvent(self, e): ...
    def mouseMoveEvent(self, e): ...
    def mouseReleaseEvent(self, e): ...
    def wheelEvent(self, e): ...
    def sizeHint(self): ...
