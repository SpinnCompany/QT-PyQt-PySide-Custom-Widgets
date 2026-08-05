# file name: QCustomQLineSeries.py
from typing import List, Tuple, Optional
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QPen
from qtpy.QtCharts import QLineSeries, QScatterSeries

from .QCustomChartConstants import QCustomChartConstants


class QCustomQLineSeries(QCustomChartConstants):
    """
    Factory for creating styled line and marker series.
    Handles line styles, marker styles, and other series properties.
    """
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
    
    def createLineSeries(self, name: str, data: List[Tuple[float, float]],
                        color: QColor, line_width: float = 2.0,
                        line_style: str = "solid",
                        visible: bool = True) -> QLineSeries:
        """Create a styled line series"""
        series = QLineSeries()
        series.setName(name)
        
        # Add data points
        for x, y in data:
            series.append(x, y)
        
        # Apply styling
        series.setColor(color)
        
        pen = series.pen()
        pen.setWidthF(line_width)
        
        # Set line style
        if line_style == self.LINE_DASH:
            pen.setStyle(Qt.DashLine)
        elif line_style == self.LINE_DOT:
            pen.setStyle(Qt.DotLine)
        elif line_style == self.LINE_DASH_DOT:
            pen.setStyle(Qt.DashDotLine)
        elif line_style == self.LINE_DASH_DOT_DOT:
            pen.setStyle(Qt.DashDotDotLine)
        elif line_style == self.LINE_NONE:
            pen.setStyle(Qt.NoPen)
        else:
            pen.setStyle(Qt.SolidLine)
        
        series.setPen(pen)
        series.setVisible(visible)
        
        return series
    
    def createMarkerSeries(self, name: str, data: List[Tuple[float, float]],
                          color: QColor, marker_size: float = 8.0,
                          marker_style: str = "circle",
                          visible: bool = True) -> QScatterSeries:
        """Create a styled marker series"""
        series = QScatterSeries()
        series.setName(name)
        series.setColor(color)
        series.setMarkerSize(marker_size)
        
        # Set marker shape
        if marker_style == self.MARKER_RECTANGLE:
            series.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
        elif marker_style == self.MARKER_ROTATED_RECTANGLE:
            series.setMarkerShape(QScatterSeries.MarkerShapeRotatedRectangle)
        elif marker_style == self.MARKER_TRIANGLE:
            series.setMarkerShape(QScatterSeries.MarkerShapeTriangle)
        elif marker_style == self.MARKER_STAR:
            series.setMarkerShape(QScatterSeries.MarkerShapeStar)
        elif marker_style == self.MARKER_PENTAGON:
            series.setMarkerShape(QScatterSeries.MarkerShapePentagon)
        else:
            series.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        
        # Add data points
        for x, y in data:
            series.append(x, y)
        
        series.setVisible(visible)
        
        return series
    
    def penStyleFromString(self, style: str) -> Qt.PenStyle:
        """Convert string line style to Qt.PenStyle"""
        if style == self.LINE_DASH:
            return Qt.DashLine
        elif style == self.LINE_DOT:
            return Qt.DotLine
        elif style == self.LINE_DASH_DOT:
            return Qt.DashDotLine
        elif style == self.LINE_DASH_DOT_DOT:
            return Qt.DashDotDotLine
        elif style == self.LINE_NONE:
            return Qt.NoPen
        else:
            return Qt.SolidLine
    
    def isValidLineStyle(self, style: str) -> bool:
        """Check if line style is valid"""
        valid_styles = [
            self.LINE_SOLID,
            self.LINE_DASH,
            self.LINE_DOT,
            self.LINE_DASH_DOT,
            self.LINE_DASH_DOT_DOT,
            self.LINE_NONE
        ]
        return style in valid_styles
    
    def isValidMarkerStyle(self, style: str) -> bool:
        """Check if marker style is valid"""
        valid_styles = [
            self.MARKER_CIRCLE,
            self.MARKER_RECTANGLE,
            self.MARKER_ROTATED_RECTANGLE,
            self.MARKER_TRIANGLE,
            self.MARKER_STAR,
            self.MARKER_PENTAGON,
            self.MARKER_NONE
        ]
        return style in valid_styles