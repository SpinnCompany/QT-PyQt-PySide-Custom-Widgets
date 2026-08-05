########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomScatterChart - a painted x/y scatter plot.
##
## Points in a cartesian plane, one colour per series, optionally sized by a
## third value (a bubble plot). The most conspicuous absence for a general
## chart library: nothing in the catalog plotted two continuous variables
## against each other.
##
## QPainter only, NO QtCharts - Qt Charts is GPLv3-or-commercial with no LGPL
## option, so anything built on it cannot ship in a proprietary wheel (see
## docs/design/mui-charts-gap.md).
##
## Axis ticks come from _chart_axis, shared with the other cartesian charts so
## they agree about where round numbers fall.
##
## Data goes in with addSeries(name, points) in code, or pointsCsv in Qt
## Designer:
##
##     pointsCsv = "Alpha=1,2;2,4;3,9|Beta=1,5;2,3"
##                  name   x,y pairs separated by ";", series by "|"
##
## Emits pointHovered(int, int) and pointClicked(int, int) - series index and
## point index, or (-1, -1) for nothing.
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy

from ._chart_axis import formatTick, niceTicks, tickValues


class QCustomScatterChart(QWidget):
    pointHovered = Signal(int, int)
    pointClicked = Signal(int, int)

    WIDGET_ICON = "components/icons/scatter_plot.png"
    WIDGET_TOOLTIP = "A painted x/y scatter plot"
    WIDGET_MODULE = "Custom_Widgets.QCustomScatterChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomScatterChart' name='customScatterChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>420</width><height>300</height></rect></property>
            <property name='pointsCsv'><string>Alpha=1,2;2,4;3,9;4,7</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomScatterChart",
        "props": {"pointsCsv": {"type": "string", "default": ""},
                  "seriesColorsCsv": {"type": "string", "default": ""},
                  "xAxisTitle": {"type": "string", "default": ""},
                  "yAxisTitle": {"type": "string", "default": ""},
                  "markerSize": {"type": "float", "default": 7.0},
                  "markerShape": {"type": "enum",
                                  "values": ["circle", "square", "diamond", "triangle"],
                                  "default": "circle"},
                  "markerOpacity": {"type": "float", "default": 0.85},
                  "tickCount": {"type": "int", "default": 5},
                  "showGrid": {"type": "bool", "default": True},
                  "showAxes": {"type": "bool", "default": True},
                  "showLegend": {"type": "bool", "default": True},
                  "showTooltip": {"type": "bool", "default": True},
                  "gridColor": {"type": "color", "default": "#e2e8f0"},
                  "axisColor": {"type": "color", "default": "#cbd5e1"},
                  "labelColor": {"type": "color", "default": "#64748b"}},
        "signals": ["pointHovered", "pointClicked"],
        "tokens_used": ["accent", "outline", "on-surface", "surface-muted"],
    }

    _DEFAULT_COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed",
                       "#0891b2"]
    _PAD = 10.0

    def __init__(self, parent=None, series=None):
        super().__init__(parent)
        self.setObjectName("QCustomScatterChart")
        self._series = []           # list of (name, [(x, y, size|None), ...])
        self._colors = []
        self._xTitle = ""
        self._yTitle = ""
        self._markerSize = 7.0
        self._markerShape = "circle"
        self._markerOpacity = 0.85
        self._tickCount = 5
        self._showGrid = True
        self._showAxes = True
        self._showLegend = True
        self._showTooltip = True
        self._hover = (-1, -1)

        self._gridColor = QColor("#e2e8f0")
        self._axisColor = QColor("#cbd5e1")
        self._labelColor = QColor("#64748b")
        self._tooltipBg = QColor("#0f172a")
        self._tooltipText = QColor("#f8fafc")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        for name, points in (series or []):
            self.addSeries(name, points)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coercePoint(point):
        """(x, y) or (x, y, size); returns (x, y, size|None) or None."""
        if isinstance(point, dict):
            values = (point.get("x"), point.get("y"), point.get("size"))
        else:
            try:
                values = tuple(point)
            except TypeError:
                return None
        if len(values) < 2:
            return None
        try:
            x, y = float(values[0]), float(values[1])
        except (TypeError, ValueError):
            return None
        size = None
        if len(values) > 2 and values[2] is not None:
            try:
                size = max(0.0, float(values[2]))
            except (TypeError, ValueError):
                size = None
        return (x, y, size)

    def addSeries(self, name, points, color=None):
        cleaned = [p for p in (self._coercePoint(pt) for pt in (points or [])) if p]
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
                self.addSeries(item.get("name", ""), item.get("points", []))
            elif isinstance(item, (tuple, list)) and len(item) >= 2:
                self.addSeries(item[0], item[1])
        self.update()

    def series(self):
        return [(name, list(points)) for name, points in self._series]

    def seriesCount(self):
        return len(self._series)

    def pointCount(self):
        return sum(len(points) for _name, points in self._series)

    def clearSeries(self):
        self._series = []
        self._colors = []
        self._hover = (-1, -1)
        self.update()

    def removeSeries(self, index):
        if 0 <= index < len(self._series):
            del self._series[index]
            if index < len(self._colors):
                del self._colors[index]
            self._hover = (-1, -1)
            self.update()
            return True
        return False

    def seriesColor(self, index):
        if 0 <= index < len(self._colors) and self._colors[index] is not None:
            return QColor(self._colors[index])
        return QColor(self._DEFAULT_COLORS[index % len(self._DEFAULT_COLORS)])

    def dataBounds(self):
        """(xmin, xmax, ymin, ymax) across every series."""
        xs = [p[0] for _n, pts in self._series for p in pts]
        ys = [p[1] for _n, pts in self._series for p in pts]
        if not xs:
            return (0.0, 1.0, 0.0, 1.0)
        return (min(xs), max(xs), min(ys), max(ys))

    def xRange(self):
        xmin, xmax, _ymin, _ymax = self.dataBounds()
        start, stop, _step = niceTicks(xmin, xmax, self._tickCount)
        return (start, stop)

    def yRange(self):
        _xmin, _xmax, ymin, ymax = self.dataBounds()
        start, stop, _step = niceTicks(ymin, ymax, self._tickCount)
        return (start, stop)

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(420, 300)

    def minimumSizeHint(self):
        return QSize(140, 110)

    def _legendHeight(self):
        if not (self._showLegend and self._series):
            return 0.0
        return QFontMetrics(self.font()).height() + 8

    def _plotRect(self):
        fm = QFontMetrics(self.font())
        left = self._PAD
        bottom = self._PAD + self._legendHeight()
        if self._showAxes:
            ylo, yhi = self.yRange()
            _s, _e, step = niceTicks(*self.dataBounds()[2:], count=self._tickCount)
            widest = max(fm.horizontalAdvance(formatTick(v, step))
                         for v in (ylo, yhi))
            left += widest + 8
            bottom += fm.height() + 4
        if self._yTitle:
            left += fm.height() + 2
        if self._xTitle:
            bottom += fm.height() + 2
        return QRectF(left, self._PAD,
                      max(1.0, self.width() - left - self._PAD),
                      max(1.0, self.height() - self._PAD - bottom))

    def mapPoint(self, x, y):
        """Data coordinates -> widget coordinates."""
        rect = self._plotRect()
        xlo, xhi = self.xRange()
        ylo, yhi = self.yRange()
        xspan = (xhi - xlo) or 1.0
        yspan = (yhi - ylo) or 1.0
        return QPointF(rect.left() + (x - xlo) / xspan * rect.width(),
                       rect.bottom() - (y - ylo) / yspan * rect.height())

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        rect = self._plotRect()

        if self._showGrid or self._showAxes:
            self._paintGridAndTicks(p, rect)
        if self._showAxes:
            p.setPen(QPen(self._axisColor, 1))
            p.drawLine(rect.bottomLeft(), rect.bottomRight())
            p.drawLine(rect.topLeft(), rect.bottomLeft())
        self._paintTitles(p, rect)

        for si, (_name, points) in enumerate(self._series):
            self._paintSeries(p, si, points)

        if self._showLegend and self._series:
            self._paintLegend(p)
        if self._showTooltip and self._hover != (-1, -1):
            self._paintTooltip(p, rect)

    def _paintGridAndTicks(self, p, rect):
        fm = QFontMetrics(self.font())
        xmin, xmax, ymin, ymax = self.dataBounds()
        _xs, _xe, xstep = niceTicks(xmin, xmax, self._tickCount)
        _ys, _ye, ystep = niceTicks(ymin, ymax, self._tickCount)

        for value in tickValues(ymin, ymax, self._tickCount):
            point = self.mapPoint(self.xRange()[0], value)
            if self._showGrid:
                p.setPen(QPen(self._gridColor, 1))
                p.drawLine(QPointF(rect.left(), point.y()),
                           QPointF(rect.right(), point.y()))
            if self._showAxes:
                p.setPen(QPen(self._labelColor))
                text = formatTick(value, ystep)
                p.drawText(QRectF(0, point.y() - fm.height() / 2.0,
                                  rect.left() - 6, fm.height()),
                           int(Qt.AlignRight | Qt.AlignVCenter), text)

        for value in tickValues(xmin, xmax, self._tickCount):
            point = self.mapPoint(value, self.yRange()[0])
            if self._showGrid:
                p.setPen(QPen(self._gridColor, 1))
                p.drawLine(QPointF(point.x(), rect.top()),
                           QPointF(point.x(), rect.bottom()))
            if self._showAxes:
                p.setPen(QPen(self._labelColor))
                text = formatTick(value, xstep)
                width = fm.horizontalAdvance(text) + 8
                p.drawText(QRectF(point.x() - width / 2.0, rect.bottom() + 3,
                                  width, fm.height()),
                           int(Qt.AlignHCenter | Qt.AlignVCenter), text)

    def _paintTitles(self, p, rect):
        fm = QFontMetrics(self.font())
        p.setPen(QPen(self._labelColor))
        if self._xTitle:
            p.drawText(QRectF(rect.left(),
                              rect.bottom() + fm.height() + 5,
                              rect.width(), fm.height()),
                       int(Qt.AlignHCenter | Qt.AlignVCenter), self._xTitle)
        if self._yTitle:
            p.save()
            p.translate(fm.height(), rect.center().y())
            p.rotate(-90)
            p.drawText(QRectF(-rect.height() / 2.0, -fm.height() / 2.0,
                              rect.height(), fm.height()),
                       int(Qt.AlignCenter), self._yTitle)
            p.restore()

    def _markerPath(self, p, centre, radius):
        shape = self._markerShape
        if shape == "square":
            p.drawRect(QRectF(centre.x() - radius, centre.y() - radius,
                              radius * 2, radius * 2))
        elif shape == "diamond":
            from qtpy.QtGui import QPolygonF
            p.drawPolygon(QPolygonF([
                QPointF(centre.x(), centre.y() - radius),
                QPointF(centre.x() + radius, centre.y()),
                QPointF(centre.x(), centre.y() + radius),
                QPointF(centre.x() - radius, centre.y())]))
        elif shape == "triangle":
            from qtpy.QtGui import QPolygonF
            p.drawPolygon(QPolygonF([
                QPointF(centre.x(), centre.y() - radius),
                QPointF(centre.x() + radius, centre.y() + radius),
                QPointF(centre.x() - radius, centre.y() + radius)]))
        else:
            p.drawEllipse(centre, radius, radius)

    def _paintSeries(self, p, index, points):
        colour = QColor(self.seriesColor(index))
        colour.setAlphaF(max(0.0, min(1.0, self._markerOpacity)))
        p.setPen(QPen(self.seriesColor(index), 1))
        p.setBrush(QBrush(colour))
        for pi, (x, y, size) in enumerate(points):
            radius = (size if size is not None else self._markerSize) / 2.0
            if (index, pi) == self._hover:
                radius += 2.0
            self._markerPath(p, self.mapPoint(x, y), max(1.0, radius))

    def _paintLegend(self, p):
        fm = QFontMetrics(self.font())
        swatch, gap = 9.0, 14.0
        widths = [swatch + 5 + fm.horizontalAdvance(name)
                  for name, _pts in self._series]
        x = (self.width() - (sum(widths) + gap * (len(widths) - 1))) / 2.0
        y = self.height() - self._legendHeight() + 2
        for index, (name, _points) in enumerate(self._series):
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self.seriesColor(index)))
            p.drawEllipse(QRectF(x, y + (fm.height() - swatch) / 2.0,
                                 swatch, swatch))
            p.setPen(QPen(self._labelColor))
            p.drawText(QRectF(x + swatch + 5, y, widths[index], fm.height()),
                       int(Qt.AlignLeft | Qt.AlignVCenter), name)
            x += widths[index] + gap

    def _paintTooltip(self, p, rect):
        si, pi = self._hover
        name, points = self._series[si]
        x, y, _size = points[pi]
        rows = [name, "x %g" % x, "y %g" % y]
        fm = QFontMetrics(self.font())
        width = max(fm.horizontalAdvance(r) for r in rows) + 16
        height = fm.height() * len(rows) + 10
        anchor = self.mapPoint(x, y)
        px = anchor.x() + 12
        if px + width > rect.right():
            px = anchor.x() - 12 - width
        px = max(rect.left(), min(px, rect.right() - width))
        py = max(rect.top(), min(anchor.y() - height / 2.0, rect.bottom() - height))

        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(self._tooltipBg.red(), self._tooltipBg.green(),
                                 self._tooltipBg.blue(), 235)))
        p.drawRoundedRect(QRectF(px, py, width, height), 6, 6)
        p.setPen(QPen(self._tooltipText))
        for i, text in enumerate(rows):
            p.drawText(QRectF(px + 8, py + 5 + i * fm.height(),
                              width - 16, fm.height()),
                       int(Qt.AlignLeft | Qt.AlignVCenter), text)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def pointAt(self, pos, tolerance=None):
        """(series, point) nearest a position within tolerance, else (-1, -1).

        Later series win ties so hit-testing agrees with what is painted on top.
        """
        point = QPointF(pos)
        limit = tolerance if tolerance is not None else max(6.0, self._markerSize)
        best, bestDistance = (-1, -1), None
        for si in range(len(self._series) - 1, -1, -1):
            for pi, (x, y, _size) in enumerate(self._series[si][1]):
                mapped = self.mapPoint(x, y)
                dx, dy = point.x() - mapped.x(), point.y() - mapped.y()
                distance = (dx * dx + dy * dy) ** 0.5
                if distance <= limit and (bestDistance is None or distance < bestDistance):
                    best, bestDistance = (si, pi), distance
        return best

    def mouseMoveEvent(self, e):
        hit = self.pointAt(e.pos())
        if hit != self._hover:
            self._hover = hit
            self.pointHovered.emit(hit[0], hit[1])
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover != (-1, -1):
            self._hover = (-1, -1)
            self.pointHovered.emit(-1, -1)
            self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            si, pi = self.pointAt(e.pos())
            if si >= 0:
                self.pointClicked.emit(si, pi)
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def pointsCsv(self):
        chunks = []
        for name, points in self._series:
            pairs = ";".join("%g,%g" % (x, y) if size is None
                             else "%g,%g,%g" % (x, y, size)
                             for x, y, size in points)
            chunks.append("%s=%s" % (name, pairs))
        return "|".join(chunks)

    @pointsCsv.setter
    def pointsCsv(self, text):
        series = []
        for index, chunk in enumerate(str(text).split("|")):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" in chunk:
                name, _, raw = chunk.partition("=")
                name = name.strip() or "Series %d" % (len(series) + 1)
            else:
                name, raw = "Series %d" % (len(series) + 1), chunk
            points = []
            for pair in raw.split(";"):
                pair = pair.strip()
                if not pair:
                    continue
                parts = [t.strip() for t in pair.split(",") if t.strip()]
                coerced = self._coercePoint(parts) if len(parts) >= 2 else None
                if coerced:
                    points.append(coerced)
            if points:
                series.append((name, points))
        self._series = []
        for name, points in series:
            self.addSeries(name, points)
        self.update()

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

    @Property(str)
    def xAxisTitle(self):
        return self._xTitle

    @xAxisTitle.setter
    def xAxisTitle(self, text):
        self._xTitle = str(text); self.update()

    @Property(str)
    def yAxisTitle(self):
        return self._yTitle

    @yAxisTitle.setter
    def yAxisTitle(self, text):
        self._yTitle = str(text); self.update()

    @Property(float)
    def markerSize(self):
        return self._markerSize

    @markerSize.setter
    def markerSize(self, value):
        self._markerSize = max(1.0, float(value)); self.update()

    @Property(str)
    def markerShape(self):
        return self._markerShape

    @markerShape.setter
    def markerShape(self, value):
        value = str(value)
        self._markerShape = value if value in ("circle", "square", "diamond",
                                               "triangle") else "circle"
        self.update()

    @Property(float)
    def markerOpacity(self):
        return self._markerOpacity

    @markerOpacity.setter
    def markerOpacity(self, value):
        self._markerOpacity = max(0.0, min(1.0, float(value))); self.update()

    @Property(int)
    def tickCount(self):
        return self._tickCount

    @tickCount.setter
    def tickCount(self, value):
        self._tickCount = max(1, int(value)); self.update()

    @Property(bool)
    def showGrid(self):
        return self._showGrid

    @showGrid.setter
    def showGrid(self, value):
        self._showGrid = bool(value); self.update()

    @Property(bool)
    def showAxes(self):
        return self._showAxes

    @showAxes.setter
    def showAxes(self, value):
        self._showAxes = bool(value); self.update()

    @Property(bool)
    def showLegend(self):
        return self._showLegend

    @showLegend.setter
    def showLegend(self, value):
        self._showLegend = bool(value); self.updateGeometry(); self.update()

    @Property(bool)
    def showTooltip(self):
        return self._showTooltip

    @showTooltip.setter
    def showTooltip(self, value):
        self._showTooltip = bool(value); self.update()

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
