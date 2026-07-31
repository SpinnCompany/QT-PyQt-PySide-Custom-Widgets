# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomRadioButton(QWidget):
    toggled: ClassVar[Signal]
    selected: ClassVar[Signal]
    checked: bool
    text: str
    value: str
    autoExclusive: bool
    sizeVariant: str
    dotScale: Any
    ringColor: Any
    ringCheckedColor: Any
    dotColor: Any
    textColor: Any
    def __init__(self, parent = ..., text = ..., checked = ..., value = ...) -> None: ...
    def sizeHint(self): ...
    def minimumSizeHint(self): ...
    def paintEvent(self, e): ...
    def mouseReleaseEvent(self, e): ...
    def keyPressEvent(self, e): ...
    def isChecked(self): ...
    def setChecked(self, checked) -> None: ...
