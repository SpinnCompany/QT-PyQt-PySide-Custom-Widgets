# file name: QCustomChartConstants.py
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor

class QCustomChartConstants:
    """Shared constants for the chart module"""
    
    # Line style constants
    LINE_SOLID = "solid"
    LINE_DASH = "dash"
    LINE_DOT = "dot"
    LINE_DASH_DOT = "dash_dot"
    LINE_DASH_DOT_DOT = "dash_dot_dot"
    LINE_NONE = "none"

    # Marker style constants
    MARKER_CIRCLE = "circle"
    MARKER_RECTANGLE = "rectangle"
    MARKER_ROTATED_RECTANGLE = "rotated_rectangle"
    MARKER_TRIANGLE = "triangle"
    MARKER_STAR = "star"
    MARKER_PENTAGON = "pentagon"
    MARKER_NONE = "none"
    
    # Theme constants
    THEME_APP_THEME = "App Theme"
    THEME_LIGHT = "Light"
    THEME_DARK = "Dark"
    THEME_BLUE_NCS = "Blue NCS"
    THEME_BLUE_ICY = "Blue Icy"
    THEME_HIGH_CONTRAST = "High Contrast"
    THEME_QT_LIGHT = "Qt Light"
    THEME_QT_DARK = "Qt Dark"
    THEME_QT_BROWN_SAND = "Qt Brown Sand"
    
    # Legend position constants
    LEGEND_TOP = "Top"
    LEGEND_BOTTOM = "Bottom"
    LEGEND_LEFT = "Left"
    LEGEND_RIGHT = "Right"
    LEGEND_FLOATING = "Floating"
    
    # Export format constants
    FORMAT_PNG = "PNG"
    FORMAT_JPEG = "JPEG"
    FORMAT_PDF = "PDF"
    FORMAT_SVG = "SVG"
    FORMAT_CSV = "CSV"
    FORMAT_JSON = "JSON"
    
    # Default colors
    DEFAULT_SERIES_COLORS = [
        QColor(255, 100, 100),    # Red
        QColor(100, 200, 100),    # Green
        QColor(100, 150, 255),    # Blue
        QColor(200, 100, 200),    # Purple
        QColor(255, 150, 50),     # Orange
        QColor(50, 200, 200),     # Cyan
        QColor(200, 200, 50),     # Yellow
        QColor(150, 100, 255),    # Violet
    ]