# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomVoiceMessage(QWidget):
    playToggled: ClassVar[Signal]
    seeked: ClassVar[Signal]
    valuesCsv: str
    duration: str
    progress: float
    playing: bool
    playedColor: str
    unplayedColor: str
    buttonColor: str
    buttonIconColor: str
    durationColor: str
    buttonDiameter: int
    def __init__(self, parent = ...) -> None: ...
