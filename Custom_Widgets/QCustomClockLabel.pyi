# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel
from typing import Any, ClassVar


class QCustomClockLabel(QLabel):
    format: str
    interval: int
    running: bool
    def __init__(self, parent = ...) -> None: ...
