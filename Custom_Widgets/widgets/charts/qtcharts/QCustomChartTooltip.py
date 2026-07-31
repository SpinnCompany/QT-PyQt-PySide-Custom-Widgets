# file name: QCustomChartTooltip.py
from typing import Optional, Dict, Any, Tuple
from qtpy.QtCore import Qt, Signal, QObject, QTimer, QPoint, QRect, QPointF
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QColor, QFont, QIcon, QPixmap, QPainter, QBrush, QCursor
from Custom_Widgets.QCustomTipOverlay import QCustomTipOverlay


class QCustomChartTooltip(QObject):
    """
    Advanced tooltip management system for charts.
    Handles tooltip display, positioning, formatting, and timing.
    """
    
    # Signals
    tooltipShown = Signal(float, float, str)  # x, y, series_name
    tooltipHidden = Signal()
    tooltipClicked = Signal(float, float, str)  # x, y, series_name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Tooltip properties
        self._enabled = True
        self._delay = 500  # ms delay before showing
        self._duration = 5000  # ms duration before auto-hide (0 = never auto-hide)
        self._currentTooltip = None
        self._lastPoint = None
        self._lastSeries = None
        
        # Formatting
        self._titleFormat = "{series} - Data Point"
        self._contentFormat = "X: {x:.2f}\nY: {y:.2f}"
        self._fontSize = 9
        self._backgroundColor = QColor(255, 255, 255, 230)
        self._textColor = QColor(0, 0, 0)
        self._borderColor = QColor(0, 0, 0, 100)
        self._highlightColor = QColor(0, 120, 215, 50)
        
        # Timer for delayed display
        self._hoverTimer = QTimer()
        self._hoverTimer.setSingleShot(True)
        self._hoverTimer.timeout.connect(self._showDelayedTooltip)
        
        # Auto-hide timer
        self._hideTimer = QTimer()
        self._hideTimer.setSingleShot(True)
        self._hideTimer.timeout.connect(self.hide)
    
    def setEnabled(self, enabled: bool):
        """Enable or disable tooltips"""
        self._enabled = enabled
        if not enabled:
            self.hide()
            self._hoverTimer.stop()
    
    def isEnabled(self) -> bool:
        """Check if tooltips are enabled"""
        return self._enabled
    
    def setDelay(self, delay_ms: int):
        """Set tooltip display delay in milliseconds"""
        self._delay = max(0, delay_ms)
    
    def getDelay(self) -> int:
        """Get tooltip display delay"""
        return self._delay
    
    def setDuration(self, duration_ms: int):
        """Set tooltip display duration in milliseconds (0 = never auto-hide)"""
        self._duration = max(0, duration_ms)
    
    def getDuration(self) -> int:
        """Get tooltip display duration"""
        return self._duration
    
    def setTitleFormat(self, format_str: str):
        """Set tooltip title format string"""
        self._titleFormat = format_str
    
    def getTitleFormat(self) -> str:
        """Get tooltip title format"""
        return self._titleFormat
    
    def setContentFormat(self, format_str: str):
        """Set tooltip content format string"""
        self._contentFormat = format_str
    
    def getContentFormat(self) -> str:
        """Get tooltip content format"""
        return self._contentFormat
    
    def setFontSize(self, size: int):
        """Set tooltip font size"""
        self._fontSize = size
    
    def getFontSize(self) -> int:
        """Get tooltip font size"""
        return self._fontSize
    
    def setColors(self, background: QColor, text: QColor, 
                 border: QColor, highlight: QColor):
        """Set tooltip colors"""
        self._backgroundColor = background
        self._textColor = text
        self._borderColor = border
        self._highlightColor = highlight
    
    def getColors(self) -> Dict[str, QColor]:
        """Get tooltip colors"""
        return {
            "background": self._backgroundColor,
            "text": self._textColor,
            "border": self._borderColor,
            "highlight": self._highlightColor
        }
    
    def startHoverTimer(self, x: float, y: float, series_name: str):
        """Start the hover timer for delayed tooltip display"""
        if not self._enabled:
            return
            
        self._lastPoint = (x, y)
        self._lastSeries = series_name
        self._hoverTimer.start(self._delay)
    
    def stopHoverTimer(self):
        """Stop the hover timer"""
        self._hoverTimer.stop()
    
    def isHoverTimerActive(self) -> bool:
        """Check if hover timer is active"""
        return self._hoverTimer.isActive()
    
    def _showDelayedTooltip(self):
        """Show tooltip after delay"""
        if self._lastPoint and self._lastSeries and self._enabled:
            self.show(self._lastPoint[0], self._lastPoint[1], self._lastSeries)
    
    def show(self, x: float, y: float, series_name: str, 
            custom_title: Optional[str] = None,
            custom_content: Optional[str] = None,
            icon: Optional[QIcon] = None,
            custom_data: Optional[Dict[str, Any]] = None):
        """
        Show a tooltip at the specified coordinates.
        
        Args:
            x, y: Chart coordinates
            series_name: Name of the series
            custom_title: Optional custom title (overrides format)
            custom_content: Optional custom content (overrides format)
            icon: Optional icon to display
            custom_data: Optional additional data for formatting
        """
        if not self._enabled:
            return
        
        # Hide any existing tooltip
        self.hide()
        
        # Format title and content
        if custom_title:
            title = custom_title
        else:
            title = self._titleFormat.format(
                series=series_name,
                x=x,
                y=y,
                **(custom_data or {})
            )
        
        if custom_content:
            content = custom_content
        else:
            content = self._contentFormat.format(
                series=series_name,
                x=x,
                y=y,
                **(custom_data or {})
            )
        
        # Create icon from series color if not provided
        if not icon and self.parent():
            # Try to get series color from parent
            try:
                if hasattr(self.parent(), '_data_manager'):
                    data_manager = getattr(self.parent(), '_data_manager')
                    color = data_manager.getSeriesColor(series_name)
                    if color:
                        icon_pixmap = QPixmap(24, 24)
                        icon_pixmap.fill(Qt.transparent)
                        painter = QPainter(icon_pixmap)
                        painter.setRenderHint(QPainter.Antialiasing)
                        painter.setBrush(QBrush(color))
                        painter.setPen(Qt.NoPen)
                        painter.drawEllipse(0, 0, 24, 24)
                        painter.end()
                        icon = QIcon(icon_pixmap)
            except:
                pass
        
        # Get parent widget for positioning
        parent_widget = None
        if self.parent():
            parent_widget = self.parent()
            
            # Try to get chart view if parent is a chart
            if hasattr(parent_widget, '_chart_view'):
                chart_view = parent_widget._chart_view
            elif hasattr(parent_widget, 'getChartView'):
                chart_view = parent_widget.getChartView()
            else:
                chart_view = None
                
            if chart_view:
                # Convert chart coordinates to screen position
                chart_coords = QPointF(x, y)
                scene_pos = chart_view.chart().mapToPosition(chart_coords)
                view_pos = chart_view.mapFromScene(scene_pos)
                
                # Adjust position to be within chart view bounds
                view_rect = chart_view.rect()
                target_pos = QPoint(
                    max(10, min(view_rect.width() - 100, view_pos.x())),
                    max(10, min(view_rect.height() - 100, view_pos.y()))
                )
                
                # Convert to global coordinates for tooltip
                global_pos = chart_view.mapToGlobal(target_pos)
                
                # Create tooltip overlay
                self._currentTooltip = QCustomTipOverlay(
                    parent=chart_view,  # Use chart view as parent
                    title=title,
                    description=content,
                    icon=icon,
                    target=target_pos,  # Use local position within chart view
                    duration=self._duration,
                    tailPosition="auto",
                    isClosable=False,
                    deleteOnClose=True,
                    toolFlag=True
                )
            else:
                # Fallback to using parent widget
                global_pos = QCursor.pos()
                local_pos = parent_widget.mapFromGlobal(global_pos)
                
                # Create tooltip overlay
                self._currentTooltip = QCustomTipOverlay(
                    parent=parent_widget,
                    title=title,
                    description=content,
                    icon=icon,
                    target=local_pos,
                    duration=self._duration,
                    tailPosition="auto",
                    isClosable=False,
                    deleteOnClose=True,
                    toolFlag=True
                )
        else:
            # No parent widget, use cursor position
            global_pos = QCursor.pos()
            main_window = QApplication.activeWindow()
            
            if main_window:
                local_pos = main_window.mapFromGlobal(global_pos)
                self._currentTooltip = QCustomTipOverlay(
                    parent=main_window,
                    title=title,
                    description=content,
                    icon=icon,
                    target=local_pos,
                    duration=self._duration,
                    tailPosition="auto",
                    isClosable=False,
                    deleteOnClose=True,
                    toolFlag=True
                )
        
        if self._currentTooltip:
            # Apply custom colors if needed
            if self._backgroundColor != QColor(255, 255, 255, 230):
                # Note: QCustomTipOverlay might need color customization methods
                pass
            
            # Connect signals
            self._currentTooltip.closed.connect(self._onTooltipClosed)
            
            # Show tooltip
            self._currentTooltip.show()
            
            # Start auto-hide timer if duration > 0
            if self._duration > 0:
                self._hideTimer.start(self._duration)
            
            # Emit signal
            self.tooltipShown.emit(x, y, series_name)
    
    def hide(self):
        """Hide the current tooltip"""
        if self._currentTooltip:
            self._currentTooltip.close()
            self._currentTooltip = None
        
        self._hideTimer.stop()
        self.tooltipHidden.emit()
    
    def _onTooltipClosed(self):
        """Handle tooltip closed signal"""
        self._currentTooltip = None
        self.tooltipHidden.emit()
    
    def updatePosition(self, x: float, y: float):
        """Update tooltip position (for following mouse)"""
        if self._currentTooltip and self._lastSeries and self.parent():
            parent_widget = self.parent()
            
            if hasattr(parent_widget, '_chart_view'):
                chart_view = parent_widget._chart_view
                # Convert chart coordinates to screen position
                chart_coords = QPointF(x, y)
                scene_pos = chart_view.chart().mapToPosition(chart_coords)
                view_pos = chart_view.mapFromScene(scene_pos)
                
                # Adjust position to be within chart view bounds
                view_rect = chart_view.rect()
                target_pos = QPoint(
                    max(10, min(view_rect.width() - 100, view_pos.x())),
                    max(10, min(view_rect.height() - 100, view_pos.y()))
                )
                
                # Update the tooltip position
                try:
                    self._currentTooltip.setTargetPosition(target_pos)
                except:
                    pass
    
    def isVisible(self) -> bool:
        """Check if a tooltip is currently visible"""
        return self._currentTooltip is not None and self._currentTooltip.isVisible()
    
    def getCurrentTooltipInfo(self) -> Optional[Dict[str, Any]]:
        """Get information about current tooltip"""
        if not self._currentTooltip:
            return None
        
        return {
            "x": self._lastPoint[0] if self._lastPoint else 0,
            "y": self._lastPoint[1] if self._lastPoint else 0,
            "series": self._lastSeries,
            "visible": self.isVisible()
        }
    
    def setFormatFromTemplate(self, template_name: str):
        """Set formatting from a predefined template"""
        templates = {
            "simple": {
                "title": "{series}",
                "content": "X: {x:.2f}, Y: {y:.2f}",
                "font_size": 9
            },
            "detailed": {
                "title": "Data Point - {series}",
                "content": "Coordinates:\n  X: {x:.4f}\n  Y: {y:.4f}",
                "font_size": 8
            },
            "minimal": {
                "title": "",
                "content": "({x:.1f}, {y:.1f})",
                "font_size": 8
            }
        }
        
        if template_name in templates:
            template = templates[template_name]
            self._titleFormat = template["title"]
            self._contentFormat = template["content"]
            self._fontSize = template["font_size"]
    
    def createCustomFormat(self, title: str, content: str, 
                          font_size: int = None,
                          colors: Dict[str, QColor] = None):
        """Create a custom tooltip format"""
        self._titleFormat = title
        self._contentFormat = content
        
        if font_size:
            self._fontSize = font_size
        
        if colors:
            self.setColors(
                colors.get("background", self._backgroundColor),
                colors.get("text", self._textColor),
                colors.get("border", self._borderColor),
                colors.get("highlight", self._highlightColor)
            )
    
    def resetToDefaults(self):
        """Reset tooltip to default settings"""
        self._enabled = True
        self._delay = 500
        self._duration = 5000
        self._titleFormat = "{series} - Data Point"
        self._contentFormat = "X: {x:.2f}\nY: {y:.2f}"
        self._fontSize = 9
        self._backgroundColor = QColor(255, 255, 255, 230)
        self._textColor = QColor(0, 0, 0)
        self._borderColor = QColor(0, 0, 0, 100)
        self._highlightColor = QColor(0, 120, 215, 50)
        
        self.hide()
        self._hoverTimer.stop()
        self._hideTimer.stop()