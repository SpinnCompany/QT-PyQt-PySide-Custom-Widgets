# file name: QCustomChartBase.py
from typing import List, Dict, Any, Optional, Tuple
from qtpy.QtCore import Qt, Signal, QObject, QPointF, QTimer
from qtpy.QtWidgets import QWidget, QVBoxLayout
from qtpy.QtGui import QColor, QPainter, QPen
from qtpy.QtCharts import QChart, QChartView, QLegend

# Use relative imports for the modular structure
from .QCustomChartConstants import QCustomChartConstants
from .QCustomChartThemeManager import QCustomChartThemeManager
from .QCustomChartToolbar import QCustomChartToolbar
from .QCustomChartExporter import QCustomChartExporter
from .QCustomChartDataManager import QCustomChartDataManager
from .QCustomChartView import QCustomChartView
from .QCustomChartTooltip import QCustomChartTooltip
from .QCustomLegendManager import QCustomLegendManager


class QCustomChartBase(QWidget, QCustomChartConstants):
    """
    Abstract base class for all chart widgets.
    Provides common functionality and integration points.
    """
    
    # Common signals
    chartClicked = Signal(float, float)  # Chart coordinates
    chartHovered = Signal(float, float)  # Chart coordinates
    dataChanged = Signal()
    themeChanged = Signal(str)
    exportComplete = Signal(str, bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Core components
        self._chart = QChart()
        self._chart_view = QCustomChartView(self, self._chart)
        
        # Managers
        self._theme_manager = QCustomChartThemeManager(self)
        self._data_manager = QCustomChartDataManager(self)
        self._legend_manager = QCustomLegendManager(self, self._chart)
        self._exporter = QCustomChartExporter(self)
        self._tooltip_manager = QCustomChartTooltip(self)
        
        # Toolbar
        self._toolbar = QCustomChartToolbar(self)
        
        # Layout
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._toolbar)
        self._layout.addWidget(self._chart_view, 1)
        
        # Initialize
        self._setupConnections()
        self._applyTheme()
        
    def _setupConnections(self):
        """Setup signal connections between components"""
        # Theme manager signals
        self._theme_manager.themeChanged.connect(self._onThemeChanged)
        self._theme_manager.themeApplied.connect(self._onThemeApplied)
        
        # Toolbar signals
        self._toolbar.themeChanged.connect(self._onToolbarThemeChanged)
        self._toolbar.legendPositionChanged.connect(self._onLegendPositionChanged)
        self._toolbar.zoomInRequested.connect(self._chart_view.zoomIn)
        self._toolbar.zoomOutRequested.connect(self._chart_view.zoomOut)
        self._toolbar.resetViewRequested.connect(self._chart_view.zoomReset)
        self._toolbar.exportRequested.connect(self._exportChart)
        self._toolbar.toggleGrid.connect(self.setGridVisible)
        self._toolbar.toggleLegend.connect(self.setLegendVisible)
        self._toolbar.toggleCrosshair.connect(self._chart_view.setCrosshairVisible)
        self._toolbar.toggleTooltips.connect(self._tooltip_manager.setEnabled)
        self._toolbar.markerSizeChanged.connect(self._onMarkerSizeChanged)
        self._toolbar.animationToggled.connect(self.setAnimationEnabled)
        self._toolbar.antialiasingToggled.connect(self.setAntialiasingEnabled)
        
        # Chart view signals
        self._chart_view.mouseMoved.connect(self._onMouseMoved)
        self._chart_view.crosshairMoved.connect(self._onCrosshairMoved)
        self._chart_view.chartClicked.connect(self.chartClicked)
        self._chart_view.chartHovered.connect(self.chartHovered)
        
        # Data manager signals
        self._data_manager.dataChanged.connect(self._onDataChanged)
        self._data_manager.seriesAdded.connect(self._onSeriesAdded)
        self._data_manager.seriesRemoved.connect(self._onSeriesRemoved)
        
        # Tooltip manager signals
        self._tooltip_manager.tooltipShown.connect(self._onTooltipShown)
        self._tooltip_manager.tooltipHidden.connect(self._onTooltipHidden)
        
        # Exporter signals
        self._exporter.exportComplete.connect(self.exportComplete)
        
    def _applyTheme(self):
        """Apply current theme to chart"""
        self._theme_manager.applyTheme(self._chart)
        
        # Update crosshair color
        is_dark = self._theme_manager.isDarkTheme()
        self._chart_view.updateCrosshairTheme(is_dark)
        
        # Update legend colors
        text_color = self._theme_manager.getTextColor()
        bg_color = self._theme_manager.getBackgroundColor()
        self._legend_manager.applyThemeColors(text_color, bg_color)
        
        # Emit theme changed signal
        self.themeChanged.emit(self._theme_manager.getTheme())
    
    def _onThemeChanged(self, theme_name: str):
        """Handle theme changes from theme manager"""
        # Only update toolbar if theme is different to prevent circular updates
        current_toolbar_theme = self._toolbar.getCurrentTheme()
        if theme_name != current_toolbar_theme:
            self._toolbar.setCurrentTheme(theme_name)
        self.themeChanged.emit(theme_name)
        
    def _onThemeApplied(self, theme_name: str):
        """Handle theme applied signal"""
        # Update toolbar with current theme
        current_toolbar_theme = self._toolbar.getCurrentTheme()
        if theme_name != current_toolbar_theme:
            self._toolbar.setCurrentTheme(theme_name)
    
    def _onToolbarThemeChanged(self, theme_name: str):
        """Handle theme changes from toolbar"""
        # Only set theme if different to prevent circular updates
        current_manager_theme = self._theme_manager.getTheme()
        if theme_name != current_manager_theme:
            self._theme_manager.setTheme(theme_name)
            self._applyTheme()
        
    def _onLegendPositionChanged(self, position: str):
        """Handle legend position changes from toolbar"""
        self._legend_manager.setPosition(position)
    
    def _onMouseMoved(self, point: QPointF):
        """Handle mouse movement on chart"""
        self.chartHovered.emit(point.x(), point.y())
        
        # Update crosshair position
        if self._chart_view.isCrosshairVisible():
            self._chart_view.showCrosshairAt(point.x(), point.y())
        
        # Start tooltip hover timer
        if self._tooltip_manager.isEnabled():
            # Find closest series and data point
            closest_series, closest_point = self._findClosestDataPoint(point)
            if closest_series and closest_point:
                self._tooltip_manager.startHoverTimer(
                    closest_point[0], 
                    closest_point[1], 
                    closest_series
                )
            else:
                self._tooltip_manager.stopHoverTimer()
    
    def _onCrosshairMoved(self, x: float, y: float):
        """Handle crosshair movement"""
        # Update status or other components as needed
        pass
    
    def _onDataChanged(self, series_name: str):
        """Handle data changes"""
        self.updateChart()
        self.dataChanged.emit()
    
    def _onSeriesAdded(self, series_name: str):
        """Handle series added"""
        pass
    
    def _onSeriesRemoved(self, series_name: str):
        """Handle series removed"""
        pass
    
    def _onTooltipShown(self, x: float, y: float, series_name: str):
        """Handle tooltip shown"""
        pass
    
    def _onTooltipHidden(self):
        """Handle tooltip hidden"""
        pass
    
    def _onMarkerSizeChanged(self, size: float):
        """Handle marker size change"""
        self._data_manager.setAllMarkerSizes(size)
    
    def _findClosestDataPoint(self, point: QPointF) -> Tuple[Optional[str], Optional[Tuple[float, float]]]:
        """
        Find the closest data point to the given chart coordinates.
        To be implemented by concrete chart classes.
        """
        return None, None
    
    def _exportChart(self):
        """Export chart using exporter"""
        format = self.FORMAT_PNG  # Use constant from base class
        self._exporter.exportChart(self._chart_view, format, parent_widget=self)
    
    # ============ ABSTRACT METHODS ============
    
    def updateChart(self):
        """Update chart display - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement updateChart()")
    
    def addSeries(self, name: str, data: List[Tuple[float, float]], **kwargs):
        """Add a series - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement addSeries()")
    
    def removeSeries(self, name: str):
        """Remove a series - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement removeSeries()")
    
    # ============ PUBLIC API ============
    
    def setTheme(self, theme_name: str):
        """Set chart theme"""
        self._theme_manager.setTheme(theme_name)
        self._applyTheme()
    
    def getTheme(self) -> str:
        """Get current theme"""
        return self._theme_manager.getTheme()
    
    def setLegendPosition(self, position: str):
        """Set legend position"""
        self._legend_manager.setPosition(position)
        self._toolbar.setLegendPosition(position)
    
    def getLegendPosition(self) -> str:
        """Get legend position"""
        return self._legend_manager.getPosition()
    
    def setLegendVisible(self, visible: bool):
        """Set legend visibility"""
        self._legend_manager.setVisible(visible)
        self._toolbar.setLegendVisible(visible)
    
    def isLegendVisible(self) -> bool:
        """Check if legend is visible"""
        return self._legend_manager.isVisible()
    
    def setGridVisible(self, visible: bool):
        """Set grid visibility"""
        for axis in self._chart.axes():
            axis.setGridLineVisible(visible)
        self._toolbar.setGridVisible(visible)
    
    def isGridVisible(self) -> bool:
        """Check if grid is visible"""
        axes = self._chart.axes()
        return axes[0].isGridLineVisible() if axes else False
    
    def setCrosshairVisible(self, visible: bool):
        """Set crosshair visibility"""
        self._chart_view.setCrosshairVisible(visible)
        self._toolbar.setCrosshairVisible(visible)
    
    def isCrosshairVisible(self) -> bool:
        """Check if crosshair is visible"""
        return self._chart_view.isCrosshairVisible()
    
    def setTooltipsEnabled(self, enabled: bool):
        """Set tooltips enabled"""
        self._tooltip_manager.setEnabled(enabled)
        self._toolbar.setTooltipsEnabled(enabled)
    
    def areTooltipsEnabled(self) -> bool:
        """Check if tooltips are enabled"""
        return self._tooltip_manager.isEnabled()
    
    def setAnimationEnabled(self, enabled: bool):
        """Set animation enabled"""
        if enabled:
            self._chart.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self._chart.setAnimationOptions(QChart.NoAnimation)
        self._toolbar.setAnimationEnabled(enabled)
    
    def isAnimationEnabled(self) -> bool:
        """Check if animation is enabled"""
        return self._chart.animationOptions() != QChart.NoAnimation
    
    def setAntialiasingEnabled(self, enabled: bool):
        """Set antialiasing enabled"""
        self._chart_view.setRenderHint(QPainter.Antialiasing, enabled)
        self._toolbar.setAntialiasingEnabled(enabled)
    
    def isAntialiasingEnabled(self) -> bool:
        """Check if antialiasing is enabled"""
        return self._chart_view.renderHints() & QPainter.Antialiasing
    
    def zoomIn(self):
        """Zoom in chart"""
        self._chart_view.zoomIn()
    
    def zoomOut(self):
        """Zoom out chart"""
        self._chart_view.zoomOut()
    
    def zoomReset(self):
        """Reset chart zoom"""
        self._chart_view.zoomReset()
    
    def exportToFile(self, format: str = None, filename: str = None):
        """Export chart to file"""
        if format is None:
            format = self.FORMAT_PNG
        return self._exporter.exportChart(self._chart_view, format, filename, self)
    
    def exportToClipboard(self):
        """Export chart to clipboard"""
        return self._exporter.exportToClipboard(self._chart_view)
    
    def printChart(self):
        """Print chart"""
        return self._exporter.printChart(self._chart_view)
    
    def getSeriesNames(self) -> List[str]:
        """Get list of series names"""
        return self._data_manager.getSeriesNames()
    
    def getSeriesData(self, name: str) -> List[Tuple[float, float]]:
        """Get data for a series"""
        return self._data_manager.getSeriesData(name)
    
    def setSeriesColor(self, name: str, color: QColor):
        """Set color for a series"""
        return self._data_manager.setSeriesColor(name, color)
    
    def setSeriesVisibility(self, name: str, visible: bool):
        """Set visibility for a series"""
        return self._data_manager.setSeriesVisibility(name, visible)
    
    def clearAllData(self):
        """Clear all chart data"""
        self._data_manager.clearAllData()
        self.updateChart()
    
    def getChart(self) -> QChart:
        """Get underlying QChart object"""
        return self._chart
    
    def getChartView(self) -> QCustomChartView:  # Changed return type
        """Get chart view widget"""
        return self._chart_view
    
    def getToolbar(self) -> QCustomChartToolbar:
        """Get toolbar widget"""
        return self._toolbar
    
    def setToolbarVisible(self, visible: bool):
        """Set toolbar visibility"""
        self._toolbar.setVisible(visible)
    
    def isToolbarVisible(self) -> bool:
        """Check if toolbar is visible"""
        return self._toolbar.isVisible()
    
    def setCompactMode(self, compact: bool):
        """Set compact mode for toolbar"""
        self._toolbar.setCompactMode(compact)
    
    def isCompactMode(self) -> bool:
        """Check if compact mode is enabled"""
        return self._toolbar.isCompactMode()
    
    def setAppTheme(self, app_theme):
        """Set application theme for App Theme mode"""
        self._theme_manager.setAppTheme(app_theme)
        # Update toolbar with available themes
        self._toolbar.setAvailableThemes(self._theme_manager.getAvailableThemes())
        self._applyTheme()