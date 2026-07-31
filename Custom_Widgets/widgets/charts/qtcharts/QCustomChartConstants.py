# file name: QCustomChartConstants.py
from enum import IntEnum
from qtpy.QtCore import Qt, QEasingCurve
from qtpy.QtGui import QColor, QBrush


def _build_maps(enum_cls, values):
    """Given an IntEnum class and its ordered list of string constants,
    return (name->int, int->name) so chart properties can be typed as int
    for Qt Designer while the rendering code keeps using the string
    constants. Values must line up with the enum members by order."""
    members = list(enum_cls)
    str_to_int = {v: int(m) for m, v in zip(members, values)}
    int_to_str = {int(m): v for m, v in zip(members, values)}
    return str_to_int, int_to_str

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
    
    # Pie chart constants
    LABELS_POSITION_OUTSIDE = "outside"
    LABELS_POSITION_INSIDE = "inside"
    LABELS_POSITION_INSIDE_TANGENTIAL = "inside_tangential"
    LABELS_POSITION_CALLOUT = "callout"
    
    GRADIENT_RADIAL = "radial"
    GRADIENT_CONICAL = "conical"
    
    ORIENTATION_RIGHT = "right"
    ORIENTATION_TOP = "top"
    ORIENTATION_LEFT = "left"
    ORIENTATION_BOTTOM = "bottom"
    
    # Pie chart default slice colors
    DEFAULT_PIE_SLICE_COLORS = [
        QColor(255, 100, 100),    # Red
        QColor(100, 200, 100),    # Green
        QColor(100, 150, 255),    # Blue
        QColor(200, 100, 200),    # Purple
        QColor(255, 150, 50),     # Orange
        QColor(50, 200, 200),     # Cyan
        QColor(200, 200, 50),     # Yellow
        QColor(150, 100, 255),    # Violet
        QColor(100, 200, 150),    # Teal
        QColor(255, 100, 150),    # Pink
    ]
    
    # ============ BAR CHART CONSTANTS ============

    # Bar label position constants (for Designer properties)
    BAR_LABELS_CENTER = "center"
    BAR_LABELS_INSIDE_BASE = "inside_base"
    BAR_LABELS_INSIDE_END = "inside_end"
    BAR_LABELS_OUTSIDE_END = "outside_end"

    # Bar pattern constants
    BAR_PATTERN_SOLID = "solid"
    BAR_PATTERN_HORIZONTAL = "horizontal"
    BAR_PATTERN_VERTICAL = "vertical"
    BAR_PATTERN_CROSS = "cross"
    BAR_PATTERN_DIAGONAL = "diagonal"
    BAR_PATTERN_REVERSE_DIAGONAL = "reverse_diagonal"
    BAR_PATTERN_DIAGONAL_CROSS = "diagonal_cross"
    BAR_PATTERN_DENSE = "dense"
    BAR_PATTERN_SPARSE = "sparse"
    
    # Bar border style constants
    BAR_BORDER_SOLID = "solid"
    BAR_BORDER_DASHED = "dashed"
    BAR_BORDER_DOTTED = "dotted"
    BAR_BORDER_DASH_DOT = "dash_dot"
    
    
    # Bar selection mode constants
    BAR_SELECTION_NONE = "none"
    BAR_SELECTION_SINGLE = "single"
    BAR_SELECTION_MULTIPLE = "multiple"
    BAR_SELECTION_CATEGORY = "category"
    
    # Bar chart default colors with transparency
    DEFAULT_BAR_COLORS = [
        QColor(255, 100, 100, 200),    # Red with transparency
        QColor(100, 200, 100, 200),    # Green with transparency
        QColor(100, 150, 255, 200),    # Blue with transparency
        QColor(200, 100, 200, 200),    # Purple with transparency
        QColor(255, 150, 50, 200),     # Orange with transparency
        QColor(50, 200, 200, 200),     # Cyan with transparency
        QColor(200, 200, 50, 200),     # Yellow with transparency
        QColor(150, 100, 255, 200),    # Violet with transparency
    ]
    
    # Bar chart negative value colors
    DEFAULT_NEGATIVE_BAR_COLORS = [
        QColor(255, 150, 150, 200),    # Light red
        QColor(150, 220, 150, 200),    # Light green
        QColor(150, 180, 255, 200),    # Light blue
        QColor(220, 150, 220, 200),    # Light purple
    ]
    
    # Bar chart highlight colors
    DEFAULT_HIGHLIGHT_COLORS = [
        QColor(255, 200, 200, 230),    # Highlight red
        QColor(200, 255, 200, 230),    # Highlight green
        QColor(200, 220, 255, 230),    # Highlight blue
        QColor(255, 255, 200, 230),    # Highlight yellow
    ]
    
    # Bar chart error bar colors
    DEFAULT_ERROR_BAR_COLORS = [
        QColor(0, 0, 0, 180),          # Black
        QColor(100, 100, 100, 180),    # Dark gray
        QColor(150, 150, 150, 180),    # Gray
        QColor(200, 200, 200, 180),    # Light gray
    ]
    
    # Default bar properties
    DEFAULT_BAR_WIDTH = 0.7
    DEFAULT_BAR_SPACING = 0.3
    DEFAULT_BAR_BORDER_WIDTH = 1.0
    DEFAULT_BAR_BORDER_COLOR = QColor(255, 255, 255, 150)
    DEFAULT_BAR_SHADOW_BLUR = 10.0
    DEFAULT_BAR_SHADOW_OFFSET = 3.0
    DEFAULT_BAR_ANIMATION_DURATION = 800
    DEFAULT_BAR_VALUE_FONT_SIZE = 8
    DEFAULT_BAR_VALUE_COLOR = QColor(0, 0, 0, 220)
    DEFAULT_BAR_TOOLTIP_FORMAT = "Category: {category}\nSeries: {series}\nValue: {value:.2f}\nPercentage: {percentage:.1f}%"
    
    # Brush patterns mapping
    BAR_PATTERN_BRUSHES = {
        "solid": Qt.SolidPattern,
        "horizontal": Qt.HorPattern,
        "vertical": Qt.VerPattern,
        "cross": Qt.CrossPattern,
        "diagonal": Qt.FDiagPattern,
        "reverse_diagonal": Qt.BDiagPattern,
        "diagonal_cross": Qt.DiagCrossPattern,
        "dense": Qt.Dense1Pattern,
        "sparse": Qt.Dense7Pattern
    }
    
    # Border style mapping
    BAR_BORDER_STYLES = {
        "solid": Qt.SolidLine,
        "dashed": Qt.DashLine,
        "dotted": Qt.DotLine,
        "dash_dot": Qt.DashDotLine
    }

    
    # ============ ANIMATION EASING CURVE CONSTANTS ============
    
    # Easing curve type constants
    EASING_LINEAR = "linear"
    EASING_IN_QUAD = "in_quad"
    EASING_OUT_QUAD = "out_quad"
    EASING_IN_OUT_QUAD = "in_out_quad"
    EASING_IN_CUBIC = "in_cubic"
    EASING_OUT_CUBIC = "out_cubic"
    EASING_IN_OUT_CUBIC = "in_out_cubic"
    EASING_IN_QUART = "in_quart"
    EASING_OUT_QUART = "out_quart"
    EASING_IN_OUT_QUART = "in_out_quart"
    EASING_IN_QUINT = "in_quint"
    EASING_OUT_QUINT = "out_quint"
    EASING_IN_OUT_QUINT = "in_out_quint"
    EASING_IN_SINE = "in_sine"
    EASING_OUT_SINE = "out_sine"
    EASING_IN_OUT_SINE = "in_out_sine"
    EASING_IN_EXPO = "in_expo"
    EASING_OUT_EXPO = "out_expo"
    EASING_IN_OUT_EXPO = "in_out_expo"
    EASING_IN_CIRC = "in_circ"
    EASING_OUT_CIRC = "out_circ"
    EASING_IN_OUT_CIRC = "in_out_circ"
    EASING_IN_BACK = "in_back"
    EASING_OUT_BACK = "out_back"
    EASING_IN_OUT_BACK = "in_out_back"
    EASING_IN_ELASTIC = "in_elastic"
    EASING_OUT_ELASTIC = "out_elastic"
    EASING_IN_OUT_ELASTIC = "in_out_elastic"
    EASING_IN_BOUNCE = "in_bounce"
    EASING_OUT_BOUNCE = "out_bounce"
    EASING_IN_OUT_BOUNCE = "in_out_bounce"
    
    # Default animation properties
    DEFAULT_ANIMATION_DURATION = 800
    DEFAULT_ANIMATION_EASING = "out_quad"
    
    # Easing curve mapping
    EASING_CURVE_MAP = {
        "linear": QEasingCurve.Linear,
        "in_quad": QEasingCurve.InQuad,
        "out_quad": QEasingCurve.OutQuad,
        "in_out_quad": QEasingCurve.InOutQuad,
        "in_cubic": QEasingCurve.InCubic,
        "out_cubic": QEasingCurve.OutCubic,
        "in_out_cubic": QEasingCurve.InOutCubic,
        "in_quart": QEasingCurve.InQuart,
        "out_quart": QEasingCurve.OutQuart,
        "in_out_quart": QEasingCurve.InOutQuart,
        "in_quint": QEasingCurve.InQuint,
        "out_quint": QEasingCurve.OutQuint,
        "in_out_quint": QEasingCurve.InOutQuint,
        "in_sine": QEasingCurve.InSine,
        "out_sine": QEasingCurve.OutSine,
        "in_out_sine": QEasingCurve.InOutSine,
        "in_expo": QEasingCurve.InExpo,
        "out_expo": QEasingCurve.OutExpo,
        "in_out_expo": QEasingCurve.InOutExpo,
        "in_circ": QEasingCurve.InCirc,
        "out_circ": QEasingCurve.OutCirc,
        "in_out_circ": QEasingCurve.InOutCirc,
        "in_back": QEasingCurve.InBack,
        "out_back": QEasingCurve.OutBack,
        "in_out_back": QEasingCurve.InOutBack,
        "in_elastic": QEasingCurve.InElastic,
        "out_elastic": QEasingCurve.OutElastic,
        "in_out_elastic": QEasingCurve.InOutElastic,
        "in_bounce": QEasingCurve.InBounce,
        "out_bounce": QEasingCurve.OutBounce,
        "in_out_bounce": QEasingCurve.InOutBounce,
    }

