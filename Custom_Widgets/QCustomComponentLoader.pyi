# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from typing import Any, ClassVar


class QCustomComponentLoader(QWidget):
    filePath: Any
    formClassName: Any
    hotReload: Any
    previewComponent: Any
    def __init__(self, parent = ...) -> None: ...
    def showEvent(self, event): ...
    def applyThemeIcons(self): ...
    def loadComponent(self, formClass = ..., formClassName = ..., filePath = ...): ...
    def paintEvent(self, e): ...
