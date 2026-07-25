# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from typing import Any, ClassVar


class QCustomListRow(QFrame):
    title: str
    subtitle: str
    value: str
    meta: str
    iconText: str
    chipColor: str
    chipTextColor: str
    subtitleColor: str
    valueColor: str
    chipSize: int
    chipRadius: int
    showDragHandle: bool
    dragHandleColor: str
    def __init__(self, parent = ..., title = ..., subtitle = ..., value = ..., meta = ..., icon = ...) -> None: ...
    def setTitle(self, text) -> None: ...
    def setSubtitle(self, text) -> None: ...
    def setValue(self, text) -> None: ...
    def setMeta(self, text) -> None: ...
    def setIcon(self, icon) -> None: ...
    def setIconText(self, text) -> None: ...
