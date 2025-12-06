# QCustomCharts.py
import os
import json
from typing import List, Tuple, Dict, Any, Optional, Union
from enum import Enum
from qtpy.QtCore import Qt, Signal, Property, QRect, QPointF, QTimer, QEvent
from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, 
    QLabel, QSlider, QCheckBox, QColorDialog, QSpinBox, QGroupBox, 
    QFormLayout, QMenu, QAction, QSizePolicy, QFrame, QScrollArea,
    QGridLayout, QToolButton, QInputDialog, QMessageBox, QFileDialog
)
from qtpy.QtGui import (
    QColor, QFont, QPainter, QPen, QBrush, QLinearGradient, 
    QGradient, QIcon, QPalette, QCursor, QPixmap, QFontMetrics
)
from qtpy.QtCharts import (
    QChart, QChartView, QLineSeries, QSplineSeries, QScatterSeries,
    QBarSeries, QBarSet, QPieSeries, QAreaSeries, QValueAxis,
    QCategoryAxis, QDateTimeAxis, QBarCategoryAxis, QLogValueAxis,
    QHorizontalBarSeries, QStackedBarSeries, QPercentBarSeries,
    QHorizontalStackedBarSeries, QHorizontalPercentBarSeries,
    QPieSlice, QCandlestickSeries, QBoxPlotSeries
)
from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Log import logInfo, logWarning, logError

class ChartType(Enum):
    """Available chart types"""
    LINE = "Line"
    SPLINE = "Spline"
    SCATTER = "Scatter"
    BAR = "Bar"
    HORIZONTAL_BAR = "Horizontal Bar"
    STACKED_BAR = "Stacked Bar"
    PERCENT_BAR = "Percent Bar"
    HORIZONTAL_STACKED_BAR = "Horizontal Stacked Bar"
    HORIZONTAL_PERCENT_BAR = "Horizontal Percent Bar"
    PIE = "Pie"
    DONUT = "Donut"
    AREA = "Area"
    CANDLESTICK = "Candlestick"
    BOXPLOT = "Box Plot"

class ChartTheme(Enum):
    """Built-in Qt Chart themes"""
    APP_THEME = "App Theme"  # Custom theme using QCustomTheme colors
    LIGHT = "Light"
    BLUE_CERULEAN = "Blue Cerulean"
    DARK = "Dark"
    BROWN_SAND = "Brown Sand"
    BLUE_NCS = "Blue NCS"
    HIGH_CONTRAST = "High Contrast"
    BLUE_ICY = "Blue Icy"
    QT = "Qt"

