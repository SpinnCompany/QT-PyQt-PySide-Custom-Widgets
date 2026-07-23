# file name: QCustomBarChart.py
from typing import List, Tuple, Optional, Dict, Any
from qtpy.QtCore import Qt, QPointF, Signal, Property, QRect
from qtpy.QtGui import QColor, QPen, QPainter, QPalette, QBrush
from qtpy.QtCharts import QChart, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis

from .QCustomChartBase import QCustomChartBase
from .QCustomBarChartBase import _RoundedBarOverlay
from .QCustomChartProps import ChartCommonProps, AxisChartProps
from Custom_Widgets.Utils import is_in_designer
from Custom_Widgets.QCustomCharts.QCustomChartConstants import (
    QCustomChartEnums as _CE,
    QCustomChartConstants as _CC, chart_str_to_int, chart_int_to_str,
    BAR_LABELS_TO_INT, INT_TO_BAR_LABELS)

class QCustomBarChart(QCustomChartBase, AxisChartProps, ChartCommonProps):
    """
    Bar chart implementation using the modular architecture.
    Qt Designer compatible with property exposure.
    """
    
    # Designer registration constants
    WIDGET_ICON = "components/icons/bar_chart.png"
    WIDGET_TOOLTIP = "Customizable bar chart with advanced styling"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomBarChart' name='customBarChart'>
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

    # Rich editors for the Designer "Custom Properties" dock (see
    # DesignerTools.CustomPropertiesDock).
    DESIGNER_CUSTOM_PROPS = [
        {"name": "chartTitle", "kind": "str", "group": "Titles"},
        {"name": "xAxisTitle", "kind": "str", "group": "Titles"},
        {"name": "yAxisTitle", "kind": "str", "group": "Titles"},
        {"name": "theme", "kind": "choice", "enum": _CE.ChartTheme, "group": "Appearance"},
        {"name": "showGrid", "kind": "bool", "group": "Appearance"},
        {"name": "gridColor", "kind": "color", "group": "Appearance"},
        {"name": "antialiasing", "kind": "bool", "group": "Appearance"},
        {"name": "compactMode", "kind": "bool", "group": "Appearance"},
        {"name": "autoScale", "kind": "bool", "group": "Appearance"},
        {"name": "barWidth", "kind": "float", "group": "Bars"},
        {"name": "stacked", "kind": "bool", "group": "Bars"},
        {"name": "showValueLabels", "kind": "bool", "group": "Bars"},
        {"name": "valueLabelsFormat", "kind": "str", "group": "Bars"},
        {"name": "labelsPosition", "kind": "choice", "enum": _CE.BarLabelsPosition, "group": "Bars"},
        {"name": "showLegend", "kind": "bool", "group": "Legend"},
        {"name": "legendPosition", "kind": "choice", "enum": _CE.LegendPosition, "group": "Legend"},
        {"name": "legendFontSize", "kind": "int", "group": "Legend"},
        {"name": "legendBackgroundVisible", "kind": "bool", "group": "Legend"},
        {"name": "showCrosshair", "kind": "bool", "group": "Crosshair"},
        {"name": "crosshairColor", "kind": "color", "group": "Crosshair"},
        {"name": "crosshairWidth", "kind": "float", "group": "Crosshair"},
        {"name": "animationEnabled", "kind": "bool", "group": "Animation"},
        {"name": "animationDuration", "kind": "int", "group": "Animation"},
        {"name": "showToolbar", "kind": "bool", "group": "Interaction"},
        {"name": "tooltipsEnabled", "kind": "bool", "group": "Interaction"},
        {"name": "tooltipDelay", "kind": "int", "group": "Interaction"},
        {"name": "tooltipDuration", "kind": "int", "group": "Interaction"},
    ]
    
    # Additional signals for bar chart
    barClicked = Signal(str, float, str)  # category, value, series_name
    barHovered = Signal(str, float, str)  # category, value, series_name
    seriesAdded = Signal(str)
    seriesRemoved = Signal(str)
    chartExportComplete = Signal(str, bool)  # filename, success
    legendPositionChanged = Signal(str)  # New signal for legend position changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Bar chart specific properties
        self._bar_series_dict = {}  # {series_name: QBarSeries}
        self._bar_sets_dict = {}    # {series_name: QBarSet}
        self._bar_corner_radius = 0     # px; >0 draws top-rounded bars via overlay
        self._bar_group_frac = 0.7      # last group width fraction (for the overlay)
        self._rounded_overlay = None
        self._orientation = "vertical"  # QCustomBarChart renders vertical bars
        self._bar_colors = {}           # {series_name: [QColor|None, ...]} per-bar override
        self._bar_highlight = {}        # {series_name: {index: QColor}} single-bar accents
        
        # Chart configuration
        self._chart.setTitle("Bar Chart")
        self._chart.legend().setVisible(True)
        
        # Initialize axes for bar chart
        self._axis_x = QBarCategoryAxis()
        self._axis_x.setTitleText("Categories")
        self._chart.addAxis(self._axis_x, Qt.AlignBottom)
        
        self._axis_y = QValueAxis()
        self._axis_y.setTitleText("Values")
        self._axis_y.setGridLineVisible(True)
        self._chart.addAxis(self._axis_y, Qt.AlignLeft)
        
        # Additional properties for Designer
        self._chart_title = "Bar Chart"
        self._x_axis_title = "Categories"
        self._y_axis_title = "Values"
        self._show_grid = True
        self._auto_scale = True
        self._animation_enabled = True
        self._animation_duration = 1000
        self._antialiasing = True
        self._bar_width = 0.7  # Relative bar width (0.0 to 1.0)
        self._bar_spacing = 0.3  # Spacing between bars in same category
        self._show_labels = True
        self._labels_angle = 0
        # Use constants from QCustomChartConstants
        self._labels_position = self.BAR_LABELS_CENTER
        self._show_legend = True
        self._stacked = False
        self._grouped = True
        self._show_value_labels = True
        self._value_labels_format = "{:.1f}"
        self._grid_color = QColor(200, 200, 200, 100)
        
        # Use constants from QCustomChartConstants
        self._default_bar_colors = self.DEFAULT_BAR_COLORS
        
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
            # Generate dummy bar chart data
            self._addDummyBarData(num_series=3, num_categories=5)
            
            # Update the chart display
            self.updateChart()
            
            # Set nice chart title for designer
            self._chart.setTitle("Bar Chart Preview (Designer Mode)")
            self._axis_x.setTitleText("Categories - Dummy Data")
            self._axis_y.setTitleText("Values - Dummy Data")
            
            print("Designer mode detected - showing dummy bar chart data")
    
    def _addDummyBarData(self, num_series=3, num_categories=5):
        """Add dummy bar chart data"""
        import random
        
        # Clear existing data first
        self.clearAllData()
        
        # Generate categories
        categories = [f"Category {i+1}" for i in range(num_categories)]
        
        # Add series
        for i in range(num_series):
            series_name = f"Series {i+1}"
            data = []
            
            # Generate random values for each category
            for j, category in enumerate(categories):
                value = random.uniform(10, 100) + i * 20
                # For bar chart, we store data as (category_index, value)
                # where category_index is used for positioning
                data.append((j, value))
            
            # Get color from default colors
            color_idx = i % len(self._default_bar_colors)
            
            # Add series to data manager
            self._data_manager.addSeries(
                name=series_name,
                data=data,  # Note: Bar chart uses (category_index, value) format
                color=self._default_bar_colors[color_idx],
                visible=True,
                line_style=self.LINE_NONE,  # No line for bar chart
                line_width=1.0,
                marker_style=self.MARKER_NONE,
                marker_size=0.0
            )
        
        # Store categories in data manager for reference
        if hasattr(self._data_manager, '_categories'):
            self._data_manager._categories = categories
        else:
            # Create custom attribute if not exists
            self._data_manager._categories = categories
    
    def generateExampleData(self, example_type: str = "simple"):
        """
        Generate example bar chart data for testing.
        
        Args:
            example_type: Type of example data to generate
                Options: "simple", "comparison", "stacked", "negative", "all"
        """
        import random
        
        # Clear existing data first
        self.clearAllData()
        
        # Define categories based on example type
        if example_type in ["simple", "comparison"]:
            categories = ["Q1", "Q2", "Q3", "Q4"]
            num_series = 1 if example_type == "simple" else 3
        elif example_type == "stacked":
            categories = ["Jan", "Feb", "Mar", "Apr", "May"]
            num_series = 4
            self._stacked = True
        elif example_type == "negative":
            categories = ["A", "B", "C", "D", "E"]
            num_series = 2
        else:  # "all" or default
            categories = ["Group 1", "Group 2", "Group 3", "Group 4"]
            num_series = 3
        
        # Add series
        for i in range(num_series):
            series_name = f"Data {chr(65 + i)}"  # A, B, C, etc.
            data = []
            
            for j, category in enumerate(categories):
                if example_type == "simple":
                    value = random.uniform(20, 80)
                elif example_type == "comparison":
                    value = random.uniform(30, 90) + i * 10
                elif example_type == "stacked":
                    value = random.uniform(10, 30)  # Smaller values for stacking
                elif example_type == "negative":
                    # Generate both positive and negative values
                    value = random.uniform(-50, 50)
                else:  # "all" or default
                    value = random.uniform(10, 100)
                
                data.append((j, value))
            
            # Get color
            color_idx = i % len(self._default_bar_colors)
            
            self.addSeries(
                name=series_name,
                values=[value for _, value in data],
                categories=categories,
                color=self._default_bar_colors[color_idx],
                visible=True
            )
        
        # Store categories
        self._data_manager._categories = categories
        
        # Update chart
        self.updateChart()
        self._chart.setTitle(f"Bar Chart: {example_type.replace('_', ' ').title()}")
    
    def _onChartClicked(self, x: float, y: float):
        """Handle chart click and emit barClicked"""
        bar_info = self._findBarAtPoint(QPointF(x, y))
        if bar_info:
            category, value, series_name = bar_info
            self.barClicked.emit(category, value, series_name)
    
    def _onChartHovered(self, x: float, y: float):
        """Handle chart hover and emit barHovered"""
        bar_info = self._findBarAtPoint(QPointF(x, y))
        if bar_info:
            category, value, series_name = bar_info
            self.barHovered.emit(category, value, series_name)
    
    def _findClosestDataPoint(self, point: QPointF):
        """
        Find the closest data point to the given chart coordinates.
        Returns (series_name, (category_index, value)) or (None, None).
        """
        bar_info = self._findBarAtPoint(point)
        if bar_info:
            category, value, series_name = bar_info
            # Find category index
            categories = getattr(self._data_manager, '_categories', [])
            if category in categories:
                category_index = categories.index(category)
                return series_name, (category_index, value)
        return None, None
    
    def _findBarAtPoint(self, point: QPointF):
        """
        Find the bar at the given chart coordinates.
        Returns (category, value, series_name) or None.
        """
        # Get all series data
        series_data = self._data_manager.getVisibleSeriesData()
        
        # Get categories
        categories = getattr(self._data_manager, '_categories', [])
        if not categories:
            return None
        
        # Calculate bar dimensions
        num_series = len(series_data)
        num_categories = len(categories)
        
        if num_series == 0 or num_categories == 0:
            return None
        
        # Get axis ranges
        y_min, y_max = self._axis_y.min(), self._axis_y.max()
        
        # Check if point is within valid Y range (above 0 for positive values)
        if point.y() < y_min or point.y() > y_max:
            return None
        
        # Calculate which category the point is in
        # Assuming equal spacing of categories
        category_width = 1.0  # Each category occupies 1 unit in chart coordinates
        category_index = int(point.x() // category_width)
        
        if 0 <= category_index < len(categories):
            category = categories[category_index]
            
            # Calculate bar positions within category
            bar_width = self._bar_width / num_series
            bar_offset = (point.x() - category_index) - 0.5  # Center of category
            
            # Find which series/bar the point is in
            for series_idx, (series_name, data) in enumerate(series_data.items()):
                if not data or len(data) <= category_index:
                    continue
                
                # Get bar value for this category
                bar_data = data[category_index]
                if isinstance(bar_data, tuple) and len(bar_data) == 2:
                    cat_idx, value = bar_data
                else:
                    continue
                
                # Calculate bar position
                bar_start = (series_idx * bar_width) - (self._bar_width / 2)
                bar_end = bar_start + bar_width
                
                # Check if point is within this bar horizontally
                if bar_start <= bar_offset <= bar_end:
                    # Check if point is within bar vertically (above 0 for positive bars)
                    if 0 <= point.y() <= value or (value < 0 and value <= point.y() <= 0):
                        return category, value, series_name
        
        return None
    
    def _isPointInChartBounds(self, point: QPointF) -> bool:
        """Check if point is within chart bounds"""
        try:
            x_min, x_max = 0, len(getattr(self._data_manager, '_categories', []))
            y_min, y_max = self._axis_y.min(), self._axis_y.max()
            
            return (0 <= point.x() <= x_max) and (y_min <= point.y() <= y_max)
        except:
            return False
    
    def updateChart(self):
        """Update the chart display based on current data"""
        # Clear existing bar series
        for series in list(self._bar_series_dict.values()):
            self._chart.removeSeries(series)
        self._bar_series_dict.clear()
        self._bar_sets_dict.clear()
        
        # Get visible series data
        series_data = self._data_manager.getVisibleSeriesData()
        
        if not series_data:
            # Clear axes if no data
            self._axis_x.clear()
            self._axis_y.setRange(0, 10)
            return
        
        # Get or create categories
        categories = getattr(self._data_manager, '_categories', [])
        if not categories:
            # Generate categories from data
            max_len = max(len(data) for data in series_data.values())
            categories = [f"Cat {i+1}" for i in range(max_len)]
            self._data_manager._categories = categories
        
        # Update X axis with categories
        self._axis_x.clear()
        self._axis_x.append(categories)
        
        # Create bar sets for each series
        bar_sets = []
        for series_name, data_points in series_data.items():
            if not data_points:
                continue
            
            # Create bar set
            bar_set = QBarSet(series_name)
            
            # Get series color
            color = self._data_manager.getSeriesColor(series_name)
            if color:
                # Apply some transparency for better visibility
                bar_color = QColor(color)
                bar_color.setAlpha(200)
                bar_set.setColor(bar_color)
                bar_set.setBorderColor(color.darker(150))
            
            # Add values to bar set
            for i, cat in enumerate(categories):
                if i < len(data_points):
                    # data_points[i] should be (category_index, value)
                    if isinstance(data_points[i], tuple) and len(data_points[i]) == 2:
                        _, value = data_points[i]
                    else:
                        value = data_points[i] if isinstance(data_points[i], (int, float)) else 0
                else:
                    value = 0
                bar_set.append(value)

            # Per-bar colours / single-bar highlight (native rendering). The
            # rounded overlay reads the same overrides so both modes match.
            self._applyPerBarColors(bar_set, series_name)

            # Store bar set
            self._bar_sets_dict[series_name] = bar_set
            bar_sets.append(bar_set)
        
        if bar_sets:
            # Create bar series
            if self._stacked:
                bar_series = QBarSeries()
                bar_series.setBarWidth(self._bar_width)
                for bar_set in bar_sets:
                    bar_series.append(bar_set)
            else:
                # Grouped bars
                bar_series = QBarSeries()
                bar_series.setBarWidth(self._bar_width)
                for bar_set in bar_sets:
                    bar_series.append(bar_set)
            
            # Store series reference
            self._bar_series_dict["main"] = bar_series
            
            # Add series to chart
            self._chart.addSeries(bar_series)
            
            # Attach axes
            bar_series.attachAxis(self._axis_x)
            bar_series.attachAxis(self._axis_y)
            
            # Configure value labels if enabled
            if self._show_value_labels:
                bar_series.setLabelsVisible(True)
                bar_series.setLabelsFormat(self._value_labels_format)
                bar_series.setLabelsPosition(
                    getattr(QBarSeries, f"Labels{self._labels_position}", QBarSeries.LabelsCenter)
                )
            
            # Calculate Y axis range
            all_values = []
            for bar_set in bar_sets:
                for i in range(bar_set.count()):
                    all_values.append(bar_set.at(i))
            
            if all_values and self._auto_scale:
                y_min, y_max = min(all_values), max(all_values)
                
                # Add some margin
                margin = 0.1 * (y_max - y_min) if y_max > y_min else 0.1 * y_max if y_max != 0 else 1
                
                # Handle negative values
                if y_min < 0:
                    y_min -= margin
                else:
                    y_min = max(0, y_min - margin)
                
                y_max += margin
                
                self._axis_y.setRange(y_min, y_max)
        
        # Set axis titles
        self._axis_x.setTitleText(self._x_axis_title)
        self._axis_y.setTitleText(self._y_axis_title)
        
        # Set chart title
        self._chart.setTitle(self._chart_title)
        
        # Set grid visibility and color
        self._axis_y.setGridLineVisible(self._show_grid)
        self._axis_y.setGridLineColor(self._grid_color)

        # Rounded bars: hide native fills and let the overlay paint them
        self._bar_group_frac = self._bar_width
        self._applyRoundedBars(bar_sets)

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
    
    def _applyRoundedBars(self, bar_sets):
        """Toggle rounded-bar rendering: hide native fills + drive the overlay."""
        if self._bar_corner_radius > 0:
            transparent = QColor(0, 0, 0, 0)
            for bs in bar_sets:
                bs.setColor(transparent)
                bs.setBorderColor(transparent)
            if self._rounded_overlay is None:
                self._rounded_overlay = _RoundedBarOverlay(self)
                try:
                    self._chart.plotAreaChanged.connect(
                        lambda *_: self._rounded_overlay and self._rounded_overlay.refresh())
                except Exception:
                    pass
            self._rounded_overlay.setVisible(True)
            self._rounded_overlay.refresh()
        elif self._rounded_overlay is not None:
            self._rounded_overlay.setVisible(False)

    def setBarCornerRadius(self, radius: int):
        """Round the top corners of bars (px). 0 restores native square bars.

        QtCharts has no rounded-bar support, so this paints a rounded overlay
        over the (hidden) native bars. Vertical bars only.
        """
        self._bar_corner_radius = max(0, int(radius))
        self.updateChart()

    def getBarCornerRadius(self) -> int:
        return self._bar_corner_radius

    # ============ PER-BAR COLOURS / HIGHLIGHT ============

    def _colorForBar(self, series_name: str, index: int):
        """Resolve the override colour for one bar, or None to use the series
        colour. Highlight wins over the per-bar list."""
        hl = self._bar_highlight.get(series_name, {})
        if index in hl:
            return hl[index]
        cols = self._bar_colors.get(series_name)
        if cols and index < len(cols) and cols[index] is not None:
            return QColor(cols[index])
        return None

    def _applyPerBarColors(self, bar_set, series_name):
        for i in range(bar_set.count()):
            c = self._colorForBar(series_name, i)
            if c is not None:
                bar_set.setColor(i, QColor(c))

    def setBarColors(self, colors, series_name: str = None):
        """Give each bar its own colour. ``colors`` is a list parallel to the
        series values (use None for a bar that should keep the series colour).
        With one series you can omit ``series_name``.
        """
        name = series_name or self._firstSeriesName()
        if name is None:
            return
        self._bar_colors[name] = [None if c is None else QColor(c) for c in (colors or [])]
        self.updateChart()

    def highlightIndex(self, index: int, color=None, series_name: str = None):
        """Accent a single bar (by category index). ``color`` defaults to a
        lightened series colour. Pass color=None + index<0 semantics via
        clearHighlight()."""
        name = series_name or self._firstSeriesName()
        if name is None:
            return
        if color is None:
            base = self._data_manager.getSeriesColor(name)
            color = base.lighter(140) if base and base.isValid() else QColor("#2fce80")
        self._bar_highlight.setdefault(name, {})[int(index)] = QColor(color)
        self.updateChart()

    def clearHighlight(self, series_name: str = None):
        if series_name:
            self._bar_highlight.pop(series_name, None)
        else:
            self._bar_highlight.clear()
        self.updateChart()

    def clearBarColors(self, series_name: str = None):
        if series_name:
            self._bar_colors.pop(series_name, None)
        else:
            self._bar_colors.clear()
        self.updateChart()

    def _firstSeriesName(self):
        names = self._data_manager.getSeriesNames()
        return names[0] if names else None

    def setGridLineColor(self, color, alpha: Optional[int] = None):
        """Set the grid line colour (and optionally its alpha 0-255)."""
        c = QColor(color)
        if alpha is not None:
            c.setAlpha(max(0, min(255, int(alpha))))
        self._grid_color = c
        try:
            self._axis_y.setGridLineColor(c)
            self._axis_x.setGridLineColor(c)
        except Exception:
            pass

    def setGridLineAlpha(self, alpha: int):
        """Set just the grid line opacity (0-255), keeping the current hue."""
        c = QColor(self._grid_color)
        c.setAlpha(max(0, min(255, int(alpha))))
        self.setGridLineColor(c)

    def _updateLegendSettings(self):
        """Update legend settings"""
        legend = self._chart.legend()
        if legend:
            legend.setVisible(self._show_legend)
            font = legend.font()
            font.setPointSize(self._legend_font_size)
            legend.setFont(font)
            legend.setBackgroundVisible(self._legend_background_visible)
    
    # ============ PUBLIC API (Matching LineChart) ============
    
    def addSeries(self, name: str, values: List[float], 
                 categories: Optional[List[str]] = None,
                 color: Optional[QColor] = None,
                 visible: bool = True) -> bool:
        """
        Add a bar series to the chart.
        
        Args:
            name: Unique series name
            values: List of bar values
            categories: Optional list of category names
            color: Optional series color
            visible: Optional visibility
            
        Returns:
            bool: True if added successfully
        """
        # Convert values to (category_index, value) format
        data = [(i, value) for i, value in enumerate(values)]
        
        # Update categories if provided
        if categories:
            self._data_manager._categories = categories
        elif not hasattr(self._data_manager, '_categories'):
            # Create default categories if none exist
            self._data_manager._categories = [f"Cat {i+1}" for i in range(len(values))]
        
        success = self._data_manager.addSeries(
            name=name,
            data=data,
            color=color,
            visible=visible,
            line_style=self.LINE_NONE,
            line_width=1.0,
            marker_style=self.MARKER_NONE,
            marker_size=0.0
        )
        
        if success:
            self.updateChart()
        
        return success
    
    def setCategories(self, categories: List[str]):
        """Set the category names for the X axis"""
        self._data_manager._categories = categories
        self.updateChart()
    
    def getCategories(self) -> List[str]:
        """Get the current category names"""
        return getattr(self._data_manager, '_categories', [])
    
    def setXAxisTitle(self, title: str):
        """Set X axis title"""
        self._x_axis_title = title
        self._axis_x.setTitleText(title)
    
    def setYAxisTitle(self, title: str):
        """Set Y axis title"""
        self._y_axis_title = title
        self._axis_y.setTitleText(title)
    
    def setYAxisRange(self, min_val: float, max_val: float):
        """Set Y axis range"""
        self._auto_scale = False
        self._axis_y.setRange(min_val, max_val)
    
    def getYAxisRange(self) -> Tuple[float, float]:
        """Get Y axis range"""
        return self._axis_y.min(), self._axis_y.max()
    
    # Compatibility methods (same as LineChart)
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
    
    def removeSeries(self, name: str) -> bool:
        """Remove a series from the chart"""
        success = self._data_manager.removeSeries(name)
        if success:
            self.updateChart()
        return success
    
    def updateSeriesData(self, name: str, values: List[float]) -> bool:
        """Update data for an existing series"""
        # Convert values to (category_index, value) format
        data = [(i, value) for i, value in enumerate(values)]
        success = self._data_manager.updateSeriesData(name, data)
        if success:
            self.updateChart()
        return success
    
    def appendToSeries(self, name: str, values: List[float]) -> bool:
        """Append values to an existing series"""
        # Convert values to (category_index, value) format
        # Need to offset indices based on current data length
        current_data = self._data_manager.getSeriesData(name) or []
        start_index = len(current_data)
        data = [(start_index + i, value) for i, value in enumerate(values)]
        success = self._data_manager.appendToSeries(name, data)
        if success:
            self.updateChart()
        return success
    
    # ============ BAR-SPECIFIC METHODS ============
    
    def setBarWidth(self, width: float):
        """Set relative bar width (0.0 to 1.0)"""
        self._bar_width = max(0.0, min(1.0, width))
        self.updateChart()
    
    def getBarWidth(self) -> float:
        """Get current bar width"""
        return self._bar_width
    
    def setStacked(self, stacked: bool):
        """Set whether bars are stacked"""
        self._stacked = stacked
        self.updateChart()
    
    def isStacked(self) -> bool:
        """Check if bars are stacked"""
        return self._stacked
    
    def setShowValueLabels(self, show: bool):
        """Set whether value labels are shown on bars"""
        self._show_value_labels = show
        self.updateChart()
    
    def getShowValueLabels(self) -> bool:
        """Check if value labels are shown"""
        return self._show_value_labels
    
    def setValueLabelsFormat(self, format_str: str):
        """Set format string for value labels"""
        self._value_labels_format = format_str
        self.updateChart()
    
    def getValueLabelsFormat(self) -> str:
        """Get value labels format string"""
        return self._value_labels_format
    
    def setLabelsPosition(self, position: str):
        """Set position of value labels"""
        valid_positions = [self.BAR_LABELS_CENTER, self.BAR_LABELS_INSIDE_BASE, 
                          self.BAR_LABELS_INSIDE_END, self.BAR_LABELS_OUTSIDE_END]
        if position in valid_positions:
            self._labels_position = position
            self.updateChart()
    
    def getLabelsPosition(self) -> str:
        """Get current labels position"""
        return self._labels_position
    
    def getBarSet(self, series_name: str) -> Optional[QBarSet]:
        """Get QBarSet for a series"""
        return self._bar_sets_dict.get(series_name)
    
    def highlightBar(self, category: str, series_name: str, highlight: bool = True):
        """Highlight a specific bar"""
        if series_name in self._bar_sets_dict:
            bar_set = self._bar_sets_dict[series_name]
            categories = getattr(self._data_manager, '_categories', [])
            
            if category in categories:
                index = categories.index(category)
                if highlight:
                    bar_set.setColor(index, bar_set.color().lighter(150))
                else:
                    bar_set.setColor(index, self._data_manager.getSeriesColor(series_name))
    
    # ============ CROSSHAIR METHODS (Same as LineChart) ============
    
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
    
    # ============ TOOLTIP METHODS (Same as LineChart) ============
    
    def showTooltipAt(self, x: float, y: float, series_name: str, title: str = None, description: str = None):
        """Manually show tooltip at specific coordinates"""
        # This would need to be implemented in the tooltip manager
        pass
    
    def hideTooltip(self):
        """Manually hide tooltip"""
        self._tooltip_manager.hide()
    
    # ============ LEGEND METHODS (Same as LineChart) ============
    
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
    
    # ============ THEME METHODS (Same as LineChart) ============
    
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
    
    # ============ EXPORT METHODS (Same as LineChart) ============
    
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
    # Common properties are inherited from ChartCommonProps and
    # AxisChartProps (see QCustomChartProps.py). Only bar-chart specific
    # implementations live here (the bar chart grid/legend variants
    # intentionally differ from the line/area charts).

    @Property(bool)
    def showGrid(self):
        """Get grid visibility"""
        return self._show_grid

    @showGrid.setter
    def showGrid(self, value: bool):
        """Set grid visibility (value axis only)"""
        self._show_grid = value
        self._axis_y.setGridLineVisible(value)

    @Property(QColor)
    def gridColor(self):
        """Get grid color"""
        return self._grid_color

    @gridColor.setter
    def gridColor(self, value: QColor):
        """Set grid color (value axis only)"""
        self._grid_color = value
        self._axis_y.setGridLineColor(value)

    @Property(bool)
    def showLegend(self):
        """Get legend visibility"""
        return self._show_legend

    @showLegend.setter
    def showLegend(self, value: bool):
        """Set legend visibility"""
        self._show_legend = value
        self._updateLegendSettings()

    @Property(float)
    def barWidth(self):
        """Get bar width"""
        return self._bar_width

    @barWidth.setter
    def barWidth(self, value: float):
        """Set bar width"""
        self._bar_width = max(0.0, min(1.0, value))
        self.updateChart()

    @Property(bool)
    def stacked(self):
        """Get stacked state"""
        return self._stacked

    @stacked.setter
    def stacked(self, value: bool):
        """Set stacked state"""
        self._stacked = value
        self.updateChart()

    @Property(bool)
    def showValueLabels(self):
        """Get value labels visibility"""
        return self._show_value_labels

    @showValueLabels.setter
    def showValueLabels(self, value: bool):
        """Set value labels visibility"""
        self._show_value_labels = value
        self.updateChart()

    @Property(str)
    def valueLabelsFormat(self):
        """Get value labels format"""
        return self._value_labels_format

    @valueLabelsFormat.setter
    def valueLabelsFormat(self, value: str):
        """Set value labels format"""
        self._value_labels_format = value
        self.updateChart()

    @Property(int)
    def labelsPosition(self):
        """Bar labels position (int; see QCustomChartEnums.BarLabelsPosition)."""
        return chart_str_to_int(BAR_LABELS_TO_INT, self._labels_position)

    @labelsPosition.setter
    def labelsPosition(self, value):
        self._labels_position = chart_int_to_str(INT_TO_BAR_LABELS, value, _CC.BAR_LABELS_CENTER)
        self.updateChart()
