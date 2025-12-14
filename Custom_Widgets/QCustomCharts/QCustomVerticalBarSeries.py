# file name: QCustomVerticalBarSeries.py
import csv
import json
import io
import random
from typing import List, Tuple, Optional, Dict, Any, Union
from qtpy.QtCore import Qt, QPointF, Signal, Property, QTimer, QEasingCurve
from qtpy.QtGui import QColor, QPen, QPainter, QPalette, QBrush, QFont
from qtpy.QtCharts import QChart, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QAbstractBarSeries

from .QCustomChartBase import QCustomChartBase
from Custom_Widgets.Utils import is_in_designer


class QCustomVerticalBarSeries(QCustomChartBase):
    """
    Vertical grouped bar chart implementation using the modular architecture.
    Qt Designer compatible with property exposure.
    """
    
    # Designer registration constants
    WIDGET_ICON = "components/icons/bar_chart.png"
    WIDGET_TOOLTIP = "Customizable vertical grouped bar chart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomVerticalBarSeries' name='customVerticalBarSeries'>
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
    
    # Additional signals for bar chart
    barClicked = Signal(str, float, str)  # category, value, series_name
    barHovered = Signal(str, float, str)  # category, value, series_name
    barValueChanged = Signal(str, str, float, float)  # category, series_name, old_value, new_value
    seriesAdded = Signal(str)
    seriesRemoved = Signal(str)
    chartExportComplete = Signal(str, bool)  # filename, success
    legendPositionChanged = Signal(str)  # New signal for legend position changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Bar chart specific properties
        self._bar_series_dict = {}  # {series_name: QBarSeries}
        self._bar_sets_dict = {}    # {series_name: QBarSet}
        
        # Track current hovered bar to prevent multiple tooltips
        self._current_hovered_bar = None  # (category, series_name) tuple
        
        # Chart configuration
        self._chart.setTitle("Vertical Bar Chart")
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
        self._chart_title = "Vertical Bar Chart"
        self._x_axis_title = "Categories"
        self._y_axis_title = "Values"
        self._show_grid = True
        self._auto_scale = True
        self._animation_enabled = True
        self._animation_duration = self.DEFAULT_BAR_ANIMATION_DURATION
        self._antialiasing = True
        
        # Bar width and spacing properties
        self._bar_width = self.DEFAULT_BAR_WIDTH  # Use constant
        self._custom_category_spacing = self.DEFAULT_BAR_SPACING  # Use constant
        self._bar_spacing = 0.1  # Spacing between bars within same category
        
        # Bar animation properties - USING CONSTANTS
        self._animation_easing_curve = QEasingCurve(self.EASING_CURVE_MAP[self.DEFAULT_ANIMATION_EASING])
        
        # Value labels properties
        self._show_labels = True
        self._labels_angle = 0
        self._labels_position = QAbstractBarSeries.LabelsCenter  # Qt constant
        self._show_legend = True
        self._show_value_labels = True
        self._value_labels_format = "{:.1f}"
        self._custom_value_labels_font_size = self.DEFAULT_BAR_VALUE_FONT_SIZE
        self._custom_value_labels_color = self.DEFAULT_BAR_VALUE_COLOR
        self._custom_value_labels_background = QColor(255, 255, 255, 180)
        self._custom_grid_color = QColor(200, 200, 200, 100)
        
        # Bar styling properties - APPLIED TO ENTIRE BAR SET
        self._custom_bar_border_width = self.DEFAULT_BAR_BORDER_WIDTH
        self._custom_bar_border_color = self.DEFAULT_BAR_BORDER_COLOR
        self._bar_pattern = self.BAR_PATTERN_SOLID
        
        # Bar border style
        self._bar_border_style = self.BAR_BORDER_SOLID
        
        # Bar selection properties
        self._bar_selection_mode = self.BAR_SELECTION_NONE
        self._selected_bars = {}  # {series_name: [bar_indices]}
        
        # Tooltip properties
        self._tooltip_delay = 500
        self._tooltip_duration = 5000
        self._custom_tooltip_format = self.DEFAULT_BAR_TOOLTIP_FORMAT
        
        # Legend properties
        self._legend_font_size = 8
        self._legend_background_visible = False
        
        # Performance properties
        self._lazy_loading = False
        self._virtualization = False
        self._batch_size = 50
        
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
            self._chart.setTitle("Vertical Bar Chart Preview (Designer Mode)")
            self._axis_x.setTitleText("Categories - Dummy Data")
            self._axis_y.setTitleText("Values - Dummy Data")
            
            print("Designer mode detected - showing dummy bar chart data")
    
    def _addDummyBarData(self, num_series=3, num_categories=5):
        """Add dummy bar chart data"""        
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
                data.append((j, value))
            
            # Get color from default colors
            color_idx = i % len(self.DEFAULT_BAR_COLORS)
            
            # Add series to data manager
            self._data_manager.addSeries(
                name=series_name,
                data=data,
                color=self.DEFAULT_BAR_COLORS[color_idx],
                visible=True,
                line_style=self.LINE_NONE,
                line_width=1.0,
                marker_style=self.MARKER_NONE,
                marker_size=0.0
            )
        
        # Store categories in data manager for reference
        self._data_manager._categories = categories

    # ============ BAR STYLING METHODS ============
    
    def _applyBarPattern(self, bar_set):
        """Apply pattern to entire bar set"""
        if self._bar_pattern != self.BAR_PATTERN_SOLID:
            # Apply pattern to entire bar set
            current_brush = bar_set.brush()
            if not current_brush:
                current_brush = QBrush(bar_set.color())
            
            pattern_brush = QBrush(current_brush.color(), 
                                self.BAR_PATTERN_BRUSHES.get(self._bar_pattern, Qt.SolidPattern))
            bar_set.setBrush(pattern_brush)
    
    def _applyBarBorderStyle(self, bar_set):
        """Apply border style to bar set"""
        pen = bar_set.pen()
        
        # Set width
        if self._custom_bar_border_width > 0:
            pen.setWidthF(self._custom_bar_border_width)
        
        # Set color
        if self._custom_bar_border_color.isValid():
            pen.setColor(self._custom_bar_border_color)
        
        # Set style
        style = self.BAR_BORDER_STYLES.get(self._bar_border_style, Qt.SolidLine)
        pen.setStyle(style)
        
        bar_set.setPen(pen)
    
    def generateExampleData(self, example_type: str = "simple"):
        """
        Generate example bar chart data for testing.
        
        Args:
            example_type: Type of example data to generate
                Options: "simple", "comparison", "negative", "mixed", "all"
        """
        # Clear existing data first
        self.clearAllData()
        
        # Define categories based on example type
        if example_type == "simple":
            categories = ["Q1", "Q2", "Q3", "Q4"]
            num_series = 1
        elif example_type == "comparison":
            categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
            num_series = 3
        elif example_type == "negative":
            categories = ["A", "B", "C", "D", "E"]
            num_series = 2
        elif example_type == "mixed":
            categories = ["Group 1", "Group 2", "Group 3", "Group 4"]
            num_series = 4
        else:  # "all" or default
            categories = ["Category A", "Category B", "Category C", "Category D", "Category E"]
            num_series = 3
        
        # Add series
        for i in range(num_series):
            series_name = f"Data {chr(65 + i)}"  # A, B, C, etc.
            values = []
            
            for j, category in enumerate(categories):
                if example_type == "simple":
                    value = random.uniform(20, 80)
                elif example_type == "comparison":
                    value = random.uniform(30, 90) + i * 10
                elif example_type == "negative":
                    # Generate both positive and negative values
                    value = random.uniform(-50, 50)
                elif example_type == "mixed":
                    value = random.uniform(-30, 100)
                else:  # "all" or default
                    value = random.uniform(10, 100)
                
                values.append(value)
            
            # Get color
            color_idx = i % len(self.DEFAULT_BAR_COLORS)
            
            self.addSeries(
                name=series_name,
                values=values,
                categories=categories,
                color=self.DEFAULT_BAR_COLORS[color_idx],
                visible=True
            )
        
        # Update chart
        self.updateChart()
        self._chart.setTitle(f"Vertical Bar Chart: {example_type.replace('_', ' ').title()}")

    def _onChartClicked(self, x: float, y: float):
        """Handle chart click and emit barClicked"""
        bar_info = self._findBarAtPoint(QPointF(x, y))
        if bar_info:
            category, value, series_name = bar_info
            self.barClicked.emit(category, value, series_name)
            
            # Handle bar selection
            if self._bar_selection_mode != self.BAR_SELECTION_NONE:
                self._handleBarSelection(category, series_name)

    def _handleBarSelection(self, category: str, series_name: str):
        """Handle bar selection based on selection mode"""
        categories = self.getCategories()
        if category not in categories:
            return
        
        bar_index = categories.index(category)
        
        if self._bar_selection_mode == self.BAR_SELECTION_SINGLE:
            # Clear all selections and select this bar
            self._selected_bars.clear()
            self._selected_bars[series_name] = [bar_index]
        elif self._bar_selection_mode == self.BAR_SELECTION_MULTIPLE:
            # Toggle selection of this bar
            if series_name not in self._selected_bars:
                self._selected_bars[series_name] = []
            
            if bar_index in self._selected_bars[series_name]:
                self._selected_bars[series_name].remove(bar_index)
            else:
                self._selected_bars[series_name].append(bar_index)
        elif self._bar_selection_mode == self.BAR_SELECTION_CATEGORY:
            # Select all bars in this category across all series
            self._selected_bars.clear()
            for s_name in self.getSeriesNames():
                self._selected_bars[s_name] = [bar_index]
        
        # Update chart to show selection
        self.updateChart()

    def _onChartHovered(self, x: float, y: float):
        """Handle chart hover and emit barHovered"""
        bar_info = self._findBarAtPoint(QPointF(x, y))
        
        if bar_info:
            category, value, series_name = bar_info
            current_bar = (category, series_name)
            
            # Only show tooltip if it's a different bar than currently hovered
            if current_bar != self._current_hovered_bar:
                self.barHovered.emit(category, value, series_name)
                
                # Show tooltip if enabled
                if self.areTooltipsEnabled():
                    self._showBarTooltip(category, series_name, value, x, y)
                
                # Update current hovered bar
                self._current_hovered_bar = current_bar
        else:
            # Hide tooltip if no bar is hovered
            self._current_hovered_bar = None
            self.hideTooltip()

    def _showBarTooltip(self, category: str, series_name: str, value: float, x: float, y: float):
        """Show tooltip for bar - ensures only one tooltip per bar"""
        # Hide any existing tooltip first
        self.hideTooltip()
        
        # Calculate percentage if we have total for category
        categories = self.getCategories()
        if category in categories:
            bar_index = categories.index(category)
            category_total = 0
            for s_name in self.getSeriesNames():
                data = self.getSeriesData(s_name)
                if data and bar_index < len(data):
                    if isinstance(data[bar_index], tuple):
                        _, val = data[bar_index]
                        category_total += val
            
            percentage = (value / category_total * 100) if category_total != 0 else 0
            
            # Format tooltip
            tooltip_text = self._custom_tooltip_format.format(
                category=category,
                series=series_name,
                value=value,
                percentage=percentage,
                index=bar_index
            )
            
            # Show tooltip
            self._tooltip_manager.show(x, y, f"{series_name} - {category}", 
                                     tooltip_text, f"Value: {value:.2f}")

    def _findBarAtPoint(self, point: QPointF):
        """
        Find the bar at the given chart coordinates.
        Returns (category, value, series_name) or None.
        """
        # Get all series data
        series_data = self._data_manager.getVisibleSeriesData()
        
        # Get categories
        categories = self.getCategories()
        if not categories:
            return None
        
        # Calculate bar dimensions
        num_series = len(series_data)
        num_categories = len(categories)
        
        if num_series == 0 or num_categories == 0:
            return None
        
        # Get axis ranges
        y_min, y_max = self._axis_y.min(), self._axis_y.max()
        
        # Check if point is within valid Y range
        if point.y() < y_min or point.y() > y_max:
            return None
        
        # Calculate which category the point is in
        category_width = 1.0  # Each category occupies 1 unit in chart coordinates
        category_index = int(point.x() // category_width)
        
        if 0 <= category_index < len(categories):
            category = categories[category_index]
            
            # Calculate bar positions
            bar_width, bar_group_width = self._calculateBarPositions(num_series, num_categories)
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
                    value = bar_data if isinstance(bar_data, (int, float)) else 0
                
                # Calculate bar position
                bar_start = (series_idx * (bar_width + self._bar_spacing)) - (bar_group_width / 2)
                bar_end = bar_start + bar_width
                
                # Check if point is within this bar horizontally
                if bar_start <= bar_offset <= bar_end:
                    # Check if point is within bar vertically
                    bar_bottom = 0 if value >= 0 else value
                    bar_top = value if value >= 0 else 0
                    if bar_bottom <= point.y() <= bar_top:
                        return category, value, series_name
        
        return None

    def _calculateBarPositions(self, num_series, num_categories):
        """Calculate bar positions based on spacing and width settings"""
        # Calculate total space available per category (1.0 unit)
        total_available = 1.0
        
        # Apply category spacing (space between categories)
        if self._custom_category_spacing > 0:
            available_in_category = total_available - self._custom_category_spacing
        else:
            available_in_category = total_available
        
        # Apply bar width to control width within category
        bar_group_width = available_in_category * self._bar_width
        
        # Calculate individual bar width accounting for bar spacing
        total_spacing = (num_series - 1) * self._bar_spacing if num_series > 1 else 0
        bar_width = (bar_group_width - total_spacing) / num_series if num_series > 0 else 0
        
        return bar_width, bar_group_width

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
        categories = self.getCategories()
        if not categories:
            # Generate categories from data
            max_len = max(len(data) for data in series_data.values())
            categories = [f"Cat {i+1}" for i in range(max_len)]
            self._data_manager._categories = categories
        
        # Update X axis with categories
        self._axis_x.clear()
        self._axis_x.append(categories)
        
        # Calculate bar positions
        num_series = len(series_data)
        num_categories = len(categories)
        bar_width, bar_group_width = self._calculateBarPositions(num_series, num_categories)
        
        # Create bar sets for each series
        bar_sets = []
        for series_name, data_points in series_data.items():
            if not data_points:
                continue
            
            # Create bar set
            bar_set = QBarSet(series_name)
            
            # Get series base color
            base_color = self._data_manager.getSeriesColor(series_name)
            if not base_color.isValid():
                base_color = self.DEFAULT_BAR_COLORS[0]
            
            # Set default color for bar set
            bar_set.setColor(base_color)
            bar_set.setBorderColor(base_color.darker(150))
            
            # Apply border styling to entire bar set
            self._applyBarBorderStyle(bar_set)
            
            # Apply pattern to entire bar set
            if self._bar_pattern != self.BAR_PATTERN_SOLID:
                self._applyBarPattern(bar_set)
            
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
            
            # Store bar set
            self._bar_sets_dict[series_name] = bar_set
            bar_sets.append(bar_set)
        
        if bar_sets:
            # Create bar series with calculated width
            bar_series = QBarSeries()
            # Apply the calculated bar group width
            bar_series.setBarWidth(bar_group_width)
            
            # Connect bar series signals
            bar_series.clicked.connect(self._onBarSeriesClicked)
            bar_series.hovered.connect(self._onBarSeriesHovered)
            bar_series.doubleClicked.connect(self._onBarSeriesDoubleClicked)
            
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
            bar_series.setLabelsVisible(self._show_value_labels)
            bar_series.setLabelsFormat(self._value_labels_format)
            bar_series.setLabelsPosition(self._labels_position)
            bar_series.setLabelsAngle(self._labels_angle)
            
            # Apply custom label color and font size to all bar sets
            for bar_set in bar_sets:
                # Apply label brush (color)
                label_brush = QBrush(self._custom_value_labels_color)
                bar_set.setLabelBrush(label_brush)
                
                # Apply label font with custom size
                label_font = QFont()
                label_font.setPointSizeF(self._custom_value_labels_font_size)
                bar_set.setLabelFont(label_font)
            
            # Calculate Y axis range
            all_values = []
            for bar_set in bar_sets:
                for i in range(bar_set.count()):
                    all_values.append(bar_set.at(i))
            
            if all_values and self._auto_scale:
                y_min, y_max = min(all_values), max(all_values)
                
                # Add some margin
                margin = 0.1 * (y_max - y_min) if y_max > y_min else 0.1 * abs(y_max) if y_max != 0 else 1
                
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
        self._axis_y.setGridLineColor(self._custom_grid_color)
        
        # Set animation
        if self._animation_enabled:
            self._chart.setAnimationOptions(QChart.SeriesAnimations)
            self._chart.setAnimationDuration(self._animation_duration)
            self._chart.setAnimationEasingCurve(self._animation_easing_curve)
        else:
            self._chart.setAnimationOptions(QChart.NoAnimation)
        
        # Set antialiasing
        self._chart_view.setRenderHint(QPainter.Antialiasing, self._antialiasing)
        
        # Update legend
        self._updateLegendSettings()

    def _onBarSeriesClicked(self, index: int, bar_set: QBarSet):
        """Handle bar series clicked signal"""
        categories = self.getCategories()
        if 0 <= index < len(categories):
            value = bar_set.at(index)
            self.barClicked.emit(categories[index], value, bar_set.label())

    def _onBarSeriesHovered(self, state: bool, index: int, bar_set: QBarSet):
        """Handle bar series hovered signal"""
        if state:
            categories = self.getCategories()
            if 0 <= index < len(categories):
                value = bar_set.at(index)
                self.barHovered.emit(categories[index], value, bar_set.label())

    def _onBarSeriesDoubleClicked(self, index: int, bar_set: QBarSet):
        """Handle bar series double clicked signal"""
        categories = self.getCategories()
        if 0 <= index < len(categories):
            value = bar_set.at(index)
            # Emit custom signal or perform action
            print(f"Bar double clicked: {categories[index]}, {bar_set.label()}, {value}")

    def _updateLegendSettings(self):
        """Update legend settings"""
        legend = self._chart.legend()
        if legend:
            legend.setVisible(self._show_legend)
            font = legend.font()
            font.setPointSize(self._legend_font_size)
            legend.setFont(font)
            legend.setBackgroundVisible(self._legend_background_visible)

    # ============ ANIMATION CONFIGURATION METHODS ============
    
    def setAnimationEasingCurve(self, curve: str):
        """Set easing curve for animation by string name"""
        if curve in self.EASING_CURVE_MAP:
            curve_type = self.EASING_CURVE_MAP[curve]
            self._animation_easing_curve = QEasingCurve(curve_type)
            if self._animation_enabled:
                self._chart.setAnimationEasingCurve(self._animation_easing_curve)
    
    def setAnimationEasingCurveType(self, curve_type: QEasingCurve.Type):
        """Set easing curve for animation by Qt type"""
        self._animation_easing_curve = QEasingCurve(curve_type)
        if self._animation_enabled:
            self._chart.setAnimationEasingCurve(self._animation_easing_curve)
    
    def getAnimationEasingCurve(self) -> QEasingCurve:
        """Get the current animation easing curve"""
        return self._animation_easing_curve
    
    def getAnimationEasingCurveName(self) -> str:
        """Get the current animation easing curve as string name"""
        for name, curve_type in self.EASING_CURVE_MAP.items():
            if curve_type == self._animation_easing_curve.type():
                return name
        return "out_quad"  # Default
    
    def getAvailableAnimationEasingCurves(self) -> List[str]:
        """Get list of available animation easing curve names"""
        return list(self.EASING_CURVE_MAP.keys())
    
    def configureAnimation(self, enabled: bool = None, duration: int = None, 
                          easing_curve: str = None, easing_curve_type: QEasingCurve.Type = None):
        """Configure animation with all parameters at once"""
        if enabled is not None:
            self._animation_enabled = enabled
        
        if duration is not None:
            self._animation_duration = duration
        
        if easing_curve is not None:
            self.setAnimationEasingCurve(easing_curve)
        elif easing_curve_type is not None:
            self.setAnimationEasingCurveType(easing_curve_type)
        
        # Apply the settings
        self.updateChart()
    
    def setBarWidth(self, width: float):
        """Set relative bar width (0.0 to 1.0)"""
        self._bar_width = max(0.0, min(1.0, width))
        self.updateChart()
    
    def getBarWidth(self) -> float:
        """Get current bar width"""
        return self._bar_width
    
    def setBarSpacing(self, spacing: float):
        """Set spacing between bars within same category"""
        self._bar_spacing = max(0.0, min(0.5, spacing))
        self.updateChart()
    
    def getBarSpacing(self) -> float:
        """Get current bar spacing"""
        return self._bar_spacing

    # ============ BAR STYLING CONFIGURATION METHODS ============
    
    def setBarPattern(self, pattern: str):
        """Set pattern for bars"""
        valid_patterns = [
            self.BAR_PATTERN_SOLID,
            self.BAR_PATTERN_HORIZONTAL,
            self.BAR_PATTERN_VERTICAL,
            self.BAR_PATTERN_CROSS,
            self.BAR_PATTERN_DIAGONAL,
            self.BAR_PATTERN_REVERSE_DIAGONAL,
            self.BAR_PATTERN_DIAGONAL_CROSS,
            self.BAR_PATTERN_DENSE,
            self.BAR_PATTERN_SPARSE
        ]
        
        if pattern in valid_patterns:
            self._bar_pattern = pattern
            self.updateChart()
    
    def getBarPattern(self) -> str:
        """Get current bar pattern"""
        return self._bar_pattern
    
    def setBarBorderStyle(self, style: str):
        """Set border style for bars"""
        valid_styles = [
            self.BAR_BORDER_SOLID,
            self.BAR_BORDER_DASHED,
            self.BAR_BORDER_DOTTED,
            self.BAR_BORDER_DASH_DOT
        ]
        
        if style in valid_styles:
            self._bar_border_style = style
            self.updateChart()
    
    def getBarBorderStyle(self) -> str:
        """Get current bar border style"""
        return self._bar_border_style

    # ============ SELECTION CONFIGURATION METHODS ============
    
    def setBarSelectionMode(self, mode: str):
        """Set bar selection mode"""
        valid_modes = [
            self.BAR_SELECTION_NONE,
            self.BAR_SELECTION_SINGLE,
            self.BAR_SELECTION_MULTIPLE,
            self.BAR_SELECTION_CATEGORY
        ]
        
        if mode in valid_modes:
            self._bar_selection_mode = mode
            self.updateChart()
    
    def getBarSelectionMode(self) -> str:
        """Get current bar selection mode"""
        return self._bar_selection_mode
    
    def clearSelection(self):
        """Clear all bar selections"""
        self._selected_bars.clear()
        self.updateChart()
    
    def getSelectedBars(self) -> Dict[str, List[int]]:
        """Get currently selected bars"""
        return self._selected_bars.copy()

    # ============ PUBLIC API ============
    
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
    
    def setBarValue(self, series_name: str, bar_index: int, value: float):
        """Set value for specific bar"""
        if series_name not in self._bar_sets_dict:
            return False
        
        bar_set = self._bar_sets_dict[series_name]
        if bar_index >= bar_set.count():
            return False
        
        old_value = bar_set.at(bar_index)
        bar_set.replace(bar_index, value)
        
        # Emit value changed signal
        categories = self.getCategories()
        if bar_index < len(categories):
            self.barValueChanged.emit(categories[bar_index], series_name, old_value, value)
        
        self.updateChart()
        return True
    
    def getBarValue(self, series_name: str, bar_index: int) -> Optional[float]:
        """Get value for specific bar"""
        if series_name not in self._bar_sets_dict:
            return None
        
        bar_set = self._bar_sets_dict[series_name]
        if bar_index >= bar_set.count():
            return None
        
        return bar_set.at(bar_index)
    
    def setCategories(self, categories: List[str]):
        """Set the category names for the X axis"""
        self._data_manager._categories = categories
        self.updateChart()
    
    def getCategories(self) -> List[str]:
        """Get the current category names"""
        return getattr(self._data_manager, '_categories', [])
    
    # ============ QtCharts COMPATIBLE METHODS ============
    
    def setCategorySpacing(self, spacing: float):
        """Set spacing between categories - QtCharts compatible method"""
        self._custom_category_spacing = max(0.0, min(1.0, spacing))
        self.updateChart()
    
    def categorySpacing(self) -> float:
        """Get category spacing - QtCharts compatible method"""
        return self._custom_category_spacing
    
    # ============ CUSTOM METHODS (with compatibility aliases) ============
    
    def setCustomCategorySpacing(self, spacing: float):
        """Set spacing between categories"""
        self.setCategorySpacing(spacing)
    
    def getCustomCategorySpacing(self) -> float:
        """Get category spacing"""
        return self.categorySpacing()
    
    def setShowValueLabels(self, show: bool):
        """Set whether value labels are shown on bars"""
        self._show_value_labels = show
        self.updateChart()
    
    def getShowValueLabels(self) -> bool:
        """Check if value labels are shown"""
        return self._show_value_labels
    
    def setValueLabelsPosition(self, position: str):
        """Set position of value labels"""
        # Map string position to Qt constant
        position_map = {
            "inside_center": QAbstractBarSeries.LabelsCenter,
            "inside_end": QAbstractBarSeries.LabelsInsideEnd,
            "inside_base": QAbstractBarSeries.LabelsInsideBase,
            "outside_end": QAbstractBarSeries.LabelsOutsideEnd
        }
        
        if position in position_map:
            self._labels_position = position_map[position]
            self.updateChart()
    
    def getValueLabelsPosition(self) -> str:
        """Get value labels position as string"""
        # Map Qt constant to string
        if self._labels_position == QAbstractBarSeries.LabelsCenter:
            return "center"
        elif self._labels_position == QAbstractBarSeries.LabelsInsideEnd:
            return "inside_end"
        elif self._labels_position == QAbstractBarSeries.LabelsInsideBase:
            return "inside_base"
        elif self._labels_position == QAbstractBarSeries.LabelsOutsideEnd:
            return "outside_end"
        else:
            return "center"
    
    def setValueLabelsFormat(self, format_str: str):
        """Set format string for value labels"""
        self._value_labels_format = format_str
        self.updateChart()
    
    def getValueLabelsFormat(self) -> str:
        """Get value labels format string"""
        return self._value_labels_format
    
    def setCustomValueLabelsFontSize(self, size: float):
        """Set font size for value labels"""
        self._custom_value_labels_font_size = max(1.0, size)
        self.updateChart()
    
    def getCustomValueLabelsFontSize(self) -> float:
        """Get font size for value labels"""
        return self._custom_value_labels_font_size
    
    def setCustomValueLabelsColor(self, color: QColor):
        """Set color for value labels"""
        self._custom_value_labels_color = color
        self.updateChart()
    
    def getCustomValueLabelsColor(self) -> QColor:
        """Get color for value labels"""
        return self._custom_value_labels_color
    
    def setCustomBarBorderWidth(self, width: float):
        """Set border width for bars"""
        self._custom_bar_border_width = max(0.0, width)
        self.updateChart()
    
    def getCustomBarBorderWidth(self) -> float:
        """Get border width for bars"""
        return self._custom_bar_border_width
    
    def setCustomBarBorderColor(self, color: QColor):
        """Set border color for bars"""
        self._custom_bar_border_color = color
        self.updateChart()
    
    def getCustomBarBorderColor(self) -> QColor:
        """Get border color for bars"""
        return self._custom_bar_border_color
    
    def setAnimationEnabled(self, enabled: bool):
        """Set animation enabled state"""
        self._animation_enabled = enabled
        self.updateChart()
    
    def getAnimationEnabled(self) -> bool:
        """Get animation enabled state"""
        return self._animation_enabled
    
    def setAnimationDuration(self, duration: int):
        """Set animation duration"""
        self._animation_duration = duration
        self.updateChart()
    
    def getAnimationDuration(self) -> int:
        """Get animation duration"""
        return self._animation_duration
    
    def setCustomTooltipFormat(self, format_str: str):
        """Set tooltip format string"""
        self._custom_tooltip_format = format_str
    
    def getCustomTooltipFormat(self) -> str:
        """Get tooltip format string"""
        return self._custom_tooltip_format
    
    def setLazyLoading(self, enabled: bool):
        """Enable/disable lazy loading"""
        self._lazy_loading = enabled
    
    def getLazyLoading(self) -> bool:
        """Check if lazy loading is enabled"""
        return self._lazy_loading
    
    def setVirtualization(self, enabled: bool):
        """Enable/disable virtualization"""
        self._virtualization = enabled
    
    def getVirtualization(self) -> bool:
        """Check if virtualization is enabled"""
        return self._virtualization
    
    def setBatchSize(self, size: int):
        """Set batch size for rendering"""
        self._batch_size = max(1, size)
    
    def getBatchSize(self) -> int:
        """Get batch size for rendering"""
        return self._batch_size
    
    def setAntialiasing(self, enabled: bool):
        """Set antialiasing state"""
        self._antialiasing = enabled
        self._chart_view.setRenderHint(QPainter.Antialiasing, enabled)

    def setShowGrid(self, show: bool):
        """Set grid visibility"""
        self._show_grid = show
        self._axis_y.setGridLineVisible(show)

    def setShowLegend(self, show: bool):
        """Set legend visibility"""
        self._show_legend = show
        self._updateLegendSettings()

    def getAntialiasing(self) -> bool:
        """Get antialiasing state"""
        return self._antialiasing

    def getShowGrid(self) -> bool:
        """Get grid visibility"""
        return self._show_grid

    def getShowLegend(self) -> bool:
        """Get legend visibility"""
        return self._show_legend

    # ============ COMPATIBILITY METHODS ============
    
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
            # Clear current hovered bar if it's from this series
            if self._current_hovered_bar and self._current_hovered_bar[1] == name:
                self._current_hovered_bar = None
                self.hideTooltip()
            
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
    
    def setLabelsPosition(self, position: str):
        """Set position of value labels - compatibility method"""
        self.setValueLabelsPosition(position)
    
    def getLabelsPosition(self) -> str:
        """Get current labels position - compatibility method"""
        return self.getValueLabelsPosition()
    
    def getBarSet(self, series_name: str) -> Optional[QBarSet]:
        """Get QBarSet for a series"""
        return self._bar_sets_dict.get(series_name)
    
    # ============ STATISTICAL METHODS ============
    
    def getBarStatistics(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all bars"""
        stats = {}
        categories = self.getCategories()
        
        for i, category in enumerate(categories):
            values = []
            for series_name in self.getSeriesNames():
                data = self.getSeriesData(series_name)
                if i < len(data):
                    if isinstance(data[i], tuple):
                        _, value = data[i]
                        values.append(value)
                    else:
                        values.append(data[i])
            
            if values:
                stats[category] = {
                    'count': len(values),
                    'sum': sum(values),
                    'mean': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'range': max(values) - min(values)
                }
                
                # Calculate standard deviation if we have at least 2 values
                if len(values) > 1:
                    mean = stats[category]['mean']
                    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
                    stats[category]['std_dev'] = variance ** 0.5
        
        return stats
    
    def exportBarData(self, format: str = "csv") -> str:
        """Export bar data to string"""
        categories = self.getCategories()
        series_names = self.getSeriesNames()
        
        if format.lower() == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            header = ["Category"] + series_names
            writer.writerow(header)
            
            # Write data
            for i, category in enumerate(categories):
                row = [category]
                for series_name in series_names:
                    data = self.getSeriesData(series_name)
                    if i < len(data):
                        if isinstance(data[i], tuple):
                            _, value = data[i]
                            row.append(str(value))
                        else:
                            row.append(str(data[i]))
                    else:
                        row.append("")
                writer.writerow(row)
            
            return output.getvalue()
        
        elif format.lower() == "json":
            data_dict = {
                "categories": categories,
                "series": {}
            }
            
            for series_name in series_names:
                data_dict["series"][series_name] = []
                data = self.getSeriesData(series_name)
                for i in range(len(categories)):
                    if i < len(data):
                        if isinstance(data[i], tuple):
                            _, value = data[i]
                            data_dict["series"][series_name].append(value)
                        else:
                            data_dict["series"][series_name].append(data[i])
                    else:
                        data_dict["series"][series_name].append(None)
            
            return json.dumps(data_dict, indent=2)
        
        else:
            return f"Unsupported format: {format}"
    
    # ============ VALIDATION METHODS ============
    
    def validateBarData(self, data: List[float]) -> bool:
        """Validate bar data (no NaN, infinite values, etc.)"""
        import math
        for value in data:
            if math.isnan(value) or math.isinf(value):
                return False
        return True
    
    def sanitizeBarData(self, data: List[float]) -> List[float]:
        """Clean bar data (replace invalid values with 0)"""
        import math
        sanitized = []
        for value in data:
            if math.isnan(value) or math.isinf(value):
                sanitized.append(0.0)
            else:
                sanitized.append(value)
        return sanitized
    
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
        if title and description:
            self._tooltip_manager.show(x, y, title, description)
    
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
        self.updateChart()
    
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
    
    @Property(str)
    def animationEasingCurve(self):
        """Get animation easing curve as string name"""
        return self.getAnimationEasingCurveName()
    
    @animationEasingCurve.setter
    def animationEasingCurve(self, value: str):
        """Set animation easing curve by string name"""
        self.setAnimationEasingCurve(value)
    
    @Property(str)
    def availableAnimationEasingCurves(self):
        """Get list of available animation easing curve names (read-only)"""
        return list(self.EASING_CURVE_MAP.keys())
    
    @Property(bool)
    def antialiasing(self):
        """Get antialiasing state"""
        return self._antialiasing
    
    @antialiasing.setter
    def antialiasing(self, value: bool):
        """Set antialiasing state"""
        self._antialiasing = value
        self._chart_view.setRenderHint(QPainter.Antialiasing, value)
    
    @Property(float)
    def customCategorySpacing(self):
        """Get category spacing"""
        return self._custom_category_spacing
    
    @customCategorySpacing.setter
    def customCategorySpacing(self, value: float):
        """Set category spacing"""
        self.setCategorySpacing(value)
    
    @Property(float)
    def barWidth(self):
        """Get bar width"""
        return self._bar_width
    
    @barWidth.setter
    def barWidth(self, value: float):
        """Set bar width"""
        self.setBarWidth(value)
    
    @Property(float)
    def barSpacing(self):
        """Get bar spacing"""
        return self._bar_spacing
    
    @barSpacing.setter
    def barSpacing(self, value: float):
        """Set bar spacing"""
        self.setBarSpacing(value)
    
    @Property(str)
    def barPattern(self):
        """Get bar pattern"""
        return self._bar_pattern
    
    @barPattern.setter
    def barPattern(self, value: str):
        """Set bar pattern"""
        self.setBarPattern(value)
    
    @Property(str)
    def barSelectionMode(self):
        """Get bar selection mode"""
        return self._bar_selection_mode
    
    @barSelectionMode.setter
    def barSelectionMode(self, value: str):
        """Set bar selection mode"""
        self.setBarSelectionMode(value)
    
    @Property(bool)
    def showLegend(self):
        """Get legend visibility"""
        return self._show_legend
    
    @showLegend.setter
    def showLegend(self, value: bool):
        """Set legend visibility"""
        self._show_legend = value
        self._updateLegendSettings()
    
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
    def valueLabelsPosition(self):
        """Get value labels position"""
        return self.getValueLabelsPosition()
    
    @valueLabelsPosition.setter
    def valueLabelsPosition(self, value: str):
        """Set value labels position"""
        self.setValueLabelsPosition(value)
    
    @Property(str)
    def valueLabelsFormat(self):
        """Get value labels format"""
        return self._value_labels_format
    
    @valueLabelsFormat.setter
    def valueLabelsFormat(self, value: str):
        """Set value labels format"""
        self._value_labels_format = value
        self.updateChart()
    
    @Property(float)
    def customValueLabelsFontSize(self):
        """Get value labels font size"""
        return self._custom_value_labels_font_size
    
    @customValueLabelsFontSize.setter
    def customValueLabelsFontSize(self, value: float):
        """Set value labels font size"""
        self.setCustomValueLabelsFontSize(value)
    
    @Property(QColor)
    def customValueLabelsColor(self):
        """Get value labels color"""
        return self._custom_value_labels_color
    
    @customValueLabelsColor.setter
    def customValueLabelsColor(self, value: QColor):
        """Set value labels color"""
        self.setCustomValueLabelsColor(value)
    
    @Property(str)
    def labelsPosition(self):
        """Get labels position"""
        return self.getValueLabelsPosition()
    
    @labelsPosition.setter
    def labelsPosition(self, value: str):
        """Set labels position"""
        self.setValueLabelsPosition(value)
    
    @Property(QColor)
    def customGridColor(self):
        """Get grid color"""
        return self._custom_grid_color
    
    @customGridColor.setter
    def customGridColor(self, value: QColor):
        """Set grid color"""
        self._custom_grid_color = value
        self._axis_y.setGridLineColor(value)
    
    @Property(float)
    def customBarBorderWidth(self):
        """Get bar border width"""
        return self._custom_bar_border_width
    
    @customBarBorderWidth.setter
    def customBarBorderWidth(self, value: float):
        """Set bar border width"""
        self.setCustomBarBorderWidth(value)
    
    @Property(QColor)
    def customBarBorderColor(self):
        """Get bar border color"""
        return self._custom_bar_border_color
    
    @customBarBorderColor.setter
    def customBarBorderColor(self, value: QColor):
        """Set bar border color"""
        self.setCustomBarBorderColor(value)
    
    @Property(str)
    def customTooltipFormat(self):
        """Get tooltip format"""
        return self._custom_tooltip_format
    
    @customTooltipFormat.setter
    def customTooltipFormat(self, value: str):
        """Set tooltip format"""
        self.setCustomTooltipFormat(value)
    
    @Property(bool)
    def lazyLoading(self):
        """Get lazy loading state"""
        return self._lazy_loading
    
    @lazyLoading.setter
    def lazyLoading(self, value: bool):
        """Set lazy loading state"""
        self.setLazyLoading(value)
    
    @Property(bool)
    def virtualization(self):
        """Get virtualization state"""
        return self._virtualization
    
    @virtualization.setter
    def virtualization(self, value: bool):
        """Set virtualization state"""
        self.setVirtualization(value)
    
    @Property(int)
    def batchSize(self):
        """Get batch size"""
        return self._batch_size
    
    @batchSize.setter
    def batchSize(self, value: int):
        """Set batch size"""
        self.setBatchSize(value)
    
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
    def showCrosshair(self):
        """Get crosshair visibility"""
        return self.isCrosshairVisible()
    
    @showCrosshair.setter
    def showCrosshair(self, value: bool):
        """Set crosshair visibility"""
        self.setCrosshairVisible(value)
    
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
    
    @Property(bool)
    def compactMode(self):
        """Get compact mode state"""
        return self.isCompactMode()
    
    @compactMode.setter
    def compactMode(self, value: bool):
        """Set compact mode state"""
        self.setCompactMode(value)