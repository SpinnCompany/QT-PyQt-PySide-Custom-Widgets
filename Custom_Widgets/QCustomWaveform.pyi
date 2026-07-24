# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomWaveform(QWidget):
    valuePushed: ClassVar[Signal]
    mode: str
    valuesCsv: str
    capacity: int
    barColor: str
    barColor2: str
    barWidth: float
    barGap: float
    cornerRadius: int
    mirror: bool
    lineColor: str
    lineWidth: float
    showGrid: bool
    gridColor: str
    fillArea: bool
    glow: bool
    glowStrength: float
    animated: bool
    def __init__(self, parent = ..., values = ..., mode = ...) -> None: ...
    def setValues(self, values) -> None: ...
    def push(self, value): ...
    def clear(self): ...
    def setMode(self, mode) -> None: ...
    def values(self): ...
    def showEvent(self, e): ...
    def hideEvent(self, e): ...
    def setAnimated(self, on) -> None: ...
    def paintEvent(self, e): ...
