# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton
from typing import Any, ClassVar


class QCustomThemeDarkLightToggle(QPushButton):
    darkTheme: Any
    lightTheme: Any
    updateLabelText: Any
    updateButtonIcon: Any
    darkThemeIcon: Any
    lightThemeIcon: Any
    def __init__(self, parent = ..., *args, **kwargs) -> None: ...
    def showEvent(self, event): ...
    def toggle_theme(self): ...
    def setText(self, text: str): ...
    def update_button_text(self): ...
    def update_button_icon(self): ...
