# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomWallpaper(QWidget):
    imageLoaded: ClassVar[Signal]
    imageSource: str
    fallbackTop: str
    fallbackMid: str
    fallbackBottom: str
    def __init__(self, parent = ...) -> None: ...
    def setImageSource(self, source) -> None: ...
    def pixmap(self): ...
    def paintEvent(self, e): ...