########################################################################
## TYPED ENUMS FOR QT DESIGNER
##
## Chart state/mode properties are exposed to Qt Designer as int (backed
## by these IntEnums) instead of free-form strings. The rendering code
## keeps using the string constants above; properties map int<->string at
## the boundary via the paired maps. Developers can use e.g.
## QCustomChartEnums.LegendPosition.Top.
########################################################################
class QCustomChartEnums:

    class LineStyle(IntEnum):
        Solid = 0; Dash = 1; Dot = 2; DashDot = 3; DashDotDot = 4; NoneStyle = 5

    class MarkerStyle(IntEnum):
        Circle = 0; Rectangle = 1; RotatedRectangle = 2; Triangle = 3
        Star = 4; Pentagon = 5; NoneStyle = 6

    class ChartTheme(IntEnum):
        AppTheme = 0; Light = 1; Dark = 2; BlueNcs = 3; BlueIcy = 4
        HighContrast = 5; QtLight = 6; QtDark = 7; QtBrownSand = 8

    class LegendPosition(IntEnum):
        Top = 0; Bottom = 1; Left = 2; Right = 3; Floating = 4

    class LabelsPosition(IntEnum):
        Outside = 0; Inside = 1; InsideTangential = 2; Callout = 3

    class BarLabelsPosition(IntEnum):
        Center = 0; InsideBase = 1; InsideEnd = 2; OutsideEnd = 3

    class BarPattern(IntEnum):
        Solid = 0; Horizontal = 1; Vertical = 2; Cross = 3; Diagonal = 4
        ReverseDiagonal = 5; DiagonalCross = 6; Dense = 7; Sparse = 8

    class BarBorderStyle(IntEnum):
        Solid = 0; Dashed = 1; Dotted = 2; DashDot = 3

    class BarSelectionMode(IntEnum):
        NoneMode = 0; Single = 1; Multiple = 2; Category = 3


