# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from typing import Any, ClassVar


class QCustomActionButton(QFrame):
    clicked: ClassVar[Signal]
    caption: str
    icon: Any
    buttonSize: int
    iconSize: int
    bgColor: str
    hoverColor: str
    captionColor: str
    def __init__(self, parent = ..., caption = ..., icon = ...) -> None: ...
