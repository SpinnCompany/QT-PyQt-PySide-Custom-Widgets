# file name: QCustomVerticalBarSeries.py
from qtpy.QtCore import Property
from qtpy.QtGui import QColor

from .QCustomBarChartBase import QCustomBarChartBase
from Custom_Widgets.Utils import is_in_designer


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
        self._axis_y.setGridLineVisible(value)  # vertical bars: grid on Y axis
    
    @Property(QColor)
    def customGridColor(self):
        """Get grid color"""
        return self._custom_grid_color
    
    @customGridColor.setter
    def customGridColor(self, value: QColor):
        """Set grid color"""
        self._custom_grid_color = value
        self._axis_y.setGridLineColor(value)  # vertical bars: grid on Y axis
