########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomRadialLines - a painted polar line chart.
##
## A line chart wrapped onto a circle: the x axis is angular, so the series
## closes back on itself. The right form for cyclical data - hours of a day,
## months of a year, compass bearings - where a cartesian line chart puts an
## artificial break between the last point and the first.
##
## Distinct from QCustomRadarChart: radar compares a handful of NAMED axes as
## a shape; this plots a continuous series around a circle and does not label
## every sample.
##
## QPainter only, NO QtCharts (see docs/design/mui-charts-gap.md). Angles come
## from the shared _chart_axis polar helpers so it winds the same way as the
## other radial charts.
##
## Data goes in with addSeries(name, values) in code, or seriesCsv in Qt
## Designer:
##
##     seriesCsv = "Weekday=30,45,60,52,48,70,64;Weekend=20,25,40,38,30,35,28"
##
## Emits seriesHovered(int) and pointClicked(int, int); -1 means "nothing".
########################################################################
import math

from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QPolygonF, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy

from ._chart_axis import polarAngle, polarPoint


class QCustomRadialLines(QWidget):
    seriesHovered = Signal(int)
    pointClicked = Signal(int, int)

    WIDGET_ICON = "components/icons/track_changes.png"
    WIDGET_TOOLTIP = "A painted polar line chart for cyclical data"
    WIDGET_MODULE = "Custom_Widgets.QCustomRadialLines"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRadialLines' name='customRadialLines'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>300</width><height>300</height></rect></property>
            <property name='seriesCsv'><string>Weekday=30,45,60,52,48,70,64</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRadialLines",
        "props": {"seriesCsv": {"type": "string", "default": ""},
                  "labelsCsv": {"type": "string", "default": ""},
                  "colorsCsv": {"type": "string", "default": ""},
                  "maxValue": {"type": "float", "default": 0.0},
                  "startAngle": {"type": "int", "default": 90},
                  "clockwise": {"type": "bool", "default": True},
                  "rings": {"type": "int", "default": 4},
                  "lineWidth": {"type": "float", "default": 2.0},
                  "fillOpacity": {"type": "float", "default": 0.15},
                  "closed": {"type": "bool", "default": True},
                  "smooth": {"type": "bool", "default": False},
                  "showGrid": {"type": "bool", "default": True},
                  "showMarkers": {"type": "bool", "default": False},
                  "showLabels": {"type": "bool", "default": True},
                  "showLegend": {"type": "bool", "default": True},
                  "gridColor": {"type": "color", "default": "#e2e8f0"},
                  "labelColor": {"type": "color", "default": "#64748b"}},
        "signals": ["seriesHovered", "pointClicked"],
        "tokens_used": ["accent", "surface-muted", "on-surface"],
    }

    _DEFAULT_COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed",
                       "#0891b2"]

    def __init__(self, parent=None, series=None, labels=None):
        super().__init__(parent)
        self.setObjectName("QCustomRadialLines")
        self._series = []           # list of (name, [values])
        self._labels = []
        self._colors = []
        self._maxValue = 0.0
        self._startAngle = 90
        self._clockwise = True
        self._rings = 4
        self._lineWidth = 2.0
        self._fillOpacity = 0.15
        self._closed = True
        self._smooth = False
        self._showGrid = True
        self._showMarkers = False
        self._showLabels = True
        self._showLegend = True
        self._hover = -1

        self._gridColor = QColor("#e2e8f0")
        self._labelColor = QColor("#64748b")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        if labels:
            self._labels = [str(x) for x in labels]
        for name, values in (series or []):
            self.addSeries(name, values)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    def addSeries(self, name, values, color=None):
        cleaned = []
        for value in values or []:
            try:
                cleaned.append(float(value))
            except (TypeError, ValueError):
                continue
        self._series.append((str(name), cleaned))
        if color is not None:
            while len(self._colors) < len(self._series) - 1:
                self._colors.append(None)
            self._colors.append(QColor(color))
        self.update()
        return len(self._series) - 1

    def setSeries(self, series):
        self._series = []
        for item in series or []:
            if isinstance(item, dict):
                self.addSeries(item.get("name", ""), item.get("values", []))
            elif isinstance(item, (tuple, list)) and len(item) >= 2:
                self.addSeries(item[0], item[1])
        self.update()

    def series(self):
        return [(name, list(values)) for name, values in self._series]

    def seriesCount(self):
        return len(self._series)

    def clearSeries(self):
        self._series = []
        self._colors = []
        self._hover = -1
        self.update()

    def setLabels(self, labels):
        self._labels = [str(x) for x in (labels or [])]
        self.update()

    def labels(self):
        return list(self._labels)

    def sampleCount(self):
        """Samples around the circle — the longest series wins."""
        return max((len(v) for _n, v in self._series), default=0)

    def seriesColor(self, index):
        if 0 <= index < len(self._colors) and self._colors[index] is not None:
            return QColor(self._colors[index])
        return QColor(self._DEFAULT_COLORS[index % len(self._DEFAULT_COLORS)])

    def maximum(self):
        if self._maxValue > 0:
            return self._maxValue
        peak = max((v for _n, values in self._series for v in values), default=0.0)
        return peak or 1.0

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(300, 300)

    def minimumSizeHint(self):
        return QSize(110, 110)

    def _legendHeight(self):
        if not (self._showLegend and self._series):
            return 0.0
        return QFontMetrics(self.font()).height() + 8

    def _plotRect(self):
        pad = 10.0
        if self._showLabels and self._labels:
            pad += QFontMetrics(self.font()).height() + 4
        bottom = self._legendHeight()
        side = max(10.0, min(self.width() - 2 * pad,
                             self.height() - 2 * pad - bottom))
        return QRectF((self.width() - side) / 2.0,
                      (self.height() - bottom - side) / 2.0, side, side)

    def _angleFor(self, index):
        return polarAngle(index, max(1, self.sampleCount()),
                          self._startAngle, self._clockwise)

    def pointFor(self, seriesIndex, sampleIndex):
        """Widget-space point for one sample of one series."""
        rect = self._plotRect()
        values = self._series[seriesIndex][1]
        if not values:
            return QPointF(rect.center())
        value = values[sampleIndex % len(values)]
        radius = rect.width() / 2.0 * max(0.0, min(1.0, value / self.maximum()))
        x, y = polarPoint(rect.center().x(), rect.center().y(), radius,
                          self._angleFor(sampleIndex))
        return QPointF(x, y)

    def _polygonFor(self, seriesIndex):
        values = self._series[seriesIndex][1]
        return QPolygonF([self.pointFor(seriesIndex, i)
                          for i in range(len(values))])

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        if not self._series or not self.sampleCount():
            return

        if self._showGrid:
            self._paintGrid(p)
        for index in range(len(self._series)):
            self._paintSeries(p, index)
        if self._showLabels and self._labels:
            self._paintLabels(p)
        if self._showLegend:
            self._paintLegend(p)

    def _paintGrid(self, p):
        rect = self._plotRect()
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(self._gridColor, 1))
        for ring in range(1, max(1, self._rings) + 1):
            radius = rect.width() / 2.0 * ring / float(max(1, self._rings))
            p.drawEllipse(rect.center(), radius, radius)
        # spokes only where a label exists, so a 60-sample series does not
        # bury the data under 60 grid lines
        count = len(self._labels) if self._labels else min(self.sampleCount(), 12)
        for i in range(count):
            step = max(1, self.sampleCount() // max(1, count))
            angle = self._angleFor(i * step)
            x, y = polarPoint(rect.center().x(), rect.center().y(),
                              rect.width() / 2.0, angle)
            p.drawLine(rect.center(), QPointF(x, y))

    def _paintSeries(self, p, index):
        colour = self.seriesColor(index)
        hovered = index == self._hover
        poly = self._polygonFor(index)
        if poly.count() < 2:
            return

        if self._fillOpacity > 0 and self._closed:
            fill = QColor(colour)
            fill.setAlphaF(max(0.0, min(1.0, self._fillOpacity *
                                        (1.8 if hovered else 1.0))))
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(fill))
            p.drawPolygon(poly)

        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(colour, self._lineWidth + (1.0 if hovered else 0.0)))
        if self._closed:
            p.drawPolygon(poly)
        else:
            p.drawPolyline(poly)

        if self._showMarkers:
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(colour))
            radius = 3.0 + (1.0 if hovered else 0.0)
            for point in poly:
                p.drawEllipse(point, radius, radius)

    def _paintLabels(self, p):
        rect = self._plotRect()
        fm = QFontMetrics(self.font())
        p.setPen(QPen(self._labelColor))
        count = self.sampleCount()
        for i, label in enumerate(self._labels[:count]):
            step = max(1, count // max(1, len(self._labels)))
            angle = self._angleFor(i * step)
            x, y = polarPoint(rect.center().x(), rect.center().y(),
                              rect.width() / 2.0 + 6, angle)
            width = fm.horizontalAdvance(label)
            if x < rect.center().x() - 1:
                x -= width
            elif abs(x - rect.center().x()) <= 1:
                x -= width / 2.0
            p.drawText(QRectF(x, y - fm.height() / 2.0, width, fm.height()),
                       int(Qt.AlignCenter), label)

    def _paintLegend(self, p):
        fm = QFontMetrics(self.font())
        swatch, gap = 9.0, 14.0
        widths = [swatch + 5 + fm.horizontalAdvance(name)
                  for name, _v in self._series]
        x = (self.width() - (sum(widths) + gap * (len(widths) - 1))) / 2.0
        y = self.height() - self._legendHeight() + 2
        for index, (name, _values) in enumerate(self._series):
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self.seriesColor(index)))
            p.drawEllipse(QRectF(x, y + (fm.height() - swatch) / 2.0,
                                 swatch, swatch))
            p.setPen(QPen(self._labelColor))
            p.drawText(QRectF(x + swatch + 5, y, widths[index], fm.height()),
                       int(Qt.AlignLeft | Qt.AlignVCenter), name)
            x += widths[index] + gap

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def sampleAt(self, pos):
        """(series, sample) nearest a point, or (-1, -1)."""
        point = QPointF(pos)
        best, bestDistance = (-1, -1), None
        for si in range(len(self._series) - 1, -1, -1):
            for i in range(len(self._series[si][1])):
                mapped = self.pointFor(si, i)
                distance = math.hypot(point.x() - mapped.x(),
                                      point.y() - mapped.y())
                if distance <= 10.0 and (bestDistance is None or distance < bestDistance):
                    best, bestDistance = (si, i), distance
        return best

    def seriesAt(self, pos):
        """Index of the series whose closed shape contains a point, else -1."""
        point = QPointF(pos)
        for index in range(len(self._series) - 1, -1, -1):
            poly = self._polygonFor(index)
            if poly.count() >= 3 and poly.containsPoint(point, Qt.OddEvenFill):
                return index
        return -1

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
            si, i = self.sampleAt(e.pos())
            if si >= 0:
                self.pointClicked.emit(si, i)
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def seriesCsv(self):
        return ";".join("%s=%s" % (name, ",".join("%g" % v for v in values))
                        for name, values in self._series)

    @seriesCsv.setter
    def seriesCsv(self, text):
        parsed = []
        for chunk in str(text).replace("|", ";").split(";"):
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
    def labelsCsv(self):
        return ",".join(self._labels)

    @labelsCsv.setter
    def labelsCsv(self, text):
        self.setLabels([t.strip() for t in str(text).replace(";", ",").split(",")
                        if t.strip()])

    @Property(str)
    def colorsCsv(self):
        return ",".join(c.name() if c is not None else "" for c in self._colors)

    @colorsCsv.setter
    def colorsCsv(self, text):
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
        self._maxValue = max(0.0, float(value)); self.update()

    @Property(int)
    def startAngle(self):
        return self._startAngle

    @startAngle.setter
    def startAngle(self, value):
        self._startAngle = int(value) % 360; self.update()

    @Property(bool)
    def clockwise(self):
        return self._clockwise

    @clockwise.setter
    def clockwise(self, value):
        self._clockwise = bool(value); self.update()

    @Property(int)
    def rings(self):
        return self._rings

    @rings.setter
    def rings(self, value):
        self._rings = max(1, int(value)); self.update()

    @Property(float)
    def lineWidth(self):
        return self._lineWidth

    @lineWidth.setter
    def lineWidth(self, value):
        self._lineWidth = max(0.0, float(value)); self.update()

    @Property(float)
    def fillOpacity(self):
        return self._fillOpacity

    @fillOpacity.setter
    def fillOpacity(self, value):
        self._fillOpacity = max(0.0, min(1.0, float(value))); self.update()

    @Property(bool)
    def closed(self):
        return self._closed

    @closed.setter
    def closed(self, value):
        self._closed = bool(value); self.update()

    @Property(bool)
    def smooth(self):
        return self._smooth

    @smooth.setter
    def smooth(self, value):
        self._smooth = bool(value); self.update()

    @Property(bool)
    def showGrid(self):
        return self._showGrid

    @showGrid.setter
    def showGrid(self, value):
        self._showGrid = bool(value); self.update()

    @Property(bool)
    def showMarkers(self):
        return self._showMarkers

    @showMarkers.setter
    def showMarkers(self, value):
        self._showMarkers = bool(value); self.update()

    @Property(bool)
    def showLabels(self):
        return self._showLabels

    @showLabels.setter
    def showLabels(self, value):
        self._showLabels = bool(value); self.updateGeometry(); self.update()

    @Property(bool)
    def showLegend(self):
        return self._showLegend

    @showLegend.setter
    def showLegend(self, value):
        self._showLegend = bool(value); self.updateGeometry(); self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def gridColor(self):
        return self._gridColor

    @gridColor.setter
    def gridColor(self, c):
        self._gridColor = QColor(c); self.update()

    @Property(QColor)
    def labelColor(self):
        return self._labelColor

    @labelColor.setter
    def labelColor(self, c):
        self._labelColor = QColor(c); self.update()
