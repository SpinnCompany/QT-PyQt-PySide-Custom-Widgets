# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomReactionBar(QWidget):
    reactionClicked: ClassVar[Signal]
    addRequested: ClassVar[Signal]
    reactions: str
    showAdd: bool
    addColor: str
    def __init__(self, parent = ...) -> None: ...
    def setReactions(self, reactions) -> None: ...
