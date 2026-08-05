# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomAvatarGroup(QWidget):
    maxVisible: int
    ringColor: Any
    overflowBg: Any
    overflowText: Any
    def __init__(self, parent = ..., maxVisible = ..., size = ...) -> None: ...
    def setAvatars(self, names) -> None: ...
    def names(self): ...
