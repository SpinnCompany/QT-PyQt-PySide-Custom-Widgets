"""
Custom Charts Module - Modular Architecture
"""

from .QCustomChartConstants import QCustomChartConstants
from .QCustomChartBase import QCustomChartBase
from .QCustomChartView import QCustomChartView
from .QCustomChartThemeManager import QCustomChartThemeManager
from .QCustomChartToolbar import QCustomChartToolbar
from .QCustomChartExporter import QCustomChartExporter
from .QCustomChartDataManager import QCustomChartDataManager
from .QCustomChartTooltip import QCustomChartTooltip
from .QCustomLegendManager import QCustomLegendManager
from .QCustomQLineSeries import QCustomQLineSeries
from .QCustomLineChart import QCustomLineChart
from .QCustomBarChart import QCustomBarChart
from .QCustomAreaChart import QCustomAreaChart
from .QCustomPieChart import QCustomPieChart
from .QCustomVerticalBarSeries import QCustomVerticalBarSeries
from .QCustomBarChartBase import QCustomBarChartBase
from .QCustomHorizontalBarSeries import QCustomHorizontalBarSeries


# Expose constants for convenience
LINE_SOLID = QCustomChartConstants.LINE_SOLID
LINE_DASH = QCustomChartConstants.LINE_DASH
LINE_DOT = QCustomChartConstants.LINE_DOT
LINE_DASH_DOT = QCustomChartConstants.LINE_DASH_DOT
LINE_DASH_DOT_DOT = QCustomChartConstants.LINE_DASH_DOT_DOT
LINE_NONE = QCustomChartConstants.LINE_NONE

MARKER_CIRCLE = QCustomChartConstants.MARKER_CIRCLE
MARKER_RECTANGLE = QCustomChartConstants.MARKER_RECTANGLE
MARKER_ROTATED_RECTANGLE = QCustomChartConstants.MARKER_ROTATED_RECTANGLE
MARKER_TRIANGLE = QCustomChartConstants.MARKER_TRIANGLE
MARKER_STAR = QCustomChartConstants.MARKER_STAR
MARKER_PENTAGON = QCustomChartConstants.MARKER_PENTAGON
MARKER_NONE = QCustomChartConstants.MARKER_NONE

LEGEND_TOP = QCustomChartConstants.LEGEND_TOP
LEGEND_BOTTOM = QCustomChartConstants.LEGEND_BOTTOM
LEGEND_LEFT = QCustomChartConstants.LEGEND_LEFT
LEGEND_RIGHT = QCustomChartConstants.LEGEND_RIGHT
LEGEND_FLOATING = QCustomChartConstants.LEGEND_FLOATING

THEME_APP_THEME = QCustomChartConstants.THEME_APP_THEME
THEME_LIGHT = QCustomChartConstants.THEME_LIGHT
THEME_DARK = QCustomChartConstants.THEME_DARK
THEME_BLUE_NCS = QCustomChartConstants.THEME_BLUE_NCS
THEME_BLUE_ICY = QCustomChartConstants.THEME_BLUE_ICY
THEME_HIGH_CONTRAST = QCustomChartConstants.THEME_HIGH_CONTRAST
THEME_QT_LIGHT = QCustomChartConstants.THEME_QT_LIGHT
THEME_QT_DARK = QCustomChartConstants.THEME_QT_DARK
THEME_QT_BROWN_SAND = QCustomChartConstants.THEME_QT_BROWN_SAND

FORMAT_PNG = QCustomChartConstants.FORMAT_PNG
FORMAT_JPEG = QCustomChartConstants.FORMAT_JPEG
FORMAT_PDF = QCustomChartConstants.FORMAT_PDF
FORMAT_SVG = QCustomChartConstants.FORMAT_SVG
FORMAT_CSV = QCustomChartConstants.FORMAT_CSV
FORMAT_JSON = QCustomChartConstants.FORMAT_JSON

__all__ = [
    'QCustomChartConstants',
    'QCustomChartBase',
    'QCustomChartView',
    'QCustomChartThemeManager',
    'QCustomChartToolbar',
    'QCustomChartExporter',
    'QCustomChartDataManager',
    'QCustomChartTooltip',
    'QCustomLegendManager',
    'QCustomQLineSeries',
    'QCustomLineChart',
    'QCustomBarChart',
    'QCustomAreaChart', 
    'QCustomPieChart',
    'QCustomVerticalBarSeries',
    'QCustomBarChartBase',
    'QCustomHorizontalBarSeries',
    
    # Constants
    'LINE_SOLID',
    'LINE_DASH',
    'LINE_DOT',
    'LINE_DASH_DOT',
    'LINE_DASH_DOT_DOT',
    'LINE_NONE',
    
    'MARKER_CIRCLE',
    'MARKER_RECTANGLE',
    'MARKER_ROTATED_RECTANGLE',
    'MARKER_TRIANGLE',
    'MARKER_STAR',
    'MARKER_PENTAGON',
    'MARKER_NONE',
    
    'LEGEND_TOP',
    'LEGEND_BOTTOM',
    'LEGEND_LEFT',
    'LEGEND_RIGHT',
    'LEGEND_FLOATING',
    
    'THEME_APP_THEME',
    'THEME_LIGHT',
    'THEME_DARK',
    'THEME_BLUE_NCS',
    'THEME_BLUE_ICY',
    'THEME_HIGH_CONTRAST',
    'THEME_QT_LIGHT',
    'THEME_QT_DARK',
    'THEME_QT_BROWN_SAND',
    
    'FORMAT_PNG',
    'FORMAT_JPEG',
    'FORMAT_PDF',
    'FORMAT_SVG',
    'FORMAT_CSV',
    'FORMAT_JSON'
]