# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from Custom_Widgets.widgets.navigation.QCustomSlideMenu import QCustomSlideMenu
from PySide6.QtCore import Signal
from typing import Any, ClassVar


class QCustomSidebar(QCustomSlideMenu):
    defaultWidth: Any
    defaultHeight: Any
    collapsedWidth: Any
    collapsedHeight: Any
    expandedWidth: Any
    expandedHeight: Any
    toggleButtonName: Any
    iconCollapsed: Any
    iconExpanded: Any
    animationDuration: Any
    animationEasingCurve: Any
    shadowColor: Any
    shadowBlurRadius: Any
    shadowXOffset: Any
    shadowYOffset: Any
    def __init__(self, parent = ...) -> None: ...
    def updateProperties(self, state = ...): ...
    def convert_to_int(self, s): ...
    def showEvent(self, event): ...
    def paintEvent(self, e): ...
