# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from typing import Any, ClassVar


class QCustomChatThread(QFrame):
    reactionAddRequested: ClassVar[Signal]
    reactionClicked: ClassVar[Signal]
    inlineMediaCreated: ClassVar[Signal]
    mediaOpenRequested: ClassVar[Signal]
    linkClicked: ClassVar[Signal]
    incomingBubbleColor: str
    incomingTextColor: str
    outgoingBubbleColor: str
    outgoingTextColor: str
    metaColor: str
    dateBgColor: str
    dateTextColor: str
    accentColor: str
    waveUnplayedColor: str
    maxBubbleWidth: int
    spacing: int
    showReactionAdd: bool
    def __init__(self, parent = ...) -> None: ...
    def setSenderName(self, name) -> None: ...
    def setMessages(self, messages) -> None: ...
    def addReaction(self, index, emoji): ...
