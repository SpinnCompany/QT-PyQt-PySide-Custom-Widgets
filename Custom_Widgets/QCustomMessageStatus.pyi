# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomMessageStatus(QWidget):
    status: str
    tickColor: str
    readColor: str
    tickSize: int
    def __init__(self, parent = ...) -> None: ...
    def setStatus(self, s) -> None: ...
    def paintEvent(self, e): ...
