# file name: QCustomVerticalBarSeries.py
from qtpy.QtCore import Property
from qtpy.QtGui import QColor

from .QCustomBarChartBase import QCustomBarChartBase
from Custom_Widgets.Utils import is_in_designer
from Custom_Widgets.QCustomCharts.QCustomChartConstants import (
    QCustomChartConstants as _CC, chart_str_to_int, chart_int_to_str,
    CHART_THEME_TO_INT, INT_TO_CHART_THEME,
    LEGEND_POSITION_TO_INT, INT_TO_LEGEND_POSITION,
    BAR_PATTERN_TO_INT, INT_TO_BAR_PATTERN,
    BAR_SELECTION_TO_INT, INT_TO_BAR_SELECTION)


class QCustomVerticalBarSeries(QCustomBarChartBase):
    """
    Vertical grouped bar chart implementation for Qt Designer.
    Inherits from QCustomBarChartBase and adds designer-specific functionality.
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
    
    def __init__(self, parent=None):
        """Initialize vertical bar chart widget"""
        super().__init__(parent, orientation="vertical")
        
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
    
    @Property(int)
    def barPattern(self):
        """Bar pattern (int; see QCustomChartEnums.BarPattern)."""
        return chart_str_to_int(BAR_PATTERN_TO_INT, self._bar_pattern)

    @barPattern.setter
    def barPattern(self, value):
        self.setBarPattern(chart_int_to_str(INT_TO_BAR_PATTERN, value, _CC.BAR_PATTERN_SOLID))

    @Property(int)
    def barSelectionMode(self):
        """Bar selection mode (int; see QCustomChartEnums.BarSelectionMode)."""
        return chart_str_to_int(BAR_SELECTION_TO_INT, self._bar_selection_mode)

    @barSelectionMode.setter
    def barSelectionMode(self, value):
        self.setBarSelectionMode(chart_int_to_str(INT_TO_BAR_SELECTION, value, _CC.BAR_SELECTION_NONE))
    
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
    
    @Property(int)
    def theme(self):
        """Current theme (int; see QCustomChartEnums.ChartTheme)."""
        return chart_str_to_int(CHART_THEME_TO_INT, self.getTheme())

    @theme.setter
    def theme(self, value):
        self.setTheme(chart_int_to_str(INT_TO_CHART_THEME, value, _CC.THEME_APP_THEME))

    @Property(int)
    def legendPosition(self):
        """Legend position (int; see QCustomChartEnums.LegendPosition)."""
        return chart_str_to_int(LEGEND_POSITION_TO_INT, self.getLegendPosition())

    @legendPosition.setter
    def legendPosition(self, value):
        self.setLegendPosition(chart_int_to_str(INT_TO_LEGEND_POSITION, value, _CC.LEGEND_BOTTOM))
    
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