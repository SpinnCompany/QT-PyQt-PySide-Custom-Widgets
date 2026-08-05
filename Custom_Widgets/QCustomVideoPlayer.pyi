# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomVideoPlayer(QWidget):
    playToggled: ClassVar[Signal]
    seeked: ClassVar[Signal]
    duration: str
    progress: float
    playing: bool
    radius: int
    accentColor: str
    posterColor: str
    barColor: str
    trackColor: str
    textColor: str
    def __init__(self, parent = ...) -> None: ...
    def setPoster(self, pm) -> None: ...
    def setPlaying(self, v) -> None: ...
    def toggle(self): ...
    def paintEvent(self, e): ...
    def mousePressEvent(self, e): ...
