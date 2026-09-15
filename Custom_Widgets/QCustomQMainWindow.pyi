# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow
from typing import Any, ClassVar


class QCustomQMainWindow(QMainWindow):
    appTheme: Any
    jsonStylesheetFilePath: Any
    frameless: Any
    translucentBg: Any
    minimizeBtn: Any
    closeBtn: Any
    restoreBtn: Any
    restoreBtnNormalIcon: Any
    restoreBtnMaximizedIcon: Any
    titleBar: Any
    moveWindow: Any
    sizeGrip: Any
    shadowColor: Any
    shadowBlurRadius: Any
    shadowXOffset: Any
    shadowYOffset: Any
    windowBorderRadius: Any
    customSideDrawers: Any
    def __init__(self, parent = ..., frameless: bool = ..., translucentBg: bool = ..., minimizeBtn: Any = ..., closeBtn: Any = ..., restoreBtn: Any = ..., restoreBtnNormalIcon: Any = ..., restoreBtnMaximizedIcon: Any = ..., titleBar: Any = ..., moveWindow: Any = ..., sizeGrip: Any = ...) -> None: ...
    def isValidTheme(self, value: str): ...
    def closeEvent(self, event): ...
    def paintEvent(self, event: Any): ...
