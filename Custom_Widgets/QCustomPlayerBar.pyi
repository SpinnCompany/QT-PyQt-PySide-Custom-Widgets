# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomPlayerBar(QWidget):
    playToggled: ClassVar[Signal]
    nextClicked: ClassVar[Signal]
    prevClicked: ClassVar[Signal]
    seeked: ClassVar[Signal]
    favoriteToggled: ClassVar[Signal]
    shuffleToggled: ClassVar[Signal]
    repeatToggled: ClassVar[Signal]
    volumeClicked: ClassVar[Signal]
    title: str
    artist: str
    elapsedText: str
    totalText: str
    playing: bool
    favorite: bool
    shuffle: bool
    repeat: bool
    barColor: str
    accentColor: str
    trackColor: str
    textColor: str
    subTextColor: str
    iconColor: str
    playBtnColor: str
    coverPath: str
    position: float
    cornerRadius: int
    durationSeconds: Any
    elapsedSeconds: Any
    compactMode: bool
    def __init__(self, parent = ...) -> None: ...
    def setTrack(self, title = ..., artist = ..., coverPath = ..., elapsed = ..., total = ..., position = ...) -> None: ...
    def setPlaying(self, on) -> None: ...
    def setCoverSource(self, source) -> None: ...
    def paintEvent(self, e): ...
    def mousePressEvent(self, e): ...
    def mouseMoveEvent(self, e): ...
    def mouseReleaseEvent(self, e): ...
    def leaveEvent(self, e): ...
    def sizeHint(self): ...