_C = QCustomChartConstants
_E = QCustomChartEnums

# name<->int maps, ordered to line up with each IntEnum's members
LINE_STYLE_TO_INT, INT_TO_LINE_STYLE = _build_maps(
    _E.LineStyle, [_C.LINE_SOLID, _C.LINE_DASH, _C.LINE_DOT,
                   _C.LINE_DASH_DOT, _C.LINE_DASH_DOT_DOT, _C.LINE_NONE])
MARKER_STYLE_TO_INT, INT_TO_MARKER_STYLE = _build_maps(
    _E.MarkerStyle, [_C.MARKER_CIRCLE, _C.MARKER_RECTANGLE, _C.MARKER_ROTATED_RECTANGLE,
                     _C.MARKER_TRIANGLE, _C.MARKER_STAR, _C.MARKER_PENTAGON, _C.MARKER_NONE])
CHART_THEME_TO_INT, INT_TO_CHART_THEME = _build_maps(
    _E.ChartTheme, [_C.THEME_APP_THEME, _C.THEME_LIGHT, _C.THEME_DARK, _C.THEME_BLUE_NCS,
                    _C.THEME_BLUE_ICY, _C.THEME_HIGH_CONTRAST, _C.THEME_QT_LIGHT,
                    _C.THEME_QT_DARK, _C.THEME_QT_BROWN_SAND])
