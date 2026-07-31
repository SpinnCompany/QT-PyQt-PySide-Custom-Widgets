########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomDonut - a painted donut / multi-ring radial chart.
##
## Two modes:
##   mode="rings" (default) - CONCENTRIC gauge rings, one per value: each value
##       is its own ring at a decreasing radius, sweeping an arc proportional to
##       value / max(values) over a faint track, with rounded caps. This is the
##       "several rings" radial-bar look (outer = largest value).
##   mode="segments" - a single ring split into coloured segments (a classic
##       donut), rounded caps + gaps.
##
## Painted directly with QPainter, so it stays crisp at ANY size (a QChart pie
## collapses to a hairline in constrained panels). Give values/colours via
## setData(...) in code, or the valuesCsv / colorsCsv properties in Qt Designer.
########################################################################
import math

from qtpy.QtCore import Qt, Property, QRectF, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFont
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomDonut(QWidget):

    WIDGET_ICON = "components/icons/donut.png"
    WIDGET_TOOLTIP = "A painted donut / multi-ring radial chart"
    WIDGET_MODULE = "Custom_Widgets.QCustomDonut"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomDonut' name='customDonut'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>220</width><height>220</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomDonut",
        "props": {"valuesCsv": {"type": "string", "default": "52,33,15"},
                  "colorsCsv": {"type": "string", "default": "#7c6cf6,#f2794b,#f4c44e"},
                  "mode": {"type": "enum", "values": ["rings", "segments"], "default": "rings"},
                  "holeRatio": {"type": "float", "default": 0.42},
                  "maxSweep": {"type": "float", "default": 324.0},
                  "gapDegrees": {"type": "float", "default": 4.0},
                  "showPercentLabels": {"type": "bool", "default": False},
                  "percentLabelColor": {"type": "color", "default": "#ffffff"},
                  "percentPill": {"type": "bool", "default": True},
                  "percentPillColor": {"type": "color", "default": "#12141c"},
                  "minLabelPercent": {"type": "float", "default": 4.0},
                  "hatchCsv": {"type": "string", "default": ""},
                  "hatchPattern": {"type": "enum",
                                   "values": ["bdiag", "fdiag", "cross", "horizontal", "vertical", "dense"],
                                   "default": "bdiag"}},
        "signals": [],
        "tokens_used": ["accent"],
    }

    _DEFAULT_COLORS = ["#7c6cf6", "#f2794b", "#f4c44e", "#3ddc97", "#f5678a"]

    def __init__(self, parent=None, values=None, colors=None):
        super().__init__(parent)
        self.setObjectName("QCustomDonut")
        self._values = [float(v) for v in (values or [52, 33, 15])]
        self._colors = [QColor(c) for c in (colors or self._DEFAULT_COLORS)]
        self._mode = "rings"
        self._hole = 0.42          # inner radius fraction (empty core)
        self._max_sweep = 324.0    # degrees the largest value sweeps (gap at top)
        self._gap = 4.0            # segments mode: gap between segments (deg)
        self._start = 90.0         # 12 o'clock
        self._track = QColor(255, 255, 255, 22)   # faint ring behind each value
        self._gap_color = QColor("#1b1e26")        # segments mode: gap colour
        # --- opt-in enhancements (segments mode; default OFF = unchanged look) ---
        self._show_pct = False         # draw % callout labels ON each arc
        self._pct_color = QColor("#ffffff")
        self._pct_pill = True          # small rounded pill behind the % text
        self._pct_pill_color = QColor("#12141c")
        self._min_pct = 4.0            # hide labels for tiny segments (< this %)
        self._hatch = set()           # segment indices rendered with a hatch fill
        self._hatch_pattern = "bdiag"
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(80, 80)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setData(self, values, colors=None):
        self._values = [float(v) for v in (values or [])]
        if colors is not None:
            self._colors = [QColor(c) for c in colors]
        self.update()

    def setColors(self, colors):
        self._colors = [QColor(c) for c in colors]
        self.update()

    def setTrackColor(self, color):
        self._track = QColor(color)
        self.update()

    def setGapColor(self, color):
        self._gap_color = QColor(color)
        self.update()

    def setMode(self, mode):
        self._mode = "segments" if str(mode) == "segments" else "rings"
        self.update()

    def setShowPercentLabels(self, on):
        self._show_pct = bool(on)
        self.update()

    def setHatchIndices(self, indices):
        """Segment indices (segments mode) rendered with a hatch/pattern fill."""
        self._hatch = set(int(i) for i in (indices or []))
        self.update()

    def setHatchPattern(self, name):
        self._hatch_pattern = str(name)
        self.update()

    def values(self):
        return list(self._values)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if not self._values:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        if self._mode == "segments":
            self._paint_segments(p)
        else:
            self._paint_rings(p)
        p.end()

    def _paint_rings(self, p):
        vals = self._values
        n = len(vals)
        maxv = max(vals) or 1.0
        w, h = self.width(), self.height()
        side = min(w, h)
        cx, cy = w / 2.0, h / 2.0
        r_outer = side / 2.0 - 6
        band = r_outer * (1.0 - self._hole)        # radial room for all rings
        # thickness + a 45%-of-thickness gap between rings must fit the band
        thickness = band / (n + (n - 1) * 0.45)
        ring_gap = thickness * 0.45
        for i, val in enumerate(vals):
            r_mid = r_outer - thickness / 2.0 - i * (thickness + ring_gap)
            if r_mid <= 0:
                break
            rect = QRectF(cx - r_mid, cy - r_mid, 2 * r_mid, 2 * r_mid)
            color = self._colors[i % len(self._colors)] if self._colors else QColor("#888888")
            # faint full-length track
            track = QPen(self._track, thickness)
            track.setCapStyle(Qt.RoundCap)
            p.setPen(track)
            p.drawArc(rect, int(self._start * 16), int(-self._max_sweep * 16))
            # value arc (proportional to the largest value)
            sweep = (val / maxv) * self._max_sweep
            pen = QPen(color, thickness)
            pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            p.drawArc(rect, int(self._start * 16), int(-sweep * 16))

    def _paint_segments(self, p):
        vals = self._values
        total = float(sum(vals)) or 1.0
        w, h = self.width(), self.height()
        side = min(w, h)
        thickness = side * (1.0 - max(self._hole, 0.55)) * 0.5 + side * 0.08
        margin = thickness / 2.0 + 6
        rect = QRectF((w - side) / 2.0 + margin, (h - side) / 2.0 + margin,
                      side - 2 * margin, side - 2 * margin)
        cx, cy = rect.center().x(), rect.center().y()
        radius = rect.width() / 2.0
        start = self._start
        gap = self._gap if len(vals) > 1 else 0.0
        labels = []                    # (mid_deg, pct) — drawn on top after arcs
        for i, val in enumerate(vals):
            span = val / total * 360.0
            color = self._colors[i % len(self._colors)] if self._colors else QColor("#888888")
            a0 = (start - gap / 2.0)
            sweep = -(span - gap)
            if i in self._hatch:
                # a dim base shows through the hatch lines -> a "hatched" segment
                base = QColor(color); base.setAlpha(70)
                p.setPen(self._arc_pen(base, thickness))
                p.drawArc(rect, int(a0 * 16), int(sweep * 16))
                p.setPen(self._arc_pen(QBrush(color, self._hatch_qt()), thickness))
                p.drawArc(rect, int(a0 * 16), int(sweep * 16))
            else:
                p.setPen(self._arc_pen(color, thickness))
                p.drawArc(rect, int(a0 * 16), int(sweep * 16))
            labels.append((start - span / 2.0, val / total * 100.0))
            start -= span
        if self._show_pct:
            self._paint_pct_labels(p, cx, cy, radius, labels)

    @staticmethod
    def _arc_pen(color_or_brush, thickness):
        pen = QPen(color_or_brush, thickness)
        pen.setCapStyle(Qt.RoundCap)
        return pen

    def _hatch_qt(self):
        return {"bdiag": Qt.BDiagPattern, "fdiag": Qt.FDiagPattern,
                "cross": Qt.DiagCrossPattern, "horizontal": Qt.HorPattern,
                "vertical": Qt.VerPattern, "dense": Qt.Dense5Pattern,
                }.get(self._hatch_pattern, Qt.BDiagPattern)

    def _paint_pct_labels(self, p, cx, cy, radius, labels):
        f = QFont(self.font())
        f.setBold(True)
        f.setPointSizeF(max(7.0, radius * 0.13))
        p.setFont(f)
        fm = p.fontMetrics()
        th = fm.height()
        for mid_deg, pct in labels:
            if pct < self._min_pct:
                continue
            a = math.radians(mid_deg)
            lx = cx + radius * math.cos(a)
            ly = cy - radius * math.sin(a)
            text = "%d%%" % round(pct)
            tw = fm.horizontalAdvance(text)
            if self._pct_pill:
                pad = th * 0.30
                pill = QRectF(lx - tw / 2.0 - pad, ly - th / 2.0, tw + 2 * pad, th)
                bg = QColor(self._pct_pill_color); bg.setAlpha(220)
                p.setPen(Qt.NoPen); p.setBrush(QBrush(bg))
                p.drawRoundedRect(pill, th / 2.0, th / 2.0)
            p.setPen(QPen(self._pct_color)); p.setBrush(Qt.NoBrush)
            p.drawText(QRectF(lx - tw / 2.0 - 6, ly - th / 2.0, tw + 12, th),
                       Qt.AlignCenter, text)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, m):
        self.setMode(m)

    @Property(str)
    def valuesCsv(self):
        return ",".join("%g" % v for v in self._values)

    @valuesCsv.setter
    def valuesCsv(self, text):
        out = []
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if tok:
                try:
                    out.append(float(tok))
                except ValueError:
                    pass
        self.setData(out)

    @Property(str)
    def colorsCsv(self):
        return ",".join(c.name() for c in self._colors)

    @colorsCsv.setter
    def colorsCsv(self, text):
        cols = [t.strip() for t in str(text).replace(";", ",").split(",") if t.strip()]
        if cols:
            self.setColors(cols)

    @Property(float)
    def holeRatio(self):
        return self._hole

    @holeRatio.setter
    def holeRatio(self, r):
        self._hole = max(0.0, min(0.95, float(r)))
        self.update()

    @Property(float)
    def maxSweep(self):
        return self._max_sweep

    @maxSweep.setter
    def maxSweep(self, s):
        self._max_sweep = max(30.0, min(360.0, float(s)))
        self.update()

    @Property(float)
    def gapDegrees(self):
        return self._gap

    @gapDegrees.setter
    def gapDegrees(self, g):
        self._gap = max(0.0, float(g))
        self.update()

    @Property(QColor)
    def trackColor(self):
        return self._track

    @trackColor.setter
    def trackColor(self, c):
        self._track = QColor(c)
        self.update()

    @Property(QColor)
    def gapColor(self):
        return self._gap_color

    @gapColor.setter
    def gapColor(self, c):
        self._gap_color = QColor(c)
        self.update()

    # ------------------------------------------------------------------ #
    ## Enhancements: % callout labels + hatch fills (opt-in, segments mode)
    # ------------------------------------------------------------------ #
    @Property(bool)
    def showPercentLabels(self):
        return self._show_pct

    @showPercentLabels.setter
    def showPercentLabels(self, v):
        self._show_pct = bool(v)
        self.update()

    @Property(QColor)
    def percentLabelColor(self):
        return self._pct_color

    @percentLabelColor.setter
    def percentLabelColor(self, c):
        self._pct_color = QColor(c)
        self.update()

    @Property(bool)
    def percentPill(self):
        return self._pct_pill

    @percentPill.setter
    def percentPill(self, v):
        self._pct_pill = bool(v)
        self.update()

    @Property(QColor)
    def percentPillColor(self):
        return self._pct_pill_color

    @percentPillColor.setter
    def percentPillColor(self, c):
        self._pct_pill_color = QColor(c)
        self.update()

    @Property(float)
    def minLabelPercent(self):
        return self._min_pct

    @minLabelPercent.setter
    def minLabelPercent(self, v):
        self._min_pct = max(0.0, float(v))
        self.update()

    @Property(str)
    def hatchCsv(self):
        return ",".join(str(i) for i in sorted(self._hatch))

    @hatchCsv.setter
    def hatchCsv(self, text):
        out = set()
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if tok:
                try:
                    out.add(int(float(tok)))
                except ValueError:
                    pass
        self._hatch = out
        self.update()

    @Property(str)
    def hatchPattern(self):
        return self._hatch_pattern

    @hatchPattern.setter
    def hatchPattern(self, v):
        self._hatch_pattern = str(v)
        self.update()
