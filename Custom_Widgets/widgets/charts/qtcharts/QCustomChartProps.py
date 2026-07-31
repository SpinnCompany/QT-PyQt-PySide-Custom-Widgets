# file name: QCustomChartProps.py
"""
Shared Qt Designer property mixins for the chart widgets.

These are plain (non-QObject) mixin classes: PySide collects ``Property``
descriptors from plain classes in the MRO into the subclass's QMetaObject,
so the concrete chart widgets only need to inherit the mixins to expose
the properties. The explicit ``name = Property(type, getter, setter)``
form is used because the decorator form does not work reliably in plain
mixins.

Only properties whose getter/setter bodies are identical across the
charts that share them live here; divergent implementations stay on the
concrete widget classes.
"""
from qtpy.QtCore import Property
from qtpy.QtGui import QColor, QPainter
from qtpy.QtCharts import QChart

from .QCustomChartConstants import (
    QCustomChartConstants as _CC, chart_str_to_int, chart_int_to_str,
    CHART_THEME_TO_INT, INT_TO_CHART_THEME,
    LEGEND_POSITION_TO_INT, INT_TO_LEGEND_POSITION,
    LINE_STYLE_TO_INT, MARKER_STYLE_TO_INT)


class ChartCommonProps:
    """Designer properties shared by every chart widget."""

    def _getChartTitle(self):
        """Get chart title"""
        return self._chart_title

    def _setChartTitle(self, value: str):
        """Set chart title"""
        self._chart_title = value
        self._chart.setTitle(value)

    chartTitle = Property(str, _getChartTitle, _setChartTitle)

    def _getAnimationEnabled(self):
        """Get animation enabled state"""
        return self._animation_enabled

    def _setAnimationEnabled(self, value: bool):
        """Set animation enabled state"""
        self._animation_enabled = value
        if value:
            self._chart.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self._chart.setAnimationOptions(QChart.NoAnimation)

    animationEnabled = Property(bool, _getAnimationEnabled, _setAnimationEnabled)

    def _getAnimationDuration(self):
        """Get animation duration in ms"""
        return self._animation_duration

    def _setAnimationDuration(self, value: int):
        """Set animation duration in ms"""
        self._animation_duration = value
        if self._animation_enabled:
            self._chart.setAnimationDuration(value)

    animationDuration = Property(int, _getAnimationDuration, _setAnimationDuration)

    def _getAntialiasing(self):
        """Get antialiasing state"""
        return self._antialiasing

    def _setAntialiasing(self, value: bool):
        """Set antialiasing state"""
        self._antialiasing = value
        self._chart_view.setRenderHint(QPainter.Antialiasing, value)

    antialiasing = Property(bool, _getAntialiasing, _setAntialiasing)

    def _getShowToolbar(self):
        """Get toolbar visibility"""
        return self.isToolbarVisible()

    def _setShowToolbar(self, value: bool):
        """Set toolbar visibility"""
        self.setToolbarVisible(value)

    showToolbar = Property(bool, _getShowToolbar, _setShowToolbar)

    def _getTooltipsEnabled(self):
        """Get tooltips enabled state"""
        return self.areTooltipsEnabled()

    def _setTooltipsEnabled(self, value: bool):
        """Set tooltips enabled state"""
        self.setTooltipsEnabled(value)

    tooltipsEnabled = Property(bool, _getTooltipsEnabled, _setTooltipsEnabled)

    def _getTooltipDelay(self):
        """Get tooltip delay in ms"""
        return self._tooltip_delay

    def _setTooltipDelay(self, value: int):
        """Set tooltip delay in ms"""
        self._tooltip_delay = value
        self._tooltip_manager.setDelay(value)

    tooltipDelay = Property(int, _getTooltipDelay, _setTooltipDelay)

    def _getTooltipDuration(self):
        """Get tooltip duration in ms"""
        return self._tooltip_duration

    def _setTooltipDuration(self, value: int):
        """Set tooltip duration in ms"""
        self._tooltip_duration = value
        self._tooltip_manager.setDuration(value)

    tooltipDuration = Property(int, _getTooltipDuration, _setTooltipDuration)

    def _getThemeProp(self):
        """Current theme (int; see QCustomChartEnums.ChartTheme)."""
        return chart_str_to_int(CHART_THEME_TO_INT, self.getTheme())

    def _setThemeProp(self, value):
        self.setTheme(chart_int_to_str(INT_TO_CHART_THEME, value, _CC.THEME_APP_THEME))

    theme = Property(int, _getThemeProp, _setThemeProp)

    def _getLegendPosition(self):
        """Legend position (int; see QCustomChartEnums.LegendPosition)."""
        return chart_str_to_int(LEGEND_POSITION_TO_INT, self.getLegendPosition())

    def _setLegendPositionProp(self, value):
        self.setLegendPosition(chart_int_to_str(INT_TO_LEGEND_POSITION, value, _CC.LEGEND_BOTTOM))

    legendPosition = Property(int, _getLegendPosition, _setLegendPositionProp)

    def _getLegendFontSize(self):
        """Get legend font size"""
        return self._legend_font_size

    def _setLegendFontSizeProp(self, value: int):
        """Set legend font size"""
        self._legend_font_size = value
        self._legend_manager.setFontSize(value)

    legendFontSize = Property(int, _getLegendFontSize, _setLegendFontSizeProp)

    def _getLegendBackgroundVisible(self):
        """Get legend background visibility"""
        return self._legend_background_visible

    def _setLegendBackgroundVisibleProp(self, value: bool):
        """Set legend background visibility"""
        self._legend_background_visible = value
        self._legend_manager.setBackgroundVisible(value)

    legendBackgroundVisible = Property(bool, _getLegendBackgroundVisible,
                                       _setLegendBackgroundVisibleProp)

    def _getCompactMode(self):
        """Get compact mode state"""
        return self.isCompactMode()

    def _setCompactModeProp(self, value: bool):
        """Set compact mode state"""
        self.setCompactMode(value)

    compactMode = Property(bool, _getCompactMode, _setCompactModeProp)


