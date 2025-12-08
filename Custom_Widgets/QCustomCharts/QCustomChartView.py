# file name: QCustomChartView.py
from typing import Optional, Tuple, Any
from qtpy.QtCore import Qt, QPointF, QTimer, QEvent, Signal, QRectF
from qtpy.QtWidgets import QGraphicsView, QApplication
from qtpy.QtGui import QPainter, QPen, QColor, QBrush, QCursor
from qtpy.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QBarCategoryAxis


class QCustomChartView(QChartView):
    """
    Enhanced QChartView with crosshair functionality, mouse tracking,
    and common chart interaction features.
    """
    
    # Signals
    mouseMoved = Signal(QPointF)  # Chart coordinates when mouse moves
    mouseEntered = Signal()
    mouseLeft = Signal()
    crosshairMoved = Signal(float, float)  # x, y chart coordinates
    chartClicked = Signal(float, float)  # x, y chart coordinates
    chartHovered = Signal(float, float)  # x, y chart coordinates
    viewportEntered = Signal()  # New signal for mouse enter
    viewportLeft = Signal()  # New signal for mouse leave
    
    def __init__(self, parent=None, chart: Optional[QChart] = None):
        """
        Initialize the custom chart view.
        
        Args:
            parent: Parent widget
            chart: Optional QChart instance to display
        """
        if chart:
            super().__init__(chart, parent)
        else:
            super().__init__(parent)
            self.setChart(QChart())
        
        # Crosshair properties
        self._showCrosshair = True
        self._crosshairVisible = False
        self._currentMousePoint = QPointF(0, 0)
        
        # Crosshair lines
        self._verticalLine = QLineSeries()
        self._horizontalLine = QLineSeries()
        self._crosshairPen = QPen()
        self._crosshairPen.setWidthF(1.0)
        self._crosshairPen.setStyle(Qt.DotLine)
        self._crosshairPen.setColor(QColor(0, 0, 0, 180))
        
        # Mouse tracking
        self.setMouseTracking(True)
        self.setRubberBand(QChartView.RectangleRubberBand)
        
        # Tooltip delay timer
        self._hoverTimer = QTimer()
        self._hoverTimer.setSingleShot(True)
        self._hoverDelay = 500  # ms
        
        # Initialize crosshair
        self._setupCrosshair()
        
        # Apply default settings
        self.setRenderHint(QPainter.Antialiasing, True)
        if chart:
            chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Initialize viewport tracking
        self._isMouseInViewport = False
    
    def _setupCrosshair(self):
        """Setup crosshair lines with initial positions"""
        # Configure crosshair lines - set names to hide from legend
        self._verticalLine.setName("__vertical_crosshair")
        self._horizontalLine.setName("__horizontal_crosshair")
        self._verticalLine.setObjectName("__vertical_crosshair")
        self._horizontalLine.setObjectName("__horizontal_crosshair")
        
        # Set initial empty data
        self._verticalLine.append(0, 0)
        self._verticalLine.append(0, 1)
        self._horizontalLine.append(0, 0)
        self._horizontalLine.append(1, 0)
        
        # Apply crosshair pen
        self._verticalLine.setPen(self._crosshairPen)
        self._horizontalLine.setPen(self._crosshairPen)
    
    def setCrosshairVisible(self, visible: bool):
        """Set crosshair visibility"""
        self._showCrosshair = visible
        if not visible:
            self._hideCrosshair()
    
    def _hideCrosshair(self):
        """Hide crosshair"""
        self._verticalLine.setVisible(False)
        self._horizontalLine.setVisible(False)
        self._crosshairVisible = False
        
        # Ensure crosshair is hidden from legend
        self._hideCrosshairFromLegend()
    
    def _hideCrosshairFromLegend(self):
        """Hide crosshair series from the legend"""
        if self.chart():
            legend = self.chart().legend()
            if legend:
                markers = legend.markers()
                for marker in markers:
                    series = marker.series()
                    if series and series.name() in ["__vertical_crosshair", "__horizontal_crosshair"]:
                        marker.setVisible(False)
    
    def isCrosshairVisible(self) -> bool:
        """Get crosshair visibility"""
        return self._showCrosshair
    
    def setCrosshairColor(self, color: QColor):
        """Set crosshair line color"""
        self._crosshairPen.setColor(color)
        self._verticalLine.setPen(self._crosshairPen)
        self._horizontalLine.setPen(self._crosshairPen)
    
    def setCrosshairWidth(self, width: float):
        """Set crosshair line width"""
        self._crosshairPen.setWidthF(width)
        self._verticalLine.setPen(self._crosshairPen)
        self._horizontalLine.setPen(self._crosshairPen)
    
    def setCrosshairStyle(self, style: Qt.PenStyle):
        """Set crosshair line style"""
        self._crosshairPen.setStyle(style)
        self._verticalLine.setPen(self._crosshairPen)
        self._horizontalLine.setPen(self._crosshairPen)
    
    def showCrosshairAt(self, x: float, y: float):
        """Manually show crosshair at specific chart coordinates"""
        self._currentMousePoint = QPointF(x, y)
        self._updateCrosshair(QPointF(x, y), True)
    
    def hideCrosshair(self):
        """Manually hide crosshair"""
        self._updateCrosshair(None, False)
    
    # file name: QCustomChartView.py

    def _updateCrosshair(self, point: Optional[QPointF], state: bool):
        """Update crosshair position based on mouse point"""
        if state and point and self._showCrosshair:
            # Check if point is within valid chart coordinates
            if not self._isPointInChartBounds(point):
                self._hideCrosshair()
                return
            
            # Store the current mouse point
            self._currentMousePoint = point
            self._crosshairVisible = True
            
            # Get axis ranges
            x_min, x_max = self._getAxisRange(Qt.Horizontal)
            y_min, y_max = self._getAxisRange(Qt.Vertical)
            
            if x_min is not None and x_max is not None and y_min is not None and y_max is not None:
                # Handle string categories for bar charts
                try:
                    # Try to convert x_min and x_max to floats
                    if isinstance(x_min, str) or isinstance(x_max, str):
                        # For bar charts, use numeric positions
                        # Categories are at integer positions (0, 1, 2, ...)
                        categories = self._getCategories()
                        if categories:
                            # Use numeric positions for crosshair
                            num_categories = len(categories)
                            x_min_val = 0 - 0.5  # Start before first category
                            x_max_val = num_categories - 0.5  # End after last category
                        else:
                            x_min_val = 0
                            x_max_val = 1
                    else:
                        # For numeric axes, use the values directly
                        x_min_val = float(x_min)
                        x_max_val = float(x_max)
                    
                    # Convert y values to float
                    y_min_val = float(y_min)
                    y_max_val = float(y_max)
                    
                    # Clear existing points
                    self._verticalLine.clear()
                    self._horizontalLine.clear()
                    
                    # Update vertical line (x = point.x(), y from min to max)
                    # Use QPointF objects for better compatibility
                    self._verticalLine.append(QPointF(point.x(), y_min_val))
                    self._verticalLine.append(QPointF(point.x(), y_max_val))
                    
                    # Update horizontal line (y = point.y(), x from min to max)
                    self._horizontalLine.append(QPointF(x_min_val, point.y()))
                    self._horizontalLine.append(QPointF(x_max_val, point.y()))
                    
                except Exception as e:
                    print(f"Error updating crosshair: {e}")
                    # Fallback to simple numeric values
                    self._verticalLine.clear()
                    self._horizontalLine.clear()
                    self._verticalLine.append(QPointF(0, 0))
                    self._verticalLine.append(QPointF(0, 1))
                    self._horizontalLine.append(QPointF(0, 0))
                    self._horizontalLine.append(QPointF(1, 0))
                
                # Show crosshair if lines are attached to chart
                if self.chart():
                    if self._verticalLine not in self.chart().series():
                        self.chart().addSeries(self._verticalLine)
                        # Attach to axes
                        for axis in self.chart().axes():
                            self._verticalLine.attachAxis(axis)
                    
                    if self._horizontalLine not in self.chart().series():
                        self.chart().addSeries(self._horizontalLine)
                        # Attach to axes
                        for axis in self.chart().axes():
                            self._horizontalLine.attachAxis(axis)
                
                # Show lines
                self._verticalLine.setVisible(True)
                self._horizontalLine.setVisible(True)
                
                # Hide from legend
                self._hideCrosshairFromLegend()
                
                # Emit signal
                self.crosshairMoved.emit(point.x(), point.y())
        else:
            # Hide crosshair when mouse leaves or crosshair disabled
            self._verticalLine.setVisible(False)
            self._horizontalLine.setVisible(False)
            self._crosshairVisible = False

    def _isPointInChartBounds(self, point: QPointF) -> bool:
        """Check if point is within chart bounds"""
        try:
            x_min, x_max = self._getAxisRange(Qt.Horizontal)
            y_min, y_max = self._getAxisRange(Qt.Vertical)
            
            if x_min is None or x_max is None or y_min is None or y_max is None:
                return False
            
            # Handle string categories for bar charts
            if isinstance(x_min, str) or isinstance(x_max, str):
                # For bar charts with category axes, we need to check differently
                # Get the chart to check axis type
                chart = self.chart()
                if chart:
                    axes = chart.axes(Qt.Horizontal)
                    if axes and isinstance(axes[0], QBarCategoryAxis):
                        # Bar chart - check if x is within category range
                        # Categories are at integer positions (0, 1, 2, ...)
                        x_val = point.x()
                        return (0 <= x_val <= len(self._getCategories()) - 0.5) and (y_min <= point.y() <= y_max)
            
            # Regular numeric comparison for line charts
            return (x_min <= point.x() <= x_max) and (y_min <= point.y() <= y_max)
            
        except Exception as e:
            print(f"Error in _isPointInChartBounds: {e}")
            return False

    def _getCategories(self):
        """Get categories from bar chart axis if available"""
        chart = self.chart()
        if chart:
            axes = chart.axes(Qt.Horizontal)
            if axes and isinstance(axes[0], QBarCategoryAxis):
                axis = axes[0]
                categories = []
                for i in range(axis.count()):
                    categories.append(axis.at(i))
                return categories
        return []
    
    def _getAxisRange(self, orientation: Qt.Orientation) -> Tuple[Optional[Any], Optional[Any]]:
        """Get the current axis range for specified orientation"""
        chart = self.chart()
        if not chart:
            return None, None
            
        for axis in chart.axes():
            if axis.orientation() == orientation:
                # Check if it's a category axis
                if hasattr(axis, 'categories') and callable(getattr(axis, 'categories')):
                    # For category axis, return string values
                    categories = axis.categories()
                    if categories:
                        return categories[0], categories[-1]
                    else:
                        return None, None
                else:
                    # For value axis, return numeric values
                    return axis.min(), axis.max()
        return None, None
    
    def setChart(self, chart: QChart):
        """Override setChart to ensure crosshair lines are properly attached"""
        # Remove crosshair lines from old chart
        old_chart = self.chart()
        if old_chart:
            old_chart.removeSeries(self._verticalLine)
            old_chart.removeSeries(self._horizontalLine)
        
        # Set new chart
        super().setChart(chart)
        
        # Add crosshair lines to new chart
        if chart:
            chart.addSeries(self._verticalLine)
            chart.addSeries(self._horizontalLine)
            
            # Attach to axes
            for axis in chart.axes():
                self._verticalLine.attachAxis(axis)
                self._horizontalLine.attachAxis(axis)
            
            # Initially hide crosshair
            self._verticalLine.setVisible(False)
            self._horizontalLine.setVisible(False)
            
            # Hide from legend
            self._hideCrosshairFromLegend()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events for crosshair"""
        # First, check if mouse is actually in viewport
        if not self.rect().contains(event.pos()):
            if self._isMouseInViewport:
                self._isMouseInViewport = False
                self.mouseLeft.emit()
                self.viewportLeft.emit()
                self._updateCrosshair(None, False)
            return
        
        if not self._isMouseInViewport:
            self._isMouseInViewport = True
            self.mouseEntered.emit()
            self.viewportEntered.emit()
        
        # Convert to chart coordinates
        chart_pos = self.mapToScene(event.pos())
        try:
            chart_coords = self.chart().mapToValue(chart_pos)
        except Exception as e:
            # Handle mapping errors (e.g., invalid position)
            chart_coords = QPointF(0, 0)
        
        # Check if coordinates are valid
        if not self._isValidChartPoint(chart_coords):
            self._updateCrosshair(None, False)
            return
        
        # Emit signal with chart coordinates
        self.mouseMoved.emit(chart_coords)
        self.chartHovered.emit(chart_coords.x(), chart_coords.y())
        
        # Update crosshair if enabled
        if self._showCrosshair:
            self._updateCrosshair(chart_coords, True)
        
        super().mouseMoveEvent(event)
    
    def _isValidChartPoint(self, point: QPointF) -> bool:
        """Check if point is valid (not NaN or infinite)"""
        import math
        return not (math.isnan(point.x()) or math.isnan(point.y()) or 
                   math.isinf(point.x()) or math.isinf(point.y()))
    
    def mousePressEvent(self, event):
        """Handle mouse click events"""
        if event.button() == Qt.LeftButton:
            # Convert to chart coordinates
            chart_pos = self.mapToScene(event.pos())
            chart_coords = self.chart().mapToValue(chart_pos)
            
            # Only emit if valid point
            if self._isValidChartPoint(chart_coords):
                self.chartClicked.emit(chart_coords.x(), chart_coords.y())
        
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        """Handle mouse enter events"""
        self._isMouseInViewport = True
        self.mouseEntered.emit()
        self.viewportEntered.emit()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave events"""
        self._isMouseInViewport = False
        self.mouseLeft.emit()
        self.viewportLeft.emit()
        if self._showCrosshair:
            self._updateCrosshair(None, False)
        super().leaveEvent(event)
    
    def zoomIn(self):
        """Zoom in chart"""
        self.chart().zoomIn()
        # Update crosshair if visible
        if self._crosshairVisible:
            self._updateCrosshair(self._currentMousePoint, True)
    
    def zoomOut(self):
        """Zoom out chart"""
        self.chart().zoomOut()
        # Update crosshair if visible
        if self._crosshairVisible:
            self._updateCrosshair(self._currentMousePoint, True)
    
    def zoomReset(self):
        """Reset chart zoom"""
        self.chart().zoomReset()
        # Update crosshair if visible
        if self._crosshairVisible:
            self._updateCrosshair(self._currentMousePoint, True)
    
    def setRenderHints(self, antialiasing: bool = True, smooth_pixmap: bool = False):
        """Set rendering hints"""
        hints = QPainter.Antialiasing if antialiasing else 0
        if smooth_pixmap:
            hints |= QPainter.SmoothPixmapTransform
        self.setRenderHint(QPainter.RenderHint(hints))
    
    def getCurrentMousePoint(self) -> QPointF:
        """Get the current mouse position in chart coordinates"""
        return self._currentMousePoint
    
    def isCrosshairShowing(self) -> bool:
        """Check if crosshair is currently visible"""
        return self._crosshairVisible
    
    def getCrosshairPen(self) -> QPen:
        """Get the current crosshair pen"""
        return self._crosshairPen
    
    def updateCrosshairTheme(self, is_dark_theme: bool):
        """Update crosshair color based on theme"""
        if is_dark_theme:
            # Dark themes - use light crosshair
            crosshair_color = QColor(255, 255, 255, 200)
        else:
            # Light themes - use dark crosshair
            crosshair_color = QColor(0, 0, 0, 200)
        
        self.setCrosshairColor(crosshair_color)
    
    def setHoverDelay(self, delay_ms: int):
        """Set hover delay for tooltips"""
        self._hoverDelay = max(0, delay_ms)
    
    def getHoverDelay(self) -> int:
        """Get hover delay for tooltips"""
        return self._hoverDelay
    
    def startHoverTimer(self):
        """Start the hover timer"""
        self._hoverTimer.start(self._hoverDelay)
    
    def stopHoverTimer(self):
        """Stop the hover timer"""
        self._hoverTimer.stop()
    
    def isHoverTimerActive(self) -> bool:
        """Check if hover timer is active"""
        return self._hoverTimer.isActive()
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        # Update crosshair if visible
        if self._crosshairVisible:
            self._updateCrosshair(self._currentMousePoint, True)