# file name: QCustomPieChart.py
from typing import List, Tuple, Optional, Dict, Any
from qtpy.QtCore import Qt, QPointF, Signal, Property, QRect, QTimer
from qtpy.QtGui import QColor, QPen, QPainter, QPalette, QBrush, QLinearGradient, QRadialGradient
from qtpy.QtCharts import QChart, QPieSeries, QPieSlice, QChartView
from qtpy.QtWidgets import QGraphicsLayout

from .QCustomChartBase import QCustomChartBase # This already includes QCustomChartConstants
from Custom_Widgets.Utils import is_in_designer


class QCustomPieChart(QCustomChartBase):
    """
    Pie chart implementation using the modular architecture.
    Qt Designer compatible with property exposure.
    """    
    # Designer registration constants
    WIDGET_ICON = "components/icons/pie_chart.png"
    WIDGET_TOOLTIP = "Customizable pie chart with exploded slices and gradient filling"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomPieChart' name='customPieChart'>
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
    
    # Additional signals for pie chart
    sliceClicked = Signal(str, float)  # slice_name, value
    sliceHovered = Signal(str, float)  # slice_name, value
    sliceExploded = Signal(str, bool)  # slice_name, exploded
    seriesAdded = Signal(str)
    seriesRemoved = Signal(str)
    chartExportComplete = Signal(str, bool)  # filename, success
    legendPositionChanged = Signal(str)  # New signal for legend position changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Chart configuration
        self._chart.setTitle("Pie Chart")
        self._chart.legend().setVisible(True)
        
        # Pie chart doesn't use axes, so remove them
        for axis in self._chart.axes():
            self._chart.removeAxis(axis)
        
        # Additional properties for Designer
        self._chart_title = "Pie Chart"
        self._show_legend = True
        self._animation_enabled = True
        self._animation_duration = 1000
        self._antialiasing = True
        self._show_labels = True
        self._labels_position = self.LABELS_POSITION_OUTSIDE  # Use constant
        self._show_percentages = True
        self._show_values = True
        self._exploded_slices = []  # List of exploded slice names
        self._explosion_distance = 0.1  # Distance for exploded slices (0.0 to 1.0)
        self._hole_size = 0.0  # Size of hole in donut chart (0.0 to 0.9)
        self._start_angle = 0.0  # Starting angle in degrees
        self._end_angle = 360.0  # Ending angle in degrees (for partial pie)
        self._gradient_fill = True
        self._gradient_type = self.GRADIENT_RADIAL  # Use constant
        self._border_width = 2.0
        self._border_color = QColor(255, 255, 255, 100)
        self._explode_on_hover = True
        self._hover_explosion_distance = 0.15  # Slightly more than normal explosion
        
        # New property for legend marker border
        self._legend_marker_border_width = 1.0  # Constant 1px border for legend markers
        
        # New properties for semicircle/half pie
        self._semicircle_enabled = False  # Whether to show as semicircle
        self._pie_angular_span = 180.0  # Angular span in degrees (180 = half pie)
        self._semicircle_orientation = self.ORIENTATION_RIGHT  # Use constant
        
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
        
        # Initialize data storage for pie series
        self._pie_series_cache = {}  # Cache for pie series
        self._pie_slices_cache = {}  # Cache for pie slices
        self._pie_labels = {}  # Store original label data for pie charts
        self._slice_colors = {}  # Store colors for each slice
        self._slice_names = {}  # Store slice names separately from labels
        self._legend_labels = {}  # Store legend labels separately
        
        # Hover state tracking
        self._hovered_slice = None
        self._hover_exploded = False
        self._hover_brush_backup = {}  # Store original brushes for hovered slices
        self._hover_original_color = {}  # Store original colors for hovered slices
        
        # Signal connections tracking
        self._slice_connections = {}  # Track slice signal connections
        
        # Add dummy data if in designer mode
        self._addDummyDataForDesigner()

    
    def _addDummyDataForDesigner(self):
        """Add dummy data when running in Qt Designer"""
        if is_in_designer(self):
            # Clear any existing data first
            self.clearAllData()
            
            # Generate dummy data for pie chart
            self.addSeries(
                name="Pie Series 1",
                data=[
                    ("Category A", 25.0),
                    ("Category B", 35.0),
                    ("Category C", 20.0),
                    ("Category D", 15.0),
                    ("Category E", 5.0)
                ],
                visible=True
            )
            
            # Update the chart display
            self.updateChart()
            
            # Set nice chart title for designer
            self._chart.setTitle("Pie Chart Preview (Designer Mode)")
            
            print("Designer mode detected - showing dummy pie chart data")

    def generateExampleData(self, example_type: str = "categories"):
        """
        Generate example data for testing.
        
        Args:
            example_type: Type of example data to generate
                Options: "categories", "expenses", "sales", "survey"
        """
        import random
        
        # Clear existing data first
        self.clearAllData()
        
        if example_type == "categories":
            data = [
                ("Electronics", random.uniform(20, 40)),
                ("Clothing", random.uniform(15, 30)),
                ("Food", random.uniform(10, 25)),
                ("Entertainment", random.uniform(5, 20)),
                ("Travel", random.uniform(5, 15))
            ]
        elif example_type == "expenses":
            data = [
                ("Housing", random.uniform(30, 50)),
                ("Transportation", random.uniform(10, 20)),
                ("Food", random.uniform(15, 25)),
                ("Utilities", random.uniform(5, 15)),
                ("Entertainment", random.uniform(5, 10)),
                ("Savings", random.uniform(5, 15))
            ]
        elif example_type == "sales":
            data = [
                ("Q1", random.uniform(20, 35)),
                ("Q2", random.uniform(25, 40)),
                ("Q3", random.uniform(30, 45)),
                ("Q4", random.uniform(35, 50))
            ]
        elif example_type == "survey":
            data = [
                ("Strongly Agree", random.uniform(30, 45)),
                ("Agree", random.uniform(20, 35)),
                ("Neutral", random.uniform(10, 25)),
                ("Disagree", random.uniform(5, 15)),
                ("Strongly Disagree", random.uniform(5, 10))
            ]
        else:
            # Default to categories
            data = [
                ("Category A", random.uniform(20, 40)),
                ("Category B", random.uniform(15, 30)),
                ("Category C", random.uniform(10, 25)),
                ("Category D", random.uniform(5, 20)),
                ("Category E", random.uniform(5, 15))
            ]
        
        # Add the series
        self.addSeries(
            name=f"Example: {example_type.title()}",
            data=data,
            visible=True
        )
        
        # Update the chart
        self.updateChart()
        self._chart.setTitle(f"Example: {example_type.title()} Distribution")

    def _onChartClicked(self, x: float, y: float):
        """Handle chart click and emit sliceClicked"""
        slice_name = self._findSliceAtPoint(QPointF(x, y))
        if slice_name:
            slice_data = self._getSliceData(slice_name)
            if slice_data:
                self.sliceClicked.emit(slice_name, slice_data[1])

    def _onChartHovered(self, x: float, y: float):
        """Handle chart hover and emit sliceHovered"""
        slice_name = self._findSliceAtPoint(QPointF(x, y))
        if slice_name:
            slice_data = self._getSliceData(slice_name)
            if slice_data:
                self.sliceHovered.emit(slice_name, slice_data[1])

    def updateChart(self):
        """Update the chart display based on current data"""
        # Clean up hover state before removing series
        self._cleanupHoverState()
        
        # Clear existing series
        series_to_remove = []
        for series in self._chart.series():
            series_to_remove.append(series)
        
        for series in series_to_remove:
            try:
                # Disconnect all signals from series slices before removing
                if hasattr(series, 'slices'):
                    for slice in series.slices():
                        try:
                            slice.hovered.disconnect()
                        except:
                            pass
                        try:
                            slice.clicked.disconnect()
                        except:
                            pass
                self._chart.removeSeries(series)
            except:
                pass  # Series might already be deleted
        
        # Clear the caches and connections
        self._pie_series_cache.clear()
        self._pie_slices_cache.clear()
        self._hover_brush_backup.clear()  # Clear hover brush backups
        self._hover_original_color.clear()  # Clear hover color backups
        self._slice_connections.clear()  # Clear connection tracking
        
        # Create series from stored pie data
        for series_name in list(self._pie_labels.keys()):
            if not self._data_manager.getSeriesVisibility(series_name):
                continue
                
            data_points = self._pie_labels.get(series_name, [])
            if not data_points:
                continue
            
            # Create pie series
            pie_series = self._createPieSeries(series_name, data_points)
            if pie_series:
                try:
                    self._chart.addSeries(pie_series)
                    # Store in cache
                    self._pie_series_cache[series_name] = pie_series
                except Exception as e:
                    print(f"Error adding pie series {series_name} to chart: {e}")
        
        # Set chart title
        self._chart.setTitle(self._chart_title)
        
        # Set animation
        if self._animation_enabled:
            self._chart.setAnimationOptions(QChart.SeriesAnimations)
            self._chart.setAnimationDuration(self._animation_duration)
        else:
            self._chart.setAnimationOptions(QChart.NoAnimation)
        
        # Set antialiasing
        self._chart_view.setRenderHint(QPainter.Antialiasing, self._antialiasing)
        
        # Update legend - Configure for labels only
        self._updateLegendSettings()
        
        # Force a chart update to ensure all visual changes are applied
        self._chart.update()

    def _createPieSeries(self, name: str, data: List[Tuple[str, float]]) -> Optional[QPieSeries]:
        """Create a styled pie series"""
        try:
            # Create pie series
            pie_series = QPieSeries()
            pie_series.setName(name)
            
            # Set donut hole size if needed
            if self._hole_size > 0:
                pie_series.setHoleSize(self._hole_size)
            
            # Set start and end angles based on semicircle settings
            start_angle = self._start_angle
            end_angle = self._end_angle
            
            if self._semicircle_enabled:
                # Calculate start and end angles based on orientation
                if self._semicircle_orientation == self.ORIENTATION_RIGHT:
                    start_angle = 0
                    end_angle = self._pie_angular_span
                elif self._semicircle_orientation == self.ORIENTATION_LEFT:
                    start_angle = 180
                    end_angle = 180 + self._pie_angular_span
                elif self._semicircle_orientation == self.ORIENTATION_BOTTOM:
                    start_angle = 90
                    end_angle = 90 + self._pie_angular_span
                elif self._semicircle_orientation == self.ORIENTATION_TOP:
                    start_angle = -90
                    end_angle = -90 + self._pie_angular_span
                
                pie_series.setPieStartAngle(start_angle)
                pie_series.setPieEndAngle(end_angle)
            else:
                # Use the user-defined start and end angles
                if self._start_angle != 0 or self._end_angle != 360:
                    pie_series.setPieStartAngle(self._start_angle)
                    pie_series.setPieEndAngle(self._end_angle)
            
            # Add slices
            total_value = sum(value for _, value in data)
            
            for idx, (slice_name, value) in enumerate(data):
                if value <= 0:
                    continue  # Skip zero or negative values
                    
                percentage = (value / total_value * 100) if total_value > 0 else 0
                
                # Create slice with just the value (not the name)
                slice_obj = QPieSlice("", value)  # Empty label for slice
                
                # Store the slice name separately
                self._slice_names[f"{name}_{slice_name}"] = slice_name
                
                # FIX: Determine if any visual labels should be shown
                should_show_visual_labels = False
                label_parts = []
                
                if self._show_labels:
                    # Only show visual labels if labels are enabled
                    if self._show_percentages:
                        label_parts.append(f"{percentage:.1f}%")
                        should_show_visual_labels = True
                    if self._show_values:
                        label_parts.append(f"{value:.1f}")
                        should_show_visual_labels = True
                
                # FIX: Set label visibility based on whether we have any visual content
                if should_show_visual_labels:
                    # Show data label (percentage/value) if any parts are available
                    slice_obj.setLabelVisible(True)
                    slice_obj.setLabel(" | ".join(label_parts))
                else:
                    # If no visual labels, hide the label completely
                    slice_obj.setLabelVisible(False)
                
                # Set label position only if labels are visible
                if should_show_visual_labels:
                    if self._labels_position == self.LABELS_POSITION_INSIDE:
                        slice_obj.setLabelPosition(QPieSlice.LabelInsideHorizontal)
                    elif self._labels_position == self.LABELS_POSITION_INSIDE_TANGENTIAL:
                        slice_obj.setLabelPosition(QPieSlice.LabelInsideTangential)
                        slice_obj.setLabelArmLengthFactor(0.1)
                    elif self._labels_position == self.LABELS_POSITION_CALLOUT:
                        slice_obj.setLabelPosition(QPieSlice.LabelOutside)
                        slice_obj.setLabelArmLengthFactor(0.1)
                    else:  # outside (default)
                        slice_obj.setLabelPosition(QPieSlice.LabelOutside)
                
                # Get color for this slice
                color_key = f"{name}_{slice_name}"
                if color_key in self._slice_colors:
                    color = self._slice_colors[color_key]
                else:
                    # Generate color based on slice index using constants
                    color = self._getSliceColor(idx)
                    # Store it for future reference
                    self._slice_colors[color_key] = color
                
                # Apply gradient or solid fill
                if self._gradient_fill:
                    gradient = self._createGradient(color)
                    slice_obj.setBrush(gradient)
                else:
                    slice_obj.setBrush(QBrush(color))
                
                # Set border - FIXED: Use properties properly
                pen = QPen(self._border_color)
                pen.setWidthF(self._border_width)
                slice_obj.setPen(pen)
                
                # Check if slice should be exploded
                if slice_name in self._exploded_slices:
                    slice_obj.setExploded(True)
                    slice_obj.setExplodeDistanceFactor(self._explosion_distance)
                else:
                    # FIX: Explicitly set un-exploded state
                    slice_obj.setExploded(False)
                
                # Connect slice signals
                def create_hover_handler(s_name, s_value):
                    return lambda state: self._onSliceHovered(state, s_name, s_value)
                
                def create_click_handler(s_name, s_value):
                    return lambda: self._onSliceClicked(s_name, s_value)
                
                # Create and store connections
                hover_connection = slice_obj.hovered.connect(create_hover_handler(slice_name, value))
                click_connection = slice_obj.clicked.connect(create_click_handler(slice_name, value))
                
                # Store connections
                self._slice_connections[slice_name] = {
                    'hover': hover_connection,
                    'click': click_connection
                }
                
                # Add slice to series
                pie_series.append(slice_obj)
                
                # Store slice in cache
                if name not in self._pie_slices_cache:
                    self._pie_slices_cache[name] = {}
                self._pie_slices_cache[name][slice_name] = slice_obj
            
            return pie_series
            
        except Exception as e:
            print(f"Error creating pie series for {name}: {e}")
            return None

    def _createGradient(self, base_color: QColor) -> QBrush:
        """Create a gradient brush for pie slice fill"""
        if self._gradient_type == self.GRADIENT_CONICAL:
            # Use a linear gradient as a substitute for conical
            gradient = QLinearGradient(0, 0, 1, 1)
            gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
            
            # Create a multi-color gradient for conical effect
            color1 = base_color.lighter(150)
            color2 = base_color.lighter(120)
            color3 = base_color
            color4 = base_color.darker(120)
            color5 = base_color.darker(150)
            
            gradient.setColorAt(0.0, color1)
            gradient.setColorAt(0.25, color2)
            gradient.setColorAt(0.5, color3)
            gradient.setColorAt(0.75, color4)
            gradient.setColorAt(1.0, color5)
        else:  # radial (default)
            gradient = QRadialGradient(0.5, 0.5, 0.5)
            gradient.setCoordinateMode(QRadialGradient.ObjectBoundingMode)
            
            # Create gradient colors with more contrast
            light_color = QColor(base_color)
            dark_color = QColor(base_color)
            
            # Adjust colors for gradient effect - increase the contrast
            light_color = light_color.lighter(160)
            dark_color = dark_color.darker(160)
            
            # Add an intermediate color for smoother gradient
            mid_color = base_color.lighter(130)
            
            gradient.setColorAt(0.0, light_color)
            gradient.setColorAt(0.5, mid_color)
            gradient.setColorAt(1.0, dark_color)
        
        return QBrush(gradient)

    def _getSliceColor(self, index: int) -> QColor:
        """Get a color for a slice based on index"""
        # Use the constants from QCustomChartConstants
        colors = self.DEFAULT_PIE_SLICE_COLORS
        return colors[index % len(colors)]

    def _findSliceAtPoint(self, point: QPointF) -> Optional[str]:
        """
        Find the pie slice at the given chart coordinates.
        Returns slice name if found, None otherwise.
        """
        # For pie charts, we need to check all slices in all series
        for series_name, slices_dict in self._pie_slices_cache.items():
            for slice_name, slice_obj in slices_dict.items():
                try:
                    if slice_obj.isValid() and slice_obj.contains(point):
                        return slice_name
                except:
                    continue
        return None

    def _getSliceData(self, slice_name: str) -> Optional[Tuple[str, float]]:
        """
        Get data for a specific slice.
        Returns (slice_name, value) if found, None otherwise.
        """
        # Search through all pie data
        for series_name, data_points in self._pie_labels.items():
            for data_point in data_points:
                if data_point[0] == slice_name:
                    return data_point
        return None

    def _onSliceHovered(self, state: bool, slice_name: str, value: float):
        """Handle slice hover events"""
        if not self._explode_on_hover:
            # If explode on hover is disabled, just emit the signal and return
            if state:
                self.sliceHovered.emit(slice_name, value)
            return
        
        print(f"Handling hover for slice: {slice_name}, state: {state}")
        if state:
            self.sliceHovered.emit(slice_name, value)
            
            # Store hovered slice
            self._hovered_slice = slice_name
            
            # Get the slice object
            slice_obj = self._getSliceObject(slice_name)
            if not slice_obj:
                return
            
            # Store original brush for restoration
            slice_key = slice_name
            if slice_key not in self._hover_brush_backup:
                self._hover_brush_backup[slice_key] = slice_obj.brush()
            
            # FIX: Store the original base color (not from brush which might be invalid for gradients)
            color_key = self._findColorKeyForSlice(slice_name)
            if color_key and color_key not in self._hover_original_color:
                if color_key in self._slice_colors:
                    self._hover_original_color[color_key] = self._slice_colors[color_key]
                else:
                    # Fallback to slice's color property if available
                    self._hover_original_color[color_key] = slice_obj.color()
            
            # Highlight the slice - FIX: Get base color properly
            original_color = None
            if color_key in self._slice_colors:
                original_color = self._slice_colors[color_key]
            elif color_key in self._hover_original_color:
                original_color = self._hover_original_color[color_key]
            else:
                original_color = slice_obj.color()  # Fallback
            
            if original_color.isValid():
                highlight_color = original_color.lighter(130)
                
                # Apply highlighting
                if self._gradient_fill:
                    highlight_gradient = self._createGradient(highlight_color)
                    slice_obj.setBrush(highlight_gradient)
                else:
                    slice_obj.setBrush(QBrush(highlight_color))
                
                # Also update the slice's color property for consistency
                slice_obj.setColor(highlight_color)
            
            # Explode on hover if enabled and slice is not already exploded
            if slice_name not in self._exploded_slices:
                print(f"Exploding slice on hover: {slice_name}")
                slice_obj.setExploded(True)
                slice_obj.setExplodeDistanceFactor(self._hover_explosion_distance)
                self._hover_exploded = True
                
                # Force chart update to show explosion
                self._chart.update()
        else:
            # Clear hovered slice
            if self._hovered_slice == slice_name:
                self._hovered_slice = None
            
            # Restore original appearance
            slice_obj = self._getSliceObject(slice_name)
            slice_key = slice_name
            
            if slice_obj and slice_key in self._hover_brush_backup:
                # Restore original brush
                slice_obj.setBrush(self._hover_brush_backup[slice_key])
                
                # Restore original color
                color_key = self._findColorKeyForSlice(slice_name)
                if color_key and color_key in self._hover_original_color:
                    original_color = self._hover_original_color[color_key]
                    slice_obj.setColor(original_color)
                
                # Unexplode on hover exit if we exploded it
                if self._hover_exploded and slice_name not in self._exploded_slices:
                    slice_obj.setExploded(False)
                    self._hover_exploded = False
                    
                    # Force chart update
                    self._chart.update()
                
                # Remove from backup
                if slice_key in self._hover_brush_backup:
                    del self._hover_brush_backup[slice_key]
                if color_key and color_key in self._hover_original_color:
                    del self._hover_original_color[color_key]

    def _onSliceClicked(self, slice_name: str, value: float):
        """Handle slice click events"""
        self.sliceClicked.emit(slice_name, value)
        
        # Toggle explosion
        self.toggleSliceExplosion(slice_name)

    def _getSliceObject(self, slice_name: str) -> Optional[QPieSlice]:
        """Get the QPieSlice object for a given slice name"""
        for slices_dict in self._pie_slices_cache.values():
            if slice_name in slices_dict:
                return slices_dict[slice_name]
        return None

    def _findColorKeyForSlice(self, slice_name: str) -> Optional[str]:
        """Find the color key for a slice"""
        for series_name in self._pie_labels.keys():
            for name, _ in self._pie_labels[series_name]:
                if name == slice_name:
                    return f"{series_name}_{slice_name}"
        return None

    def _getSliceIndex(self, slice_name: str) -> int:
        """Get the index of a slice within its series"""
        for series_name, data_points in self._pie_labels.items():
            for idx, (name, _) in enumerate(data_points):
                if name == slice_name:
                    return idx
        return -1

    def _updateLegendSettings(self):
        """Update legend settings - ensure legend shows only slice names"""
        legend = self._chart.legend()
        if legend:
            legend.setVisible(self._show_legend)
            font = legend.font()
            font.setPointSize(self._legend_font_size)
            legend.setFont(font)
            legend.setBackgroundVisible(self._legend_background_visible)
            
            # Set legend position
            if self._legend_manager:
                self._legend_manager.setPosition(self.getLegendPosition())
            
            # FIX: Update legend markers to show only slice names
            self._updateLegendMarkers()
            
            legend.update()
    
    def _updateLegendMarkers(self):
        """Update legend markers to show only slice names with fixed border width"""
        legend = self._chart.legend()
        if not legend:
            return
        
        # Get all legend markers
        markers = legend.markers()
        for marker in markers:
            try:
                # Get the slice associated with this marker
                slice_obj = marker.slice()
                if slice_obj:
                    # Find the slice name for this slice object
                    slice_name = self._getSliceNameForSliceObject(slice_obj)
                    if slice_name:
                        # Set the legend label to just the slice name
                        marker.setLabel(slice_name)
                    
                    # FIX: Set constant border width for legend markers (1px)
                    # Get the current pen
                    current_pen = marker.pen()
                    if current_pen:
                        # Create a new pen with constant border width
                        fixed_pen = QPen(current_pen)
                        fixed_pen.setWidthF(self._legend_marker_border_width)  # Always 1px
                        marker.setPen(fixed_pen)
            except Exception as e:
                print(f"Error updating legend marker: {e}")
                continue
    
    def _getSliceNameForSliceObject(self, slice_obj: QPieSlice) -> Optional[str]:
        """Get the slice name for a given slice object"""
        # Search through all pie slices to find which slice name this object belongs to
        for series_name, slices_dict in self._pie_slices_cache.items():
            for slice_name, obj in slices_dict.items():
                if obj == slice_obj:
                    return slice_name
        return None

    def _cleanupHoverState(self):
        """Clean up hover state before updating chart"""
        if self._hovered_slice:
            slice_obj = self._getSliceObject(self._hovered_slice)
            if slice_obj:
                # Reset explosion if hover exploded
                if self._hover_exploded:
                    slice_obj.setExploded(False)
                    self._hover_exploded = False
        
        self._hovered_slice = None
        self._hover_brush_backup.clear()
        self._hover_original_color.clear()

    # ============ PUBLIC API ============
    
    def addSeries(self, name: str, data: List[Tuple[str, float]], 
                 color: Optional[QColor] = None,
                 visible: bool = True,
                 **kwargs) -> bool:
        """
        Add a pie series to the chart.
        
        Args:
            name: Series name
            data: List of (slice_name, value) tuples
            color: Optional series color (for single series pie charts)
            visible: Whether the series is visible
        """
        # For pie charts, we store the data in a custom dictionary
        # since the data manager expects numeric data
        
        # Store the pie data
        self._pie_labels[name] = data.copy()
        
        # Store slice names
        for slice_name, _ in data:
            self._slice_names[f"{name}_{slice_name}"] = slice_name
        
        # Store colors for each slice
        for idx, (slice_name, _) in enumerate(data):
            color_key = f"{name}_{slice_name}"
            if color_key not in self._slice_colors:
                # Assign a unique color to each slice
                self._slice_colors[color_key] = self._getSliceColor(idx)
        
        # Also add to data manager with dummy numeric data
        # This ensures the data manager tracks the series
        dummy_data = [(i, value) for i, (label, value) in enumerate(data)]
        success = self._data_manager.addSeries(
            name=name,
            data=dummy_data,
            color=color,
            visible=visible,
            line_style=self.LINE_SOLID,
            line_width=0,  # Not applicable for pie
            marker_style=self.MARKER_NONE,
            marker_size=0  # Not applicable for pie
        )
        
        if success:
            self.updateChart()
        
        return success
    
    def removeSeries(self, name: str) -> bool:
        """Remove a series from the chart"""
        success = self._data_manager.removeSeries(name)
        if success:
            # Remove from pie labels cache
            if name in self._pie_labels:
                # Remove slice names and colors
                for slice_name in self.getSliceNames(name):
                    key = f"{name}_{slice_name}"
                    self._slice_names.pop(key, None)
                    self._slice_colors.pop(key, None)
                
                del self._pie_labels[name]
            
            # Remove from exploded slices
            if name in self._pie_slices_cache:
                slice_names = list(self._pie_slices_cache[name].keys())
                self._exploded_slices = [s for s in self._exploded_slices 
                                        if s not in slice_names]
            
            # Remove from caches
            self._pie_series_cache.pop(name, None)
            self._pie_slices_cache.pop(name, None)
            
            self.updateChart()
        return success
    
    def updateSeriesData(self, name: str, data: List[Tuple[str, float]]) -> bool:
        """Update data for an existing series"""
        if name not in self._pie_labels:
            return False
        
        # Update the pie data
        old_slices = set(self.getSliceNames(name))
        new_slices = {slice_name for slice_name, _ in data}
        
        # Update slice names and colors for new slices
        for idx, (slice_name, _) in enumerate(data):
            key = f"{name}_{slice_name}"
            self._slice_names[key] = slice_name
            if key not in self._slice_colors:
                self._slice_colors[key] = self._getSliceColor(idx)
        
        # Remove names and colors for deleted slices
        for slice_name in old_slices - new_slices:
            key = f"{name}_{slice_name}"
            self._slice_names.pop(key, None)
            self._slice_colors.pop(key, None)
        
        self._pie_labels[name] = data.copy()
        
        # Update dummy data in data manager
        dummy_data = [(i, value) for i, (label, value) in enumerate(data)]
        success = self._data_manager.updateSeriesData(name, dummy_data)
        
        if success:
            self.updateChart()
        
        return success
    
    def addSlice(self, series_name: str, slice_name: str, value: float) -> bool:
        """Add a slice to an existing series"""
        if series_name not in self._pie_labels:
            return False
        
        # Get current data
        current_data = self._pie_labels.get(series_name, [])
        current_data.append((slice_name, value))
        
        # Store slice name and assign a color
        key = f"{series_name}_{slice_name}"
        self._slice_names[key] = slice_name
        if key not in self._slice_colors:
            color_idx = len(current_data) - 1
            self._slice_colors[key] = self._getSliceColor(color_idx)
        
        return self.updateSeriesData(series_name, current_data)
    
    def removeSlice(self, series_name: str, slice_name: str) -> bool:
        """Remove a slice from a series"""
        if series_name not in self._pie_labels:
            return False
        
        # Remove slice from data
        new_data = [(name, value) for name, value in self._pie_labels[series_name] 
                   if name != slice_name]
        
        # Remove from exploded slices
        if slice_name in self._exploded_slices:
            self._exploded_slices.remove(slice_name)
        
        # Remove name and color
        key = f"{series_name}_{slice_name}"
        self._slice_names.pop(key, None)
        self._slice_colors.pop(key, None)
        
        return self.updateSeriesData(series_name, new_data)
    
    def updateSliceValue(self, series_name: str, slice_name: str, new_value: float) -> bool:
        """Update the value of a slice"""
        if series_name not in self._pie_labels:
            return False
        
        # Update slice value
        updated = False
        new_data = []
        for name, value in self._pie_labels[series_name]:
            if name == slice_name:
                new_data.append((name, new_value))
                updated = True
            else:
                new_data.append((name, value))
        
        if updated:
            return self.updateSeriesData(series_name, new_data)
        return False
    
    def getSliceNames(self, series_name: str) -> List[str]:
        """Get list of slice names for a series"""
        if series_name in self._pie_labels:
            return [name for name, _ in self._pie_labels[series_name]]
        return []
    
    def getSliceValue(self, series_name: str, slice_name: str) -> Optional[float]:
        """Get the value of a specific slice"""
        if series_name in self._pie_labels:
            for name, value in self._pie_labels[series_name]:
                if name == slice_name:
                    return value
        return None
    
    def getTotalValue(self, series_name: str) -> float:
        """Get the total value of all slices in a series"""
        if series_name in self._pie_labels:
            return sum(value for _, value in self._pie_labels[series_name])
        return 0.0
    
    def getPercentage(self, series_name: str, slice_name: str) -> float:
        """Get the percentage of a slice"""
        total = self.getTotalValue(series_name)
        value = self.getSliceValue(series_name, slice_name)
        
        if total > 0 and value is not None:
            return (value / total) * 100
        return 0.0
    
    def explodeSlice(self, slice_name: str, explode: bool = True):
        """Explode or un-explode a slice"""
        if explode and slice_name not in self._exploded_slices:
            self._exploded_slices.append(slice_name)
            self.sliceExploded.emit(slice_name, True)
        elif not explode and slice_name in self._exploded_slices:
            self._exploded_slices.remove(slice_name)
            self.sliceExploded.emit(slice_name, False)
        
        self.updateChart()
    
    def toggleSliceExplosion(self, slice_name: str):
        """Toggle explosion state of a slice"""
        # Check if slice exists in any series
        for series_name in self._pie_labels.keys():
            if slice_name in self.getSliceNames(series_name):
                self.explodeSlice(slice_name, slice_name not in self._exploded_slices)
                return
        # If slice not found, emit error signal or print debug info
        print(f"Slice '{slice_name}' not found in any series")
    
    def explodeAllSlices(self, explode: bool = True):
        """Explode or un-explode all slices"""
        if explode:
            # Get all slice names
            all_slices = []
            for series_name in self.getSeriesNames():
                all_slices.extend(self.getSliceNames(series_name))
            self._exploded_slices = all_slices
        else:
            self._exploded_slices.clear()
        
        self.updateChart()
    
    def isSliceExploded(self, slice_name: str) -> bool:
        """Check if a slice is exploded"""
        return slice_name in self._exploded_slices
    
    def setExplosionDistance(self, distance: float):
        """Set the explosion distance factor (0.0 to 1.0)"""
        self._explosion_distance = max(0.0, min(1.0, distance))
        self.updateChart()
    
    def getExplosionDistance(self) -> float:
        """Get the explosion distance factor"""
        return self._explosion_distance
    
    def setHoleSize(self, size: float):
        """Set the hole size for donut chart (0.0 to 0.9)"""
        self._hole_size = max(0.0, min(0.9, size))
        self.updateChart()
    
    def getHoleSize(self) -> float:
        """Get the hole size for donut chart"""
        return self._hole_size
    
    def setStartAngle(self, angle: float):
        """Set the starting angle in degrees"""
        self._start_angle = angle % 360
        self.updateChart()
    
    def getStartAngle(self) -> float:
        """Get the starting angle in degrees"""
        return self._start_angle
    
    def setEndAngle(self, angle: float):
        """Set the ending angle in degrees"""
        self._end_angle = angle % 360
        self.updateChart()
    
    def getEndAngle(self) -> float:
        """Get the ending angle in degrees"""
        return self._end_angle
    
    # New methods for semicircle/half pie functionality
    def setSemicircleEnabled(self, enabled: bool):
        """Enable or disable semicircle/half pie display"""
        self._semicircle_enabled = enabled
        self.updateChart()
    
    def isSemicircleEnabled(self) -> bool:
        """Check if semicircle mode is enabled"""
        return self._semicircle_enabled
    
    def setPieAngularSpan(self, span: float):
        """Set the angular span of the pie in degrees"""
        # Limit to reasonable values
        self._pie_angular_span = max(0.1, min(360.0, span))
        self.updateChart()
    
    def getPieAngularSpan(self) -> float:
        """Get the angular span of the pie in degrees"""
        return self._pie_angular_span
    
    def setSemicircleOrientation(self, orientation: str):
        """Set the orientation of the semicircle"""
        if orientation in [self.ORIENTATION_RIGHT, self.ORIENTATION_TOP, 
                          self.ORIENTATION_LEFT, self.ORIENTATION_BOTTOM]:
            self._semicircle_orientation = orientation
            self.updateChart()
    
    def getSemicircleOrientation(self) -> str:
        """Get the orientation of the semicircle"""
        return self._semicircle_orientation
    
    def setLabelsVisible(self, visible: bool):
        """Set labels visibility"""
        self._show_labels = visible
        self.updateChart()
    
    def areLabelsVisible(self) -> bool:
        """Check if labels are visible"""
        return self._show_labels
    
    def setLabelsPosition(self, position: str):
        """Set labels position: 'outside', 'inside', or 'callout'"""
        if position in [self.LABELS_POSITION_OUTSIDE, self.LABELS_POSITION_INSIDE, 
                       self.LABELS_POSITION_CALLOUT, self.LABELS_POSITION_INSIDE_TANGENTIAL]:
            self._labels_position = position
            self.updateChart()
    
    def getLabelsPosition(self) -> str:
        """Get labels position"""
        return self._labels_position
    
    def setShowPercentages(self, show: bool):
        """Set whether to show percentages in labels"""
        self._show_percentages = show
        self.updateChart()
    
    def showPercentages(self) -> bool:
        """Check if percentages are shown"""
        return self._show_percentages
    
    def setShowValues(self, show: bool):
        """Set whether to show values in labels"""
        self._show_values = show
        self.updateChart()
    
    def showValues(self) -> bool:
        """Check if values are shown"""
        return self._show_values
    
    def setGradientFill(self, enabled: bool):
        """Enable or disable gradient fill"""
        self._gradient_fill = enabled
        self.updateChart()
    
    def isGradientFillEnabled(self) -> bool:
        """Check if gradient fill is enabled"""
        return self._gradient_fill
    
    def setGradientType(self, gradient_type: str):
        """Set gradient type: 'radial' or 'conical'"""
        if gradient_type in [self.GRADIENT_RADIAL, self.GRADIENT_CONICAL]:
            self._gradient_type = gradient_type
            self.updateChart()
    
    def getGradientType(self) -> str:
        """Get gradient type"""
        return self._gradient_type
    
    def setBorderWidth(self, width: float):
        """Set border width"""
        self._border_width = max(0.0, width)
        self.updateChart()
    
    def getBorderWidth(self) -> float:
        """Get border width"""
        return self._border_width
    
    def setBorderColor(self, color: QColor):
        """Set border color"""
        self._border_color = color
        self.updateChart()
    
    def getBorderColor(self) -> QColor:
        """Get border color"""
        return self._border_color
    
    # New method for legend marker border width
    def setLegendMarkerBorderWidth(self, width: float):
        """Set the border width for legend markers"""
        self._legend_marker_border_width = max(0.0, width)
        self.updateChart()
    
    def getLegendMarkerBorderWidth(self) -> float:
        """Get the border width for legend markers"""
        return self._legend_marker_border_width
    
    # New methods for explode on hover
    def setExplodeOnHover(self, enabled: bool):
        """Enable or disable explode on hover"""
        self._explode_on_hover = enabled
        print(f"Set explode on hover to: {enabled}")
        # If turning off while a slice is hovered, clean up hover explosion
        if not enabled and self._hover_exploded:
            self._cleanupHoverExplosion()
    
    def isExplodeOnHoverEnabled(self) -> bool:
        """Check if explode on hover is enabled"""
        return self._explode_on_hover
    
    def _cleanupHoverExplosion(self):
        """Clean up any hover explosion state"""
        if self._hovered_slice:
            slice_obj = self._getSliceObject(self._hovered_slice)
            if slice_obj and self._hover_exploded and self._hovered_slice not in self._exploded_slices:
                slice_obj.setExploded(False)
                self._hover_exploded = False
                self._chart.update()
    
    def setHoverExplosionDistance(self, distance: float):
        """Set the explosion distance factor for hover (0.0 to 1.0)"""
        self._hover_explosion_distance = max(0.0, min(1.0, distance))
        # Update any currently hovered slice
        if self._hovered_slice and self._hover_exploded:
            slice_obj = self._getSliceObject(self._hovered_slice)
            if slice_obj:
                slice_obj.setExplodeDistanceFactor(distance)
                self._chart.update()
    
    def getHoverExplosionDistance(self) -> float:
        """Get the explosion distance factor for hover"""
        return self._hover_explosion_distance
    
    # Compatibility methods
    def clearData(self):
        """Clear all chart data (compatibility method)"""
        self.clearAllData()
    
    def clearAllData(self):
        """Clear all chart data"""
        # Call parent method first
        super().clearAllData()
        
        # Clear pie-specific data
        self._pie_labels.clear()
        self._pie_series_cache.clear()
        self._pie_slices_cache.clear()
        self._slice_colors.clear()
        self._slice_names.clear()
        self._exploded_slices.clear()
        self._hover_brush_backup.clear()
        self._hover_original_color.clear()
        self._slice_connections.clear()
        
        # Reset hover state
        self._hovered_slice = None
        self._hover_exploded = False
        
        # Update the chart to show empty state
        self.updateChart()
        self._chart.setTitle("Pie Chart")
    
    def getSeriesNames(self) -> List[str]:
        """Get list of all series names (overrides base method)"""
        return self._data_manager.getSeriesNames()
    
    def setSeriesColor(self, name: str, color: QColor):
        """Set color for a specific series (overrides base method)"""
        success = self._data_manager.setSeriesColor(name, color)
        if success:
            # Update all slices in this series to use the new color
            if name in self._pie_labels:
                for idx, (slice_name, _) in enumerate(self._pie_labels[name]):
                    color_key = f"{name}_{slice_name}"
                    self._slice_colors[color_key] = self._getSliceColor(idx)
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
    
    # Pie chart specific methods
    def _getSliceNamesForSeries(self, series_name: str) -> List[str]:
        """Get all slice names for a series"""
        if series_name in self._pie_labels:
            return [name for name, _ in self._pie_labels[series_name]]
        return []
    
    def getSeriesData(self, name: str) -> List[Tuple[str, float]]:
        """Get data for a specific series (pie chart version)"""
        return self._pie_labels.get(name, [])
    
    # ============ TOOLTIP METHODS ============
    
    def showTooltipAt(self, x: float, y: float, slice_name: str, title: str = None, description: str = None):
        """Manually show tooltip at specific coordinates"""
        slice_data = self._getSliceData(slice_name)
        if slice_data:
            if not title:
                title = f"Slice: {slice_name}"
            if not description:
                value = slice_data[1]
                series_name = self._findSeriesForSlice(slice_name)
                if series_name:
                    percentage = self.getPercentage(series_name, slice_name)
                    description = f"Value: {value:.2f}\nPercentage: {percentage:.1f}%"
                else:
                    description = f"Value: {value:.2f}"
            
            self._tooltip_manager.show(x, y, slice_name, title, description)
    
    def _findSeriesForSlice(self, slice_name: str) -> Optional[str]:
        """Find which series contains a given slice"""
        for series_name, slices in self._pie_labels.items():
            for name, _ in slices:
                if name == slice_name:
                    return series_name
        return None
    
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
    def showLabels(self):
        """Get labels visibility"""
        return self._show_labels
    
    @showLabels.setter
    def showLabels(self, value: bool):
        """Set labels visibility"""
        self._show_labels = value
        self.updateChart()
    
    @Property(str)
    def labelsPosition(self):
        """Get labels position"""
        return self._labels_position
    
    @labelsPosition.setter
    def labelsPosition(self, value: str):
        """Set labels position"""
        if value in [self.LABELS_POSITION_OUTSIDE, self.LABELS_POSITION_INSIDE, 
                    self.LABELS_POSITION_INSIDE_TANGENTIAL, self.LABELS_POSITION_CALLOUT]:
            self._labels_position = value
            self.updateChart()
    
    @Property(bool)
    def showPercentages(self):
        """Get show percentages state"""
        return self._show_percentages
    
    @showPercentages.setter
    def showPercentages(self, value: bool):
        """Set show percentages state"""
        self._show_percentages = value
        self.updateChart()
    
    @Property(bool)
    def showValues(self):
        """Get show values state"""
        return self._show_values
    
    @showValues.setter
    def showValues(self, value: bool):
        """Set show values state"""
        self._show_values = value
        self.updateChart()
    
    @Property(float)
    def explosionDistance(self):
        """Get explosion distance"""
        return self._explosion_distance
    
    @explosionDistance.setter
    def explosionDistance(self, value: float):
        """Set explosion distance"""
        self._explosion_distance = max(0.0, min(1.0, value))
        self.updateChart()
    
    @Property(float)
    def holeSize(self):
        """Get hole size"""
        return self._hole_size
    
    @holeSize.setter
    def holeSize(self, value: float):
        """Set hole size"""
        self._hole_size = max(0.0, min(0.9, value))
        self.updateChart()
    
    @Property(float)
    def startAngle(self):
        """Get start angle"""
        return self._start_angle
    
    @startAngle.setter
    def startAngle(self, value: float):
        """Set start angle"""
        self._start_angle = value % 360
        self.updateChart()
    
    @Property(float)
    def endAngle(self):
        """Get end angle"""
        return self._end_angle
    
    @endAngle.setter
    def endAngle(self, value: float):
        """Set end angle"""
        self._end_angle = value % 360
        self.updateChart()
    
    # New properties for semicircle/half pie
    @Property(bool)
    def semicircleEnabled(self):
        """Get semicircle enabled state"""
        return self._semicircle_enabled
    
    @semicircleEnabled.setter
    def semicircleEnabled(self, value: bool):
        """Set semicircle enabled state"""
        self._semicircle_enabled = value
        self.updateChart()
    
    @Property(float)
    def pieAngularSpan(self):
        """Get pie angular span"""
        return self._pie_angular_span
    
    @pieAngularSpan.setter
    def pieAngularSpan(self, value: float):
        """Set pie angular span"""
        self._pie_angular_span = max(0.1, min(360.0, value))
        self.updateChart()
    
    @Property(str)
    def semicircleOrientation(self):
        """Get semicircle orientation"""
        return self._semicircle_orientation
    
    @semicircleOrientation.setter
    def semicircleOrientation(self, value: str):
        """Set semicircle orientation"""
        if value in [self.ORIENTATION_RIGHT, self.ORIENTATION_TOP, 
                    self.ORIENTATION_LEFT, self.ORIENTATION_BOTTOM]:
            self._semicircle_orientation = value
            self.updateChart()
    
    @Property(bool)
    def gradientFill(self):
        """Get gradient fill state"""
        return self._gradient_fill
    
    @gradientFill.setter
    def gradientFill(self, value: bool):
        """Set gradient fill state"""
        self._gradient_fill = value
        self.updateChart()
    
    @Property(str)
    def gradientType(self):
        """Get gradient type"""
        return self._gradient_type
    
    @gradientType.setter
    def gradientType(self, value: str):
        """Set gradient type"""
        if value in [self.GRADIENT_RADIAL, self.GRADIENT_CONICAL]:
            self._gradient_type = value
            self.updateChart()
    
    @Property(float)
    def borderWidth(self):
        """Get border width"""
        return self._border_width
    
    @borderWidth.setter
    def borderWidth(self, value: float):
        """Set border width"""
        self._border_width = max(0.0, value)
        self.updateChart()
    
    @Property(QColor)
    def borderColor(self):
        """Get border color"""
        return self._border_color
    
    @borderColor.setter
    def borderColor(self, value: QColor):
        """Set border color"""
        self._border_color = value
        self.updateChart()
    
    # NEW: Property for legend marker border width
    @Property(float)
    def legendMarkerBorderWidth(self):
        """Get legend marker border width"""
        return self._legend_marker_border_width
    
    @legendMarkerBorderWidth.setter
    def legendMarkerBorderWidth(self, value: float):
        """Set legend marker border width"""
        self._legend_marker_border_width = max(0.0, value)
        self.updateChart()
    
    @Property(bool)
    def explodeOnHover(self):
        """Get explode on hover state"""
        return self._explode_on_hover

    @explodeOnHover.setter
    def explodeOnHover(self, value: bool):
        """Set explode on hover state"""
        self._explode_on_hover = value
        # Clean up any existing hover explosion
        self._cleanupHoverExplosion()
    
    @Property(float)
    def hoverExplosionDistance(self):
        """Get hover explosion distance"""
        return self._hover_explosion_distance
    
    @hoverExplosionDistance.setter
    def hoverExplosionDistance(self, value: float):
        """Set hover explosion distance"""
        self._hover_explosion_distance = max(0.0, min(1.0, value))
        # Update any currently hovered slice
        if self._hovered_slice and self._hover_exploded:
            slice_obj = self._getSliceObject(self._hovered_slice)
            if slice_obj:
                slice_obj.setExplodeDistanceFactor(value)
                self._chart.update()
    
    @Property(bool)
    def showToolbar(self):
        """Get toolbar visibility"""
        return self.isToolbarVisible()
    
    @showToolbar.setter
    def showToolbar(self, value: bool):
        """Set toolbar visibility"""
        self.setToolbarVisible(value)
    
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