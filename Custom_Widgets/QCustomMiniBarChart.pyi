# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomMiniBarChart(QWidget):
    valuesCsv: str
    colorsCsv: str
    labelsCsv: str
    barColor: str
    idleColor: str
    highlightColor: str
    highlightIndexProp: Any
    barWidth: int
    cornerRadius: int
    showLabels: bool
    labelColor: Any
    calloutText: str
    calloutBg: str
    calloutTextColor: str
    yLabelsCsv: str
    yLabelColor: str
    def __init__(self, parent = ..., values = ..., colors = ..., labels = ...) -> None: ...
    def setData(self, values, colors = ..., labels = ...) -> None: ...
    def setValues(self, values) -> None: ...
    def setBarColors(self, colors) -> None: ...
    def setLabels(self, labels) -> None: ...
    def highlightIndex(self, index, color = ...): ...
    def clearHighlight(self): ...
    def setIdleThreshold(self, value) -> None: ...
    def values(self): ...
    def paintEvent(self, e): ...
