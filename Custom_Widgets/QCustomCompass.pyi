# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomCompass(QWidget):
    headingChanged: ClassVar[Signal]
    heading: float
    rotateBezel: bool
    showIntercardinals: bool
    showReadout: bool
    animated: bool
    interactive: bool
    northColor: str
    southColor: str
    ringColor: str
    tickColor: str
    cardinalColor: str
    readoutColor: str
    hubColor: str
    def __init__(self, parent = ..., heading = ...) -> None: ...
    def setHeading(self, deg) -> None: ...
    @staticmethod
    def cardinal16(deg): ...
    def paintEvent(self, e): ...
    def mousePressEvent(self, e): ...
    def mouseMoveEvent(self, e): ...
