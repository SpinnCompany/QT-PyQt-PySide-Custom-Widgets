# file name: QCustomHorizontalBarSeries.py
from qtpy.QtCore import Property
from qtpy.QtGui import QColor

from .QCustomBarChartBase import QCustomBarChartBase
from Custom_Widgets.Utils import is_in_designer


class QCustomHorizontalBarSeries(QCustomBarChartBase):
    """
    Horizontal grouped bar chart implementation for Qt Designer.
    Inherits from QCustomBarChartBase and adds designer-specific functionality.
    """
    
    # Designer registration constants
    WIDGET_ICON = "components/icons/bar_chart_horizontal.png"
    WIDGET_TOOLTIP = "Customizable horizontal grouped bar chart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomHorizontalBarSeries' name='customHorizontalBarSeries'>
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
        """Initialize horizontal bar chart widget"""
        super().__init__(parent, orientation="horizontal")
        
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
            self._chart.setTitle("Horizontal Bar Chart Preview (Designer Mode)")
            self._axis_x.setTitleText("Values - Dummy Data")
            self._axis_y.setTitleText("Categories - Dummy Data")
            
            print("Designer mode detected - showing dummy horizontal bar chart data")

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
        self._axis_x.setGridLineVisible(value)  # horizontal bars: grid on X axis
    
    @Property(QColor)
    def customGridColor(self):
        """Get grid color"""
        return self._custom_grid_color
    
    @customGridColor.setter
    def customGridColor(self, value: QColor):
        """Set grid color"""
        self._custom_grid_color = value
        self._axis_x.setGridLineColor(value)  # horizontal bars: grid on X axis
