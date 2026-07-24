# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from typing import Any, ClassVar


class QCustomChatInput(QFrame):
    sendMessage: ClassVar[Signal]
    attachClicked: ClassVar[Signal]
    micClicked: ClassVar[Signal]
    emojiClicked: ClassVar[Signal]
    textChanged: ClassVar[Signal]
    placeholder: str
    clearOnSend: bool
    showAttach: bool
    showMic: bool
    showEmoji: bool
    iconSize: int
    def __init__(self, parent = ...) -> None: ...
    def field(self): ...
    def text(self): ...
    def setText(self, t) -> None: ...
    def insertText(self, t): ...
    def sendButton(self): ...
    def emojiButton(self): ...
