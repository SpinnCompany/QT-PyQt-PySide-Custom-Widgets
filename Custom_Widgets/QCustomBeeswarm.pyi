# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomBeeswarm(QWidget):
    dataCsv: str
    colorsCsv: str
    textColorsCsv: str
    lineColor: str
    minSize: int
    maxSize: int
    bubbleWidth: int
    gap: int
    showValues: bool
    jitter: int
    def __init__(self, parent = ..., columns = ...) -> None: ...
    def setData(self, columns) -> None: ...
    def data(self): ...
    def setColors(self, fills, texts = ...) -> None: ...
    def paintEvent(self, e): ...
