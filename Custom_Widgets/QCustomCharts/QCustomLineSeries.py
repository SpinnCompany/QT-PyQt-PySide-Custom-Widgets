import os
import enum
from typing import List, Tuple, Dict, Any, Optional
from qtpy.QtCore import Qt, Signal, Property, QRect, QPointF, QTimer, QEvent, QPoint, QSize
from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
    QLabel, QSlider, QCheckBox, QColorDialog, QSpinBox, QGroupBox,
    QFormLayout, QMenu, QAction, QSizePolicy, QFrame, QScrollArea,
    QGridLayout, QToolButton, QInputDialog, QMessageBox, QFileDialog,
    QGraphicsDropShadowEffect, QApplication, QStyleFactory, QStyleOption, QStyle
)
from qtpy.QtGui import (
    QColor, QFont, QPainter, QPen, QBrush, QLinearGradient,
    QGradient, QIcon, QPalette, QCursor, QPixmap, QFontMetrics,
    QPainterPath, QPolygonF, QRadialGradient, QConicalGradient,
    QKeySequence, QPaintEvent, QPainterPathStroker
)
from qtpy.QtCharts import (
    QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis,
    QCategoryAxis, QScatterSeries, QAreaSeries
)

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Log import logInfo, logWarning, logError
from Custom_Widgets.QCustomTipOverlay import QCustomTipOverlay 


