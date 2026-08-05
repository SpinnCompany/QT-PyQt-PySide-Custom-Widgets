########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomWaveform - a standalone audio-bars / streaming-line visualiser.
##
## Two modes (`mode`):
##   "bars" (default) - an equalizer / audio-level bar viz (the "Water" card):
##       one rounded bar per value, optional centre `mirror` (grows up + down),
##       gradient + optional glow.
##   "line" - a streaming line viz (the "110 bpm" ECG card): a polyline over an
##       optional faint grid, with an optional gradient fill under it.
##
## Feed it a fixed series with setValues([...]) / the `valuesCsv` property, or
## stream live with push(value) (a ring buffer of `capacity` samples scrolls).
## Turn on `animated` for a self-running demo (audio levels / a heartbeat), so it
## previews live in Designer / a demo without a data source.
##
## Painted with QPainter; it FLEXes to the widget and all colours are qproperties
## so they flip with the theme. Unlike QCustomVoiceMessage this is NOT chat-bound.
########################################################################
import math
from collections import deque

from qtpy.QtCore import Qt, Property, Signal, QRectF, QPointF, QTimer
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QPainterPath,
                        QLinearGradient)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomWaveform(QWidget):

    valuePushed = Signal(float)

    WIDGET_ICON = "components/icons/waveform.png"
    WIDGET_TOOLTIP = "A waveform / equalizer / streaming-ECG visualiser"
    WIDGET_MODULE = "Custom_Widgets.QCustomWaveform"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomWaveform' name='customWaveform'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>120</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomWaveform",
        "props": {
            "mode": {"type": "enum", "values": ["bars", "line"], "default": "bars"},
            "valuesCsv": {"type": "string", "default": ""},
            "capacity": {"type": "int", "default": 48},
            "barColor": {"type": "color", "default": "#3aa0ff"},
            "barColor2": {"type": "color", "default": "#7c5cff"},
            "barWidth": {"type": "float", "default": 0.0},
            "barGap": {"type": "float", "default": 3.0},
            "cornerRadius": {"type": "int", "default": 3},
            "mirror": {"type": "bool", "default": False},
            "lineColor": {"type": "color", "default": "#ff5c6c"},
            "lineWidth": {"type": "float", "default": 2.2},
            "showGrid": {"type": "bool", "default": False},
            "gridColor": {"type": "color", "default": "#242a38"},
            "fillArea": {"type": "bool", "default": False},
            "glow": {"type": "bool", "default": False},
            "glowStrength": {"type": "float", "default": 0.6},
            "animated": {"type": "bool", "default": False},
        },
        "signals": ["valuePushed"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, values=None, mode="bars"):
        super().__init__(parent)
        self.setObjectName("QCustomWaveform")
        self._mode = "line" if str(mode) == "line" else "bars"
        self._capacity = 48
        self._buf = deque((values if values is not None else self._seed()),
                          maxlen=self._capacity)
        self._bar1 = QColor("#3aa0ff")
        self._bar2 = QColor("#7c5cff")
        self._bar_w = 0.0            # 0 -> auto
        self._bar_gap = 3.0
        self._radius = 3
        self._mirror = False
        self._line = QColor("#ff5c6c")
        self._line_w = 2.2
        self._show_grid = False
        self._grid = QColor("#242a38")
        self._fill = False
        self._glow = False
        self._glow_strength = 0.6
        self._animated = False
        self._timer = None
        self._phase = 0
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumSize(80, 48)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _seed():
        return [0.2, 0.5, 0.35, 0.75, 0.6, 0.9, 0.45, 0.7, 0.3, 0.55, 0.8, 0.4,
                0.65, 0.5, 0.85, 0.35, 0.6, 0.7, 0.25, 0.5, 0.4, 0.75, 0.55, 0.3]

    def setValues(self, values):
        self._buf = deque([float(v) for v in (values or [])], maxlen=self._capacity)
        self.update()

    def push(self, value):
        self._buf.append(float(value))
        self.valuePushed.emit(float(value))
        self.update()

    def clear(self):
        self._buf.clear()
        self.update()

    def setMode(self, mode):
        self._mode = "line" if str(mode) == "line" else "bars"
        self.update()

    def values(self):
        return list(self._buf)

    def _range(self):
        vals = self._buf
        if not vals:
            return 0.0, 1.0
        lo, hi = min(vals), max(vals)
        if self._mode == "line":
            m = max(abs(lo), abs(hi), 1e-6)
            return -m, m
        return min(lo, 0.0), max(hi, 1e-6)

    # ------------------------------------------------------------------ #
    ## Self-running demo (audio levels / heartbeat)
    # ------------------------------------------------------------------ #
    def _ensure_timer(self):
        if self._timer is None:
            self._timer = QTimer(self)
            self._timer.setInterval(40)
            self._timer.timeout.connect(self._demo_tick)

    def _demo_tick(self):
        self._phase += 1
        if self._mode == "line":
            self.push(self._heartbeat(self._phase))
        else:
            # a lively pseudo-audio level (deterministic, no RNG needed)
            t = self._phase
            v = (0.5 + 0.34 * math.sin(t * 0.5)
                 + 0.16 * math.sin(t * 1.7 + 1.0)) * (0.6 + 0.4 * abs(math.sin(t * 0.13)))
            self.push(max(0.03, min(1.0, v)))

    @staticmethod
    def _heartbeat(t):
        """A repeating PQRST-ish ECG sample in [-1, 1]."""
        x = (t % 25) / 25.0
        if 0.30 <= x < 0.36:            # Q dip
            return -0.25
        if 0.36 <= x < 0.42:            # R spike
            return 1.0
        if 0.42 <= x < 0.48:            # S dip
            return -0.45
        if 0.10 <= x < 0.20:            # P wave
            return 0.18 * math.sin((x - 0.10) / 0.10 * math.pi)
        if 0.55 <= x < 0.75:            # T wave
            return 0.28 * math.sin((x - 0.55) / 0.20 * math.pi)
        return 0.0

    def showEvent(self, e):
        if self._animated:
            self._ensure_timer(); self._timer.start()
        super().showEvent(e)

    def hideEvent(self, e):
        if self._timer is not None:
            self._timer.stop()
        super().hideEvent(e)

    def setAnimated(self, on):
        self._animated = bool(on)
        if self._timer is not None:
            (self._timer.start if (on and self.isVisible()) else self._timer.stop)()

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if not self._buf:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        m = 6.0
        rect = QRectF(m, m, self.width() - 2 * m, self.height() - 2 * m)
        if self._mode == "line":
            self._paint_line(p, rect)
        else:
            self._paint_bars(p, rect)
        p.end()

    def _paint_bars(self, p, rect):
        vals = list(self._buf)
        n = len(vals)
        lo, hi = self._range()
        span = (hi - lo) or 1.0
        gap = self._bar_gap
        bw = self._bar_w if self._bar_w > 0 else max(1.5, (rect.width() - (n - 1) * gap) / n)
        step = (rect.width() - bw) / max(1, n - 1) if n > 1 else 0
        grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        grad.setColorAt(0.0, self._bar2)
        grad.setColorAt(1.0, self._bar1)
        for i, v in enumerate(vals):
            frac = (v - lo) / span
            x = rect.left() + i * step
            if self._mirror:
                h = frac * rect.height()
                y = rect.center().y() - h / 2.0
            else:
                h = frac * rect.height()
                y = rect.bottom() - h
            h = max(h, bw * 0.6)               # keep a visible cap
            br = QRectF(x, y, bw, h)
            if self._glow:
                self._bar_glow(p, br)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(grad))
            p.drawRoundedRect(br, self._radius, self._radius)

    def _bar_glow(self, p, br):
        for k in range(3, 0, -1):
            t = k / 3.0
            col = QColor(self._bar1)
            col.setAlphaF(self._glow_strength * 0.16 * (1.1 - t))
            grow = br.adjusted(-t * 4, -t * 4, t * 4, t * 4)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(col))
            p.drawRoundedRect(grow, self._radius + 2, self._radius + 2)

    def _paint_line(self, p, rect):
        if self._show_grid:
            pen = QPen(self._grid, 1.0)
            p.setPen(pen)
            for i in range(1, 5):
                y = rect.top() + rect.height() * i / 5.0
                p.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))
            for i in range(1, 8):
                x = rect.left() + rect.width() * i / 8.0
                p.drawLine(QPointF(x, rect.top()), QPointF(x, rect.bottom()))

        vals = list(self._buf)
        n = len(vals)
        lo, hi = self._range()
        span = (hi - lo) or 1.0
        step = rect.width() / max(1, n - 1)

        def y_at(v):
            return rect.bottom() - ((v - lo) / span) * rect.height()

        path = QPainterPath()
        path.moveTo(rect.left(), y_at(vals[0]))
        for i in range(1, n):
            path.lineTo(rect.left() + i * step, y_at(vals[i]))

        if self._fill:
            fillp = QPainterPath(path)
            fillp.lineTo(rect.right(), rect.bottom())
            fillp.lineTo(rect.left(), rect.bottom())
            fillp.closeSubpath()
            grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            c = QColor(self._line); c.setAlphaF(0.28)
            c2 = QColor(self._line); c2.setAlphaF(0.0)
            grad.setColorAt(0.0, c); grad.setColorAt(1.0, c2)
            p.setPen(Qt.NoPen); p.setBrush(QBrush(grad))
            p.drawPath(fillp)

        if self._glow:
            for k in range(3, 0, -1):
                t = k / 3.0
                gc = QColor(self._line); gc.setAlphaF(self._glow_strength * 0.18 * (1.1 - t))
                gp = QPen(gc, self._line_w + t * 6.0)
                gp.setJoinStyle(Qt.RoundJoin); gp.setCapStyle(Qt.RoundCap)
                p.setPen(gp); p.setBrush(Qt.NoBrush)
                p.drawPath(path)

        pen = QPen(self._line, self._line_w)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

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
        return ",".join("%g" % v for v in self._buf)

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
        if out:
            self.setValues(out)

    @Property(int)
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, v):
        self._capacity = max(2, int(v))
        self._buf = deque(self._buf, maxlen=self._capacity)
        self.update()

    @Property(QColor)
    def barColor(self):
        return self._bar1

    @barColor.setter
    def barColor(self, c):
        self._bar1 = QColor(c)
        self.update()

    @Property(QColor)
    def barColor2(self):
        return self._bar2

    @barColor2.setter
    def barColor2(self, c):
        self._bar2 = QColor(c)
        self.update()

    @Property(float)
    def barWidth(self):
        return self._bar_w

    @barWidth.setter
    def barWidth(self, v):
        self._bar_w = max(0.0, float(v))
        self.update()

    @Property(float)
    def barGap(self):
        return self._bar_gap

    @barGap.setter
    def barGap(self, v):
        self._bar_gap = max(0.0, float(v))
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(bool)
    def mirror(self):
        return self._mirror

    @mirror.setter
    def mirror(self, v):
        self._mirror = bool(v)
        self.update()

    @Property(QColor)
    def lineColor(self):
        return self._line

    @lineColor.setter
    def lineColor(self, c):
        self._line = QColor(c)
        self.update()

    @Property(float)
    def lineWidth(self):
        return self._line_w

    @lineWidth.setter
    def lineWidth(self, v):
        self._line_w = max(0.5, float(v))
        self.update()

    @Property(bool)
    def showGrid(self):
        return self._show_grid

    @showGrid.setter
    def showGrid(self, v):
        self._show_grid = bool(v)
        self.update()

    @Property(QColor)
    def gridColor(self):
        return self._grid

    @gridColor.setter
    def gridColor(self, c):
        self._grid = QColor(c)
        self.update()

    @Property(bool)
    def fillArea(self):
        return self._fill

    @fillArea.setter
    def fillArea(self, v):
        self._fill = bool(v)
        self.update()

    @Property(bool)
    def glow(self):
        return self._glow

    @glow.setter
    def glow(self, v):
        self._glow = bool(v)
        self.update()

    @Property(float)
    def glowStrength(self):
        return self._glow_strength

    @glowStrength.setter
    def glowStrength(self, v):
        self._glow_strength = max(0.0, min(1.0, float(v)))
        self.update()

    @Property(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, v):
        self.setAnimated(v)
