# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomGanttChart(QWidget):
    dataCsv: str
    colorsCsv: str
    textColorsCsv: str
    xMax: float
    gridStep: float
    barHeight: int
    labelColor: str
    axisTextColor: str
    gridColor: str
    showGrid: bool
    showMarkers: bool
    def __init__(self, parent = ..., rows = ...) -> None: ...
    def setData(self, rows) -> None: ...
    def data(self): ...
    def setColors(self, fills, texts = ...) -> None: ...
    def paintEvent(self, e): ...
