########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomLiquidGauge - a wavy liquid-fill level gauge.
##
## A circular (or rounded-rect) container with an animated sine-wave liquid fill
## whose height tracks the value - the classic fuel / battery / tank / storage /
## humidity disc. Two offset waves give the surface depth; a QTimer drifts them
## horizontally so the liquid ripples. The centre shows the value + a suffix
## (e.g. "3.61 gal", "72%") and an optional status chip below.
##
## Painted with QPainter so it stays crisp at any size; the disc + centre text
## FLEX to the box (reserving room for the chip) so nothing clips. Colours are
## qproperties so they flip with the theme. Drive it with setValue(...); the fill
## eases to the new level when `animated`.
########################################################################
import math

from qtpy.QtCore import (Qt, Property, Signal, QRectF, QPointF, QTimer,
                         QVariantAnimation, QEasingCurve)
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QFont, QPainterPath,
                        QLinearGradient, QFontMetrics)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomLiquidGauge(QWidget):

    valueChanged = Signal(float)

    WIDGET_ICON = "components/icons/liquid.png"
    WIDGET_TOOLTIP = "A wavy liquid-fill level gauge (fuel / battery / tank)"
    WIDGET_MODULE = "Custom_Widgets.QCustomLiquidGauge"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomLiquidGauge' name='customLiquidGauge'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>200</width><height>220</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomLiquidGauge",
        "props": {
            "value": {"type": "float", "default": 68.0},
            "minimum": {"type": "float", "default": 0.0},
            "maximum": {"type": "float", "default": 100.0},
            "shape": {"type": "enum", "values": ["circle", "roundedRect"], "default": "circle"},
            "cornerRadius": {"type": "int", "default": 22},
            "fillColor": {"type": "color", "default": "#3aa0ff"},
            "fillColor2": {"type": "color", "default": "#7c5cff"},
            "backgroundColor": {"type": "color", "default": "#141826"},
            "ringColor": {"type": "color", "default": "#2b3145"},
            "ringWidth": {"type": "int", "default": 6},
            "waveAmplitude": {"type": "float", "default": 0.0},
            "waveLength": {"type": "float", "default": 0.0},
            "waveSpeed": {"type": "float", "default": 0.06},
            "animated": {"type": "bool", "default": True},
            "centerText": {"type": "string", "default": ""},
            "centerSuffix": {"type": "string", "default": "%"},
            "centerTextColor": {"type": "color", "default": "#f4f6fb"},
            "badgeText": {"type": "string", "default": ""},
            "badgeColor": {"type": "color", "default": ""},
        },
        "signals": ["valueChanged"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, value=68.0, minimum=0.0, maximum=100.0):
        super().__init__(parent)
        self.setObjectName("QCustomLiquidGauge")
        self._min = float(minimum)
        self._max = float(maximum)
        self._value = float(value)
        self._disp = self._value          # animated fill level
        self._shape = "circle"
        self._radius = 22
        self._fill1 = QColor("#3aa0ff")
        self._fill2 = QColor("#7c5cff")
        self._bg = QColor("#141826")
        self._ring = QColor("#2b3145")
        self._ring_w = 6
        self._amp = 0.0                   # 0 -> auto (fraction of side)
        self._wavelen = 0.0               # 0 -> auto
        self._speed = 0.06
        self._animated = True
        self._phase = 0.0
        self._center_text = ""
        self._center_suffix = "%"
        self._center_color = QColor("#f4f6fb")
        self._badge_text = ""
        self._badge_color = QColor()
        self._timer = None
        self._anim = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(90, 100)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setValue(self, value):
        v = max(self._min, min(self._max, float(value)))
        if v == self._value:
            return
        self._value = v
        self.valueChanged.emit(v)
        if self._animated:
            self._animate_to(v)
        else:
            self._disp = v
            self.update()

    def _animate_to(self, target):
        if self._anim is None:
            self._anim = QVariantAnimation(self)
            self._anim.setEasingCurve(QEasingCurve.OutCubic)
            self._anim.setDuration(700)
            self._anim.valueChanged.connect(self._on_level)
        self._anim.stop()
        self._anim.setStartValue(float(self._disp))
        self._anim.setEndValue(float(target))
        self._anim.start()

    def _on_level(self, v):
        self._disp = float(v)
        self.update()

    def setRange(self, minimum, maximum):
        self._min, self._max = float(minimum), float(maximum)
        self._value = max(self._min, min(self._max, self._value))
        self._disp = max(self._min, min(self._max, self._disp))
        self.update()

    def setColors(self, fill1, fill2=None, background=None):
        self._fill1 = QColor(fill1)
        self._fill2 = QColor(fill2) if fill2 is not None else QColor(fill1).lighter(115)
        if background is not None:
            self._bg = QColor(background)
        self.update()

    def setCenterText(self, text):
        self._center_text = str(text)
        self.update()

    def setBadge(self, text, color=None):
        self._badge_text = str(text)
        if color is not None:
            self._badge_color = QColor(color)
        self.update()

    def value(self):
        return self._value

    # ------------------------------------------------------------------ #
    ## Wave animation lifecycle (only run while visible)
    # ------------------------------------------------------------------ #
    def _ensure_timer(self):
        if self._timer is None:
            self._timer = QTimer(self)
            self._timer.setInterval(33)          # ~30 fps
            self._timer.timeout.connect(self._tick)

    def _tick(self):
        self._phase += self._speed
        self.update()

    def showEvent(self, e):
        if self._animated:
            self._ensure_timer()
            self._timer.start()
        super().showEvent(e)

    def hideEvent(self, e):
        if self._timer is not None:
            self._timer.stop()
        super().hideEvent(e)

    def setAnimated(self, on):
        self._animated = bool(on)
        if self._timer is not None:
            (self._timer.start if (on and self.isVisible()) else self._timer.stop)()
        self.update()

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def _fraction(self):
        span = (self._max - self._min) or 1.0
        return max(0.0, min(1.0, (self._disp - self._min) / span))

    def _disc_box(self):
        """Flex layout: the disc square, reserving room below for the badge."""
        w, h = self.width(), self.height()
        m = 6.0
        badge_h = 0.0
        if self._badge_text:
            fm = QFontMetrics(self._badge_font(min(w, h)))
            badge_h = fm.height() + 12.0
        side = min(w - 2 * m, h - 2 * m - badge_h)
        side = max(side, 8.0)
        x = (w - side) / 2.0
        y = m + (h - 2 * m - badge_h - side) / 2.0
        return QRectF(x, y, side, side), badge_h

    def _shape_path(self, box):
        path = QPainterPath()
        if self._shape == "roundedRect":
            path.addRoundedRect(box, self._radius, self._radius)
        else:
            path.addEllipse(box)
        return path

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        box, badge_h = self._disc_box()
        side = box.width()
        path = self._shape_path(box)

        # container background
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._bg))
        p.drawPath(path)

        # liquid (clipped to the container)
        frac = self._fraction()
        if frac > 0:
            p.save()
            p.setClipPath(path)
            self._paint_wave(p, box, frac)
            p.restore()

        # ring outline
        if self._ring_w > 0:
            pen = QPen(self._ring, float(self._ring_w))
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            p.drawPath(path)

        self._paint_center(p, box)
        if self._badge_text:
            self._paint_badge(p, box, badge_h)
        p.end()

    def _paint_wave(self, p, box, frac):
        amp = self._amp if self._amp > 0 else box.height() * 0.035
        wavelen = self._wavelen if self._wavelen > 0 else box.width() * 0.9
        surface = box.bottom() - frac * box.height()
        k = 2.0 * math.pi / max(1.0, wavelen)
        step = max(2.0, box.width() / 48.0)

        def wave_path(phase, lift):
            path = QPainterPath()
            x = box.left()
            path.moveTo(x, surface - lift + amp * math.sin(k * x + phase))
            while x <= box.right():
                y = surface - lift + amp * math.sin(k * x + phase)
                path.lineTo(x, y)
                x += step
            path.lineTo(box.right(), box.bottom())
            path.lineTo(box.left(), box.bottom())
            path.closeSubpath()
            return path

        # back wave (lighter / offset), then front wave (gradient)
        back = QColor(self._fill1)
        back.setAlpha(120)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(back))
        p.drawPath(wave_path(self._phase + math.pi * 0.9, amp * 0.4))

        grad = QLinearGradient(box.topLeft(), box.bottomLeft())
        grad.setColorAt(0.0, self._fill2)
        grad.setColorAt(1.0, self._fill1)
        p.setBrush(QBrush(grad))
        p.drawPath(wave_path(self._phase, 0.0))

    def _paint_center(self, p, box):
        cx, cy = box.center().x(), box.center().y()
        side = box.width()
        big = self._center_text or ("%g" % round(self._disp))
        bf = QFont(self.font())
        bf.setBold(True)
        bf.setPointSizeF(max(11.0, side * 0.20))
        p.setFont(bf)
        bfm = p.fontMetrics()
        big_w = bfm.horizontalAdvance(big)

        suffix = self._center_suffix or ""
        sf = QFont(self.font())
        sf.setPointSizeF(max(8.0, side * 0.11))
        sfm_w = 0.0
        if suffix:
            sfm = QFontMetrics(sf)
            sfm_w = sfm.horizontalAdvance(suffix) + side * 0.02

        total = big_w + sfm_w
        x = cx - total / 2.0
        baseline = cy + (bfm.ascent() - bfm.descent()) / 2.0
        p.setFont(bf)
        p.setPen(QPen(self._center_color))
        p.drawText(QPointF(x, baseline), big)
        if suffix:
            p.setFont(sf)
            sc = QColor(self._center_color)
            sc.setAlpha(180)
            p.setPen(QPen(sc))
            p.drawText(QPointF(x + big_w + side * 0.02, baseline), suffix)

    def _badge_font(self, side):
        f = QFont(self.font())
        f.setBold(True)
        f.setPointSizeF(max(7.5, side * 0.055))
        return f

    def _paint_badge(self, p, box, badge_h):
        col = self._badge_color if self._badge_color.isValid() else QColor(self._fill1)
        p.setFont(self._badge_font(box.width()))
        fm = p.fontMetrics()
        tw = fm.horizontalAdvance(self._badge_text)
        pad_x = max(8.0, box.width() * 0.05)
        bw = tw + 2 * pad_x
        bh = fm.height() + 6.0
        cx = box.center().x()
        top = box.bottom() + (badge_h - bh) / 2.0
        rect = QRectF(cx - bw / 2.0, top, bw, bh)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(col))
        p.drawRoundedRect(rect, bh / 2.0, bh / 2.0)
        lum = 0.299 * col.red() + 0.587 * col.green() + 0.114 * col.blue()
        p.setPen(QPen(QColor("#10131a") if lum > 150 else QColor("#ffffff")))
        p.drawText(rect, Qt.AlignCenter, self._badge_text)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(float)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self.setValue(v)

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

    @Property(str)
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, v):
        self._shape = "roundedRect" if str(v) == "roundedRect" else "circle"
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(QColor)
    def fillColor(self):
        return self._fill1

    @fillColor.setter
    def fillColor(self, c):
        self._fill1 = QColor(c)
        self.update()

    @Property(QColor)
    def fillColor2(self):
        return self._fill2

    @fillColor2.setter
    def fillColor2(self, c):
        self._fill2 = QColor(c)
        self.update()

    @Property(QColor)
    def backgroundColor(self):
        return self._bg

    @backgroundColor.setter
    def backgroundColor(self, c):
        self._bg = QColor(c)
        self.update()

    @Property(QColor)
    def ringColor(self):
        return self._ring

    @ringColor.setter
    def ringColor(self, c):
        self._ring = QColor(c)
        self.update()

    @Property(int)
    def ringWidth(self):
        return self._ring_w

    @ringWidth.setter
    def ringWidth(self, v):
        self._ring_w = max(0, int(v))
        self.update()

    @Property(float)
    def waveAmplitude(self):
        return self._amp

    @waveAmplitude.setter
    def waveAmplitude(self, v):
        self._amp = max(0.0, float(v))
        self.update()

    @Property(float)
    def waveLength(self):
        return self._wavelen

    @waveLength.setter
    def waveLength(self, v):
        self._wavelen = max(0.0, float(v))
        self.update()

    @Property(float)
    def waveSpeed(self):
        return self._speed

    @waveSpeed.setter
    def waveSpeed(self, v):
        self._speed = float(v)

    @Property(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, v):
        self.setAnimated(v)

    @Property(str)
    def centerText(self):
        return self._center_text

    @centerText.setter
    def centerText(self, v):
        self.setCenterText(v)

    @Property(str)
    def centerSuffix(self):
        return self._center_suffix

    @centerSuffix.setter
    def centerSuffix(self, v):
        self._center_suffix = str(v)
        self.update()

    @Property(QColor)
    def centerTextColor(self):
        return self._center_color

    @centerTextColor.setter
    def centerTextColor(self, c):
        self._center_color = QColor(c)
        self.update()

    @Property(str)
    def badgeText(self):
        return self._badge_text

    @badgeText.setter
    def badgeText(self, v):
        self.setBadge(v)

    @Property(QColor)
    def badgeColor(self):
        return self._badge_color

    @badgeColor.setter
    def badgeColor(self, c):
        self._badge_color = QColor(c) if c else QColor()
        self.update()
