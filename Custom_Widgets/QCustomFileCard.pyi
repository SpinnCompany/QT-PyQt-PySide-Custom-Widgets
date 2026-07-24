# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomFileCard(QWidget):
    clicked: ClassVar[Signal]
    downloadClicked: ClassVar[Signal]
    fileName: str
    fileSize: str
    fileExt: str
    fileDate: str
    badgeColor: str
    iconColor: str
    def __init__(self, parent = ...) -> None: ...
    def setFile(self, name, size = ..., ext = ..., date = ...) -> None: ...
    def mousePressEvent(self, e): ...
