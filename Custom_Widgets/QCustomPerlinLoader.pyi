# Auto-generated type stub — DO NOT EDIT.
# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from typing import Any, ClassVar


class QCustomPerlinLoader(QFrame):
    message: Any
    color: Any
    fontFamily: Any
    fontSize: Any
    rayon: Any
    duration: Any
    backgroundColor: Any
    circleColor1: Any
    circleColor2: Any
    circleColor3: Any
    def __init__(self, parent: Any = ..., size: Any = ..., message: str = ..., color = ..., fontFamily = ..., fontSize = ..., rayon: int = ..., duration: int = ..., noiseOctaves: float = ..., noiseSeed: int = ..., backgroundColor: Any = ..., circleColor1: Any = ..., circleColor2: Any = ..., circleColor3: Any = ...) -> None: ...
    def start_animation(self): ...
    def update_start_angle(self, new_value: float): ...
    def get_deformed_point(self, angle: float, noise_generator: Any): ...
    def draw_deformed_circles(self, painter: Any): ...
    def draw_message(self, painter: Any): ...
    def paintEvent(self, e: Any): ...
