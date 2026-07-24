# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QAbstractButton
from typing import Any, ClassVar


class QCustomTileButton(QAbstractButton):
    caption: str
    iconPath: str
    gradientStart: str
    gradientEnd: str
    bgColor: str
    iconColor: str
    activeColor: str
    cornerRadius: int
    iconSize: int
    def __init__(self, parent = ..., caption = ..., iconPath = ...) -> None: ...
    def setCaption(self, text) -> None: ...
    def setIconPath(self, path) -> None: ...
    def setGradient(self, start, end) -> None: ...
    def paintEvent(self, e): ...
    def sizeHint(self): ...
