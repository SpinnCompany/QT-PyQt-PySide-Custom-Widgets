# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel
from typing import Any, ClassVar


class QCustomQLabel(QLabel):
    iconColor: str
    iconSize: int
    imageSource: str
    imageCornerRadius: int
    def __init__(self, parent = ..., iconColor = ...) -> None: ...
    def resizeEvent(self, e): ...
    def setImageSource(self, source) -> None: ...
