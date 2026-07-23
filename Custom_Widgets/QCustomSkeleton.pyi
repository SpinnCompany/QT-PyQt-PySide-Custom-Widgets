# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomSkeleton(QWidget):
    shape: str
    baseColor: Any
    highlightColor: Any
    def __init__(self, parent = ..., shape = ...) -> None: ...
    def start(self): ...
    def stop(self): ...
    def paintEvent(self, e): ...
