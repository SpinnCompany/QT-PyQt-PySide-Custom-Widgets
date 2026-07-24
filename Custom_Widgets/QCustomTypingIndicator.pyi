# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomTypingIndicator(QWidget):
    running: bool
    dotColor: str
    dotSize: int
    bubble: bool
    bubbleColor: str
    def __init__(self, parent = ...) -> None: ...
    def start(self): ...
    def stop(self): ...
    def paintEvent(self, e): ...
