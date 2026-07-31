########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomRulerPicker - a numbered tick-ruler value selector.
##
## A measurement-style ruler (the weight / height "55 … 65 … 90" picker): a strip
## of minor ticks with taller MAJOR ticks + numeric labels, and an indicator at
## the current value. Drag or scroll to change the value; it snaps to `step`.
##
## Two looks (`centered`):
##   False (default) - a FIXED ruler: min..max mapped across the width, the
##       indicator slides to the value (matches the reference weight card).
##   True            - a SCROLLING ruler: the value is pinned under a fixed centre
##       indicator and the scale scrolls (an iOS-style picker).
##
## Horizontal or vertical (`orientation`). Painted with QPainter; the strip FLEXes
## to the widget, and an optional big value + unit readout sits above. Colours are
## qproperties so they flip with the theme. Signal: valueChanged(float).
########################################################################
import math

from qtpy.QtCore import Qt, Property, Signal, QRectF, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QFont, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomRulerPicker(QWidget):

    valueChanged = Signal(float)

    WIDGET_ICON = "components/icons/ruler.png"
    WIDGET_TOOLTIP = "A numbered tick-ruler value selector (weight / height)"
    WIDGET_MODULE = "Custom_Widgets.QCustomRulerPicker"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRulerPicker' name='customRulerPicker'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>360</width><height>110</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRulerPicker",
        "props": {
            "orientation": {"type": "enum", "values": ["horizontal", "vertical"], "default": "horizontal"},
            "minimum": {"type": "float", "default": 40.0},
            "maximum": {"type": "float", "default": 120.0},
            "value": {"type": "float", "default": 65.0},
            "step": {"type": "float", "default": 1.0},
            "majorEvery": {"type": "int", "default": 5},
            "centered": {"type": "bool", "default": False},
            "tickSpacing": {"type": "float", "default": 9.0},
            "snap": {"type": "bool", "default": True},
            "unit": {"type": "string", "default": "Kg"},
            "showValue": {"type": "bool", "default": False},
            "tickColor": {"type": "color", "default": "#4a4f5e"},
            "majorTickColor": {"type": "color", "default": "#8b90a0"},
            "indicatorColor": {"type": "color", "default": "#f4f6fb"},
            "labelColor": {"type": "color", "default": "#8b90a0"},
            "valueColor": {"type": "color", "default": "#f4f6fb"},
        },
        "signals": ["valueChanged"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, value=65.0, minimum=40.0, maximum=120.0,
                 step=1.0, orientation="horizontal"):
        super().__init__(parent)
        self.setObjectName("QCustomRulerPicker")
        self._min = float(minimum)
        self._max = float(maximum)
        self._step = float(step) or 1.0
        self._value = self._clamp(float(value))
        self._orient = "vertical" if str(orientation) == "vertical" else "horizontal"
        self._major_every = 5
        self._centered = False
        self._spacing = 9.0
        self._snap = True
        self._unit = "Kg"
        self._show_value = False
        self._tick = QColor("#4a4f5e")
        self._major = QColor("#8b90a0")
        self._indicator = QColor("#f4f6fb")
        self._label_color = QColor("#8b90a0")
        self._value_color = QColor("#f4f6fb")
        self._drag_last = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumSize(120, 70)
        self.setCursor(Qt.SizeHorCursor if self._orient == "horizontal"
                       else Qt.SizeVerCursor)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def _clamp(self, v):
        return max(self._min, min(self._max, v))

    def _snapped(self, v):
        if not self._snap:
            return self._clamp(v)
        n = round((v - self._min) / self._step)
        return self._clamp(self._min + n * self._step)

    def setValue(self, value):
        v = self._snapped(float(value))
        if v != self._value:
            self._value = v
            self.valueChanged.emit(v)
            self.update()

    def setRange(self, minimum, maximum):
        self._min, self._max = float(minimum), float(maximum)
        self._value = self._clamp(self._value)
        self.update()

    def setUnit(self, unit):
        self._unit = str(unit)
        self.update()

    def value(self):
        return self._value

    # ------------------------------------------------------------------ #
    ## Geometry — one axis helper, so horizontal & vertical share the maths
    # ------------------------------------------------------------------ #
    def _horizontal(self):
        return self._orient == "horizontal"

    def _long_extent(self):
        return (self.width() if self._horizontal() else self.height())

    def _strip_geom(self):
        """Return (a0, a1, base, depth, label_a, lab) along the long axis:
        a0..a1 the usable long span, base the tick baseline (short axis), depth
        the (capped) tick length, label_a the short-axis coord for labels. The
        [labels + ticks] block is CENTRED in the short axis so tall widgets keep
        short ticks instead of stretching them."""
        w, h = self.width(), self.height()
        pad = 10.0
        fm = QFontMetrics(self._label_font())
        lab = fm.height() + 4.0
        val = (self._value_font_h() + 6.0) if self._show_value else 0.0
        if self._horizontal():
            a0, a1 = pad, w - pad
            avail = h - val
            depth = min(52.0, max(16.0, avail * 0.5))
            top = val + max(0.0, (avail - (lab + depth)) / 2.0)
            label_a = top
            base = top + lab
        else:
            a0, a1 = pad + val, h - pad
            label_w = fm.horizontalAdvance("000") + 8.0
            depth = min(52.0, max(16.0, (w - label_w) * 0.55))
            left = max(0.0, (w - (label_w + depth)) / 2.0)
            label_a = left
            base = left + label_w
        return a0, a1, base, depth, label_a, lab

    def _pos(self, v, a0, a1):
        """Long-axis coordinate for value v."""
        if self._centered:
            pxu = self._spacing / self._step
            center = (a0 + a1) / 2.0
            d = (v - self._value) * pxu
            return center + (d if self._horizontal() else -d)
        frac = 0.0 if self._max <= self._min else (v - self._min) / (self._max - self._min)
        return a0 + frac * (a1 - a0) if self._horizontal() else a1 - frac * (a1 - a0)

    def _value_at(self, a, a0, a1):
        """Inverse: value at long-axis coordinate a."""
        if self._centered:
            pxu = self._spacing / self._step
            center = (a0 + a1) / 2.0
            d = (a - center) if self._horizontal() else (center - a)
            return self._value + d / pxu
        span = (a1 - a0) or 1.0
        frac = (a - a0) / span if self._horizontal() else (a1 - a) / span
        return self._min + frac * (self._max - self._min)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def _label_font(self):
        f = QFont(self.font())
        f.setPointSizeF(max(7.5, min(11.0, self._long_extent() * 0.026)))
        return f

    def _value_font_h(self):
        return QFontMetrics(self._value_font()).height()

    def _value_font(self):
        f = QFont(self.font())
        f.setBold(True)
        f.setPointSizeF(max(13.0, min(30.0, min(self.width(), self.height()) * 0.22)))
        return f

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        a0, a1, base, depth, label_a, lab = self._strip_geom()
        horiz = self._horizontal()

        # tick values across the (visible) range
        first = math.floor((self._min) / self._step) * self._step
        n_steps = int(round((self._max - self._min) / self._step))
        vfont = self._label_font()

        for i in range(n_steps + 1):
            v = self._min + i * self._step
            a = self._pos(v, a0, a1)
            if a < a0 - 2 or a > a1 + 2:
                continue
            is_major = (i % max(1, self._major_every) == 0)
            length = depth * (0.62 if is_major else 0.34)
            pen = QPen(self._major if is_major else self._tick,
                       2.0 if is_major else 1.0)
            pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            if horiz:
                p.drawLine(QPointF(a, base), QPointF(a, base + length))
            else:
                p.drawLine(QPointF(base, a), QPointF(base + length, a))
            if is_major:
                near = abs(v - self._value) < self._step / 2.0
                p.setFont(vfont)
                p.setPen(QPen(self._indicator if near else self._label_color))
                txt = "%g" % v
                fm = p.fontMetrics()
                if horiz:
                    p.drawText(QRectF(a - 24, label_a, 48, lab),
                               Qt.AlignHCenter | Qt.AlignVCenter, txt)
                else:
                    p.drawText(QRectF(0, a - lab / 2.0, base - 6, lab),
                               Qt.AlignRight | Qt.AlignVCenter, txt)

        # indicator at the current value (taller, accent)
        ai = self._pos(self._value, a0, a1)
        pen = QPen(self._indicator, 2.6)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        if horiz:
            p.drawLine(QPointF(ai, base - 3), QPointF(ai, base + depth))
            p.setBrush(self._indicator)
            p.setPen(Qt.NoPen)
            s = 4.0
            p.drawEllipse(QPointF(ai, base - 3), s, s)
        else:
            p.drawLine(QPointF(base - 3, ai), QPointF(base + depth, ai))
            p.setBrush(self._indicator)
            p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(base - 3, ai), 4.0, 4.0)

        # optional big value + unit readout
        if self._show_value:
            p.setFont(self._value_font())
            p.setPen(QPen(self._value_color))
            txt = "%g" % self._value
            fm = p.fontMetrics()
            vw = fm.horizontalAdvance(txt)
            uf = QFont(self.font()); uf.setPointSizeF(max(8.0, self._value_font().pointSizeF() * 0.5))
            uw = QFontMetrics(uf).horizontalAdvance(self._unit) + 6 if self._unit else 0
            x = (self.width() - vw - uw) / 2.0 if horiz else 8.0
            y = fm.ascent() + 2
            p.drawText(QPointF(x, y), txt)
            if self._unit:
                p.setFont(uf)
                p.setPen(QPen(self._label_color))
                p.drawText(QPointF(x + vw + 6, y), self._unit)
        p.end()

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def _coord(self, pos):
        return pos.x() if self._horizontal() else pos.y()

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return super().mousePressEvent(e)
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        self._drag_last = self._coord(pos)
        if not self._centered:                       # fixed: jump to the point
            a0, a1, *_ = self._strip_geom()
            self.setValue(self._value_at(self._coord(pos), a0, a1))
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self._drag_last is None:
            return
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        c = self._coord(pos)
        a0, a1, *_ = self._strip_geom()
        if self._centered:
            pxu = self._spacing / self._step
            d = (c - self._drag_last)
            dv = (d if self._horizontal() else -d) / pxu
            self.setValue(self._value + dv)
        else:
            self.setValue(self._value_at(c, a0, a1))
        self._drag_last = c
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        self._drag_last = None
        if self._snap:
            self.setValue(self._value)               # re-snap
        super().mouseReleaseEvent(e)

    def wheelEvent(self, e):
        d = e.angleDelta().y()
        if d:
            self.setValue(self._value + (self._step if d > 0 else -self._step))
            e.accept()

    def sizeHint(self):
        from qtpy.QtCore import QSize
        return QSize(360, 90) if self._horizontal() else QSize(90, 320)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def orientation(self):
        return self._orient

    @orientation.setter
    def orientation(self, v):
        self._orient = "vertical" if str(v) == "vertical" else "horizontal"
        self.setCursor(Qt.SizeHorCursor if self._horizontal() else Qt.SizeVerCursor)
        self.updateGeometry()
        self.update()

    @Property(float)
    def minimum(self):
        return self._min

    @minimum.setter
    def minimum(self, v):
        self.setRange(float(v), self._max)

    @Property(float)
    def maximum(self):
        return self._max

    @maximum.setter
    def maximum(self, v):
        self.setRange(self._min, float(v))

    @Property(float)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self.setValue(v)

    @Property(float)
    def step(self):
        return self._step

    @step.setter
    def step(self, v):
        self._step = float(v) or 1.0
        self.update()

    @Property(int)
    def majorEvery(self):
        return self._major_every

    @majorEvery.setter
    def majorEvery(self, v):
        self._major_every = max(1, int(v))
        self.update()

    @Property(bool)
    def centered(self):
        return self._centered

    @centered.setter
    def centered(self, v):
        self._centered = bool(v)
        self.update()

    @Property(float)
    def tickSpacing(self):
        return self._spacing

    @tickSpacing.setter
    def tickSpacing(self, v):
        self._spacing = max(2.0, float(v))
        self.update()

    @Property(bool)
    def snap(self):
        return self._snap

    @snap.setter
    def snap(self, v):
        self._snap = bool(v)
        self.update()

    @Property(str)
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, v):
        self.setUnit(v)

    @Property(bool)
    def showValue(self):
        return self._show_value

    @showValue.setter
    def showValue(self, v):
        self._show_value = bool(v)
        self.updateGeometry()
        self.update()

    @Property(QColor)
    def tickColor(self):
        return self._tick

    @tickColor.setter
    def tickColor(self, c):
        self._tick = QColor(c)
        self.update()

    @Property(QColor)
    def majorTickColor(self):
        return self._major

    @majorTickColor.setter
    def majorTickColor(self, c):
        self._major = QColor(c)
        self.update()

    @Property(QColor)
    def indicatorColor(self):
        return self._indicator

    @indicatorColor.setter
    def indicatorColor(self, c):
        self._indicator = QColor(c)
        self.update()

    @Property(QColor)
    def labelColor(self):
        return self._label_color

    @labelColor.setter
    def labelColor(self, c):
        self._label_color = QColor(c)
        self.update()

    @Property(QColor)
    def valueColor(self):
        return self._value_color

    @valueColor.setter
    def valueColor(self, c):
        self._value_color = QColor(c)
        self.update()
