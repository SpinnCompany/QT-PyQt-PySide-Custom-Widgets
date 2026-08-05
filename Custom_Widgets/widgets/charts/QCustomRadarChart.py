########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomRadarChart - a painted radar / spider chart.
##
## N axes radiating from a centre, one filled polygon per series. Used to
## compare several entities across the same set of measures - the shape of the
## polygon is the comparison, which no cartesian chart gives you.
##
## This is the catalog's first polar chart of any kind. Rendered entirely with
## QPainter and NO QtCharts: Qt Charts is GPLv3-or-commercial with no LGPL
## option, so anything built on it cannot ship inside a proprietary wheel (see
## docs/design/mui-charts-gap.md). A test asserts the import graph stays clean.
##
## Data goes in with setAxes([...]) + addSeries(name, values) in code, or the
## axesCsv / seriesCsv properties in Qt Designer, following the same convention
## as the other charts:
##
##     axesCsv    = "Speed,Power,Range,Agility"
##     seriesCsv  = "Alpha=80,60,90,70;Beta=60,90,50,80"
##
## Emits seriesHovered(int) and axisClicked(int); -1 means "nothing".
########################################################################
import math

from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QPolygonF, QFontMetrics)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomRadarChart(QWidget):
    seriesHovered = Signal(int)
    axisClicked = Signal(int)

    WIDGET_ICON = "components/icons/radar.png"
    WIDGET_TOOLTIP = "A painted radar / spider chart"
    WIDGET_MODULE = "Custom_Widgets.QCustomRadarChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRadarChart' name='customRadarChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>300</height></rect></property>
            <property name='axesCsv'><string>Speed,Power,Range,Agility,Cost</string></property>
            <property name='seriesCsv'><string>Alpha=80,60,90,70,50</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRadarChart",
        "props": {"axesCsv": {"type": "string", "default": ""},
                  "seriesCsv": {"type": "string", "default": ""},
                  "seriesColorsCsv": {"type": "string", "default": ""},
                  "maxValue": {"type": "float", "default": 0.0},
                  "rings": {"type": "int", "default": 4},
                  "gridStyle": {"type": "enum", "values": ["polygon", "circle"],
                                "default": "polygon"},
                  "startAngle": {"type": "int", "default": 90},
                  "fillOpacity": {"type": "float", "default": 0.25},
                  "lineWidth": {"type": "float", "default": 2.0},
                  "showAxisLabels": {"type": "bool", "default": True},
                  "showRingLabels": {"type": "bool", "default": False},
                  "showMarkers": {"type": "bool", "default": True},
                  "showLegend": {"type": "bool", "default": True},
                  "gridColor": {"type": "color", "default": "#e2e8f0"},
                  "axisColor": {"type": "color", "default": "#cbd5e1"},
                  "labelColor": {"type": "color", "default": "#0f172a"}},
        "signals": ["seriesHovered", "axisClicked"],
        "tokens_used": ["accent", "outline", "on-surface", "surface-muted"],
    }

    _DEFAULT_COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed",
                       "#0891b2"]
    _LEGEND_SWATCH = 10

    def __init__(self, parent=None, axes=None, series=None):
        super().__init__(parent)
        self.setObjectName("QCustomRadarChart")
        self._axes = []             # axis labels
        self._series = []           # list of (name, [values])
        self._colors = []           # explicit per-series colours
        self._maxValue = 0.0        # 0 = derive from the data
        self._rings = 4
        self._gridStyle = "polygon"
        self._startAngle = 90       # degrees, counter-clockwise from +x
        self._fillOpacity = 0.25
        self._lineWidth = 2.0
        self._showAxisLabels = True
        self._showRingLabels = False
        self._showMarkers = True
        self._showLegend = True
        self._hover = -1

        self._gridColor = QColor("#e2e8f0")
        self._axisColor = QColor("#cbd5e1")
        self._labelColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        if axes:
            self.setAxes(axes)
        for name, values in (series or []):
            self.addSeries(name, values)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    def setAxes(self, labels):
        """Replace the axis labels. Existing series are re-fitted to the new
        count so a shortened axis list cannot leave a series over-long."""
        self._axes = [str(x) for x in (labels or [])]
        self._series = [(name, self._fit(values)) for name, values in self._series]
        self.update()

    def axes(self):
        return list(self._axes)

    def axisCount(self):
        return len(self._axes)

    def _fit(self, values):
        """Pad with zeros / truncate so a series matches the axis count."""
        count = len(self._axes)
        values = [float(v) for v in values][:count]
        return values + [0.0] * (count - len(values))

    def addSeries(self, name, values, color=None):
        self._series.append((str(name), self._fit(values)))
        if color is not None:
            while len(self._colors) < len(self._series) - 1:
                self._colors.append(None)
            self._colors.append(QColor(color))
        self.update()
        return len(self._series) - 1

    def setSeries(self, series):
        """Replace every series. Each item is (name, values)."""
        self._series = []
        for item in series or []:
            if isinstance(item, dict):
                self._series.append((str(item.get("name", "")),
                                     self._fit(item.get("values", []))))
            elif isinstance(item, (tuple, list)) and len(item) >= 2:
                self._series.append((str(item[0]), self._fit(item[1])))
        self.update()

    def series(self):
        return [(name, list(values)) for name, values in self._series]

    def seriesCount(self):
        return len(self._series)

    def removeSeries(self, index):
        if 0 <= index < len(self._series):
            del self._series[index]
            if index < len(self._colors):
                del self._colors[index]
            self._hover = -1
            self.update()
            return True
        return False

    def clearSeries(self):
        self._series = []
        self._colors = []
        self._hover = -1
        self.update()

    def seriesColor(self, index):
        if 0 <= index < len(self._colors) and self._colors[index] is not None:
            return QColor(self._colors[index])
        if not self._DEFAULT_COLORS:
            return QColor("#2563eb")
        return QColor(self._DEFAULT_COLORS[index % len(self._DEFAULT_COLORS)])

    def maximum(self):
        """The value the outermost ring represents."""
        if self._maxValue > 0:
            return self._maxValue
        peak = 0.0
        for _name, values in self._series:
            for v in values:
                peak = max(peak, v)
        return peak or 1.0

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(320, 300)

    def minimumSizeHint(self):
        return QSize(120, 120)

    def _legendHeight(self):
        if not (self._showLegend and self._series):
            return 0.0
        return QFontMetrics(self.font()).height() + 10

    def _plotRect(self):
        pad = 8.0
        bottom = self._legendHeight()
        if self._showAxisLabels and self._axes:
            pad += QFontMetrics(self.font()).height() + 6
        side = min(self.width() - 2 * pad, self.height() - 2 * pad - bottom)
        side = max(10.0, side)
        return QRectF((self.width() - side) / 2.0,
                      (self.height() - bottom - side) / 2.0, side, side)

    def _angleFor(self, index):
        """Radians for axis `index`, running clockwise from startAngle."""
        count = max(1, len(self._axes))
        return math.radians(self._startAngle) - index * (2 * math.pi / count)

    def _pointAt(self, index, fraction):
        """Cartesian point `fraction` (0..1) of the way along an axis."""
        rect = self._plotRect()
        radius = rect.width() / 2.0 * max(0.0, min(1.0, fraction))
        angle = self._angleFor(index)
        return QPointF(rect.center().x() + radius * math.cos(angle),
                       rect.center().y() - radius * math.sin(angle))

    def _ringLabelPoint(self, fraction):
        """Where a ring's value label sits.

        On the bisector between the first two axes, not along axis 0: an axis
        already carries its own label at the rim, and the outermost ring label
        collided with it.
        """
        rect = self._plotRect()
        count = max(1, len(self._axes))
        angle = self._angleFor(0) - (math.pi / count)
        radius = rect.width() / 2.0 * max(0.0, min(1.0, fraction))
        return QPointF(rect.center().x() + radius * math.cos(angle),
                       rect.center().y() - radius * math.sin(angle))

    def _polygonFor(self, values):
        peak = self.maximum()
        poly = QPolygonF()
        for i, value in enumerate(values):
            poly.append(self._pointAt(i, value / peak if peak else 0.0))
        return poly

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        if not self._axes:
            return

        self._paintGrid(p)
        self._paintAxes(p)
        for index, (_name, values) in enumerate(self._series):
            self._paintSeries(p, index, values)
        if self._showAxisLabels:
            self._paintAxisLabels(p)
        if self._showLegend and self._series:
            self._paintLegend(p)

    def _paintGrid(self, p):
        rect = self._plotRect()
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(self._gridColor, 1))
        for ring in range(1, max(1, self._rings) + 1):
            fraction = ring / float(max(1, self._rings))
            if self._gridStyle == "circle":
                radius = rect.width() / 2.0 * fraction
                p.drawEllipse(rect.center(), radius, radius)
            else:
                poly = QPolygonF([self._pointAt(i, fraction)
                                  for i in range(len(self._axes))])
                p.drawPolygon(poly)
            if self._showRingLabels:
                value = self.maximum() * fraction
                point = self._ringLabelPoint(fraction)
                p.setPen(QPen(self._labelColor))
                p.drawText(QPointF(point.x() + 3, point.y() - 2), "%g" % value)
                p.setPen(QPen(self._gridColor, 1))

    def _paintAxes(self, p):
        p.setPen(QPen(self._axisColor, 1))
        for i in range(len(self._axes)):
            p.drawLine(self._plotRect().center(), self._pointAt(i, 1.0))

    def _paintSeries(self, p, index, values):
        colour = self.seriesColor(index)
        hovered = index == self._hover
        # A hovered series is drawn more opaque rather than moved, so the
        # shapes stay comparable while one is emphasised.
        fill = QColor(colour)
        opacity = self._fillOpacity * (1.9 if hovered else 1.0)
        fill.setAlphaF(max(0.0, min(1.0, opacity)))
        poly = self._polygonFor(values)

        p.setBrush(QBrush(fill))
        p.setPen(QPen(colour, self._lineWidth + (1.0 if hovered else 0.0)))
        p.drawPolygon(poly)

        if self._showMarkers:
            p.setBrush(QBrush(colour))
            p.setPen(Qt.NoPen)
            radius = 3.0 + (1.0 if hovered else 0.0)
            for point in poly:
                p.drawEllipse(point, radius, radius)

    def _paintAxisLabels(self, p):
        fm = QFontMetrics(self.font())
        p.setPen(QPen(self._labelColor))
        for i, label in enumerate(self._axes):
            anchor = self._pointAt(i, 1.08)
            width = fm.horizontalAdvance(label)
            height = fm.height()
            # Nudge the box so a label never overlaps its own axis tip: left of
            # centre reads right-aligned, right of centre left-aligned.
            centre = self._plotRect().center()
            if anchor.x() < centre.x() - 1:
                x = anchor.x() - width
            elif anchor.x() > centre.x() + 1:
                x = anchor.x()
            else:
                x = anchor.x() - width / 2.0
            y = anchor.y() - height / 2.0
            p.drawText(QRectF(x, y, width, height),
                       int(Qt.AlignCenter), label)

    def _paintLegend(self, p):
        fm = QFontMetrics(self.font())
        swatch = self._LEGEND_SWATCH
        gap = 14.0
        widths = [swatch + 5 + fm.horizontalAdvance(name)
                  for name, _v in self._series]
        total = sum(widths) + gap * (len(widths) - 1)
        x = (self.width() - total) / 2.0
        y = self.height() - self._legendHeight() + 4

        for index, (name, _values) in enumerate(self._series):
            colour = self.seriesColor(index)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(colour))
            p.drawEllipse(QRectF(x, y + (fm.height() - swatch) / 2.0,
                                 swatch, swatch))
            p.setPen(QPen(self._labelColor))
            p.drawText(QRectF(x + swatch + 5, y, widths[index], fm.height()),
                       int(Qt.AlignLeft | Qt.AlignVCenter), name)
            x += widths[index] + gap

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def seriesAt(self, pos):
        """Index of the series whose polygon contains a point, or -1.

        Later series are checked first so the one painted on top wins, which
        is what the user sees.
        """
        point = QPointF(pos)
        for index in range(len(self._series) - 1, -1, -1):
            if self._polygonFor(self._series[index][1]).containsPoint(
                    point, Qt.OddEvenFill):
                return index
        return -1

    def axisAt(self, pos):
        """Index of the nearest axis to a point, or -1 when outside the plot."""
        if not self._axes:
            return -1
        rect = self._plotRect()
        centre = rect.center()
        dx, dy = QPointF(pos).x() - centre.x(), QPointF(pos).y() - centre.y()
        distance = math.hypot(dx, dy)
        if distance > rect.width() / 2.0 or distance < 1e-6:
            return -1
        angle = math.atan2(-dy, dx)
        step = 2 * math.pi / len(self._axes)
        offset = (math.radians(self._startAngle) - angle) % (2 * math.pi)
        return int(round(offset / step)) % len(self._axes)

    def mouseMoveEvent(self, e):
        index = self.seriesAt(e.pos())
        if index != self._hover:
            self._hover = index
            self.seriesHovered.emit(index)
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover != -1:
            self._hover = -1
            self.seriesHovered.emit(-1)
            self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            index = self.axisAt(e.pos())
            if index >= 0:
                self.axisClicked.emit(index)
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def axesCsv(self):
        return ",".join(self._axes)

    @axesCsv.setter
    def axesCsv(self, text):
        self.setAxes([t.strip() for t in str(text).replace(";", ",").split(",")
                      if t.strip()])

    @Property(str)
    def seriesCsv(self):
        return ";".join("%s=%s" % (name, ",".join("%g" % v for v in values))
                        for name, values in self._series)

    @seriesCsv.setter
    def seriesCsv(self, text):
        parsed = []
        for index, chunk in enumerate(str(text).replace("|", ";").split(";")):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" in chunk:
                name, _, raw = chunk.partition("=")
                name = name.strip() or "Series %d" % (len(parsed) + 1)
            else:
                name, raw = "Series %d" % (len(parsed) + 1), chunk
            values = []
            for token in raw.split(","):
                token = token.strip()
                if not token:
                    continue
                try:
                    values.append(float(token))
                except ValueError:
                    pass
            if values:
                parsed.append((name, values))
        self.setSeries(parsed)

    @Property(str)
    def seriesColorsCsv(self):
        return ",".join(c.name() if c is not None else "" for c in self._colors)

    @seriesColorsCsv.setter
    def seriesColorsCsv(self, text):
        colors = []
        for token in str(text).replace(";", ",").split(","):
            token = token.strip()
            colour = QColor(token) if token else QColor()
            colors.append(colour if colour.isValid() else None)
        self._colors = colors
        self.update()

    @Property(float)
    def maxValue(self):
        return self._maxValue

    @maxValue.setter
    def maxValue(self, value):
        self._maxValue = max(0.0, float(value))
        self.update()

    @Property(int)
    def rings(self):
        return self._rings

    @rings.setter
    def rings(self, value):
        self._rings = max(1, int(value))
        self.update()

    @Property(str)
    def gridStyle(self):
        return self._gridStyle

    @gridStyle.setter
    def gridStyle(self, value):
        self._gridStyle = "circle" if str(value) == "circle" else "polygon"
        self.update()

    @Property(int)
    def startAngle(self):
        return self._startAngle

    @startAngle.setter
    def startAngle(self, value):
        self._startAngle = int(value) % 360
        self.update()

    @Property(float)
    def fillOpacity(self):
        return self._fillOpacity

    @fillOpacity.setter
    def fillOpacity(self, value):
        self._fillOpacity = max(0.0, min(1.0, float(value)))
        self.update()

    @Property(float)
    def lineWidth(self):
        return self._lineWidth

    @lineWidth.setter
    def lineWidth(self, value):
        self._lineWidth = max(0.0, float(value))
        self.update()

    @Property(bool)
    def showAxisLabels(self):
        return self._showAxisLabels

    @showAxisLabels.setter
    def showAxisLabels(self, value):
        self._showAxisLabels = bool(value)
        self.update()

    @Property(bool)
    def showRingLabels(self):
        return self._showRingLabels

    @showRingLabels.setter
    def showRingLabels(self, value):
        self._showRingLabels = bool(value)
        self.update()

    @Property(bool)
    def showMarkers(self):
        return self._showMarkers

    @showMarkers.setter
    def showMarkers(self, value):
        self._showMarkers = bool(value)
        self.update()

    @Property(bool)
    def showLegend(self):
        return self._showLegend

    @showLegend.setter
    def showLegend(self, value):
        self._showLegend = bool(value)
        self.updateGeometry()
        self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def gridColor(self):
        return self._gridColor

    @gridColor.setter
    def gridColor(self, c):
        self._gridColor = QColor(c); self.update()

    @Property(QColor)
    def axisColor(self):
        return self._axisColor

    @axisColor.setter
    def axisColor(self, c):
        self._axisColor = QColor(c); self.update()

    @Property(QColor)
    def labelColor(self):
        return self._labelColor

    @labelColor.setter
    def labelColor(self, c):
        self._labelColor = QColor(c); self.update()
