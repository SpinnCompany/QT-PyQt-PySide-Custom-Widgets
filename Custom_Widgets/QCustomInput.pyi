# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit
from typing import Any, ClassVar


class QCustomInput(QLineEdit):
    variant: str
    sizeVariant: str
    state: Any
    def __init__(self, parent = ...) -> None: ...
    def setError(self, error_text = ...) -> None: ...
    def focusInEvent(self, event): ...
    def focusOutEvent(self, event): ...
