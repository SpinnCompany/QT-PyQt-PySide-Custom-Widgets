# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomRadialGauge(QWidget):
    valueChanged: ClassVar[Signal]
    finished: ClassVar[Signal]
    value: float
    minimum: float
    maximum: float
    gaugeStyle: str
    startAngle: float
    spanAngle: float
    tickCount: int
    arcWidth: int
    zonesCsv: str
    gradientStart: str
    gradientEnd: str
    trackColor: str
    needleColor: str
    centerText: str
    centerSuffix: str
    statusText: str
    statusColor: str
    centerTextColor: str
    scaleColor: str
    showTicks: bool
    showHandle: bool
    handleColor: str
    centerIcon: str
    iconColor: str
    innerColor: str
    showNeedle: bool
    showScaleLabels: bool
    showGuide: bool
    scaleLabelEvery: float
    emphasizeActiveTick: bool
    activeTickExtend: str
    scaleLabelRadius: float
    roundedCaps: bool
    animated: bool
    animationDuration: int
    glow: bool
    glowStrength: float
    glowRadius: int
    def __init__(self, parent = ..., value = ..., minimum = ..., maximum = ..., gaugeStyle = ...) -> None: ...
    def setValue(self, value) -> None: ...
    def setRange(self, minimum, maximum) -> None: ...
    def setStyle(self, gaugeStyle) -> None: ...
    def setZones(self, zones) -> None: ...
    def setGradient(self, start, end) -> None: ...
    def setStatusText(self, text) -> None: ...
    def setCenterText(self, text) -> None: ...
    def start(self, seconds = ..., interval_ms = ..., step = ...): ...
    def stop(self): ...
    def paintEvent(self, e): ...
