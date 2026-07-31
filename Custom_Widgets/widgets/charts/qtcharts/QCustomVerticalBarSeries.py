# file name: QCustomVerticalBarSeries.py
from qtpy.QtCore import Property
from qtpy.QtGui import QColor

from .QCustomBarChartBase import QCustomBarChartBase
from Custom_Widgets.Utils import is_in_designer
from .QCustomChartConstants import (
    QCustomChartConstants as _CC, chart_str_to_int, chart_int_to_str,
    CHART_THEME_TO_INT, INT_TO_CHART_THEME,
    LEGEND_POSITION_TO_INT, INT_TO_LEGEND_POSITION,
    BAR_PATTERN_TO_INT, INT_TO_BAR_PATTERN,
    BAR_SELECTION_TO_INT, INT_TO_BAR_SELECTION,
    BAR_LABELS_TO_INT, INT_TO_BAR_LABELS)


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
    

    # ============ PROPERTIES FOR DESIGNER ============
    # Shared bar-series properties are declared on QCustomBarChartBase.
    # Only the orientation-dependent grid properties live here.
    
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
    
    @Property(int)
    def valueLabelsPosition(self):
        """Get value labels position (int; see QCustomChartEnums.BarLabelsPosition)."""
        return chart_str_to_int(BAR_LABELS_TO_INT, self.getValueLabelsPosition())

    @valueLabelsPosition.setter
    def valueLabelsPosition(self, value):
        """Set value labels position"""
        self.setValueLabelsPosition(chart_int_to_str(INT_TO_BAR_LABELS, value, _CC.BAR_LABELS_CENTER))
    
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
    
    @Property(int)
    def labelsPosition(self):
        """Get labels position (int; see QCustomChartEnums.BarLabelsPosition)."""
        return chart_str_to_int(BAR_LABELS_TO_INT, self.getValueLabelsPosition())

    @labelsPosition.setter
    def labelsPosition(self, value):
        """Set labels position"""
        self.setValueLabelsPosition(chart_int_to_str(INT_TO_BAR_LABELS, value, _CC.BAR_LABELS_CENTER))
    
    @Property(QColor)
    def customGridColor(self):
        """Get grid color"""
        return self._custom_grid_color
    
    @customGridColor.setter
    def customGridColor(self, value: QColor):
        """Set grid color"""
        self._custom_grid_color = value
        self._axis_y.setGridLineColor(value)  # vertical bars: grid on Y axis