class QCustomCharts(QWidget):
    """
    A comprehensive, highly customizable chart widget with full theme integration.
    Supports multiple chart types, real-time updates, and Qt Designer compatibility.
    """
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/chart.png")
    WIDGET_TOOLTIP = "Interactive chart widget with theme support and multiple chart types"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCharts' name='customCharts'>
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
    
    # Signals
    dataPointClicked = Signal(float, float, str)  # x, y, series_name
    chartThemeChanged = Signal(str)
    chartTypeChanged = Signal(str)
    chartDataChanged = Signal()
    exportCompleted = Signal(str, bool)  # filename, success
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize theme system
        self._theme = QCustomTheme()
        self._theme.onThemeChanged.connect(self._onThemeChanged)
        
        # Default properties
        self._chartTitle = "Data Visualization"
        self._chartType = ChartType.LINE
        self._themeMode = ChartTheme.APP_THEME.value  # Use App Theme by default
        self._showLegend = True
        self._showTooltip = True
        self._animationEnabled = True
        self._animationDuration = 1000
        self._zoomEnabled = False
        self._panEnabled = False
        self._antialiasing = True
        self._customColors = []  # List of custom colors for series
        self._gradientEnabled = False
        self._gradientColors = []
        self._dataLabels = True
        self._gridLines = True
        self._axisTitles = True
        self._chartPadding = 10
        self._showControls = False
        self._backgroundColor = QColor(0, 0, 0, 0)  # Transparent by default
        self._titleFontSize = 14
        self._axisFontSize = 10
        self._legendFontSize = 10
        self._markerSize = 8
        self._lineWidth = 2
        self._barWidth = 0.8
        self._pieHoleSize = 0.0  # 0.0 = pie, >0 = donut
        self._xAxisTitle = "X Axis"
        self._yAxisTitle = "Y Axis"
        self._xMin = None
        self._xMax = None
        self._yMin = None
        self._yMax = None
        self._autoScale = True
        self._showGrid = True
        self._showMinorGrid = False
        self._tooltipPrecision = 2
        
        # Data storage
        self._seriesData = {}  # {series_name: [(x, y), ...]}
        self._seriesColors = {}  # {series_name: QColor}
        self._seriesVisible = {}  # {series_name: bool}
        self._seriesLineStyles = {}  # {series_name: Qt.PenStyle}
        self._seriesMarkers = {}  # {series_name: QScatterSeries.MarkerShape}
        
        # Chart components
        self.chart = QChart()
        self.chart_view = QChartView()
        self.chart_view.setChart(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing, self._antialiasing)
        
        # Control panel
        self.control_panel = QWidget()
        self.control_panel.setVisible(self._showControls)
        
        # Toolbar
        self.toolbar = QWidget()
        
        # Status bar
        self.status_bar = QLabel("Ready")
        self.status_bar.setStyleSheet("padding: 2px 5px;")
        
        # Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create toolbar
        self._createToolbar()
        
        # Add components to layout
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.chart_view, 1)
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.status_bar)
        
        # Initialize with sample data
        self._initSampleData()
        
        # Setup chart and controls
        self._setupChart()
        self._createControlPanel()
        
        # Apply initial theme
        self._applyTheme()
        
        # Setup interactions
        self._setupInteractions()
        
    def _initSampleData(self):
        """Initialize with sample data for design preview"""
        # Generate more realistic sample data
        import random
        import math
        
        # Line chart data (time series)
        time_series = {}
        categories = ["Sales", "Expenses", "Profit", "Growth"]
        for category in categories:
            data_points = []
            for i in range(12):  # 12 months
                base = random.uniform(50, 200)
                trend = i * 10
                seasonal = 20 * math.sin(i * math.pi / 6)
                noise = random.uniform(-10, 10)
                value = base + trend + seasonal + noise
                data_points.append((i + 1, max(0, value)))
            time_series[category] = data_points
        
        # Bar chart data (categorical)
        bar_data = {}
        products = ["Product A", "Product B", "Product C", "Product D"]
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        for product in products:
            data_points = []
            for i, quarter in enumerate(quarters):
                value = random.uniform(30, 100)
                data_points.append((i, value))
            bar_data[product] = data_points
        
        # Pie chart data (percentages)
        pie_data = {
            "Category A": [(0, 35)],
            "Category B": [(0, 25)],
            "Category C": [(0, 20)],
            "Category D": [(0, 15)],
            "Category E": [(0, 5)]
        }
        
        # Store all sample data
        self._sampleData = {
            "line": time_series,
            "bar": bar_data,
            "pie": pie_data
        }
        
        # Use line data by default
        self._seriesData = time_series.copy()
        
        # Initialize colors from theme
        self._initializeSeriesColors()
        
        # All series visible by default
        self._seriesVisible = {name: True for name in self._seriesData.keys()}
        
    def _initializeSeriesColors(self):
        """Initialize series colors from theme"""
        theme = self._theme.currentTheme
        
        # Get theme colors
        if hasattr(theme, 'accentColor'):
            accent_color = QColor(theme.accentColor)
        else:
            accent_color = QColor("#00bcff")  # Default accent color
        
        # Generate harmonious colors based on theme
        colors = []
        
        # Use theme color palette if available
        if hasattr(self._theme, 'COLOR_ACCENT_1') and self._theme.COLOR_ACCENT_1:
            # Use theme accent colors
            theme_colors = [
                self._theme.COLOR_ACCENT_1,
                self._theme.COLOR_ACCENT_2,
                self._theme.COLOR_ACCENT_3,
                self._theme.COLOR_ACCENT_4
            ]
            colors = [QColor(color) for color in theme_colors if color]
        else:
            # Generate colors from accent color
            for i in range(8):  # Generate up to 8 colors
                hue = (accent_color.hue() + i * 45) % 360
                saturation = min(255, accent_color.saturation() + 30)
                value = min(255, accent_color.value())
                color = QColor.fromHsv(hue, saturation, value)
                colors.append(color)
        
        # Assign colors to series
        for idx, series_name in enumerate(self._seriesData.keys()):
            color_idx = idx % len(colors)
            self._seriesColors[series_name] = colors[color_idx]
    
    def _setupChart(self):
        """Setup the chart with current data and settings"""
        try:
            # Clear existing chart components
            self.chart.removeAllSeries()
            
            # Clear existing axes
            for axis in self.chart.axes():
                self.chart.removeAxis(axis)
            
            # Apply chart title
            self.chart.setTitle(self._chartTitle)
            
            # Apply theme
            self._applyChartTheme()
            self._applyVisualSettings()
            
            # Create chart based on type
            chart_methods = {
                ChartType.LINE: self._createLineChart,
                ChartType.SPLINE: self._createSplineChart,
                ChartType.SCATTER: self._createScatterChart,
                ChartType.BAR: self._createBarChart,
                ChartType.HORIZONTAL_BAR: self._createHorizontalBarChart,
                ChartType.STACKED_BAR: self._createStackedBarChart,
                ChartType.PERCENT_BAR: self._createPercentBarChart,
                ChartType.PIE: self._createPieChart,
                ChartType.DONUT: self._createDonutChart,
                ChartType.AREA: self._createAreaChart,
            }
            
            method = chart_methods.get(self._chartType, self._createLineChart)
            method()
            
            # Configure legend
            self._configureLegend()
            
            # Configure animation
            if self._animationEnabled:
                self.chart.setAnimationOptions(QChart.SeriesAnimations)
                self.chart.setAnimationDuration(self._animationDuration)
            else:
                self.chart.setAnimationOptions(QChart.NoAnimation)
            
            # Configure interactions
            self._configureInteractions()
            
            # Update status
            self.status_bar.setText(f"{self._chartType.value} - {len(self._seriesData)} series")
            
        except Exception as e:
            logError(f"Error setting up chart: {e}")
            self.status_bar.setText(f"Error: {str(e)}")
    
    def _createLineChart(self):
        """Create line chart"""
        # Create new axes
        axis_x = QValueAxis()
        axis_y = QValueAxis()
        
        if self._axisTitles:
            axis_x.setTitleText(self._xAxisTitle)
            axis_y.setTitleText(self._yAxisTitle)
        
        all_x = []
        all_y = []
        
        for series_name, data in self._seriesData.items():
            if not self._seriesVisible.get(series_name, True):
                continue
                
            series = QLineSeries()
            series.setName(series_name)
            
            for x, y in data:
                series.append(x, y)
                all_x.append(x)
                all_y.append(y)
            
            # Apply color
            if series_name in self._seriesColors:
                series.setColor(self._seriesColors[series_name])
            
            # Apply line style
            if series_name in self._seriesLineStyles:
                pen = series.pen()
                pen.setStyle(self._seriesLineStyles[series_name])
                pen.setWidth(self._lineWidth)
                series.setPen(pen)
            else:
                pen = series.pen()
                pen.setWidth(self._lineWidth)
                series.setPen(pen)
            
            self.chart.addSeries(series)
        
        # Add axes to chart (axes were already cleared in setupChart)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        
        # Attach axes to series
        for series in self.chart.series():
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)
        
        # Set axis range
        if all_x and all_y:
            if self._autoScale:
                margin = 0.1  # 10% margin
                x_min, x_max = min(all_x), max(all_x)
                y_min, y_max = min(all_y), max(all_y)
                
                x_range = x_max - x_min
                y_range = y_max - y_min
                
                axis_x.setRange(x_min - x_range * margin, x_max + x_range * margin)
                axis_y.setRange(y_min - y_range * margin, y_max + y_range * margin)
            else:
                if self._xMin is not None and self._xMax is not None:
                    axis_x.setRange(self._xMin, self._xMax)
                if self._yMin is not None and self._yMax is not None:
                    axis_y.setRange(self._yMin, self._yMax)
        
        # Configure grid
        axis_x.setGridLineVisible(self._showGrid)
        axis_y.setGridLineVisible(self._showGrid)
        axis_x.setMinorGridLineVisible(self._showMinorGrid)
        axis_y.setMinorGridLineVisible(self._showMinorGrid)
    
    def _createSplineChart(self):
        """Create spline (curved line) chart"""
        axis_x = QValueAxis()
        axis_y = QValueAxis()
        
        if self._axisTitles:
            axis_x.setTitleText(self._xAxisTitle)
            axis_y.setTitleText(self._yAxisTitle)
        
        all_x = []
        all_y = []
        
        for series_name, data in self._seriesData.items():
            if not self._seriesVisible.get(series_name, True):
                continue
                
            series = QSplineSeries()
            series.setName(series_name)
            
            for x, y in data:
                series.append(x, y)
                all_x.append(x)
                all_y.append(y)
            
            if series_name in self._seriesColors:
                series.setColor(self._seriesColors[series_name])
            
            pen = series.pen()
            pen.setWidth(self._lineWidth)
            series.setPen(pen)
            
            self.chart.addSeries(series)
        
        # Add axes
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        
        for series in self.chart.series():
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)
        
        # Auto-scale
        if all_x and all_y:
            margin = 0.1
            x_min, x_max = min(all_x), max(all_x)
            y_min, y_max = min(all_y), max(all_y)
            
            x_range = x_max - x_min
            y_range = y_max - y_min
            
            axis_x.setRange(x_min - x_range * margin, x_max + x_range * margin)
            axis_y.setRange(y_min - y_range * margin, y_max + y_range * margin)
    
    def _createScatterChart(self):
        """Create scatter plot"""
        axis_x = QValueAxis()
        axis_y = QValueAxis()
        
        if self._axisTitles:
            axis_x.setTitleText(self._xAxisTitle)
            axis_y.setTitleText(self._yAxisTitle)
        
        all_x = []
        all_y = []
        
        for series_name, data in self._seriesData.items():
            if not self._seriesVisible.get(series_name, True):
                continue
                
            series = QScatterSeries()
            series.setName(series_name)
            series.setMarkerSize(self._markerSize)
            
            for x, y in data:
                series.append(x, y)
                all_x.append(x)
                all_y.append(y)
            
            if series_name in self._seriesColors:
                series.setColor(self._seriesColors[series_name])
            
            if series_name in self._seriesMarkers:
                series.setMarkerShape(self._seriesMarkers[series_name])
            
            self.chart.addSeries(series)
        
        # Add axes
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        
        for series in self.chart.series():
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)
        
        # Auto-scale
        if all_x and all_y:
            margin = 0.1
            x_min, x_max = min(all_x), max(all_x)
            y_min, y_max = min(all_y), max(all_y)
            
            x_range = x_max - x_min
            y_range = y_max - y_min
            
            axis_x.setRange(x_min - x_range * margin, x_max + x_range * margin)
            axis_y.setRange(y_min - y_range * margin, y_max + y_range * margin)
    
    def _createBarChart(self):
        """Create bar chart"""
        # Group data by x value
        from collections import defaultdict
        grouped_data = defaultdict(dict)
        
        for series_name, data in self._seriesData.items():
            if not self._seriesVisible.get(series_name, True):
                continue
            for x, y in data:
                grouped_data[x][series_name] = y
        
        # Create bar series
        bar_series = QBarSeries()
        
        # Create bar sets
        bar_sets = {}
        x_values = sorted(grouped_data.keys())
        
        for series_name in self._seriesData.keys():
            if not self._seriesVisible.get(series_name, True):
                continue
                
            bar_set = QBarSet(series_name)
            if series_name in self._seriesColors:
                bar_set.setColor(self._seriesColors[series_name])
            bar_sets[series_name] = bar_set
        
        # Fill bar sets
        for x in x_values:
            for series_name, bar_set in bar_sets.items():
                value = grouped_data[x].get(series_name, 0)
                bar_set.append(value)
        
        # Add bar sets to series
        for bar_set in bar_sets.values():
            bar_series.append(bar_set)
        
        self.chart.addSeries(bar_series)
        
        # Create category axis
        axis_x = QBarCategoryAxis()
        axis_y = QValueAxis()
        
        categories = [str(x) for x in x_values]
        axis_x.append(categories)
        
        if self._axisTitles:
            axis_x.setTitleText(self._xAxisTitle)
            axis_y.setTitleText(self._yAxisTitle)
        
        # Add axes
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        
        bar_series.attachAxis(axis_x)
        bar_series.attachAxis(axis_y)
    
    def _createHorizontalBarChart(self):
        """Create horizontal bar chart"""
        # Similar to bar chart but horizontal
        self._createBarChart()
        # Note: QHorizontalBarSeries would be used here
    
    def _createStackedBarChart(self):
        """Create stacked bar chart"""
        bar_series = QStackedBarSeries()
        self._addBarSetsToSeries(bar_series)
    
    def _createPercentBarChart(self):
        """Create 100% stacked bar chart"""
        bar_series = QPercentBarSeries()
        self._addBarSetsToSeries(bar_series)
    
    def _addBarSetsToSeries(self, bar_series):
        """Helper method to add bar sets to series"""
        for series_name, data in self._seriesData.items():
            if not self._seriesVisible.get(series_name, True):
                continue
                
            bar_set = QBarSet(series_name)
            if series_name in self._seriesColors:
                bar_set.setColor(self._seriesColors[series_name])
            
            for x, y in data:
                bar_set.append(y)
            
            bar_series.append(bar_set)
        
        self.chart.addSeries(bar_series)
        
        # Create axes
        axis_x = QBarCategoryAxis()
        axis_y = QValueAxis()
        
        categories = [str(i) for i in range(len(next(iter(self._seriesData.values()))))]
        axis_x.append(categories)
        
        if self._axisTitles:
            axis_x.setTitleText(self._xAxisTitle)
            axis_y.setTitleText(self._yAxisTitle)
        
        # Add axes to chart
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        
        bar_series.attachAxis(axis_x)
        bar_series.attachAxis(axis_y)
    
    def _createPieChart(self):
        """Create pie chart"""
        pie_series = QPieSeries()
        pie_series.setHoleSize(self._pieHoleSize)
        
        total_sum = 0
        for series_name, data in self._seriesData.items():
            if not self._seriesVisible.get(series_name, True):
                continue
                
            # Sum all y values for this series
            series_sum = sum(y for _, y in data) if data else 0
            total_sum += series_sum
            
            if series_sum > 0:
                slice = pie_series.append(series_name, series_sum)
                
                if series_name in self._seriesColors:
                    slice.setColor(self._seriesColors[series_name])
                
                if self._dataLabels:
                    slice.setLabelVisible(True)
                    percentage = (series_sum / total_sum * 100) if total_sum > 0 else 0
                    slice.setLabel(f"{series_name}: {percentage:.1f}%")
                    slice.setLabelArmLengthFactor(0.2)
        
        self.chart.addSeries(pie_series)
        
        # Connect slice clicked signal
        pie_series.clicked.connect(self._onPieSliceClicked)
        
        # Ensure no axes are shown for pie charts
        for axis in self.chart.axes():
            axis.hide()
    
    def _createDonutChart(self):
        """Create donut chart"""
        self._pieHoleSize = 0.4
        self._createPieChart()
    
    def _createAreaChart(self):
        """Create area chart"""
        if not self._seriesData:
            return
        
        # Use first series as upper bound
        first_series_name = next(iter(self._seriesData))
        upper_data = self._seriesData[first_series_name]
        
        # Create lower bound (could be zero or another series)
        lower_data = [(x, 0) for x, _ in upper_data]
        
        upper_series = QLineSeries()
        lower_series = QLineSeries()
        
        for (x, y1), (_, y2) in zip(upper_data, lower_data):
            upper_series.append(x, y1)
            lower_series.append(x, y2)
        
        area_series = QAreaSeries(upper_series, lower_series)
        area_series.setName(first_series_name)
        
        if first_series_name in self._seriesColors:
            color = self._seriesColors[first_series_name]
            area_series.setColor(color)
            area_series.setBorderColor(color.darker(150))
        
        self.chart.addSeries(area_series)
        
        # Create axes
        axis_x = QValueAxis()
        axis_y = QValueAxis()
        
        if self._axisTitles:
            axis_x.setTitleText(self._xAxisTitle)
            axis_y.setTitleText(self._yAxisTitle)
        
        # Add axes
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        
        area_series.attachAxis(axis_x)
        area_series.attachAxis(axis_y)
    
    def _onPieSliceClicked(self, slice):
        """Handle pie slice click"""
        self.status_bar.setText(f"Clicked: {slice.label()} ({slice.percentage():.1%})")
        slice.setExploded(not slice.isExploded())
    
    def _applyChartTheme(self):
        """Apply Qt chart theme based on theme mode"""
        theme_map = {
            ChartTheme.LIGHT: QChart.ChartThemeLight,
            ChartTheme.BLUE_CERULEAN: QChart.ChartThemeBlueCerulean,
            ChartTheme.DARK: QChart.ChartThemeDark,
            ChartTheme.BROWN_SAND: QChart.ChartThemeBrownSand,
            ChartTheme.BLUE_NCS: QChart.ChartThemeBlueNcs,
            ChartTheme.HIGH_CONTRAST: QChart.ChartThemeHighContrast,
            ChartTheme.BLUE_ICY: QChart.ChartThemeBlueIcy,
            ChartTheme.QT: QChart.ChartThemeQt
        }
        
        # Check if we're using App Theme
        if self._themeMode == ChartTheme.APP_THEME.value:
            # Apply custom theme based on QCustomTheme colors
            self._applyAppTheme()
        else:
            # Use built-in Qt themes
            for theme_name, qt_theme in theme_map.items():
                if theme_name.value == self._themeMode:
                    self.chart.setTheme(qt_theme)
                    break
            else:
                # Default to Light theme
                self.chart.setTheme(QChart.ChartThemeLight)
    
    def _applyAppTheme(self):
        """Apply custom theme based on QCustomTheme colors"""
        theme = self._theme.currentTheme
        
        # Get colors from theme
        if hasattr(self._theme, 'COLOR_BACKGROUND_1'):
            bg_color = QColor(self._theme.COLOR_BACKGROUND_1)
        else:
            bg_color = QColor(theme.backgroundColor) if hasattr(theme, 'backgroundColor') else QColor(255, 255, 255)
        
        if hasattr(self._theme, 'COLOR_TEXT_1'):
            text_color = QColor(self._theme.COLOR_TEXT_1)
        else:
            text_color = QColor(theme.textColor) if hasattr(theme, 'textColor') else QColor(0, 0, 0)
        
        if hasattr(self._theme, 'COLOR_ACCENT_1'):
            accent_color = QColor(self._theme.COLOR_ACCENT_1)
        else:
            accent_color = QColor(theme.accentColor) if hasattr(theme, 'accentColor') else QColor(0, 188, 255)
        
        # Apply colors to chart
        self.chart.setBackgroundBrush(QBrush(self._backgroundColor))  # Transparent
        
        # Set title color
        self.chart.setTitleBrush(QBrush(text_color))
        
        # Set legend colors
        legend = self.chart.legend()
        if legend:
            legend.setLabelColor(text_color)
            legend.setBorderColor(accent_color)
        
        # Set axis colors
        for axis in self.chart.axes():
            axis.setLabelsColor(text_color)
            axis.setGridLineColor(accent_color.lighter(150))
            axis.setLinePenColor(accent_color)
            axis.setTitleBrush(QBrush(text_color))
        
        # Update series colors based on theme
        self._initializeSeriesColors()
        
        # Re-apply series colors
        for series in self.chart.series():
            if isinstance(series, (QLineSeries, QSplineSeries, QScatterSeries)):
                series_name = series.name()
                if series_name in self._seriesColors:
                    series.setColor(self._seriesColors[series_name])
            elif isinstance(series, (QBarSeries, QStackedBarSeries, QPercentBarSeries)):
                for bar_set in series.barSets():
                    series_name = bar_set.label()
                    if series_name in self._seriesColors:
                        bar_set.setColor(self._seriesColors[series_name])
            elif isinstance(series, QPieSeries):
                for slice in series.slices():
                    series_name = slice.label()
                    if series_name in self._seriesColors:
                        slice.setColor(self._seriesColors[series_name])
                        slice.setLabelColor(text_color)
    
    def _applyVisualSettings(self):
        """Apply visual settings to chart"""
        # Background - always transparent for App Theme
        if self._themeMode == ChartTheme.APP_THEME.value:
            self.chart.setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
            self.chart_view.setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
        elif self._gradientEnabled and self._gradientColors:
            gradient = QLinearGradient(0, 0, 0, self.height())
            for i, color in enumerate(self._gradientColors):
                gradient.setColorAt(i / (len(self._gradientColors) - 1), QColor(color))
            self.chart.setBackgroundBrush(QBrush(gradient))
        else:
            self.chart.setBackgroundBrush(self._backgroundColor)
        
        # Title font
        title_font = self.chart.titleFont()
        title_font.setPointSize(self._titleFontSize)
        title_font.setBold(True)
        self.chart.setTitleFont(title_font)
        
        # Set title color based on theme
        if self._themeMode == ChartTheme.APP_THEME.value:
            theme = self._theme.currentTheme
            if hasattr(self._theme, 'COLOR_TEXT_1'):
                text_color = QColor(self._theme.COLOR_TEXT_1)
            else:
                text_color = QColor(theme.textColor) if hasattr(theme, 'textColor') else QColor(0, 0, 0)
            self.chart.setTitleBrush(QBrush(text_color))
        
        # Plot area background - transparent for App Theme
        if self._themeMode == ChartTheme.APP_THEME.value:
            self.chart.setPlotAreaBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
            self.chart.setPlotAreaBackgroundVisible(False)
        else:
            self.chart.setPlotAreaBackgroundBrush(QColor(self._theme.currentTheme.backgroundColor))
            self.chart.setPlotAreaBackgroundVisible(True)
    
    def _configureLegend(self):
        """Configure chart legend"""
        legend = self.chart.legend()
        legend.setVisible(self._showLegend)
        
        if self._showLegend:
            legend.setAlignment(Qt.AlignBottom)
            legend.setBackgroundVisible(False)
            
            # Set legend colors based on theme
            if self._themeMode == ChartTheme.APP_THEME.value:
                theme = self._theme.currentTheme
                if hasattr(self._theme, 'COLOR_TEXT_1'):
                    text_color = QColor(self._theme.COLOR_TEXT_1)
                else:
                    text_color = QColor(theme.textColor) if hasattr(theme, 'textColor') else QColor(0, 0, 0)
                legend.setLabelColor(text_color)
            
            legend_font = legend.font()
            legend_font.setPointSize(self._legendFontSize)
            legend.setFont(legend_font)
    
    def _configureInteractions(self):
        """Configure chart interactions"""
        if self._zoomEnabled:
            self.chart_view.setRubberBand(QChartView.RectangleRubberBand)
        else:
            self.chart_view.setRubberBand(QChartView.NoRubberBand)
            
        if self._panEnabled:
            self.chart_view.setDragMode(QChartView.ScrollHandDrag)
        else:
            self.chart_view.setDragMode(QChartView.NoDrag)
    
    def _setupInteractions(self):
        """Setup mouse and keyboard interactions"""
        self.chart_view.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
    
    def _createToolbar(self):
        """Create toolbar with chart controls"""
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(5, 2, 5, 2)
        
        # Chart type selector
        self.type_combo = QComboBox()
        for chart_type in ChartType:
            self.type_combo.addItem(chart_type.value, chart_type)
        self.type_combo.currentIndexChanged.connect(self._onChartTypeChanged)
        
        # Theme selector - App Theme is first option
        self.theme_combo = QComboBox()
        self.theme_combo.addItem(ChartTheme.APP_THEME.value, ChartTheme.APP_THEME)
        for chart_theme in ChartTheme:
            if chart_theme != ChartTheme.APP_THEME:  # Skip App Theme as it's already added
                self.theme_combo.addItem(chart_theme.value, chart_theme)
        self.theme_combo.currentIndexChanged.connect(self._onThemeChangedCombo)
        
        # Tool buttons
        self.zoom_btn = QToolButton()
        self.zoom_btn.setText("🔍")
        self.zoom_btn.setCheckable(True)
        self.zoom_btn.toggled.connect(lambda checked: setattr(self, "zoomEnabled", checked))
        self.zoom_btn.setToolTip("Zoom")
        
        self.pan_btn = QToolButton()
        self.pan_btn.setText("✋")
        self.pan_btn.setCheckable(True)
        self.pan_btn.toggled.connect(lambda checked: setattr(self, "panEnabled", checked))
        self.pan_btn.setToolTip("Pan")
        
        self.legend_btn = QToolButton()
        self.legend_btn.setText("📖")
        self.legend_btn.setCheckable(True)
        self.legend_btn.setChecked(self._showLegend)
        self.legend_btn.toggled.connect(lambda checked: setattr(self, "showLegend", checked))
        self.legend_btn.setToolTip("Toggle Legend")
        
        self.controls_btn = QToolButton()
        self.controls_btn.setText("⚙️")
        self.controls_btn.setCheckable(True)
        self.controls_btn.setChecked(self._showControls)
        self.controls_btn.toggled.connect(lambda checked: setattr(self, "showControls", checked))
        self.controls_btn.setToolTip("Show Controls")
        
        # Add widgets to toolbar
        toolbar_layout.addWidget(QLabel("Type:"))
        toolbar_layout.addWidget(self.type_combo)
        toolbar_layout.addWidget(QLabel("Theme:"))
        toolbar_layout.addWidget(self.theme_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.zoom_btn)
        toolbar_layout.addWidget(self.pan_btn)
        toolbar_layout.addWidget(self.legend_btn)
        toolbar_layout.addWidget(self.controls_btn)
        
        self.toolbar.setMaximumHeight(30)
    
    def _createControlPanel(self):
        """Create detailed control panel"""
        panel_layout = QVBoxLayout(self.control_panel)
        
        # Series controls
        series_group = QGroupBox("Series")
        series_layout = QVBoxLayout()
        
        self.series_checkboxes = {}
        self.series_color_buttons = {}
        
        for series_name in self._seriesData.keys():
            series_widget = QWidget()
            series_widget_layout = QHBoxLayout(series_widget)
            series_widget_layout.setContentsMargins(0, 0, 0, 0)
            
            checkbox = QCheckBox(series_name)
            checkbox.setChecked(self._seriesVisible.get(series_name, True))
            checkbox.toggled.connect(lambda checked, name=series_name: self._toggleSeries(name, checked))
            
            color_btn = QPushButton()
            color_btn.setFixedSize(20, 20)
            color = self._seriesColors.get(series_name, QColor("blue"))
            color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")
            color_btn.clicked.connect(lambda _, name=series_name: self._changeSeriesColor(name))
            
            series_widget_layout.addWidget(checkbox)
            series_widget_layout.addWidget(color_btn)
            series_widget_layout.addStretch()
            
            series_layout.addWidget(series_widget)
            self.series_checkboxes[series_name] = checkbox
            self.series_color_buttons[series_name] = color_btn
        
        series_group.setLayout(series_layout)
        panel_layout.addWidget(series_group)
        
        # Chart options
        options_group = QGroupBox("Options")
        options_layout = QFormLayout()
        
        # Title
        self.title_edit = QComboBox()
        self.title_edit.setEditable(True)
        self.title_edit.addItems(["Data Visualization", "Sales Report", "Performance Metrics", "Custom Title"])
        self.title_edit.setCurrentText(self._chartTitle)
        self.title_edit.currentTextChanged.connect(lambda text: setattr(self, "chartTitle", text))
        
        # Animation duration
        self.anim_slider = QSlider(Qt.Horizontal)
        self.anim_slider.setRange(0, 3000)
        self.anim_slider.setValue(self._animationDuration)
        self.anim_slider.valueChanged.connect(lambda value: setattr(self, "animationDuration", value))
        
        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(self._titleFontSize)
        self.font_size_spin.valueChanged.connect(lambda value: setattr(self, "titleFontSize", value))
        
        options_layout.addRow("Title:", self.title_edit)
        options_layout.addRow("Animation (ms):", self.anim_slider)
        options_layout.addRow("Title Font Size:", self.font_size_spin)
        
        options_group.setLayout(options_layout)
        panel_layout.addWidget(options_group)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self._exportChart)
        
        self.reset_btn = QPushButton("Reset View")
        self.reset_btn.clicked.connect(self._resetView)
        
        self.sample_btn = QPushButton("Load Sample")
        self.sample_btn.clicked.connect(self._loadSampleData)
        
        action_layout.addWidget(self.export_btn)
        action_layout.addWidget(self.reset_btn)
        action_layout.addWidget(self.sample_btn)
        
        panel_layout.addLayout(action_layout)
        
        # Add stretch
        panel_layout.addStretch()
    
    def _onChartTypeChanged(self, index):
        """Handle chart type change from toolbar"""
        chart_type = self.type_combo.currentData()
        if chart_type:
            self.chartType = chart_type.value
    
    def _onThemeChangedCombo(self, index):
        """Handle theme change from toolbar"""
        theme_data = self.theme_combo.currentData()
        if isinstance(theme_data, ChartTheme):
            self.themeMode = theme_data.value
    
    def _onThemeChanged(self):
        """Handle theme change from theme system"""
        if self._themeMode == ChartTheme.APP_THEME.value:
            self._applyTheme()
            self._applyChartTheme()
            self._setupChart()
    
    def _toggleSeries(self, series_name, visible):
        """Toggle series visibility"""
        self._seriesVisible[series_name] = visible
        self._setupChart()
    
    def _changeSeriesColor(self, series_name):
        """Change color of a series"""
        color = QColorDialog.getColor(
            self._seriesColors.get(series_name, QColor("blue")),
            self,
            f"Choose color for {series_name}"
        )
        
        if color.isValid():
            self._seriesColors[series_name] = color
            btn = self.series_color_buttons.get(series_name)
            if btn:
                btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")
            self._setupChart()
    
    def _exportChart(self):
        """Export chart to image"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Chart",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
        )
        
        if filename:
            try:
                # Determine format from extension
                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    format = "JPG"
                else:
                    format = "PNG"
                    if not filename.lower().endswith('.png'):
                        filename += '.png'
                
                # Capture chart
                pixmap = self.chart_view.grab()
                success = pixmap.save(filename, format)
                
                if success:
                    self.status_bar.setText(f"Chart exported to {filename}")
                    self.exportCompleted.emit(filename, True)
                else:
                    self.status_bar.setText("Export failed")
                    self.exportCompleted.emit(filename, False)
                    
            except Exception as e:
                logError(f"Export error: {e}")
                self.status_bar.setText(f"Export error: {str(e)}")
                self.exportCompleted.emit(filename, False)
    
    def _resetView(self):
        """Reset chart view to default"""
        self._autoScale = True
        self._xMin = self._xMax = self._yMin = self._yMax = None
        self._setupChart()
        self.status_bar.setText("View reset")
    
    def _loadSampleData(self):
        """Load sample data based on current chart type"""
        sample_key = "line"
        if self._chartType in [ChartType.BAR, ChartType.HORIZONTAL_BAR, 
                               ChartType.STACKED_BAR, ChartType.PERCENT_BAR]:
            sample_key = "bar"
        elif self._chartType in [ChartType.PIE, ChartType.DONUT]:
            sample_key = "pie"
        
        if sample_key in self._sampleData:
            self.setData(self._sampleData[sample_key])
            self.status_bar.setText(f"Loaded {sample_key} sample data")
    
    def _applyTheme(self):
        """Apply theme colors to widget"""
        theme = self._theme.currentTheme
        
        # Update toolbar colors
        toolbar_style = f"""
            QWidget {{
                background-color: {theme.backgroundColor};
                color: {theme.textColor};
            }}
        """
        self.toolbar.setStyleSheet(toolbar_style)
        
        # Update control panel colors
        control_style = f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {theme.accentColor};
                border-radius: 3px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {theme.accentColor};
            }}
        """
        self.control_panel.setStyleSheet(control_style)
        
        # Update status bar
        status_style = f"""
            QLabel {{
                background-color: {theme.backgroundColor};
                color: {theme.textColor};
                border-top: 1px solid {theme.accentColor};
            }}
        """
        self.status_bar.setStyleSheet(status_style)
        
        # Update chart
        self._applyVisualSettings()
    
    # ============ PUBLIC API METHODS ============
    
    def setData(self, data: Dict[str, List[Tuple[float, float]]], chart_type: ChartType = None):
        """
        Set chart data
        
        Args:
            data: Dictionary of {series_name: [(x, y), ...]}
            chart_type: Optional chart type override
        """
        self._seriesData = data
        
        if chart_type:
            self.chartType = chart_type.value
        
        # Initialize colors for new series
        self._initializeSeriesColors()
        
        # Initialize visibility
        for series_name in data.keys():
            if series_name not in self._seriesVisible:
                self._seriesVisible[series_name] = True
        
        # Update control panel
        self._updateControlPanel()
        
        # Setup chart
        self._setupChart()
        self.chartDataChanged.emit()
    
    def addSeries(self, name: str, data: List[Tuple[float, float]], 
                  color: QColor = None, visible: bool = True):
        """Add a new series to the chart"""
        self._seriesData[name] = data
        self._seriesVisible[name] = True
        
        if color:
            self._seriesColors[name] = color
        else:
            # Assign a color from theme
            theme = self._theme.currentTheme
            accent_color = QColor(theme.accentColor)
            hue = (accent_color.hue() + len(self._seriesColors) * 45) % 360
            self._seriesColors[name] = QColor.fromHsv(
                hue, accent_color.saturation(), accent_color.value()
            )
        
        # Update control panel
        self._updateControlPanel()
        
        self._setupChart()
        self.chartDataChanged.emit()
    
    def removeSeries(self, name: str):
        """Remove a series from the chart"""
        if name in self._seriesData:
            del self._seriesData[name]
            if name in self._seriesColors:
                del self._seriesColors[name]
            if name in self._seriesVisible:
                del self._seriesVisible[name]
            
            # Update control panel
            self._updateControlPanel()
            
            self._setupChart()
            self.chartDataChanged.emit()
    
    def clearData(self):
        """Clear all chart data"""
        self._seriesData = {}
        self._seriesColors = {}
        self._seriesVisible = {}
        
        # Clear control panel
        self._updateControlPanel()
        
        self._setupChart()
        self.chartDataChanged.emit()
    
    def getSeriesNames(self) -> List[str]:
        """Get list of all series names"""
        return list(self._seriesData.keys())
    
    def getSeriesData(self, name: str) -> List[Tuple[float, float]]:
        """Get data for a specific series"""
        return self._seriesData.get(name, [])
    
    def updateSeries(self, name: str, data: List[Tuple[float, float]]):
        """Update data for an existing series"""
        if name in self._seriesData:
            self._seriesData[name] = data
            self._setupChart()
            self.chartDataChanged.emit()
    
    def setSeriesColor(self, name: str, color: QColor):
        """Set color for a specific series"""
        self._seriesColors[name] = color
        
        # Update button in control panel
        btn = self.series_color_buttons.get(name)
        if btn:
            btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")
        
        self._setupChart()
    
    def setSeriesVisibility(self, name: str, visible: bool):
        """Set visibility for a specific series"""
        self._seriesVisible[name] = visible
        
        # Update checkbox in control panel
        checkbox = self.series_checkboxes.get(name)
        if checkbox:
            checkbox.setChecked(visible)
        
        self._setupChart()
    
    def exportToImage(self, filename: str, width: int = None, height: int = None):
        """Export chart to image file"""
        if width is None:
            width = self.width()
        if height is None:
            height = self.height()
        
        # Create a temporary chart view for export
        export_view = QChartView(self.chart)
        export_view.resize(width, height)
        
        pixmap = export_view.grab()
        success = pixmap.save(filename)
        
        if success:
            logInfo(f"Chart exported to {filename}")
        else:
            logError(f"Failed to export chart to {filename}")
        
        return success
    
    def saveSettings(self, filename: str):
        """Save chart settings to JSON file"""
        settings = {
            "chartTitle": self._chartTitle,
            "chartType": self._chartType.value,
            "themeMode": self._themeMode,
            "showLegend": self._showLegend,
            "animationEnabled": self._animationEnabled,
            "animationDuration": self._animationDuration,
            "seriesData": self._seriesData,
            "seriesColors": {
                name: color.name() for name, color in self._seriesColors.items()
            },
            "seriesVisible": self._seriesVisible
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(settings, f, indent=2, default=str)
            logInfo(f"Chart settings saved to {filename}")
            return True
        except Exception as e:
            logError(f"Failed to save chart settings: {e}")
            return False
    
    def loadSettings(self, filename: str):
        """Load chart settings from JSON file"""
        try:
            with open(filename, 'r') as f:
                settings = json.load(f)
            
            # Restore settings
            self.chartTitle = settings.get("chartTitle", self._chartTitle)
            self.chartType = settings.get("chartType", self._chartType.value)
            self.themeMode = settings.get("themeMode", self._themeMode)
            self.showLegend = settings.get("showLegend", self._showLegend)
            self.animationEnabled = settings.get("animationEnabled", self._animationEnabled)
            self.animationDuration = settings.get("animationDuration", self._animationDuration)
            
            # Restore data
            data = settings.get("seriesData", {})
            self.setData(data)
            
            # Restore colors
            colors = settings.get("seriesColors", {})
            for name, color_str in colors.items():
                self._seriesColors[name] = QColor(color_str)
            
            # Restore visibility
            self._seriesVisible = settings.get("seriesVisible", {})
            
            # Update control panel
            self._updateControlPanel()
            
            logInfo(f"Chart settings loaded from {filename}")
            return True
            
        except Exception as e:
            logError(f"Failed to load chart settings: {e}")
            return False
    
    def _updateControlPanel(self):
        """Update control panel with current series"""
        # Clear existing controls
        for checkbox in self.series_checkboxes.values():
            checkbox.deleteLater()
        for btn in self.series_color_buttons.values():
            btn.deleteLater()
        
        self.series_checkboxes = {}
        self.series_color_buttons = {}
        
        # Recreate series controls
        if hasattr(self, 'control_panel'):
            # Find series group
            for i in range(self.control_panel.layout().count()):
                item = self.control_panel.layout().itemAt(i)
                if item and item.widget() and isinstance(item.widget(), QGroupBox):
                    if item.widget().title() == "Series":
                        # Clear layout
                        layout = item.widget().layout()
                        if layout:
                            while layout.count():
                                child = layout.takeAt(0)
                                if child.widget():
                                    child.widget().deleteLater()
                        
                        # Add series controls
                        for series_name in self._seriesData.keys():
                            series_widget = QWidget()
                            series_widget_layout = QHBoxLayout(series_widget)
                            series_widget_layout.setContentsMargins(0, 0, 0, 0)
                            
                            checkbox = QCheckBox(series_name)
                            checkbox.setChecked(self._seriesVisible.get(series_name, True))
                            checkbox.toggled.connect(lambda checked, name=series_name: self._toggleSeries(name, checked))
                            
                            color_btn = QPushButton()
                            color_btn.setFixedSize(20, 20)
                            color = self._seriesColors.get(series_name, QColor("blue"))
                            color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")
                            color_btn.clicked.connect(lambda _, name=series_name: self._changeSeriesColor(name))
                            
                            series_widget_layout.addWidget(checkbox)
                            series_widget_layout.addWidget(color_btn)
                            series_widget_layout.addStretch()
                            
                            layout.addWidget(series_widget)
                            self.series_checkboxes[series_name] = checkbox
                            self.series_color_buttons[series_name] = color_btn
    
    # ============ PROPERTIES ============
    
    @Property(str)
    def chartTitle(self):
        return self._chartTitle
    
    @chartTitle.setter
    def chartTitle(self, value):
        self._chartTitle = str(value)
        if hasattr(self, 'title_edit'):
            self.title_edit.setCurrentText(value)
        self.chart.setTitle(self._chartTitle)
        self.chart.update()
    
    @Property(str)
    def chartType(self):
        return self._chartType.value
    
    @chartType.setter
    def chartType(self, value):
        # Convert string to ChartType enum
        for chart_type in ChartType:
            if chart_type.value.lower() == str(value).lower() or chart_type.name.lower() == str(value).lower():
                self._chartType = chart_type
                if hasattr(self, 'type_combo'):
                    index = self.type_combo.findText(chart_type.value)
                    if index >= 0:
                        self.type_combo.setCurrentIndex(index)
                self._setupChart()
                self.chartTypeChanged.emit(value)
                break
    
    @Property(str)
    def themeMode(self):
        return self._themeMode
    
    @themeMode.setter
    def themeMode(self, value):
        self._themeMode = value
        if hasattr(self, 'theme_combo'):
            for chart_theme in ChartTheme:
                if chart_theme.value == value:
                    index = self.theme_combo.findText(value)
                    if index >= 0:
                        self.theme_combo.setCurrentIndex(index)
                    break
        
        self._applyChartTheme()
        self.chartThemeChanged.emit(value)
    
    @Property(bool)
    def showLegend(self):
        return self._showLegend
    
    @showLegend.setter
    def showLegend(self, value):
        self._showLegend = bool(value)
        if hasattr(self, 'legend_btn'):
            self.legend_btn.setChecked(value)
        self.chart.legend().setVisible(self._showLegend)
    
    @Property(bool)
    def showTooltip(self):
        return self._showTooltip
    
    @showTooltip.setter
    def showTooltip(self, value):
        self._showTooltip = bool(value)
        # Tooltip implementation would go here
    
    @Property(bool)
    def animationEnabled(self):
        return self._animationEnabled
    
    @animationEnabled.setter
    def animationEnabled(self, value):
        self._animationEnabled = bool(value)
        if self._animationEnabled:
            self.chart.setAnimationOptions(QChart.SeriesAnimations)
            self.chart.setAnimationDuration(self._animationDuration)
        else:
            self.chart.setAnimationOptions(QChart.NoAnimation)
    
    @Property(int)
    def animationDuration(self):
        return self._animationDuration
    
    @animationDuration.setter
    def animationDuration(self, value):
        self._animationDuration = max(0, value)
        if hasattr(self, 'anim_slider'):
            self.anim_slider.setValue(value)
        if self._animationEnabled:
            self.chart.setAnimationDuration(self._animationDuration)
    
    @Property(bool)
    def zoomEnabled(self):
        return self._zoomEnabled
    
    @zoomEnabled.setter
    def zoomEnabled(self, value):
        self._zoomEnabled = bool(value)
        if hasattr(self, 'zoom_btn'):
            self.zoom_btn.setChecked(value)
        self._configureInteractions()
    
    @Property(bool)
    def panEnabled(self):
        return self._panEnabled
    
    @panEnabled.setter
    def panEnabled(self, value):
        self._panEnabled = bool(value)
        if hasattr(self, 'pan_btn'):
            self.pan_btn.setChecked(value)
        self._configureInteractions()
    
    @Property(bool)
    def antialiasing(self):
        return self._antialiasing
    
    @antialiasing.setter
    def antialiasing(self, value):
        self._antialiasing = bool(value)
        self.chart_view.setRenderHint(QPainter.Antialiasing, self._antialiasing)
    
    @Property(bool)
    def showControls(self):
        return self._showControls
    
    @showControls.setter
    def showControls(self, value):
        self._showControls = bool(value)
        if hasattr(self, 'controls_btn'):
            self.controls_btn.setChecked(value)
        self.control_panel.setVisible(self._showControls)
    
    @Property(QColor)
    def backgroundColor(self):
        return self._backgroundColor
    
    @backgroundColor.setter
    def backgroundColor(self, value):
        self._backgroundColor = value
        self._applyTheme()
    
    @Property(int)
    def titleFontSize(self):
        return self._titleFontSize
    
    @titleFontSize.setter
    def titleFontSize(self, value):
        self._titleFontSize = max(8, min(72, value))
        if hasattr(self, 'font_size_spin'):
            self.font_size_spin.setValue(value)
        self._applyVisualSettings()
    
    @Property(int)
    def axisFontSize(self):
        return self._axisFontSize
    
    @axisFontSize.setter
    def axisFontSize(self, value):
        self._axisFontSize = max(6, min(24, value))
        self._setupChart()
    
    @Property(str)
    def xAxisTitle(self):
        return self._xAxisTitle
    
    @xAxisTitle.setter
    def xAxisTitle(self, value):
        self._xAxisTitle = str(value)
        self._setupChart()
    
    @Property(str)
    def yAxisTitle(self):
        return self._yAxisTitle
    
    @yAxisTitle.setter
    def yAxisTitle(self, value):
        self._yAxisTitle = str(value)
        self._setupChart()
    
    @Property(float)
    def markerSize(self):
        return self._markerSize
    
    @markerSize.setter
    def markerSize(self, value):
        self._markerSize = max(1, min(20, value))
        self._setupChart()
    
    @Property(float)
    def lineWidth(self):
        return self._lineWidth
    
    @lineWidth.setter
    def lineWidth(self, value):
        self._lineWidth = max(0.5, min(10, value))
        self._setupChart()
    
    @Property(float)
    def pieHoleSize(self):
        return self._pieHoleSize
    
    @pieHoleSize.setter
    def pieHoleSize(self, value):
        self._pieHoleSize = max(0.0, min(0.9, value))
        self._setupChart()
    
    # ============ EVENT HANDLERS ============
    
    def mousePressEvent(self, event):
        """Handle mouse press for custom interactions"""
        if event.button() == Qt.RightButton:
            self._showContextMenu(event.pos())
        super().mousePressEvent(event)
    
    def _showContextMenu(self, pos):
        """Show context menu for chart"""
        menu = QMenu(self)
        
        # Chart type submenu
        type_menu = menu.addMenu("Chart Type")
        for chart_type in ChartType:
            action = type_menu.addAction(chart_type.value)
            action.triggered.connect(lambda checked, ct=chart_type: setattr(self, "chartType", ct.value))
        
        # Export actions
        export_menu = menu.addMenu("Export")
        export_png = export_menu.addAction("Export as PNG")
        export_png.triggered.connect(self._exportChart)
        
        export_settings = export_menu.addAction("Save Settings")
        export_settings.triggered.connect(lambda: self._saveSettingsDialog())
        
        load_settings = export_menu.addAction("Load Settings")
        load_settings.triggered.connect(lambda: self._loadSettingsDialog())
        
        # View actions
        menu.addSeparator()
        reset_action = menu.addAction("Reset View")
        reset_action.triggered.connect(self._resetView)
        
        toggle_legend = menu.addAction("Toggle Legend")
        toggle_legend.setCheckable(True)
        toggle_legend.setChecked(self._showLegend)
        toggle_legend.triggered.connect(lambda checked: setattr(self, "showLegend", not self._showLegend))
        
        menu.exec_(self.mapToGlobal(pos))
    
    def _saveSettingsDialog(self):
        """Show save settings dialog"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Chart Settings",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            if not filename.lower().endswith('.json'):
                filename += '.json'
            self.saveSettings(filename)
    
    def _loadSettingsDialog(self):
        """Show load settings dialog"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Chart Settings",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            self.loadSettings(filename)
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        # Update gradient if enabled
        if self._gradientEnabled:
            self._applyVisualSettings()
