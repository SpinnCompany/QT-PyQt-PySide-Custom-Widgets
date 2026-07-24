# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from typing import Any, ClassVar


class QCustomChatList(QFrame):
    currentChanged: ClassVar[Signal]
    itemClicked: ClassVar[Signal]
    accentColor: str
    activeColor: str
    nameColor: str
    previewColor: str
    timeColor: str
    activeNameColor: str
    activeTimeColor: str
    onlineColor: str
    surfaceColor: str
    rowSpacing: int
    def __init__(self, parent = ...) -> None: ...
    def setConversations(self, conversations) -> None: ...
    def setAvatarImageAt(self, index, image) -> None: ...
    def setCurrentIndex(self, index, emit = ...) -> None: ...
    def currentIndex(self): ...
    def count(self): ...
