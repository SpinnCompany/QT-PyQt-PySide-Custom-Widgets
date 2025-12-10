# file name: QCustomLegendManager.py
from typing import List, Optional, Dict, Any
from qtpy.QtCore import Qt, Signal, QObject, QRect, QPoint
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QFont, QColor, QBrush, QPen
from qtpy.QtCharts import QChart, QLegend

from .QCustomChartConstants import QCustomChartConstants


class QCustomLegendManager(QObject, QCustomChartConstants):
    """
    Manager for chart legend customization and positioning.
    Handles legend appearance, position, and interactive features.
    """
    # Signals
    positionChanged = Signal(str)  # New position
    visibilityChanged = Signal(bool)  # Visible/invisible
    fontChanged = Signal(QFont)  # Font changed
    backgroundChanged = Signal(bool)  # Background visible/invisible
    
    def __init__(self, parent=None, chart: Optional[QChart] = None):
        super().__init__(parent)
        
        # Legend properties
        self._chart = chart
        self._legend = chart.legend() if chart else None
        self._position = self.LEGEND_BOTTOM  # Use the imported constant
        self._visible = True
        self._backgroundVisible = False
        self._fontSize = 8
        self._font = QFont()
        self._font.setPointSize(self._fontSize)
        self._alignment = Qt.AlignBottom
        self._floatingPosition = QPoint(10, 10)
        self._floatingSize = (150, 100)
        
        # Custom colors
        self._labelColor = None
        self._backgroundColor = QColor(255, 255, 255, 200)
        self._borderColor = QColor(0, 0, 0, 100)
        
        # Initialize if chart is provided
        if self._legend:
            self._initializeLegend()
    
    def _initializeLegend(self):
        """Initialize legend with default settings"""
        if not self._legend:
            return
            
        self._legend.setVisible(self._visible)
        self._legend.setBackgroundVisible(self._backgroundVisible)
        self._legend.setFont(self._font)
        self._applyPosition()
    
    def setChart(self, chart: QChart):
        """Set the chart for this legend manager"""
        self._chart = chart
        if chart:
            self._legend = chart.legend()
            self._initializeLegend()
        else:
            self._legend = None
    
    def getChart(self) -> Optional[QChart]:
        """Get the associated chart"""
        return self._chart
    
    def setPosition(self, position: str):
        """Set legend position"""
        if position != self._position and position in self.getAvailablePositions():
            self._position = position
            self._applyPosition()
            self.positionChanged.emit(position)
    
    def getPosition(self) -> str:
        """Get current legend position"""
        return self._position
    
    def getAvailablePositions(self) -> List[str]:
        """Get list of available legend positions"""
        return [
            self.LEGEND_TOP,
            self.LEGEND_BOTTOM,
            self.LEGEND_LEFT,
            self.LEGEND_RIGHT,
            self.LEGEND_FLOATING
        ]
    
    def _applyPosition(self):
        """Apply current position to legend"""
        if not self._legend:
            return
            
        if self._position == self.LEGEND_TOP:
            self._alignment = Qt.AlignTop
            self._legend.setAlignment(Qt.AlignTop)
            self._legend.attachToChart()
        elif self._position == self.LEGEND_BOTTOM:
            self._alignment = Qt.AlignBottom
            self._legend.setAlignment(Qt.AlignBottom)
            self._legend.attachToChart()
        elif self._position == self.LEGEND_LEFT:
            self._alignment = Qt.AlignLeft
            self._legend.setAlignment(Qt.AlignLeft)
            self._legend.attachToChart()
        elif self._position == self.LEGEND_RIGHT:
            self._alignment = Qt.AlignRight
            self._legend.setAlignment(Qt.AlignRight)
            self._legend.attachToChart()
        elif self._position == self.LEGEND_FLOATING:
            self._alignment = Qt.AlignLeft | Qt.AlignTop
            self._legend.setAlignment(self._alignment)
            self._legend.detachFromChart()
            self._legend.setGeometry(QRect(
                self._floatingPosition.x(),
                self._floatingPosition.y(),
                self._floatingSize[0],
                self._floatingSize[1]
            ))
        
        if self._legend:  # Add extra safety check
            self._legend.update()
    
    def setAlignment(self, alignment: Qt.Alignment):
        """Directly set legend alignment"""
        self._alignment = alignment
        if self._legend:
            self._legend.setAlignment(alignment)
            self._legend.update()
    
    def getAlignment(self) -> Qt.Alignment:
        """Get current legend alignment"""
        if self._legend:
            return self._legend.alignment()
        return self._alignment
    
    def setVisible(self, visible: bool):
        """Set legend visibility"""
        self._visible = visible
        if self._legend:
            self._legend.setVisible(visible)
        self.visibilityChanged.emit(visible)
    
    def isVisible(self) -> bool:
        """Check if legend is visible"""
        # Add check for whether the C++ object is still valid
        try:
            if self._legend and self._legend.isVisible():
                return self._legend.isVisible()
        except RuntimeError:
            # C++ object has been deleted, return the stored value
            self._legend = None
        return self._visible
    
    def setBackgroundVisible(self, visible: bool):
        """Set legend background visibility"""
        self._backgroundVisible = visible
        if self._legend:
            self._legend.setBackgroundVisible(visible)
        self.backgroundChanged.emit(visible)
    
    def isBackgroundVisible(self) -> bool:
        """Check if legend background is visible"""
        # Add check for whether the C++ object is still valid
        try:
            if self._legend and self._legend.isBackgroundVisible():
                return self._legend.isBackgroundVisible()
        except RuntimeError:
            # C++ object has been deleted, return the stored value
            self._legend = None
        return self._backgroundVisible
    
    def setFontSize(self, size: int):
        """Set legend font size"""
        self._fontSize = size
        self._font.setPointSize(size)
        if self._legend:
            self._legend.setFont(self._font)
        self.fontChanged.emit(self._font)
    
    def getFontSize(self) -> int:
        """Get legend font size"""
        return self._fontSize
    
    def setFont(self, font: QFont):
        """Set legend font"""
        self._font = font
        self._fontSize = font.pointSize()
        if self._legend:
            self._legend.setFont(font)
        self.fontChanged.emit(font)
    
    def getFont(self) -> QFont:
        """Get legend font"""
        # Add check for whether the C++ object is still valid
        try:
            if self._legend:
                return self._legend.font()
        except RuntimeError:
            # C++ object has been deleted
            self._legend = None
        return self._font
    
    def setFloatingPosition(self, x: int, y: int):
        """Set floating legend position"""
        self._floatingPosition = QPoint(x, y)
        if self._position == self.LEGEND_FLOATING and self._legend:
            try:
                geom = self._legend.geometry()
                self._legend.setGeometry(QRect(x, y, geom.width(), geom.height()))
                self._legend.update()
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def getFloatingPosition(self) -> QPoint:
        """Get floating legend position"""
        return self._floatingPosition
    
    def setFloatingSize(self, width: int, height: int):
        """Set floating legend size"""
        self._floatingSize = (width, height)
        if self._position == self.LEGEND_FLOATING and self._legend:
            try:
                pos = self._legend.geometry().topLeft()
                self._legend.setGeometry(QRect(pos.x(), pos.y(), width, height))
                self._legend.update()
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def getFloatingSize(self) -> tuple:
        """Get floating legend size"""
        return self._floatingSize
    
    def setLabelColor(self, color: QColor):
        """Set legend label color"""
        self._labelColor = color
        if self._legend:
            try:
                self._legend.setLabelColor(color)
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def getLabelColor(self) -> Optional[QColor]:
        """Get legend label color"""
        if self._legend:
            try:
                if hasattr(self._legend, 'labelColor'):
                    return self._legend.labelColor()
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
        return self._labelColor
    
    def setBackgroundColor(self, color: QColor):
        """Set legend background color"""
        self._backgroundColor = color
        if self._legend:
            try:
                if hasattr(self._legend, 'setBrush'):
                    self._legend.setBrush(QBrush(color))
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def getBackgroundColor(self) -> QColor:
        """Get legend background color"""
        return self._backgroundColor
    
    def setBorderColor(self, color: QColor):
        """Set legend border color"""
        self._borderColor = color
        if self._legend:
            try:
                if hasattr(self._legend, 'setPen'):
                    self._legend.setPen(QPen(color))
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def getBorderColor(self) -> QColor:
        """Get legend border color"""
        return self._borderColor
    
    def setBorderWidth(self, width: float):
        """Set legend border width"""
        if self._legend:
            try:
                if hasattr(self._legend, 'pen'):
                    pen = self._legend.pen()
                    pen.setWidthF(width)
                    self._legend.setPen(pen)
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def getBorderWidth(self) -> float:
        """Get legend border width"""
        if self._legend:
            try:
                if hasattr(self._legend, 'pen'):
                    return self._legend.pen().widthF()
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
        return 1.0
    
    def setMarkerSize(self, size: float):
        """Set legend marker size"""
        if self._legend:
            try:
                markers = self._legend.markers()
                for marker in markers:
                    marker.setVisible(True)  # Ensure marker is visible
                    # Note: Marker size control might need chart-specific implementation
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def hideSeriesFromLegend(self, series_names: List[str]):
        """Hide specific series from legend"""
        if not self._legend:
            return
        
        try:
            markers = self._legend.markers()
            for marker in markers:
                series = marker.series()
                if series and series.name() in series_names:
                    marker.setVisible(False)
        except RuntimeError:
            # C++ object has been deleted
            self._legend = None
    
    def showSeriesInLegend(self, series_names: List[str]):
        """Show specific series in legend"""
        if not self._legend:
            return
        
        try:
            markers = self._legend.markers()
            for marker in markers:
                series = marker.series()
                if series and series.name() in series_names:
                    marker.setVisible(True)
        except RuntimeError:
            # C++ object has been deleted
            self._legend = None
    
    def setInteractive(self, interactive: bool):
        """Set legend interactivity (click to hide/show series)"""
        if self._legend:
            try:
                self._legend.setInteractive(interactive)
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def isInteractive(self) -> bool:
        """Check if legend is interactive"""
        if self._legend:
            try:
                return self._legend.isInteractive()
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
        return False
    
    def refresh(self):
        """Refresh legend appearance"""
        if self._legend:
            try:
                self._applyPosition()
                self._legend.update()
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
    
    def getLegendInfo(self) -> Dict[str, Any]:
        """Get information about current legend state"""
        info = {
            "position": self._position,
            "visible": self._visible,
            "background_visible": self._backgroundVisible,
            "font_size": self._fontSize,
            "alignment": int(self._alignment),
            "is_floating": self._position == self.LEGEND_FLOATING,
            "floating_position": (self._floatingPosition.x(), self._floatingPosition.y()),
            "floating_size": self._floatingSize,
            "has_chart": self._chart is not None,
            "has_legend": self._legend is not None
        }
        
        if self._legend:
            try:
                info.update({
                    "marker_count": len(self._legend.markers()),
                    "interactive": self._legend.isInteractive()
                })
            except RuntimeError:
                # C++ object has been deleted
                self._legend = None
                info["has_legend"] = False
        
        return info
    
    def applyThemeColors(self, text_color: QColor, background_color: QColor):
        """Apply theme colors to legend"""
        self.setLabelColor(text_color)
        self.setBackgroundColor(background_color)
        self.setBorderColor(QColor(text_color.red(), text_color.green(), text_color.blue(), 50))
    
    def resetToDefaults(self):
        """Reset legend to default settings"""
        self._position = self.LEGEND_BOTTOM  # Use the imported constant
        self._visible = True
        self._backgroundVisible = False
        self._fontSize = 8
        self._font.setPointSize(self._fontSize)
        self._alignment = Qt.AlignBottom
        self._floatingPosition = QPoint(10, 10)
        self._floatingSize = (150, 100)
        self._labelColor = None
        self._backgroundColor = QColor(255, 255, 255, 200)
        self._borderColor = QColor(0, 0, 0, 100)
        
        self._initializeLegend()