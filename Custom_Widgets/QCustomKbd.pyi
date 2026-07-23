# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomKbd(QWidget):
    keys: str
    separator: str
    def __init__(self, keys = ..., parent = ..., separator = ...) -> None: ...
    def setKeys(self, keys) -> None: ...
    def keysList(self): ...
