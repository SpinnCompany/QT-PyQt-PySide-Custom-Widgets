# file name: QCustomChartConstants.py
from qtpy.QtCore import Qt, QEasingCurve
from qtpy.QtGui import QColor, QBrush

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