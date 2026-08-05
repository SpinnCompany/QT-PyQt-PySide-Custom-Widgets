########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomSparkline - a compact, axis-less trend line.
##
## A tiny inline chart for KPI cards / tables: a smooth (cubic) or straight
## polyline across a value series, with an optional soft gradient fill beneath
## it. No axes, grid, legend or toolbar - just the shape of the trend. Colours
## come from qproperties so they can be tokenised from a theme. Give values via
## setValues([...]) in code, or the `valuesCsv` property in Qt Designer.
########################################################################
from qtpy.QtCore import Qt, Property, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QLinearGradient, QPainterPath
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomSparkline(QWidget):

    WIDGET_ICON = "components/icons/sparkline.png"
    WIDGET_TOOLTIP = "A compact axis-less trend line (sparkline)"
    WIDGET_MODULE = "Custom_Widgets.QCustomSparkline"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSparkline' name='customSparkline'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>120</width><height>44</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomSparkline",
        "props": {"valuesCsv": {"type": "string", "default": ""},
                  "seriesCsv": {"type": "string", "default": ""},
                  "seriesColorsCsv": {"type": "string", "default": ""},
                  "lineWidth": {"type": "float", "default": 2.2},
                  "smooth": {"type": "bool", "default": True},
                  "fillEnabled": {"type": "bool", "default": True},
                  "fillOpacity": {"type": "float", "default": 0.35}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, values=None, lineColor="#7c6cf6"):
        super().__init__(parent)
        self.setObjectName("QCustomSparkline")
        self._values = list(values) if values else []
        self._line = QColor(lineColor)
        self._fill = QColor(lineColor)
        self._fill_from_line = True     # fill tracks lineColor until set explicitly
        self._fill_enabled = True
        self._fill_opacity = 0.35
        self._line_width = 2.2
        self._smooth = True
        self._series = []          # optional multi-series: list of [floats]
        self._series_colors = []   # QColor per series (falls back to a palette)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumSize(48, 24)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setValues(self, values):
        self._values = [float(v) for v in (values or [])]
        self.update()

    def values(self):
        return list(self._values)

    def clear(self):
        self._values = []
        self._series = []
        self.update()

    def setSeries(self, series, colors=None):
        """Draw MULTIPLE overlaid lines sharing one y-scale. `series` is a list
        of value-lists; `colors` (optional) a matching list of colours. Overrides
        the single `values` series until cleared. Fill is suppressed for a clean
        multi-line read (as on the reference dashboards)."""
        self._series = [[float(v) for v in s] for s in (series or [])]
        if colors is not None:
            self._series_colors = [QColor(c) for c in colors]
        self.update()

    def setSeriesColors(self, colors):
        self._series_colors = [QColor(c) for c in (colors or [])]
        self.update()

    def series(self):
        return [list(s) for s in self._series]

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def _points(self, vals=None, lo=None, hi=None):
        vals = self._values if vals is None else vals
        if len(vals) < 2:
            return []
        w, h = self.width(), self.height()
        pad = max(2.0, self._line_width)
        if lo is None or hi is None:
            lo, hi = min(vals), max(vals)
        rng = (hi - lo) or 1.0
        step = (w - 2 * pad) / (len(vals) - 1)
        return [QPointF(pad + i * step,
                        h - pad - (v - lo) / rng * (h - 2 * pad))
                for i, v in enumerate(vals)]

    def _series_color(self, i):
        if i < len(self._series_colors):
            return self._series_colors[i]
        palette = ["#f6912b", "#8fe36b", "#7c6cf6", "#ff5d8f", "#38bdf8"]
        return QColor(palette[i % len(palette)])

    def _path(self, pts):
        path = QPainterPath(pts[0])
        if self._smooth:
            for i in range(1, len(pts)):
                a, b = pts[i - 1], pts[i]
                mx = (a.x() + b.x()) / 2.0
                path.cubicTo(mx, a.y(), mx, b.y(), b.x(), b.y())
        else:
            for pt in pts[1:]:
                path.lineTo(pt)
        return path

    def paintEvent(self, e):
        # multi-series mode: overlay each line on a shared y-scale, no fill
        if self._series:
            allv = [v for s in self._series for v in s]
            if not allv:
                return
            lo, hi = min(allv), max(allv)
            p = QPainter(self)
            p.setRenderHint(QPainter.Antialiasing, True)
            for i, s in enumerate(self._series):
                pts = self._points(s, lo, hi)
                if not pts:
                    continue
                pen = QPen(self._series_color(i), self._line_width)
                pen.setJoinStyle(Qt.RoundJoin)
                pen.setCapStyle(Qt.RoundCap)
                p.setPen(pen)
                p.setBrush(Qt.NoBrush)
                p.drawPath(self._path(pts))
            p.end()
            return

        pts = self._points()
        if not pts:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        line_path = self._path(pts)

        if self._fill_enabled:
            fill = QPainterPath(line_path)
            fill.lineTo(pts[-1].x(), self.height())
            fill.lineTo(pts[0].x(), self.height())
            fill.closeSubpath()
            base = QColor(self._fill)
            grad = QLinearGradient(0, 0, 0, self.height())
            top = QColor(base)
            top.setAlphaF(max(0.0, min(1.0, self._fill_opacity)))
            bottom = QColor(base)
            bottom.setAlpha(0)
            grad.setColorAt(0.0, top)
            grad.setColorAt(1.0, bottom)
            p.fillPath(fill, QBrush(grad))

        pen = QPen(self._line, self._line_width)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawPath(line_path)
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def valuesCsv(self):
        return ",".join("%g" % v for v in self._values)

    @valuesCsv.setter
    def valuesCsv(self, text):
        out = []
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if not tok:
                continue
            try:
                out.append(float(tok))
            except ValueError:
                pass
        self.setValues(out)

    @Property(QColor)
    def lineColor(self):
        return self._line

    @lineColor.setter
    def lineColor(self, c):
        self._line = QColor(c)
        if self._fill_from_line:
            self._fill = QColor(c)
        self.update()

    @Property(QColor)
    def fillColor(self):
        return self._fill

    @fillColor.setter
    def fillColor(self, c):
        self._fill = QColor(c)
        self._fill_from_line = False
        self.update()

    @Property(bool)
    def fillEnabled(self):
        return self._fill_enabled

    @fillEnabled.setter
    def fillEnabled(self, v):
        self._fill_enabled = bool(v)
        self.update()

    @Property(float)
    def fillOpacity(self):
        return self._fill_opacity

    @fillOpacity.setter
    def fillOpacity(self, v):
        self._fill_opacity = max(0.0, min(1.0, float(v)))
        self.update()

    @Property(float)
    def lineWidth(self):
        return self._line_width

    @lineWidth.setter
    def lineWidth(self, w):
        self._line_width = max(0.5, float(w))
        self.update()

    @Property(bool)
    def smooth(self):
        return self._smooth

    @smooth.setter
    def smooth(self, v):
        self._smooth = bool(v)
        self.update()

    @Property(str)
    def seriesCsv(self):
        return ";".join(",".join("%g" % v for v in s) for s in self._series)

    @seriesCsv.setter
    def seriesCsv(self, text):
        series = []
        for chunk in str(text).replace("|", ";").split(";"):
            chunk = chunk.strip()
            if not chunk:
                continue
            row = []
            for tok in chunk.split(","):
                tok = tok.strip()
                if not tok:
                    continue
                try:
                    row.append(float(tok))
                except ValueError:
                    pass
            if row:
                series.append(row)
        self.setSeries(series)

    @Property(str)
    def seriesColorsCsv(self):
        return ",".join(c.name() for c in self._series_colors)

    @seriesColorsCsv.setter
    def seriesColorsCsv(self, text):
        cols = [t.strip() for t in str(text).replace(";", ",").split(",") if t.strip()]
        self.setSeriesColors(cols)