class AxisChartProps:
    """Designer properties shared by axis-based charts (line/area/bar)."""

    def _getXAxisTitle(self):
        """Get X axis title"""
        return self._x_axis_title

    def _setXAxisTitle(self, value: str):
        """Set X axis title"""
        self._x_axis_title = value
        self._axis_x.setTitleText(value)

    xAxisTitle = Property(str, _getXAxisTitle, _setXAxisTitle)

    def _getYAxisTitle(self):
        """Get Y axis title"""
        return self._y_axis_title

    def _setYAxisTitle(self, value: str):
        """Set Y axis title"""
        self._y_axis_title = value
        self._axis_y.setTitleText(value)

    yAxisTitle = Property(str, _getYAxisTitle, _setYAxisTitle)

    def _getAutoScale(self):
        """Get auto-scaling state"""
        return self._auto_scale

    def _setAutoScale(self, value: bool):
        """Set auto-scaling state"""
        self._auto_scale = value
        if value:
            self.updateChart()

    autoScale = Property(bool, _getAutoScale, _setAutoScale)

    def _getShowCrosshair(self):
        """Get crosshair visibility"""
        return self.isCrosshairVisible()

    def _setShowCrosshair(self, value: bool):
        """Set crosshair visibility"""
        self.setCrosshairVisible(value)

    showCrosshair = Property(bool, _getShowCrosshair, _setShowCrosshair)

    def _getCrosshairColor(self):
        """Get crosshair color"""
        return self._crosshair_color

    def _setCrosshairColorProp(self, value: QColor):
        """Set crosshair color"""
        self._crosshair_color = value
        self._chart_view.setCrosshairColor(value)

    crosshairColor = Property(QColor, _getCrosshairColor, _setCrosshairColorProp)

    def _getCrosshairWidth(self):
        """Get crosshair width"""
        return self._crosshair_width

    def _setCrosshairWidthProp(self, value: float):
        """Set crosshair width"""
        self._crosshair_width = value
        self._chart_view.setCrosshairWidth(value)

    crosshairWidth = Property(float, _getCrosshairWidth, _setCrosshairWidthProp)


