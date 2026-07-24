# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomLiquidGauge(QWidget):
    valueChanged: ClassVar[Signal]
    value: float
    minimum: float
    maximum: float
    shape: str
    cornerRadius: int
    fillColor: str
    fillColor2: str
    backgroundColor: str
    ringColor: str
    ringWidth: int
    waveAmplitude: float
    waveLength: float
    waveSpeed: float
    animated: bool
    centerText: str
    centerSuffix: str
    centerTextColor: str
    badgeText: str
    badgeColor: str
    def __init__(self, parent = ..., value = ..., minimum = ..., maximum = ...) -> None: ...
    def setValue(self, value) -> None: ...
    def setRange(self, minimum, maximum) -> None: ...
    def setColors(self, fill1, fill2 = ..., background = ...) -> None: ...
    def setCenterText(self, text) -> None: ...
    def setBadge(self, text, color = ...) -> None: ...
    def showEvent(self, e): ...
    def hideEvent(self, e): ...
    def setAnimated(self, on) -> None: ...
    def paintEvent(self, e): ...
