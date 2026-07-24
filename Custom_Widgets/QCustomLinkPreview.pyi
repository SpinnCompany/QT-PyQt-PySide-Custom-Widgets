# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomLinkPreview(QWidget):
    clicked: ClassVar[Signal]
    title: str
    url: str
    description: str
    def __init__(self, parent = ...) -> None: ...
    def setLink(self, title, url, description = ..., thumbnail = ...) -> None: ...
    def setThumbnail(self, pm) -> None: ...
    def resizeEvent(self, e): ...
    def mousePressEvent(self, e): ...
