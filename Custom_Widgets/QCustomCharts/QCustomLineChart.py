# file name: QCustomLineChart.py
from typing import List, Tuple, Optional, Dict, Any
from qtpy.QtCore import Qt, QPointF, Signal, Property, QRect
from qtpy.QtGui import QColor, QPen, QPainter, QPalette
from qtpy.QtCharts import QChart, QLineSeries, QScatterSeries, QValueAxis

from .QCustomChartBase import QCustomChartBase
from .QCustomChartDataManager import QCustomChartDataManager
from .QCustomQLineSeries import QCustomQLineSeries
from Custom_Widgets.Utils import is_in_designer


class QCustomLineChart(QCustomChartBase):
    """
    Line chart implementation using the modular architecture.
    Qt Designer compatible with property exposure.
    """
    
    # Designer registration constants
    WIDGET_ICON = "components/icons/line_chart.png"
    WIDGET_TOOLTIP = "Customizable line series chart with advanced styling"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomLineChart' name='customLineChart'>
            <property name='geometry'>
                <rect>
                    <x>0</x>
                    <y>0</y>
                    <width>600</width>
                    <height>400</height>
                </rect>
            </property>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomCharts"
    
    # Additional signals for line chart
    dataPointClicked = Signal(float, float, str)  # x, y, series_name
    dataPointHovered = Signal(float, float, str)  # x, y, series_name
    seriesAdded = Signal(str)
    seriesRemoved = Signal(str)
    chartExportComplete = Signal(str, bool)  # filename, success
    legendPositionChanged = Signal(str)  # New signal for legend position changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Line series factory
        self._line_series_factory = QCustomQLineSeries(self)
        
        # Chart configuration
        self._chart.setTitle("Line Chart")
        self._chart.legend().setVisible(True)
        
        # Initialize axes
        self._axis_x = QValueAxis()
        self._axis_x.setTitleText("X Axis")
        self._axis_x.setGridLineVisible(True)
        self._chart.addAxis(self._axis_x, Qt.AlignBottom)
        
        self._axis_y = QValueAxis()
        self._axis_y.setTitleText("Y Axis")
        self._axis_y.setGridLineVisible(True)
        self._chart.addAxis(self._axis_y, Qt.AlignLeft)
        
        # Additional properties for Designer
        self._chart_title = "Line Chart"
        self._x_axis_title = "X Axis"
        self._y_axis_title = "Y Axis"
        self._show_grid = True
        self._auto_scale = True
        self._animation_enabled = True
        self._animation_duration = 1000
        self._antialiasing = True
        self._show_data_points = True
        self._fill_area = False
        self._enable_shadow = False
        self._highlight_size = 8
        self._shadow_blur = 15
        self._fill_opacity = 0.3
        self._grid_color = QColor(200, 200, 200, 100)
        self._show_footer = True
        
        # Crosshair properties
        self._crosshair_color = QColor(0, 0, 0, 180)
        self._crosshair_width = 1.0
        
        # Tooltip properties
        self._tooltip_delay = 500
        self._tooltip_duration = 5000
        
        # Legend properties
        self._legend_font_size = 8
        self._legend_background_visible = False
        
        # IMPORTANT: Set available themes BEFORE setting the theme
        self._toolbar.setAvailableThemes(self._theme_manager.getAvailableThemes())
        
        # Set initial theme to App Theme
        self._theme_manager.setTheme(self.THEME_APP_THEME)
        self._applyTheme()
        
        # Connect additional signals
        self.chartClicked.connect(self._onChartClicked)
        self.chartHovered.connect(self._onChartHovered)
        self._data_manager.seriesAdded.connect(self.seriesAdded)
        self._data_manager.seriesRemoved.connect(self.seriesRemoved)
        self._exporter.exportComplete.connect(self.chartExportComplete)
        self._legend_manager.positionChanged.connect(self.legendPositionChanged)
        
        # Add dummy data if in designer mode
        self._addDummyDataForDesigner()

    def _addDummyDataForDesigner(self):
        """Add dummy data when running in Qt Designer"""
        if is_in_designer(self):
            # Generate dummy data
            self._data_manager.addDummyData(num_series=3, num_points=20)
            
            # Update the chart display
            self.updateChart()
            
            # Set nice chart title for designer
            self._chart.setTitle("Line Chart Preview (Designer Mode)")
            self._axis_x.setTitleText("X Axis - Dummy Data")
            self._axis_y.setTitleText("Y Axis - Dummy Data")
            
            print("Designer mode detected - showing dummy chart data")
    
    def generateExampleData(self, example_type: str = "sine_wave"):
        """
        Generate example data for testing.
        
        Args:
            example_type: Type of example data to generate
                Options: "sine_wave", "cosine_wave", "exponential", 
                         "logarithmic", "random", "all"
        """
        import math
        import random
        from qtpy.QtGui import QColor
        
        # Clear existing data first
        self.clearAllData()
        
        example_types = []
        if example_type == "all":
            example_types = ["sine_wave", "cosine_wave", "exponential", "random"]
        else:
            example_types = [example_type]
        
        colors = [
            QColor(255, 100, 100),    # Red
            QColor(100, 200, 100),    # Green
            QColor(100, 150, 255),    # Blue
            QColor(200, 100, 200),    # Purple
            QColor(255, 150, 50),     # Orange
        ]
        
        line_styles = ["solid", "dash", "dot", "dash_dot"]
        marker_styles = ["circle", "rectangle", "triangle", "star"]
        
        for i, ex_type in enumerate(example_types):
            data = []
            series_name = ex_type.replace("_", " ").title()
            
            if ex_type == "sine_wave":
                for j in range(20):
                    x = j * 0.5
                    y = 20 * math.sin(x * math.pi / 5)
                    data.append((x, y))
                    
            elif ex_type == "cosine_wave":
                for j in range(20):
                    x = j * 0.5
                    y = 20 * math.cos(x * math.pi / 5)
                    data.append((x, y))
                    
            elif ex_type == "exponential":
                for j in range(20):
                    x = j * 0.3
                    y = math.exp(x / 3)
                    data.append((x, y))
                    
            elif ex_type == "logarithmic":
                for j in range(1, 20):
                    x = j * 0.5
                    y = 10 * math.log(x + 1)
                    data.append((x, y))
                    
            elif ex_type == "random":
                base = random.uniform(10, 30)
                for j in range(20):
                    x = j * 1.0
                    y = base + random.uniform(-10, 10)
                    data.append((x, y))
            
            else:
                # Default to sine wave
                for j in range(20):
                    x = j * 0.5
                    y = 20 * math.sin(x * math.pi / 5)
                    data.append((x, y))
            
            # Add the series
            color_idx = i % len(colors)
            line_style_idx = i % len(line_styles)
            marker_style_idx = i % len(marker_styles)
            
            self.addSeries(
                name=series_name,
                data=data,
                color=colors[color_idx],
                visible=True,
                line_style=line_styles[line_style_idx],
                line_width=2.0 + (i * 0.5),
                marker_style=marker_styles[marker_style_idx],
                marker_size=8.0 + (i * 2)
            )
        
        # Update the chart
        self.updateChart()
        self._chart.setTitle(f"Example: {example_type.replace('_', ' ').title()}")
        
    def _onChartClicked(self, x: float, y: float):
        """Handle chart click and emit dataPointClicked"""
        closest_series, closest_point = self._findClosestDataPoint(QPointF(x, y))
        if closest_series and closest_point:
            self.dataPointClicked.emit(closest_point[0], closest_point[1], closest_series)
    
    def _onChartHovered(self, x: float, y: float):
        """Handle chart hover and emit dataPointHovered"""
        closest_series, closest_point = self._findClosestDataPoint(QPointF(x, y))
        if closest_series and closest_point:
            self.dataPointHovered.emit(closest_point[0], closest_point[1], closest_series)
        
    def updateChart(self):
        """Update the chart display based on current data"""
        # Clear existing series (except crosshair)
        series_to_remove = []
        for series in self._chart.series():
            if series.name() not in ["__vertical_crosshair", "__horizontal_crosshair"]:
                series_to_remove.append(series)
        
        for series in series_to_remove:
            self._chart.removeSeries(series)
        
        # Create series from data manager
        series_data = self._data_manager.getVisibleSeriesData()
        
        # Track bounds for auto-scaling
        all_x = []
        all_y = []
        
        for series_name, data_points in series_data.items():
            if not data_points:
                continue
            
            # Create line series
            line_series = self._createLineSeries(series_name, data_points)
            self._chart.addSeries(line_series)
            line_series.attachAxis(self._axis_x)
            line_series.attachAxis(self._axis_y)
            
            # Add markers if enabled
            marker_style = self._data_manager.getSeriesMarkerStyle(series_name)
            if marker_style != self.MARKER_NONE and self._show_data_points:
                marker_series = self._createMarkerSeries(series_name, data_points)
                self._chart.addSeries(marker_series)
                marker_series.attachAxis(self._axis_x)
                marker_series.attachAxis(self._axis_y)
            
            # Update bounds
            x_vals = [p[0] for p in data_points]
            y_vals = [p[1] for p in data_points]
            all_x.extend(x_vals)
            all_y.extend(y_vals)
        
        # Auto-scale if data exists
        if all_x and all_y and self._auto_scale:
            x_min, x_max = min(all_x), max(all_x)
            y_min, y_max = min(all_y), max(all_y)
            
            margin = 0.05
            x_range = x_max - x_min
            y_range = y_max - y_min
            
            self._axis_x.setRange(
                x_min - x_range * margin,
                x_max + x_range * margin
            )
            self._axis_y.setRange(
                y_min - y_range * margin,
                y_max + y_range * margin
            )
        
        # Set axis titles
        self._axis_x.setTitleText(self._x_axis_title)
        self._axis_y.setTitleText(self._y_axis_title)
        
        # Set chart title
        self._chart.setTitle(self._chart_title)
        
        # Set grid visibility and color
        self._axis_x.setGridLineVisible(self._show_grid)
        self._axis_y.setGridLineVisible(self._show_grid)
        self._axis_x.setGridLineColor(self._grid_color)
        self._axis_y.setGridLineColor(self._grid_color)
        
        # Set animation
        if self._animation_enabled:
            self._chart.setAnimationOptions(QChart.SeriesAnimations)
            self._chart.setAnimationDuration(self._animation_duration)
        else:
            self._chart.setAnimationOptions(QChart.NoAnimation)
        
        # Set antialiasing
        self._chart_view.setRenderHint(QPainter.Antialiasing, self._antialiasing)
        
        # Update legend
        self._updateLegendSettings()
    
    def _createLineSeries(self, name: str, data: List[Tuple[float, float]]) -> QLineSeries:
        """Create a styled line series"""
        # Get series properties
        color = self._data_manager.getSeriesColor(name)
        line_width = self._data_manager.getSeriesLineWidth(name)
        line_style = self._data_manager.getSeriesLineStyle(name)
        
        # Create series using factory
        series = self._line_series_factory.createLineSeries(
            name=name,
            data=data,
            color=color,
            line_width=line_width,
            line_style=line_style,
            visible=True
        )
        
        return series
    
    def _createMarkerSeries(self, name: str, data: List[Tuple[float, float]]) -> QScatterSeries:
        """Create a marker series"""
        # Get series properties
        color = self._data_manager.getSeriesColor(name)
        marker_size = self._data_manager.getSeriesMarkerSize(name)
        marker_style = self._data_manager.getSeriesMarkerStyle(name)
        
        # Create markers using factory
        series = self._line_series_factory.createMarkerSeries(
            name=f"{name}_markers",
            data=data,
            color=color,
            marker_size=marker_size,
            marker_style=marker_style,
            visible=True
        )
        
        return series
    
    def _findClosestDataPoint(self, point: QPointF) -> Tuple[Optional[str], Optional[Tuple[float, float]]]:
        """
        Find the closest data point to the given chart coordinates.
        """
        if not self._isPointInChartBounds(point):
            return None, None
            
        closest_distance = float('inf')
        closest_series = None
        closest_point = None
        
        # Search through all series data
        series_data = self._data_manager.getAllData()
        for series_name, data_points in series_data.items():
            for data_point in data_points:
                dx = data_point[0] - point.x()
                dy = data_point[1] - point.y()
                distance = dx*dx + dy*dy  # Squared distance for comparison
                
                if distance < closest_distance:
                    closest_distance = distance
                    closest_series = series_name
                    closest_point = data_point
        
        # Check if close enough (within reasonable threshold)
        if closest_distance < 0.1:  # 0.1 units squared
            return closest_series, closest_point
        
        return None, None
    
    def _isPointInChartBounds(self, point: QPointF) -> bool:
        """Check if point is within chart bounds"""
        try:
            x_min, x_max = self._axis_x.min(), self._axis_x.max()
            y_min, y_max = self._axis_y.min(), self._axis_y.max()
            
            return (x_min <= point.x() <= x_max) and (y_min <= point.y() <= y_max)
        except:
            return False
    
    def _updateLegendSettings(self):
        """Update legend settings"""
        legend = self._chart.legend()
        if legend:
            font = legend.font()
            font.setPointSize(self._legend_font_size)
            legend.setFont(font)
            legend.setBackgroundVisible(self._legend_background_visible)
    
    # ============ PUBLIC API ============
    
    def addSeries(self, name: str, data: List[Tuple[float, float]], 
                 color: Optional[QColor] = None,
                 visible: bool = True,
                 line_style: str = "solid",
                 line_width: float = 2.0,
                 marker_style: str = "none",
                 marker_size: float = None,
                 **kwargs) -> bool:
        """
        Add a line series to the chart.
        """
        success = self._data_manager.addSeries(
            name=name,
            data=data,
            color=color,
            visible=visible,
            line_style=line_style,
            line_width=line_width,
            marker_style=marker_style,
            marker_size=marker_size
        )
        
        if success:
            self.updateChart()
        
        return success
    
    def removeSeries(self, name: str) -> bool:
        """Remove a series from the chart"""
        success = self._data_manager.removeSeries(name)
        if success:
            self.updateChart()
        return success
    
    def updateSeriesData(self, name: str, data: List[Tuple[float, float]]) -> bool:
        """Update data for an existing series"""
        success = self._data_manager.updateSeriesData(name, data)
        if success:
            self.updateChart()
        return success
    
    def appendToSeries(self, name: str, points: List[Tuple[float, float]]) -> bool:
        """Append points to an existing series"""
        success = self._data_manager.appendToSeries(name, points)
        if success:
            self.updateChart()
        return success
    
    def setSeriesLineStyle(self, name: str, style: str) -> bool:
        """Set line style for a series"""
        success = self._data_manager.setSeriesLineStyle(name, style)
        if success:
            self.updateChart()
        return success
    
    def setSeriesMarkerStyle(self, name: str, style: str) -> bool:
        """Set marker style for a series"""
        success = self._data_manager.setSeriesMarkerStyle(name, style)
        if success:
            self.updateChart()
        return success
    
    def setSeriesLineWidth(self, name: str, width: float) -> bool:
        """Set line width for a series"""
        success = self._data_manager.setSeriesLineWidth(name, width)
        if success:
            self.updateChart()
        return success
    
    def setSeriesMarkerSize(self, name: str, size: float) -> bool:
        """Set marker size for a series"""
        success = self._data_manager.setSeriesMarkerSize(name, size)
        if success:
            self.updateChart()
        return success
    
    def setXAxisTitle(self, title: str):
        """Set X axis title"""
        self._x_axis_title = title
        self._axis_x.setTitleText(title)
    
    def setYAxisTitle(self, title: str):
        """Set Y axis title"""
        self._y_axis_title = title
        self._axis_y.setTitleText(title)
    
    def setXAxisRange(self, min_val: float, max_val: float):
        """Set X axis range"""
        self._auto_scale = False
        self._axis_x.setRange(min_val, max_val)
    
    def setYAxisRange(self, min_val: float, max_val: float):
        """Set Y axis range"""
        self._auto_scale = False
        self._axis_y.setRange(min_val, max_val)
    
    def getXAxisRange(self) -> Tuple[float, float]:
        """Get X axis range"""
        return self._axis_x.min(), self._axis_x.max()
    
    def getYAxisRange(self) -> Tuple[float, float]:
        """Get Y axis range"""
        return self._axis_y.min(), self._axis_y.max()
    
    # Compatibility methods
    def clearData(self):
        """Clear all chart data (compatibility method)"""
        self.clearAllData()
    
    def getSeriesNames(self) -> List[str]:
        """Get list of all series names (overrides base method)"""
        return self._data_manager.getSeriesNames()
    
    def getSeriesData(self, name: str) -> List[Tuple[float, float]]:
        """Get data for a specific series (overrides base method)"""
        return self._data_manager.getSeriesData(name)
    
    def setSeriesColor(self, name: str, color: QColor):
        """Set color for a specific series (overrides base method)"""
        success = self._data_manager.setSeriesColor(name, color)
        if success:
            self.updateChart()
        return success
    
    def setSeriesVisibility(self, name: str, visible: bool):
        """Set visibility for a specific series (overrides base method)"""
        success = self._data_manager.setSeriesVisibility(name, visible)
        if success:
            self.updateChart()
        return success
    
    def setChartTitle(self, title: str):
        """Set chart title (compatibility method)"""
        self._chart_title = title
        self._chart.setTitle(title)
    
    def getSeriesLineStyle(self, name: str) -> str:
        """Get line style for a series"""
        return self._data_manager.getSeriesLineStyle(name)
    
    def getSeriesMarkerStyle(self, name: str) -> str:
        """Get marker style for a series"""
        return self._data_manager.getSeriesMarkerStyle(name)
    
    def getSeriesMarkerSize(self, name: str) -> float:
        """Get marker size for a specific series"""
        return self._data_manager.getSeriesMarkerSize(name)
    
    def hasCustomMarkerSize(self, series_name: str) -> bool:
        """Check if series has custom marker size"""
        return series_name in self._data_manager._seriesMarkerSizes
    
    def setAllMarkersSize(self, size: float):
        """Set marker size for all series"""
        self._data_manager.setAllMarkerSizes(size)
        self.updateChart()
    
    def resetMarkerSizes(self):
        """Reset all marker sizes to default"""
        for name in self._data_manager.getSeriesNames():
            self._data_manager.setSeriesMarkerSize(name, self._data_manager.getDefaultMarkerSize())
        self.updateChart()
    
    def getMarkerSizeRange(self) -> Tuple[float, float]:
        """Get valid marker size range"""
        return (1.0, 20.0)
    
    def isValidLineStyle(self, style: str) -> bool:
        """Check if line style is valid"""
        return self._line_series_factory.isValidLineStyle(style)
    
    def isValidMarkerStyle(self, style: str) -> bool:
        """Check if marker style is valid"""
        return self._line_series_factory.isValidMarkerStyle(style)
    
    # ============ CROSSHAIR METHODS ============
    
    def setCrosshairColor(self, color: QColor):
        """Set crosshair line color"""
        self._crosshair_color = color
        self._chart_view.setCrosshairColor(color)
    
    def setCrosshairWidth(self, width: float):
        """Set crosshair line width"""
        self._crosshair_width = width
        self._chart_view.setCrosshairWidth(width)
    
    def setCrosshairStyle(self, style: Qt.PenStyle):
        """Set crosshair line style"""
        self._chart_view.setCrosshairStyle(style)
    
    def showCrosshairAt(self, x: float, y: float):
        """Manually show crosshair at specific coordinates"""
        self._chart_view.showCrosshairAt(x, y)
    
    def hideCrosshair(self):
        """Manually hide crosshair"""
        self._chart_view.hideCrosshair()
    
    # ============ TOOLTIP METHODS ============
    
    def showTooltipAt(self, x: float, y: float, series_name: str, title: str = None, description: str = None):
        """Manually show tooltip at specific coordinates"""
        # This would need to be implemented in the tooltip manager
        pass
    
    def hideTooltip(self):
        """Manually hide tooltip"""
        self._tooltip_manager.hide()
    
    # ============ LEGEND METHODS ============
    
    def setLegendBackgroundVisible(self, visible: bool):
        """Set legend background visibility"""
        self._legend_background_visible = visible
        self._legend_manager.setBackgroundVisible(visible)
    
    def setLegendFontSize(self, size: int):
        """Set legend font size"""
        self._legend_font_size = size
        self._legend_manager.setFontSize(size)
    
    def getLegendFontSize(self) -> int:
        """Get legend font size"""
        return self._legend_font_size
    
    def getAvailableLegendPositions(self) -> List[str]:
        """Get list of available legend positions"""
        return self._legend_manager.getAvailablePositions()
    
    def setLegendAlignment(self, alignment: Qt.Alignment):
        """Directly set legend alignment"""
        self._legend_manager.setAlignment(alignment)
    
    def getLegendAlignment(self) -> Qt.Alignment:
        """Get current legend alignment"""
        return self._legend_manager.getAlignment()
    
    # ============ THEME METHODS ============
    
    def getAvailableThemes(self) -> List[str]:
        """Get list of available theme names"""
        return self._theme_manager.getAvailableThemes()
    
    def applyCustomPalette(self, palette: QPalette):
        """Apply a custom palette to the chart (for App Theme)"""
        self._theme_manager.applyCustomPalette(self._chart, palette)
    
    def refreshTheme(self):
        """Refresh the current theme (useful when app palette changes)"""
        self._theme_manager.refresh()
        self._applyTheme()
    
    # ============ EXPORT METHODS ============
    
    def exportToFile(self, format: str = None, filename: str = None):
        """Export chart to file"""
        return self._exporter.exportChart(self._chart_view, format, filename, self)
    
    def exportToClipboard(self):
        """Export chart to clipboard"""
        return self._exporter.exportToClipboard(self._chart_view)
    
    def printChart(self):
        """Print chart"""
        return self._exporter.printChart(self._chart_view)
    
    # ============ PROPERTIES FOR DESIGNER ============
    
    @Property(str)
    def chartTitle(self):
        """Get chart title"""
        return self._chart_title
    
    @chartTitle.setter
    def chartTitle(self, value: str):
        """Set chart title"""
        self._chart_title = value
        self._chart.setTitle(value)
    
    @Property(str)
    def xAxisTitle(self):
        """Get X axis title"""
        return self._x_axis_title
    
    @xAxisTitle.setter
    def xAxisTitle(self, value: str):
        """Set X axis title"""
        self._x_axis_title = value
        self._axis_x.setTitleText(value)
    
    @Property(str)
    def yAxisTitle(self):
        """Get Y axis title"""
        return self._y_axis_title
    
    @yAxisTitle.setter
    def yAxisTitle(self, value: str):
        """Set Y axis title"""
        self._y_axis_title = value
        self._axis_y.setTitleText(value)
    
    @Property(bool)
    def showGrid(self):
        """Get grid visibility"""
        return self._show_grid
    
    @showGrid.setter
    def showGrid(self, value: bool):
        """Set grid visibility"""
        self._show_grid = value
        self._axis_x.setGridLineVisible(value)
        self._axis_y.setGridLineVisible(value)
    
    @Property(bool)
    def autoScale(self):
        """Get auto-scaling state"""
        return self._auto_scale
    
    @autoScale.setter
    def autoScale(self, value: bool):
        """Set auto-scaling state"""
        self._auto_scale = value
        if value:
            self.updateChart()
    
    @Property(bool)
    def animationEnabled(self):
        """Get animation enabled state"""
        return self._animation_enabled
    
    @animationEnabled.setter
    def animationEnabled(self, value: bool):
        """Set animation enabled state"""
        self._animation_enabled = value
        if value:
            self._chart.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self._chart.setAnimationOptions(QChart.NoAnimation)
    
    @Property(int)
    def animationDuration(self):
        """Get animation duration in ms"""
        return self._animation_duration
    
    @animationDuration.setter
    def animationDuration(self, value: int):
        """Set animation duration in ms"""
        self._animation_duration = value
        if self._animation_enabled:
            self._chart.setAnimationDuration(value)
    
    @Property(bool)
    def antialiasing(self):
        """Get antialiasing state"""
        return self._antialiasing
    
    @antialiasing.setter
    def antialiasing(self, value: bool):
        """Set antialiasing state"""
        self._antialiasing = value
        self._chart_view.setRenderHint(QPainter.Antialiasing, value)
    
    @Property(bool)
    def showDataPoints(self):
        """Get data points visibility"""
        return self._show_data_points
    
    @showDataPoints.setter
    def showDataPoints(self, value: bool):
        """Set data points visibility"""
        self._show_data_points = value
        self.updateChart()
    
    @Property(bool)
    def fillArea(self):
        """Get fill area state"""
        return self._fill_area
    
    @fillArea.setter
    def fillArea(self, value: bool):
        """Set fill area state"""
        self._fill_area = value
        # Note: Area filling would need additional implementation
        self.updateChart()
    
    @Property(bool)
    def enableShadow(self):
        """Get shadow enabled state"""
        return self._enable_shadow
    
    @enableShadow.setter
    def enableShadow(self, value: bool):
        """Set shadow enabled state"""
        self._enable_shadow = value
        # Note: Shadow effects would need additional implementation
        self.updateChart()
    
    @Property(int)
    def highlightSize(self):
        """Get highlight size"""
        return self._highlight_size
    
    @highlightSize.setter
    def highlightSize(self, value: int):
        """Set highlight size"""
        self._highlight_size = value
        self.updateChart()
    
    @Property(int)
    def shadowBlur(self):
        """Get shadow blur radius"""
        return self._shadow_blur
    
    @shadowBlur.setter
    def shadowBlur(self, value: int):
        """Set shadow blur radius"""
        self._shadow_blur = value
        self.updateChart()
    
    @Property(float)
    def fillOpacity(self):
        """Get fill opacity"""
        return self._fill_opacity
    
    @fillOpacity.setter
    def fillOpacity(self, value: float):
        """Set fill opacity"""
        self._fill_opacity = value
        self.updateChart()
    
    @Property(QColor)
    def gridColor(self):
        """Get grid color"""
        return self._grid_color
    
    @gridColor.setter
    def gridColor(self, value: QColor):
        """Set grid color"""
        self._grid_color = value
        self._axis_x.setGridLineColor(value)
        self._axis_y.setGridLineColor(value)
        self._chart_view.update()
    
    @Property(QColor)
    def crosshairColor(self):
        """Get crosshair color"""
        return self._crosshair_color
    
    @crosshairColor.setter
    def crosshairColor(self, value: QColor):
        """Set crosshair color"""
        self._crosshair_color = value
        self._chart_view.setCrosshairColor(value)
    
    @Property(float)
    def crosshairWidth(self):
        """Get crosshair width"""
        return self._crosshair_width
    
    @crosshairWidth.setter
    def crosshairWidth(self, value: float):
        """Set crosshair width"""
        self._crosshair_width = value
        self._chart_view.setCrosshairWidth(value)
    
    @Property(bool)
    def showToolbar(self):
        """Get toolbar visibility"""
        return self.isToolbarVisible()
    
    @showToolbar.setter
    def showToolbar(self, value: bool):
        """Set toolbar visibility"""
        self.setToolbarVisible(value)
    
    @Property(bool)
    def showLegend(self):
        """Get legend visibility"""
        return self.isLegendVisible()
    
    @showLegend.setter
    def showLegend(self, value: bool):
        """Set legend visibility"""
        self.setLegendVisible(value)
    
    @Property(bool)
    def showCrosshair(self):
        """Get crosshair visibility"""
        return self.isCrosshairVisible()
    
    @showCrosshair.setter
    def showCrosshair(self, value: bool):
        """Set crosshair visibility"""
        self.setCrosshairVisible(value)
    
    @Property(bool)
    def showFooter(self):
        """Get footer visibility"""
        return self._show_footer
    
    @showFooter.setter
    def showFooter(self, value: bool):
        """Set footer visibility"""
        self._show_footer = value
        # Note: Footer would need to be implemented in QCustomChartBase
    
    @Property(bool)
    def tooltipsEnabled(self):
        """Get tooltips enabled state"""
        return self.areTooltipsEnabled()
    
    @tooltipsEnabled.setter
    def tooltipsEnabled(self, value: bool):
        """Set tooltips enabled state"""
        self.setTooltipsEnabled(value)
    
    @Property(int)
    def tooltipDelay(self):
        """Get tooltip delay in ms"""
        return self._tooltip_delay
    
    @tooltipDelay.setter
    def tooltipDelay(self, value: int):
        """Set tooltip delay in ms"""
        self._tooltip_delay = value
        self._tooltip_manager.setDelay(value)
    
    @Property(int)
    def tooltipDuration(self):
        """Get tooltip duration in ms"""
        return self._tooltip_duration
    
    @tooltipDuration.setter
    def tooltipDuration(self, value: int):
        """Set tooltip duration in ms"""
        self._tooltip_duration = value
        self._tooltip_manager.setDuration(value)
    
    @Property(str)
    def theme(self):
        """Get current theme"""
        return self.getTheme()
    
    @theme.setter
    def theme(self, value: str):
        """Set current theme"""
        self.setTheme(value)
    
    @Property(str)
    def legendPosition(self):
        """Get legend position"""
        return self.getLegendPosition()
    
    @legendPosition.setter
    def legendPosition(self, value: str):
        """Set legend position"""
        self.setLegendPosition(value)
    
    @Property(int)
    def legendFontSize(self):
        """Get legend font size"""
        return self._legend_font_size
    
    @legendFontSize.setter
    def legendFontSize(self, value: int):
        """Set legend font size"""
        self._legend_font_size = value
        self._legend_manager.setFontSize(value)
    
    @Property(bool)
    def legendBackgroundVisible(self):
        """Get legend background visibility"""
        return self._legend_background_visible
    
    @legendBackgroundVisible.setter
    def legendBackgroundVisible(self, value: bool):
        """Set legend background visibility"""
        self._legend_background_visible = value
        self._legend_manager.setBackgroundVisible(value)
    
    @Property(float)
    def markerSize(self):
        """Get default marker size"""
        return self._toolbar.getMarkerSize()
    
    @markerSize.setter
    def markerSize(self, value: float):
        """Set default marker size"""
        self._toolbar.setMarkerSize(value)
        self._data_manager.setAllMarkerSizes(value)
        self.updateChart()
    
    @Property(bool)
    def compactMode(self):
        """Get compact mode state"""
        return self.isCompactMode()
    
    @compactMode.setter
    def compactMode(self, value: bool):
        """Set compact mode state"""
        self.setCompactMode(value)
    
    @Property(str)
    def defaultLineStyle(self):
        """Get default line style"""
        return self.LINE_SOLID
    
    @Property(str)
    def defaultMarkerStyle(self):
        """Get default marker style"""
        return self.MARKER_NONE