class SeriesStyleProps:
    """Designer properties shared by the line and area charts."""

    def _getShowGrid(self):
        """Get grid visibility"""
        return self._show_grid

    def _setShowGrid(self, value: bool):
        """Set grid visibility"""
        self._show_grid = value
        self._axis_x.setGridLineVisible(value)
        self._axis_y.setGridLineVisible(value)

    showGrid = Property(bool, _getShowGrid, _setShowGrid)

    def _getGridColor(self):
        """Get grid color"""
        return self._grid_color

    def _setGridColor(self, value: QColor):
        """Set grid color"""
        self._grid_color = value
        self._axis_x.setGridLineColor(value)
        self._axis_y.setGridLineColor(value)
        self._chart_view.update()

    gridColor = Property(QColor, _getGridColor, _setGridColor)

    def _getShowLegend(self):
        """Get legend visibility"""
        return self.isLegendVisible()

    def _setShowLegend(self, value: bool):
        """Set legend visibility"""
        self.setLegendVisible(value)

    showLegend = Property(bool, _getShowLegend, _setShowLegend)

    def _getShowDataPoints(self):
        """Get data points visibility"""
        return self._show_data_points

    def _setShowDataPoints(self, value: bool):
        """Set data points visibility"""
        self._show_data_points = value
        self.updateChart()

    showDataPoints = Property(bool, _getShowDataPoints, _setShowDataPoints)

    def _getFillArea(self):
        """Get fill area state"""
        return self._fill_area

    def _setFillArea(self, value: bool):
        """Set fill area state"""
        self._fill_area = value
        self.updateChart()

    fillArea = Property(bool, _getFillArea, _setFillArea)

    def _getEnableShadow(self):
        """Get shadow enabled state"""
        return self._enable_shadow

    def _setEnableShadow(self, value: bool):
        """Set shadow enabled state"""
        self._enable_shadow = value
        self.updateChart()

    enableShadow = Property(bool, _getEnableShadow, _setEnableShadow)

    def _getShadowBlur(self):
        """Get shadow blur radius"""
        return self._shadow_blur

    def _setShadowBlur(self, value: int):
        """Set shadow blur radius"""
        self._shadow_blur = value
        self.updateChart()

    shadowBlur = Property(int, _getShadowBlur, _setShadowBlur)

    def _getHighlightSize(self):
        """Get highlight size"""
        return self._highlight_size

    def _setHighlightSize(self, value: int):
        """Set highlight size"""
        self._highlight_size = value
        self.updateChart()

    highlightSize = Property(int, _getHighlightSize, _setHighlightSize)

    def _getMarkerSize(self):
        """Get default marker size"""
        return self._toolbar.getMarkerSize()

    def _setMarkerSize(self, value: float):
        """Set default marker size"""
        self._toolbar.setMarkerSize(value)
        self._data_manager.setAllMarkerSizes(value)
        self.updateChart()

    markerSize = Property(float, _getMarkerSize, _setMarkerSize)

    def _getShowFooter(self):
        """Get footer visibility"""
        return self._show_footer

    def _setShowFooter(self, value: bool):
        """Set footer visibility"""
        self._show_footer = value
        # Note: Footer would need to be implemented in QCustomChartBase

    showFooter = Property(bool, _getShowFooter, _setShowFooter)

    def _getDefaultLineStyle(self):
        """Default line style (int; see QCustomChartEnums.LineStyle)."""
        return chart_str_to_int(LINE_STYLE_TO_INT, self.LINE_SOLID)

    defaultLineStyle = Property(int, _getDefaultLineStyle)

    def _getDefaultMarkerStyle(self):
        """Default marker style (int; see QCustomChartEnums.MarkerStyle)."""
        return chart_str_to_int(MARKER_STYLE_TO_INT, self.MARKER_NONE)

    defaultMarkerStyle = Property(int, _getDefaultMarkerStyle)


