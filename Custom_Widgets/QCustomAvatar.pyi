# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomAvatar(QWidget):
    clicked: ClassVar[Signal]
    text: str
    imageSource: str
    cornerRadius: int
    bgColor: str
    textColor: str
    showStatus: bool
    statusColor: str
    statusPosition: str
    statusBorderColor: str
    ringColor: str
    ringWidth: int
    def __init__(self, parent = ..., text = ..., image = ...) -> None: ...
    def setText(self, text) -> None: ...
    def setImage(self, image) -> None: ...
    def setImageSource(self, source) -> None: ...
    def setBgColor(self, c) -> None: ...
    def setStatus(self, visible, color = ...) -> None: ...
    def paintEvent(self, e): ...
    def mousePressEvent(self, e): ...