LEGEND_POSITION_TO_INT, INT_TO_LEGEND_POSITION = _build_maps(
    _E.LegendPosition, [_C.LEGEND_TOP, _C.LEGEND_BOTTOM, _C.LEGEND_LEFT,
                        _C.LEGEND_RIGHT, _C.LEGEND_FLOATING])
LABELS_POSITION_TO_INT, INT_TO_LABELS_POSITION = _build_maps(
    _E.LabelsPosition, [_C.LABELS_POSITION_OUTSIDE, _C.LABELS_POSITION_INSIDE,
                        _C.LABELS_POSITION_INSIDE_TANGENTIAL, _C.LABELS_POSITION_CALLOUT])
BAR_LABELS_TO_INT, INT_TO_BAR_LABELS = _build_maps(
    _E.BarLabelsPosition, [_C.BAR_LABELS_CENTER, _C.BAR_LABELS_INSIDE_BASE,
                           _C.BAR_LABELS_INSIDE_END, _C.BAR_LABELS_OUTSIDE_END])
BAR_PATTERN_TO_INT, INT_TO_BAR_PATTERN = _build_maps(
    _E.BarPattern, [_C.BAR_PATTERN_SOLID, _C.BAR_PATTERN_HORIZONTAL, _C.BAR_PATTERN_VERTICAL,
                    _C.BAR_PATTERN_CROSS, _C.BAR_PATTERN_DIAGONAL, _C.BAR_PATTERN_REVERSE_DIAGONAL,
                    _C.BAR_PATTERN_DIAGONAL_CROSS, _C.BAR_PATTERN_DENSE, _C.BAR_PATTERN_SPARSE])
BAR_BORDER_TO_INT, INT_TO_BAR_BORDER = _build_maps(
    _E.BarBorderStyle, [_C.BAR_BORDER_SOLID, _C.BAR_BORDER_DASHED,
                        _C.BAR_BORDER_DOTTED, _C.BAR_BORDER_DASH_DOT])
BAR_SELECTION_TO_INT, INT_TO_BAR_SELECTION = _build_maps(
    _E.BarSelectionMode, [_C.BAR_SELECTION_NONE, _C.BAR_SELECTION_SINGLE,
                          _C.BAR_SELECTION_MULTIPLE, _C.BAR_SELECTION_CATEGORY])


def chart_str_to_int(mapping, value, default=0):
    """Map a chart string constant / int / IntEnum to its int, tolerant of
    legacy string values."""
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return int(value)
    return mapping.get(value, default)


def chart_int_to_str(mapping, value, default):
    """Map an int (or legacy string) back to the string constant used by the
    rendering code."""
    if isinstance(value, str):
        return value
    return mapping.get(int(value), default)
