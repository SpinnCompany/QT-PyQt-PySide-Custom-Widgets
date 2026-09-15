# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomComponentContainer(QWidget):
    filePath: Any
    formClassName: Any
    previewComponent: Any
    hotReload: Any
    def __init__(self, parent = ...) -> None: ...
    def showEvent(self, e): ...
    def paintEvent(self, e): ...
    def resizeEvent(self, event: Any): ...