class QCustomLineSeries(QWidget):
    """
    A highly customizable line series chart widget with creative visual effects,
    multiple interpolation modes, and advanced styling options.
    Qt Designer compatible with no CSS styling - uses theme colors only.
    """

    WIDGET_ICON = "components/icons/line_chart.png"
    WIDGET_TOOLTIP = "Customizable line series chart with advanced styling"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomLineSeries' name='customLineSeries'>
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
    WIDGET_MODULE = "Custom_Widgets.QCustomCharts.QCustomLineSeries"

    # Line style constants (use these strings in properties)
    LINE_SOLID = "solid"
    LINE_DASH = "dash"
    LINE_DOT = "dot"
    LINE_DASH_DOT = "dash_dot"
    LINE_DASH_DOT_DOT = "dash_dot_dot"
    LINE_NONE = "none"

    # Marker style constants (use these strings in properties)
    MARKER_CIRCLE = "circle"
    MARKER_RECTANGLE = "rectangle"
    MARKER_ROTATED_RECTANGLE = "rotated_rectangle"
    MARKER_TRIANGLE = "triangle"
    MARKER_STAR = "star"
    MARKER_PENTAGON = "pentagon"
    MARKER_NONE = "none"
    
    # Theme constants
    THEME_APP_THEME = "App Theme"
    THEME_LIGHT = "Light"
    THEME_DARK = "Dark"
    THEME_BLUE_NCS = "Blue NCS"
    THEME_BLUE_ICY = "Blue Icy"
    THEME_HIGH_CONTRAST = "High Contrast"
    THEME_QT_LIGHT = "Qt Light"
    THEME_QT_DARK = "Qt Dark"
    THEME_QT_BROWN_SAND = "Qt Brown Sand"
    
    # Legend position constants
    LEGEND_TOP = "Top"
    LEGEND_BOTTOM = "Bottom"
    LEGEND_LEFT = "Left"
    LEGEND_RIGHT = "Right"
    LEGEND_FLOATING = "Floating"
    
    # Signals
    dataPointClicked = Signal(float, float, str)  # x, y, series_name
    dataPointHovered = Signal(float, float, str)  # x, y, series_name
    seriesAdded = Signal(str)
    seriesRemoved = Signal(str)
    chartExportComplete = Signal(str, bool)  # filename, success
    legendPositionChanged = Signal(str)  # New signal for legend position changes

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize theme system
        self._appTheme = QCustomTheme()
        self._appTheme.onThemeChanged.connect(self._applyTheme)
        self._appTheme.onThemeChangeComplete.connect(self._applyTheme)

        # Customization properties
        self._chartTitle = "Line Series Chart"
        self._showLegend = True
        self._animationEnabled = True
        self._animationDuration = 1000
        self._antialiasing = True
        self._showGrid = True
        self._autoScale = True
        self._showDataPoints = True
        self._fillArea = False
        self._enableShadow = False
        self._showCrosshair = True  # Default to enabled
        self._highlightSize = 8
        self._shadowBlur = 15
        self._fillOpacity = 0.3
        self._gridColor = QColor(200, 200, 200, 100)

        # Theme property
        self._chartTheme = self.THEME_APP_THEME
        
        # Marker size properties
        self._markerSize = 8.0
        self._seriesMarkerSizes = {}
        
        # Legend properties
        self._legendPosition = self.LEGEND_BOTTOM  # Default position
        self._legendFontSize = 8  # Default legend font size
        self._legendBackgroundVisible = False  # Default no background
        
        # Axis properties
        self._xAxisTitle = "X Axis"
        self._yAxisTitle = "Y Axis"
        self._xMin = None
        self._xMax = None
        self._yMin = None
        self._yMax = None

        # Data storage
        self._seriesData = {}
        self._seriesColors = {}
        self._seriesLineStyles = {}
        self._seriesLineWidths = {}
        self._seriesMarkerStyles = {}
        self._seriesVisible = {}

        # Toolbar and footer properties
        self._showToolbar = True
        self._showFooter = True

        # Chart components
        self.chart = QChart()
        self.chart_view = QChartView()
        self.chart_view.setChart(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing, self._antialiasing)

        # Crosshair lines
        self._verticalLine = QLineSeries()
        self._horizontalLine = QLineSeries()
        self._crosshairVisible = False
        self._currentMousePoint = QPointF(0, 0)
        self._crosshairPen = QPen()
        self._crosshairPen.setWidthF(1.0)
        self._crosshairPen.setStyle(Qt.DotLine)

        # Tooltip overlay
        self._hoverTipOverlay = None
        self._hoverTimer = QTimer()
        self._hoverTimer.setSingleShot(True)
        self._hoverTimer.timeout.connect(self._showHoverTooltip)
        self._hoverDelay = 500  # ms delay before showing tooltip
        self._lastHoverPoint = None
        self._lastHoverSeries = None

        # Toolbar
        self.toolbar = QWidget()
        self.toolbar.setObjectName("toolbar")
        
        # Theme selector in toolbar
        self.theme_combo = None
        
        # Legend controls
        self.legend_position_combo = None
        
        # Status bar (footer)
        self.status_bar = QLabel("Ready")
        self.status_bar.setObjectName("statusbar")
        self.status_bar.setMaximumHeight(20)

        # Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(2)

        # Create UI
        self._createToolbar()
        self._createStatusBar()

        # Add components to layout
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.chart_view, 1)
        self.main_layout.addWidget(self.status_bar)

        # Initialize with sample data
        self._initSampleData()

        # Setup chart with theme
        self._setupChart()
        
        # Setup crosshair lines
        self._setupCrosshair()
        
        # Apply theme
        self._applyTheme()

        # Setup interactions
        self._setupInteractions()

    def _setupCrosshair(self):
        """Setup crosshair lines with initial positions"""
        # Configure crosshair lines - set names with underscore to hide from legend
        self._verticalLine.setName("__vertical_crosshair")
        self._horizontalLine.setName("__horizontal_crosshair")
        
        # Hide from legend by not setting a visible name
        # Alternatively, we can explicitly hide them from legend
        self._verticalLine.setObjectName("__vertical_crosshair")
        self._horizontalLine.setObjectName("__horizontal_crosshair")
        
        # Set initial empty data
        self._verticalLine.append(0, 0)
        self._verticalLine.append(0, 1)
        
        self._horizontalLine.append(0, 0)
        self._horizontalLine.append(1, 0)
        
        # Apply crosshair pen - color will be set by theme
        self._verticalLine.setPen(self._crosshairPen)
        self._horizontalLine.setPen(self._crosshairPen)
        
        # Add to chart
        self.chart.addSeries(self._verticalLine)
        self.chart.addSeries(self._horizontalLine)
        
        # Attach to axes
        for axis in self.chart.axes():
            if axis.orientation() == Qt.Horizontal:
                self._verticalLine.attachAxis(axis)
                self._horizontalLine.attachAxis(axis)
            elif axis.orientation() == Qt.Vertical:
                self._verticalLine.attachAxis(axis)
                self._horizontalLine.attachAxis(axis)
        
        # Initially hide crosshair
        self._verticalLine.setVisible(False)
        self._horizontalLine.setVisible(False)

    def _updateCrosshair(self, point: QPointF, state: bool):
        """Update crosshair position based on mouse point"""
        if state and point:
            # Store the current mouse point
            self._currentMousePoint = point
            self._crosshairVisible = True
            
            # Get axis ranges
            x_min, x_max = self._getAxisRange(Qt.Horizontal)
            y_min, y_max = self._getAxisRange(Qt.Vertical)
            
            if x_min is not None and x_max is not None and y_min is not None and y_max is not None:
                # Update vertical line (x = point.x(), y from min to max)
                self._verticalLine.clear()
                self._verticalLine.append(point.x(), y_min)
                self._verticalLine.append(point.x(), y_max)
                
                # Update horizontal line (y = point.y(), x from min to max)
                self._horizontalLine.clear()
                self._horizontalLine.append(x_min, point.y())
                self._horizontalLine.append(x_max, point.y())
                
                # Show crosshair
                self._verticalLine.setVisible(True)
                self._horizontalLine.setVisible(True)
                
                # Update status bar with coordinates
                self.status_bar.setText(f"Mouse: x={point.x():.2f}, y={point.y():.2f}")
        else:
            # Hide crosshair when mouse leaves
            self._verticalLine.setVisible(False)
            self._horizontalLine.setVisible(False)
            self._crosshairVisible = False
            
            # Reset status bar
            visible_count = sum(1 for v in self._seriesVisible.values() if v)
            total_points = sum(len(data) for data in self._seriesData.values())
            self.status_bar.setText(f"<b>{visible_count}</b> series | <b>{total_points}</b> total points | Theme: <b>{self._chartTheme}</b> | Legend: <b>{self._legendPosition}</b>")

        self._hideCrosshairFromLegend()

    def _getAxisRange(self, orientation: Qt.Orientation):
        """Get the current axis range for specified orientation"""
        for axis in self.chart.axes():
            if axis.orientation() == orientation:
                return axis.min(), axis.max()
        return None, None

    def _initSampleData(self):
        """Initialize with creative sample data"""
        import random
        import math

        series_names = ["Alpha", "Beta", "Gamma", "Delta"]
        colors = [
            QColor(255, 100, 100),
            QColor(100, 200, 100),
            QColor(100, 150, 255),
            QColor(200, 100, 200),
        ]
        
        marker_styles = [
            self.MARKER_CIRCLE,
            self.MARKER_RECTANGLE,
            self.MARKER_TRIANGLE,
            self.MARKER_STAR,
            self.MARKER_PENTAGON,
            self.MARKER_ROTATED_RECTANGLE
        ]
        
        for i, name in enumerate(series_names):
            data_points = []
            for x in range(0, 100, 2):
                if i == 0:
                    y = 50 + 40 * math.sin(x * math.pi / 25)
                elif i == 1:
                    y = 50 + 30 * math.cos(x * math.pi / 25) + random.uniform(-5, 5)
                elif i == 2:
                    y = 30 + x * 0.5 + random.uniform(-3, 3)
                else:
                    y = 20 + 30 * math.exp(-x / 50) * math.sin(x * math.pi / 15)
                
                data_points.append((float(x), float(y)))
            
            self._seriesData[name] = data_points
            self._seriesColors[name] = colors[i % len(colors)]
            self._seriesVisible[name] = True
            self._seriesLineStyles[name] = self.LINE_SOLID
            self._seriesLineWidths[name] = 2.0 + i * 0.5
            self._seriesMarkerStyles[name] = marker_styles[i % len(marker_styles)]
            self._seriesMarkerSizes[name] = 6.0 + i * 2.0

    def _createToolbar(self):
        """Create toolbar with chart controls including theme selector"""
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(5, 2, 5, 2)

        # Theme selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            self.THEME_APP_THEME,
            self.THEME_LIGHT,
            self.THEME_DARK,
            self.THEME_BLUE_NCS,
            self.THEME_BLUE_ICY,
            self.THEME_HIGH_CONTRAST,
            self.THEME_QT_LIGHT,
            self.THEME_QT_DARK,
            self.THEME_QT_BROWN_SAND,
        ])
        self.theme_combo.setCurrentText(self._chartTheme)
        self.theme_combo.currentTextChanged.connect(self._onThemeChanged)
        self.theme_combo.setMaximumWidth(150)
        self.theme_combo.setToolTip("Select chart theme")

        # Legend position selector
        self.legend_position_combo = QComboBox()
        self.legend_position_combo.addItems([
            self.LEGEND_TOP,
            self.LEGEND_BOTTOM,
            self.LEGEND_LEFT,
            self.LEGEND_RIGHT,
            self.LEGEND_FLOATING
        ])
        self.legend_position_combo.setCurrentText(self._legendPosition)
        self.legend_position_combo.currentTextChanged.connect(self._onLegendPositionChanged)
        self.legend_position_combo.setMaximumWidth(100)
        self.legend_position_combo.setToolTip("Legend position")

        # Crosshair toggle button
        self.crosshair_btn = QToolButton()
        self.crosshair_btn.setText("Crosshair")
        self.crosshair_btn.setCheckable(True)
        self.crosshair_btn.setChecked(self._showCrosshair)
        self.crosshair_btn.toggled.connect(lambda checked: setattr(self, "showCrosshair", checked))
        self.crosshair_btn.setToolTip("Toggle crosshair lines")

        # Tooltip toggle button
        self.tooltip_btn = QToolButton()
        self.tooltip_btn.setText("Tooltips")
        self.tooltip_btn.setCheckable(True)
        self.tooltip_btn.setChecked(True)
        self.tooltip_btn.toggled.connect(self._onTooltipToggled)
        self.tooltip_btn.setToolTip("Toggle point tooltips")

        # Tool buttons
        self.zoom_in_btn = QToolButton()
        self.zoom_in_btn.setText("Zoom In")
        self.zoom_in_btn.clicked.connect(self._zoomIn)
        self.zoom_in_btn.setToolTip("Zoom in")

        self.zoom_out_btn = QToolButton()
        self.zoom_out_btn.setText("Zoom Out")
        self.zoom_out_btn.clicked.connect(self._zoomOut)
        self.zoom_out_btn.setToolTip("Zoom out")

        self.reset_view_btn = QToolButton()
        self.reset_view_btn.setText("Reset")
        self.reset_view_btn.clicked.connect(self._resetView)
        self.reset_view_btn.setToolTip("Reset view")

        self.export_btn = QToolButton()
        self.export_btn.setText("Export")
        self.export_btn.clicked.connect(self._exportChart)
        self.export_btn.setToolTip("Export chart")

        self.grid_btn = QToolButton()
        self.grid_btn.setText("Grid")
        self.grid_btn.setCheckable(True)
        self.grid_btn.setChecked(self._showGrid)
        self.grid_btn.toggled.connect(lambda checked: setattr(self, "showGrid", checked))
        self.grid_btn.setToolTip("Toggle grid")

        self.legend_btn = QToolButton()
        self.legend_btn.setText("Legend")
        self.legend_btn.setCheckable(True)
        self.legend_btn.setChecked(self._showLegend)
        self.legend_btn.toggled.connect(lambda checked: setattr(self, "showLegend", checked))
        self.legend_btn.setToolTip("Toggle legend")

        # Marker size control
        self.marker_size_label = QLabel("Marker:")
        self.marker_size_spin = QSpinBox()
        self.marker_size_spin.setRange(1, 20)
        self.marker_size_spin.setValue(int(self._markerSize))
        self.marker_size_spin.valueChanged.connect(self._onMarkerSizeChanged)
        self.marker_size_spin.setToolTip("Set marker size")

        # Add widgets to toolbar
        toolbar_layout.addWidget(self.zoom_in_btn)
        toolbar_layout.addWidget(self.zoom_out_btn)
        toolbar_layout.addWidget(self.reset_view_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.crosshair_btn)
        toolbar_layout.addWidget(self.tooltip_btn)
        toolbar_layout.addWidget(self.grid_btn)
        toolbar_layout.addWidget(self.legend_btn)
        toolbar_layout.addWidget(QLabel("Legend Pos:"))
        toolbar_layout.addWidget(self.legend_position_combo)
        toolbar_layout.addWidget(QLabel("L.Marker:"))
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.theme_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.marker_size_label)
        toolbar_layout.addWidget(self.marker_size_spin)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.export_btn)

        self.toolbar.setMaximumHeight(30)
        self.toolbar.setVisible(self._showToolbar)

    def _createStatusBar(self):
        """Create status bar with info display"""
        self.status_bar.setTextFormat(Qt.RichText)
        self.status_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.status_bar.setVisible(self._showFooter)

    def _applyTheme(self):
        """Apply the selected theme to the chart"""
        try:
            if self._chartTheme == self.THEME_APP_THEME:
                # Clear any existing theme
                if self._appTheme.isThemeDark:
                    self.chart.setTheme(QChart.ChartThemeDark)
                else:
                    self.chart.setTheme(QChart.ChartThemeLight)

                # Use application palette
                app = QApplication.instance()
                if app:
                    palette = app.palette()
                    
                    # Set background to window color
                    self.chart.setBackgroundBrush(QBrush(QColor(0,0,0,0)))
                    
                    # Set plot area background to base color
                    self.chart.setPlotAreaBackgroundBrush(QBrush(palette.color(QPalette.Base)))
                    self.chart.setPlotAreaBackgroundVisible(False)
                    
                    # Set title color to text color
                    title_font = self.chart.titleFont()
                    title_font.setBold(True)
                    self.chart.setTitleFont(title_font)
                    
            elif self._chartTheme == self.THEME_LIGHT:
                self.chart.setTheme(QChart.ChartThemeLight)
            elif self._chartTheme == self.THEME_DARK:
                self.chart.setTheme(QChart.ChartThemeDark)
            elif self._chartTheme == self.THEME_BLUE_NCS:
                self.chart.setTheme(QChart.ChartThemeBlueNcs)   
            elif self._chartTheme == self.THEME_BLUE_ICY:
                self.chart.setTheme(QChart.ChartThemeBlueIcy)
            elif self._chartTheme == self.THEME_HIGH_CONTRAST:
                self.chart.setTheme(QChart.ChartThemeHighContrast)
            elif self._chartTheme == self.THEME_QT_LIGHT:
                self.chart.setTheme(QChart.ChartThemeQt)
            elif self._chartTheme == self.THEME_QT_DARK:
                self.chart.setTheme(QChart.ChartThemeDark)
            elif self._chartTheme == self.THEME_QT_BROWN_SAND:
                self.chart.setTheme(QChart.ChartThemeBrownSand)
            
            # Update the view
            self.chart_view.update()
            self._updateCrosshairColor()
            
        except Exception as e:
            print(f"Error applying theme: {e}")

    def _hideCrosshairFromLegend(self):
        """Hide crosshair series from the legend"""
        legend = self.chart.legend()
        if legend:
            # Get all marker items
            markers = legend.markers()
            for marker in markers:
                series = marker.series()
                if series and series.name() in ["__vertical_crosshair", "__horizontal_crosshair"]:
                    marker.setVisible(False)
                   
                   
    def _updateCrosshairColor(self):
        """Update crosshair color based on current theme"""
        if self._chartTheme == self.THEME_APP_THEME:
            # For App Theme, use the application's text color
            app = QApplication.instance()
            if app:
                palette = app.palette()
                text_color = palette.color(QPalette.Text)
                # Add some transparency
                crosshair_color = QColor(text_color)
                crosshair_color.setAlpha(200)
                self._crosshairPen.setColor(crosshair_color)
        else:
            # For predefined themes, determine text color based on theme
            if self._chartTheme in [self.THEME_DARK, self.THEME_QT_DARK]:
                # Dark themes - use light crosshair
                crosshair_color = QColor(255, 255, 255, 200)
            else:
                # Light themes - use dark crosshair
                crosshair_color = QColor(0, 0, 0, 200)

            self._crosshairPen.setColor(crosshair_color)
        
        # Update crosshair pen for both lines
        if self._verticalLine and self._horizontalLine:
            self._verticalLine.setPen(self._crosshairPen)
            self._horizontalLine.setPen(self._crosshairPen)

    def _setupChart(self):
        """Setup the chart with current data and settings"""
        try:
            # Clear existing series except crosshair
            series_to_remove = []
            for series in self.chart.series():
                if series.name() not in ["__vertical_crosshair", "__horizontal_crosshair"]:
                    series_to_remove.append(series)
            
            for series in series_to_remove:
                self.chart.removeSeries(series)

            # Clear axes (but keep them for crosshair)
            axes_to_remove = []
            for axis in self.chart.axes():
                if axis not in self._verticalLine.attachedAxes() and axis not in self._horizontalLine.attachedAxes():
                    axes_to_remove.append(axis)
            
            for axis in axes_to_remove:
                self.chart.removeAxis(axis)

            # Set chart title
            self.chart.setTitle(self._chartTitle)

            # Create axes if they don't exist
            axis_x = None
            axis_y = None
            
            # Check if axes already exist from crosshair
            for axis in self.chart.axes():
                if axis.orientation() == Qt.Horizontal:
                    axis_x = axis
                elif axis.orientation() == Qt.Vertical:
                    axis_y = axis
            
            if axis_x is None:
                axis_x = QValueAxis()
                axis_x.setTitleText(self._xAxisTitle)
                axis_x.setGridLineVisible(self._showGrid)
                self.chart.addAxis(axis_x, Qt.AlignBottom)
            
            if axis_y is None:
                axis_y = QValueAxis()
                axis_y.setTitleText(self._yAxisTitle)
                axis_y.setGridLineVisible(self._showGrid)
                self.chart.addAxis(axis_y, Qt.AlignLeft)

            all_x = []
            all_y = []

            # Create series
            for series_name, data in self._seriesData.items():
                if not self._seriesVisible.get(series_name, True):
                    continue

                series = QLineSeries()
                series.setName(series_name)

                # Add data points
                for x, y in data:
                    series.append(x, y)
                    all_x.append(x)
                    all_y.append(y)

                # Apply styling
                color = self._seriesColors.get(series_name, QColor("#00bcff"))
                series.setColor(color)

                line_style = self._seriesLineStyles.get(series_name, self.LINE_SOLID)
                pen = series.pen()
                pen.setWidthF(self._seriesLineWidths.get(series_name, 2.0))
                
                if line_style == self.LINE_DASH:
                    pen.setStyle(Qt.DashLine)
                elif line_style == self.LINE_DOT:
                    pen.setStyle(Qt.DotLine)
                elif line_style == self.LINE_DASH_DOT:
                    pen.setStyle(Qt.DashDotLine)
                elif line_style == self.LINE_DASH_DOT_DOT:
                    pen.setStyle(Qt.DashDotDotLine)
                elif line_style == self.LINE_NONE:
                    pen.setStyle(Qt.NoPen)
                else:
                    pen.setStyle(Qt.SolidLine)
                
                series.setPen(pen)

                self.chart.addSeries(series)
                series.attachAxis(axis_x)
                series.attachAxis(axis_y)

                # Add markers if enabled
                marker_style = self._seriesMarkerStyles.get(series_name, self.MARKER_NONE)
                if marker_style != self.MARKER_NONE and self._showDataPoints:
                    scatter = QScatterSeries()
                    scatter.setName(f"{series_name}_markers")
                    scatter.setColor(color)
                    
                    marker_size = self._seriesMarkerSizes.get(series_name, self._markerSize)
                    scatter.setMarkerSize(float(marker_size))
                    
                    if marker_style == self.MARKER_CIRCLE:
                        scatter.setMarkerShape(QScatterSeries.MarkerShapeCircle)
                    elif marker_style == self.MARKER_RECTANGLE:
                        scatter.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
                    elif marker_style == self.MARKER_ROTATED_RECTANGLE:
                        scatter.setMarkerShape(QScatterSeries.MarkerShapeRotatedRectangle)
                    elif marker_style == self.MARKER_TRIANGLE:
                        scatter.setMarkerShape(QScatterSeries.MarkerShapeTriangle)
                    elif marker_style == self.MARKER_STAR:
                        scatter.setMarkerShape(QScatterSeries.MarkerShapeStar)
                    elif marker_style == self.MARKER_PENTAGON:
                        scatter.setMarkerShape(QScatterSeries.MarkerShapePentagon)
                    else:
                        scatter.setMarkerShape(QScatterSeries.MarkerShapeCircle)
                    
                    for x, y in data:
                        scatter.append(x, y)
                    
                    self.chart.addSeries(scatter)
                    scatter.attachAxis(axis_x)
                    scatter.attachAxis(axis_y)

            # Configure legend
            legend = self.chart.legend()
            legend.setVisible(self._showLegend)
            if self._showLegend:
                # Set legend alignment based on position
                if self._legendPosition == self.LEGEND_TOP:
                    legend.setAlignment(Qt.AlignTop)
                elif self._legendPosition == self.LEGEND_BOTTOM:
                    legend.setAlignment(Qt.AlignBottom)
                elif self._legendPosition == self.LEGEND_LEFT:
                    legend.setAlignment(Qt.AlignLeft)
                elif self._legendPosition == self.LEGEND_RIGHT:
                    legend.setAlignment(Qt.AlignRight)
                elif self._legendPosition == self.LEGEND_FLOATING:
                    legend.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    # For floating, position it at top-right
                    legend.detachFromChart()
                    legend.setGeometry(QRect(10, 10, 150, 100))
                    legend.update()
                
                # Apply font size
                font = legend.font()
                font.setPointSize(self._legendFontSize)
                legend.setFont(font)
                
                # Apply background and border
                legend.setBackgroundVisible(self._legendBackgroundVisible)

            # Set axis ranges
            if all_x and all_y:
                if self._autoScale:
                    margin = 0.05
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

            # Configure animation
            if self._animationEnabled:
                self.chart.setAnimationOptions(QChart.SeriesAnimations)
                self.chart.setAnimationDuration(self._animationDuration)
            else:
                self.chart.setAnimationOptions(QChart.NoAnimation)

            # Apply theme after setting up chart
            self._applyTheme()

            # Hide crosshair from legend
            self._hideCrosshairFromLegend()

            # Update status
            visible_count = sum(1 for v in self._seriesVisible.values() if v)
            total_points = sum(len(data) for data in self._seriesData.values())
            self.status_bar.setText(f"<b>{visible_count}</b> series | <b>{total_points}</b> total points | Theme: <b>{self._chartTheme}</b> | Legend: <b>{self._legendPosition}</b>")

        except Exception as e:
            print(f"Error setting up chart: {e}")
            self.status_bar.setText(f"<font color='red'>Error: {str(e)}</font>")

    def _setupInteractions(self):
        """Setup mouse and keyboard interactions"""
        self.chart_view.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.chart_view.setRubberBand(QChartView.RectangleRubberBand)
        
        # Connect all series hovered signals
        self._connectSeriesHoverSignals()
        
        # Install event filter for mouse leave events
        self.chart_view.viewport().installEventFilter(self)

    def _connectSeriesHoverSignals(self):
        """Connect hover signals for all series"""
        for series in self.chart.series():
            if isinstance(series, (QLineSeries, QScatterSeries)):
                # Only connect if it's not a crosshair series
                if series.name() not in ["__vertical_crosshair", "__horizontal_crosshair"]:
                    series.hovered.connect(self._onSeriesHovered)

    def _onSeriesHovered(self, point: QPointF, state: bool):
        """Handle series hover events to show crosshair and tooltip"""
        # Update crosshair
        self._updateCrosshair(point, state)
        
        # Handle tooltip
        if state and point:
            # Store hover information
            self._lastHoverPoint = point
            
            # Find which series was hovered
            for series in self.chart.series():
                if isinstance(series, (QLineSeries, QScatterSeries)) and series.name() not in ["__vertical_crosshair", "__horizontal_crosshair"]:
                    # Check if point is close to any data point in this series
                    for series_name, data in self._seriesData.items():
                        for data_point in data:
                            dx = abs(data_point[0] - point.x())
                            dy = abs(data_point[1] - point.y())
                            if dx < 1.0 and dy < 1.0:  # Tolerance threshold
                                self._lastHoverSeries = series_name
                                
                                # Emit signal
                                self.dataPointHovered.emit(point.x(), point.y(), series_name)
                                
                                # Start timer to show tooltip
                                if self.tooltip_btn.isChecked():
                                    self._hoverTimer.start(self._hoverDelay)
                                return
        else:
            # Mouse left the point, hide tooltip
            self._hideHoverTooltip()
            self._hoverTimer.stop()

    def _showHoverTooltip(self):
        """Show custom tooltip for hovered point"""
        if not self._lastHoverPoint or not self._lastHoverSeries:
            return
            
        # Hide existing tooltip
        self._hideHoverTooltip()
        
        # Get series information
        series_name = self._lastHoverSeries
        color = self._seriesColors.get(series_name, QColor("#00bcff"))
        
        # Create tooltip content
        title = f"Data Point - {series_name}"
        description = f"X: {self._lastHoverPoint.x():.2f}\nY: {self._lastHoverPoint.y():.2f}"
        
        # Create icon from series color
        icon_pixmap = QPixmap(24, 24)
        icon_pixmap.fill(Qt.transparent)
        painter = QPainter(icon_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 24, 24)
        painter.end()
        icon = QIcon(icon_pixmap)
        
        # Convert chart point to global screen coordinates
        chart_pos = self.chart.mapToPosition(self._lastHoverPoint)
        view_pos = self.chart_view.mapFromScene(chart_pos)
        global_pos = self.chart_view.mapToGlobal(view_pos)

        global_mouse_pos = QCursor.pos()                     # Global screen coordinates
        local_mouse_pos = self.mapFromGlobal(global_mouse_pos) 
        
        # Create tooltip overlay with QPoint target
        self._hoverTipOverlay = QCustomTipOverlay(
            parent=self,
            title=title,
            description=description,
            icon=icon,
            target=local_mouse_pos,
            duration=5000,  
            tailPosition="auto",
            isClosable=False,
            deleteOnClose=True,
            toolFlag=True
        )
        
        # Connect closed signal
        self._hoverTipOverlay.closed.connect(self._onTooltipClosed)
        
        # Show tooltip
        self._hoverTipOverlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self._hoverTipOverlay.show()

    def _hideHoverTooltip(self):
        """Hide the hover tooltip"""
        if self._hoverTipOverlay:
            self._hoverTipOverlay.close()
            self._hoverTipOverlay = None

    def _onTooltipClosed(self):
        """Handle tooltip closed signal"""
        self._hoverTipOverlay = None

    def _onTooltipToggled(self, checked: bool):
        """Handle tooltip toggle button"""
        if not checked:
            self._hideHoverTooltip()
            self._hoverTimer.stop()

    def eventFilter(self, obj, event):
        """Filter events to handle mouse leave"""
        if obj == self.chart_view.viewport():
            if event.type() == QEvent.Leave:
                # Mouse left the chart view, hide tooltip and crosshair
                self._hideHoverTooltip()
                self._hoverTimer.stop()
                self._updateCrosshair(None, False)
                return True
        
        return super().eventFilter(obj, event)

    def _zoomIn(self):
        """Zoom in chart"""
        self.chart.zoomIn()
        # Update crosshair if visible
        if self._crosshairVisible:
            self._updateCrosshair(self._currentMousePoint, True)

    def _zoomOut(self):
        """Zoom out chart"""
        self.chart.zoomOut()
        # Update crosshair if visible
        if self._crosshairVisible:
            self._updateCrosshair(self._currentMousePoint, True)

    def _resetView(self):
        """Reset chart view"""
        self.chart.zoomReset()
        self._autoScale = True
        self._setupChart()
        self.status_bar.setText("View reset")

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
                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    format = "JPG"
                else:
                    format = "PNG"
                    if not filename.lower().endswith('.png'):
                        filename += '.png'
                
                pixmap = self.chart_view.grab()
                success = pixmap.save(filename, format)
                
                if success:
                    self.status_bar.setText(f"Exported to {os.path.basename(filename)}")
                    self.chartExportComplete.emit(filename, True)
                else:
                    self.status_bar.setText("Export failed")
                    self.chartExportComplete.emit(filename, False)
                    
            except Exception as e:
                print(f"Export error: {e}")
                self.status_bar.setText(f"Export error: {str(e)}")
                self.chartExportComplete.emit(filename, False)

    def _onMarkerSizeChanged(self):
        """Handle marker size spinbox change"""
        self.markerSize = float(self.marker_size_spin.value())

    def _onLegendPositionChanged(self, position):
        """Handle legend position selection change"""
        self.legendPosition = position

    def _onThemeChanged(self, theme):
        """Handle theme selection change"""
        self.chartTheme = theme

    # ============ CROSSHAIR PROPERTIES AND METHODS ============

    @Property(bool)
    def showCrosshair(self):
        return self._showCrosshair

    @showCrosshair.setter
    def showCrosshair(self, value):
        self._showCrosshair = bool(value)
        if hasattr(self, 'crosshair_btn'):
            self.crosshair_btn.setChecked(value)
        
        if not self._showCrosshair:
            self._verticalLine.setVisible(False)
            self._horizontalLine.setVisible(False)
        elif self._crosshairVisible:
            self._verticalLine.setVisible(True)
            self._horizontalLine.setVisible(True)

    @Property(QColor)
    def crosshairColor(self):
        return self._crosshairPen.color()

    @crosshairColor.setter
    def crosshairColor(self, value):
        self._crosshairPen.setColor(value)
        if self._verticalLine and self._horizontalLine:
            self._verticalLine.setPen(self._crosshairPen)
            self._horizontalLine.setPen(self._crosshairPen)

    @Property(float)
    def crosshairWidth(self):
        return self._crosshairPen.widthF()

    @crosshairWidth.setter
    def crosshairWidth(self, value):
        self._crosshairPen.setWidthF(float(value))
        if self._verticalLine and self._horizontalLine:
            self._verticalLine.setPen(self._crosshairPen)
            self._horizontalLine.setPen(self._crosshairPen)

    def setCrosshairStyle(self, style: Qt.PenStyle):
        """Set crosshair line style"""
        self._crosshairPen.setStyle(style)
        if self._verticalLine and self._horizontalLine:
            self._verticalLine.setPen(self._crosshairPen)
            self._horizontalLine.setPen(self._crosshairPen)

    def showCrosshairAt(self, x: float, y: float):
        """Manually show crosshair at specific coordinates"""
        point = QPointF(x, y)
        self._updateCrosshair(point, True)

    def hideCrosshair(self):
        """Manually hide crosshair"""
        self._updateCrosshair(None, False)

    # ============ TOOLTIP PROPERTIES AND METHODS ============

    @Property(bool)
    def showTooltips(self):
        """Get whether tooltips are enabled"""
        return self.tooltip_btn.isChecked() if hasattr(self, 'tooltip_btn') else True

    @showTooltips.setter
    def showTooltips(self, value):
        """Set tooltips enabled"""
        if hasattr(self, 'tooltip_btn'):
            self.tooltip_btn.setChecked(bool(value))
        if not value:
            self._hideHoverTooltip()
            self._hoverTimer.stop()

    @Property(int)
    def tooltipDelay(self):
        """Get tooltip display delay in milliseconds"""
        return self._hoverDelay

    @tooltipDelay.setter
    def tooltipDelay(self, value):
        """Set tooltip display delay in milliseconds"""
        self._hoverDelay = max(0, int(value))

    @Property(int)
    def tooltipDuration(self):
        """Get tooltip display duration in milliseconds"""
        # This is handled by QCustomTipOverlay, but we can expose it if needed
        return 3000  # Default value

    @tooltipDuration.setter
    def tooltipDuration(self, value):
        """Set tooltip display duration in milliseconds"""
        # This would need to be applied when creating new tooltips
        pass

    def showTooltipAt(self, x: float, y: float, series_name: str, title: str = None, description: str = None):
        """Manually show tooltip at specific coordinates"""
        self._lastHoverPoint = QPointF(x, y)
        self._lastHoverSeries = series_name
        self._showHoverTooltip()

    def hideTooltip(self):
        """Manually hide tooltip"""
        self._hideHoverTooltip()

    # ============ PUBLIC API METHODS ============

    def addSeries(self, name: str, data: List[Tuple[float, float]], 
              color: QColor = None, line_width: float = 2.0,
              line_style: str = "solid",
              marker_style: str = "none",
              marker_size: float = None,
              visible: bool = True):
        """Add a new series to the chart"""
        self._seriesData[name] = data
        self._seriesVisible[name] = visible
        self._seriesLineWidths[name] = line_width
        self._seriesLineStyles[name] = line_style
        self._seriesMarkerStyles[name] = marker_style
        
        if color:
            self._seriesColors[name] = color
        
        if marker_size is not None:
            self._seriesMarkerSizes[name] = float(marker_size)
        
        self._setupChart()
        self._connectSeriesHoverSignals()
        self.seriesAdded.emit(name)

    def removeSeries(self, name: str):
        """Remove a series from the chart"""
        if name in self._seriesData:
            del self._seriesData[name]
            if name in self._seriesColors:
                del self._seriesColors[name]
            if name in self._seriesVisible:
                del self._seriesVisible[name]
            if name in self._seriesMarkerSizes:
                del self._seriesMarkerSizes[name]
            
            self._setupChart()
            self.seriesRemoved.emit(name)

    def updateSeries(self, name: str, data: List[Tuple[float, float]]):
        """Update data for an existing series"""
        if name in self._seriesData:
            self._seriesData[name] = data
            self._setupChart()

    def clearData(self):
        """Clear all chart data"""
        self._seriesData = {}
        self._seriesColors = {}
        self._seriesVisible = {}
        self._seriesMarkerSizes = {}
        self._setupChart()

    def getSeriesNames(self) -> List[str]:
        """Get list of all series names"""
        return list(self._seriesData.keys())

    def getSeriesData(self, name: str) -> List[Tuple[float, float]]:
        """Get data for a specific series"""
        return self._seriesData.get(name, [])

    def setSeriesColor(self, name: str, color: QColor):
        """Set color for a specific series"""
        self._seriesColors[name] = color
        self._setupChart()

    def setSeriesVisibility(self, name: str, visible: bool):
        """Set visibility for a specific series"""
        self._seriesVisible[name] = visible
        self._setupChart()

    def setSeriesLineStyle(self, name: str, style: str):
        """Set line style for a specific series"""
        self._seriesLineStyles[name] = style
        self._setupChart()

    def setSeriesMarkerStyle(self, name: str, style: str):
        """Set marker style for a specific series"""
        self._seriesMarkerStyles[name] = style
        self._setupChart()

    def setSeriesMarkerSize(self, name: str, size: float):
        """Set marker size for a specific series"""
        self._seriesMarkerSizes[name] = float(size)
        self._setupChart()

    def getSeriesMarkerSize(self, name: str) -> float:
        """Get marker size for a specific series"""
        return self._seriesMarkerSizes.get(name, self._markerSize)

    # ============ LEGEND CUSTOMIZATION METHODS ============

    def setLegendBackgroundVisible(self, visible: bool):
        """Set legend background visibility"""
        self._legendBackgroundVisible = visible
        legend = self.chart.legend()
        if legend:
            legend.setBackgroundVisible(visible)
        self.chart_view.update()

    def setLegendFontSize(self, size: int):
        """Set legend font size"""
        self._legendFontSize = size
        legend = self.chart.legend()
        if legend:
            font = legend.font()
            font.setPointSize(size)
            legend.setFont(font)
        self.chart_view.update()

    def getLegendFontSize(self) -> int:
        """Get legend font size"""
        return self._legendFontSize

    def getAvailableLegendPositions(self) -> List[str]:
        """Get list of available legend positions"""
        return [
            self.LEGEND_TOP,
            self.LEGEND_BOTTOM,
            self.LEGEND_LEFT,
            self.LEGEND_RIGHT,
            self.LEGEND_FLOATING
        ]

    def setLegendAlignment(self, alignment: Qt.Alignment):
        """Directly set legend alignment"""
        legend = self.chart.legend()
        if legend:
            legend.setAlignment(alignment)
            self.chart_view.update()

    def getLegendAlignment(self) -> Qt.Alignment:
        """Get current legend alignment"""
        legend = self.chart.legend()
        if legend:
            return legend.alignment()
        return Qt.AlignBottom

    # ============ PROPERTIES ============

    @Property(str)
    def chartTheme(self):
        """Get the current chart theme"""
        return self._chartTheme

    @chartTheme.setter
    def chartTheme(self, value):
        """Set the chart theme and apply it"""
        if value != self._chartTheme:
            self._chartTheme = str(value)
            if hasattr(self, 'theme_combo') and self.theme_combo:
                self.theme_combo.setCurrentText(value)
            self._applyTheme()
            # Update status bar
            visible_count = sum(1 for v in self._seriesVisible.values() if v)
            total_points = sum(len(data) for data in self._seriesData.values())
            self.status_bar.setText(f"<b>{visible_count}</b> series | <b>{total_points}</b> total points | Theme: <b>{self._chartTheme}</b> | Legend: <b>{self._legendPosition}</b>")

    @Property(str)
    def legendPosition(self):
        """Get the current legend position"""
        return self._legendPosition

    @legendPosition.setter
    def legendPosition(self, value):
        """Set the legend position"""
        if value != self._legendPosition and value in self.getAvailableLegendPositions():
            self._legendPosition = str(value)
            if hasattr(self, 'legend_position_combo') and self.legend_position_combo:
                self.legend_position_combo.setCurrentText(value)
            
            # Update legend position
            legend = self.chart.legend()
            if legend:
                if value == self.LEGEND_TOP:
                    legend.setAlignment(Qt.AlignTop)
                elif value == self.LEGEND_BOTTOM:
                    legend.setAlignment(Qt.AlignBottom)
                elif value == self.LEGEND_LEFT:
                    legend.setAlignment(Qt.AlignLeft)
                elif value == self.LEGEND_RIGHT:
                    legend.setAlignment(Qt.AlignRight)
                elif value == self.LEGEND_FLOATING:
                    legend.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    legend.detachFromChart()
                    legend.setGeometry(QRect(10, 10, 150, 100))
                
                legend.update()
            
            self.chart_view.update()
            self.legendPositionChanged.emit(value)
            
            # Update status bar
            self.status_bar.setText(f"Legend position changed to: <b>{value}</b>")

    @Property(str)
    def chartTitle(self):
        return self._chartTitle

    @chartTitle.setter
    def chartTitle(self, value):
        self._chartTitle = str(value)
        self.chart.setTitle(self._chartTitle)

    @Property(bool)
    def showLegend(self):
        return self._showLegend

    @showLegend.setter
    def showLegend(self, value):
        self._showLegend = bool(value)
        if hasattr(self, 'legend_btn'):
            self.legend_btn.setChecked(value)
        legend = self.chart.legend()
        if legend:
            legend.setVisible(value)

    @Property(bool)
    def showGrid(self):
        return self._showGrid

    @showGrid.setter
    def showGrid(self, value):
        self._showGrid = bool(value)
        if hasattr(self, 'grid_btn'):
            self.grid_btn.setChecked(value)
        for axis in self.chart.axes():
            axis.setGridLineVisible(value)

    @Property(bool)
    def animationEnabled(self):
        return self._animationEnabled

    @animationEnabled.setter
    def animationEnabled(self, value):
        self._animationEnabled = bool(value)
        if self._animationEnabled:
            self.chart.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self.chart.setAnimationOptions(QChart.NoAnimation)

    @Property(int)
    def animationDuration(self):
        return self._animationDuration

    @animationDuration.setter
    def animationDuration(self, value):
        self._animationDuration = int(value)
        if self._animationEnabled:
            self.chart.setAnimationDuration(self._animationDuration)

    @Property(bool)
    def antialiasing(self):
        return self._antialiasing

    @antialiasing.setter
    def antialiasing(self, value):
        self._antialiasing = bool(value)
        self.chart_view.setRenderHint(QPainter.Antialiasing, self._antialiasing)

    @Property(bool)
    def showDataPoints(self):
        return self._showDataPoints

    @showDataPoints.setter
    def showDataPoints(self, value):
        self._showDataPoints = bool(value)
        self._setupChart()

    @Property(bool)
    def fillArea(self):
        return self._fillArea

    @fillArea.setter
    def fillArea(self, value):
        self._fillArea = bool(value)
        self._setupChart()

    @Property(bool)
    def enableShadow(self):
        return self._enableShadow

    @enableShadow.setter
    def enableShadow(self, value):
        self._enableShadow = bool(value)
        self._setupChart()

    @Property(int)
    def highlightSize(self):
        return self._highlightSize

    @highlightSize.setter
    def highlightSize(self, value):
        self._highlightSize = int(value)
        self._setupChart()

    @Property(int)
    def shadowBlur(self):
        return self._shadowBlur

    @shadowBlur.setter
    def shadowBlur(self, value):
        self._shadowBlur = int(value)
        self._setupChart()

    @Property(float)
    def fillOpacity(self):
        return self._fillOpacity

    @fillOpacity.setter
    def fillOpacity(self, value):
        self._fillOpacity = float(value)
        self._setupChart()

    @Property(QColor)
    def gridColor(self):
        return self._gridColor

    @gridColor.setter
    def gridColor(self, value):
        self._gridColor = value
        for axis in self.chart.axes():
            axis.setGridLineColor(self._gridColor)
        self.chart_view.update()

    @Property(bool)
    def autoScale(self):
        return self._autoScale

    @autoScale.setter
    def autoScale(self, value):
        self._autoScale = bool(value)
        self._setupChart()

    @Property(str)
    def xAxisTitle(self):
        return self._xAxisTitle

    @xAxisTitle.setter
    def xAxisTitle(self, value):
        self._xAxisTitle = str(value)
        for axis in self.chart.axes():
            if isinstance(axis, QValueAxis) and axis.orientation() == Qt.Horizontal:
                axis.setTitleText(value)

    @Property(str)
    def yAxisTitle(self):
        return self._yAxisTitle

    @yAxisTitle.setter
    def yAxisTitle(self, value):
        self._yAxisTitle = str(value)
        for axis in self.chart.axes():
            if isinstance(axis, QValueAxis) and axis.orientation() == Qt.Vertical:
                axis.setTitleText(value)

    @Property(float)
    def xMin(self):
        return self._xMin

    @xMin.setter
    def xMin(self, value):
        self._xMin = float(value) if value is not None else None
        self._autoScale = False
        self._setupChart()

    @Property(float)
    def xMax(self):
        return self._xMax

    @xMax.setter
    def xMax(self, value):
        self._xMax = float(value) if value is not None else None
        self._autoScale = False
        self._setupChart()

    @Property(float)
    def yMin(self):
        return self._yMin

    @yMin.setter
    def yMin(self, value):
        self._yMin = float(value) if value is not None else None
        self._autoScale = False
        self._setupChart()

    @Property(float)
    def yMax(self):
        return self._yMax

    @yMax.setter
    def yMax(self, value):
        self._yMax = float(value) if value is not None else None
        self._autoScale = False
        self._setupChart()

    @Property(bool)
    def showToolbar(self):
        return self._showToolbar

    @showToolbar.setter
    def showToolbar(self, value):
        self._showToolbar = bool(value)
        if hasattr(self, 'toolbar'):
            self.toolbar.setVisible(value)

    @Property(bool)
    def showFooter(self):
        return self._showFooter

    @showFooter.setter
    def showFooter(self, value):
        self._showFooter = bool(value)
        if hasattr(self, 'status_bar'):
            self.status_bar.setVisible(value)

    @Property(float)
    def markerSize(self):
        return self._markerSize

    @markerSize.setter
    def markerSize(self, value):
        self._markerSize = float(value)
        if hasattr(self, 'marker_size_spin'):
            self.marker_size_spin.setValue(int(value))
        
        for series_name in self._seriesData.keys():
            if series_name not in self._seriesMarkerSizes:
                self._setupChart()
                return
        
        self._setupChart()

    @Property(int)
    def legendFontSize(self):
        return self._legendFontSize

    @legendFontSize.setter
    def legendFontSize(self, value):
        self._legendFontSize = int(value)
        legend = self.chart.legend()
        if legend:
            font = legend.font()
            font.setPointSize(self._legendFontSize)
            legend.setFont(font)
        self.chart_view.update()

    @Property(bool)
    def legendBackgroundVisible(self):
        return self._legendBackgroundVisible

    @legendBackgroundVisible.setter
    def legendBackgroundVisible(self, value):
        self._legendBackgroundVisible = bool(value)
        legend = self.chart.legend()
        if legend:
            legend.setBackgroundVisible(self._legendBackgroundVisible)
        self.chart_view.update()

    # ============ THEME-RELATED METHODS ============

    def getAvailableThemes(self) -> List[str]:
        """Get list of available theme names"""
        return [
            self.THEME_APP_THEME,
            self.THEME_LIGHT,
            self.THEME_DARK,
            self.THEME_BLUE_NCS,
            self.THEME_BLUE_ICY,
            self.THEME_HIGH_CONTRAST,
            self.THEME_QT_LIGHT,
            self.THEME_QT_DARK,
            self.THEME_QT_BROWN_SAND,
        ]

    def applyCustomPalette(self, palette: QPalette):
        """Apply a custom palette to the chart (for App Theme)"""
        if self._chartTheme == self.THEME_APP_THEME:
            self.chart.setBackgroundBrush(QBrush(palette.color(QPalette.Window)))
            self.chart.setPlotAreaBackgroundBrush(QBrush(palette.color(QPalette.Base)))
            
            text_color = palette.color(QPalette.Text)
            
            for axis in self.chart.axes():
                axis.setLinePenColor(text_color)
                axis.setLabelsColor(text_color)
                axis.setTitleBrush(QBrush(text_color))
                
                grid_color = text_color
                grid_color.setAlpha(80)
                axis.setGridLineColor(grid_color)
                
                if hasattr(axis, 'setMinorGridLineColor'):
                    minor_grid_color = text_color
                    minor_grid_color.setAlpha(40)
                    axis.setMinorGridLineColor(minor_grid_color)
            
            legend = self.chart.legend()
            if legend:
                legend.setLabelColor(text_color)
            
            # Update crosshair color to match text color
            crosshair_color = QColor(text_color)
            crosshair_color.setAlpha(180)
            self._crosshairPen.setColor(crosshair_color)
            if self._verticalLine and self._horizontalLine:
                self._verticalLine.setPen(self._crosshairPen)
                self._horizontalLine.setPen(self._crosshairPen)
            
            self.chart_view.update()

    def refreshTheme(self):
        """Refresh the current theme (useful when app palette changes)"""
        self._applyTheme()

    # ============ LINE AND MARKER STYLE PROPERTIES ============
    
    @Property(str)
    def defaultLineStyle(self):
        return self.LINE_SOLID

    @Property(str)
    def defaultMarkerStyle(self):
        return self.MARKER_NONE

    def getSeriesLineStyle(self, name: str) -> str:
        return self._seriesLineStyles.get(name, self.LINE_SOLID)

    def getSeriesMarkerStyle(self, name: str) -> str:
        return self._seriesMarkerStyles.get(name, self.MARKER_NONE)

    def isValidLineStyle(self, style: str) -> bool:
        valid_styles = [
            self.LINE_SOLID,
            self.LINE_DASH,
            self.LINE_DOT,
            self.LINE_DASH_DOT,
            self.LINE_DASH_DOT_DOT,
            self.LINE_NONE
        ]
        return style in valid_styles

    def isValidMarkerStyle(self, style: str) -> bool:
        valid_styles = [
            self.MARKER_CIRCLE,
            self.MARKER_RECTANGLE,
            self.MARKER_ROTATED_RECTANGLE,
            self.MARKER_TRIANGLE,
            self.MARKER_STAR,
            self.MARKER_PENTAGON,
            self.MARKER_NONE
        ]
        return style in valid_styles

    def setAllMarkersSize(self, size: float):
        self._markerSize = float(size)
        self._seriesMarkerSizes.clear()
        self._setupChart()

    def resetMarkerSizes(self):
        self._seriesMarkerSizes.clear()
        self._setupChart()

    def getMarkerSizeRange(self) -> Tuple[float, float]:
        return (1.0, 20.0)

    def hasCustomMarkerSize(self, series_name: str) -> bool:
        return series_name in self._seriesMarkerSizes
    
    # ============ EVENTS ============
    def paintEvent(self, event: QPaintEvent):
        """Apply the stylesheet during paint events."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        super().paintEvent(event)