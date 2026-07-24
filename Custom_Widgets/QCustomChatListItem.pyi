# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from typing import Any, ClassVar


class QCustomChatListItem(QFrame):
    clicked: ClassVar[Signal]
    name: str
    preview: str
    time: str
    unread: int
    online: bool
    active: bool
    muted: bool
    activeColor: str
    nameColor: str
    previewColor: str
    timeColor: str
    activeNameColor: str
    activeTimeColor: str
    accentColor: str
    radius: int
    avatarSize: int
    def __init__(self, parent = ..., name = ..., preview = ..., time = ...) -> None: ...
    def setName(self, text) -> None: ...
    def setPreview(self, text) -> None: ...
    def setTime(self, text) -> None: ...
    def setAvatarImage(self, image) -> None: ...
    def resizeEvent(self, e): ...
    def paintEvent(self, e): ...
    def mousePressEvent(self, e): ...
