# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomDotMatrix(QWidget):
    dataCsv: str
    rows: int
    cols: int
    colorsCsv: str
    emptyColor: str
    dotDiameter: int
    gapRatio: float
    emptyOpacity: float
    square: bool
    def __init__(self, parent = ..., data = ...) -> None: ...
    def setData(self, data) -> None: ...
    def data(self): ...
    def setColors(self, colors) -> None: ...
    def paintEvent(self, e): ...