class ChartDataProps:
    """Designer-authorable data entry for the QtCharts widgets.

    These charts exposed 27-37 styling properties to Qt Designer but no way to
    put anything *in* them: data arrived only through addSeries(), which is
    code-only. A form author could pick colours, legends and axis titles and
    still be left with an empty chart. This closes that, following the
    valuesCsv convention the painted charts already use.

        seriesCsv      "10,20,30"                    one unnamed series
                       "Revenue=10,20,30;Costs=5,8"  named series, ";" separated
        categoriesCsv  "Jan,Feb,Mar"                 x categories / slice labels

    Both round-trip, so Designer reads back what it wrote. Setting seriesCsv
    replaces the chart's contents rather than appending: a .ui file describes
    the whole chart, and re-applying a property on every load would otherwise
    stack duplicate series.

    Each chart implements _applyCsvSeries()/_applyCsvCategories(), because the
    underlying data shapes genuinely differ - x/y points for line and area,
    bare values plus categories for bar, (label, value) pairs for pie.
    """

    _CSV_SERIES_DEFAULT = ""
    _CSV_CATEGORIES_DEFAULT = ""

    # -- parsing helpers ------------------------------------------------ #
    @staticmethod
    def _parseCsvNumbers(chunk):
        out = []
        for token in str(chunk).split(","):
            token = token.strip()
            if not token:
                continue
            try:
                out.append(float(token))
            except ValueError:
                pass            # a stray label in a numeric column is skipped
        return out

    @classmethod
    def _parseSeriesCsv(cls, text):
        """-> [(name, [values]), ...]. Unnamed chunks get "Series N"."""
        series = []
        for index, chunk in enumerate(str(text).replace("|", ";").split(";")):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" in chunk:
                name, _, values = chunk.partition("=")
                name = name.strip() or "Series %d" % (len(series) + 1)
            else:
                name, values = "Series %d" % (len(series) + 1), chunk
            numbers = cls._parseCsvNumbers(values)
            if numbers:
                series.append((name, numbers))
        return series

    @staticmethod
    def _parseLabelsCsv(text):
        return [t.strip() for t in str(text).replace(";", ",").split(",")
                if t.strip()]

    @staticmethod
    def _formatSeriesCsv(series):
        return ";".join(
            "%s=%s" % (name, ",".join("%g" % v for v in values))
            for name, values in series)

    # -- Designer properties -------------------------------------------- #
    def _getSeriesCsv(self):
        return getattr(self, "_series_csv", self._CSV_SERIES_DEFAULT)

    def _setSeriesCsv(self, value):
        text = str(value)
        parsed = self._parseSeriesCsv(text)
        self._series_csv = self._formatSeriesCsv(parsed)
        try:
            self._applyCsvSeries(parsed)
        except Exception as exc:                  # never break form loading
            _logCsvFailure(self, "seriesCsv", exc)

    seriesCsv = Property(str, _getSeriesCsv, _setSeriesCsv)

    def _getCategoriesCsv(self):
        return getattr(self, "_categories_csv", self._CSV_CATEGORIES_DEFAULT)

    def _setCategoriesCsv(self, value):
        labels = self._parseLabelsCsv(value)
        self._categories_csv = ",".join(labels)
        try:
            self._applyCsvCategories(labels)
        except Exception as exc:
            _logCsvFailure(self, "categoriesCsv", exc)

    categoriesCsv = Property(str, _getCategoriesCsv, _setCategoriesCsv)

    # -- per-chart hooks ------------------------------------------------- #
    def _applyCsvSeries(self, series):
        raise NotImplementedError

    def _applyCsvCategories(self, labels):
        """Charts without categories ignore them rather than erroring."""
        return None


def _logCsvFailure(widget, prop, exc):
    """A malformed property in a .ui must not abort loading the form."""
    try:
        from Custom_Widgets.Log import logException
        logException(exc, message="%s: %s could not be applied"
                                  % (type(widget).__name__, prop))
    except Exception:
        pass
