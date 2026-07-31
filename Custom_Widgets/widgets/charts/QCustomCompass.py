########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomCompass - a heading / compass rose.
##
## A painted compass: a tick ring with N / E / S / W (+ intercardinals), a
## two-tone needle and a centre readout (16-point cardinal + degrees). Set the
## `heading` (0-360°, 0 = North = up); it eases to the new bearing when animated.
##
## Two looks (`rotateBezel`):
##   False (default) - a FIXED rose, the needle rotates to the heading.
##   True            - a rotating COMPASS CARD: the needle stays up and the whole
##       rose spins so the heading sits at the top (aircraft / marine style).
##
## Interactive: drag around the centre to set the heading (opt-out via
## `interactive=False`). Painted with QPainter; it FLEXes to the widget and every
## colour is a qproperty so it flips with the theme. Signal: headingChanged(float).
########################################################################
import math

from qtpy.QtCore import Qt, Property, Signal, QRectF, QPointF, QTimer
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFont, QPainterPath
from qtpy.QtWidgets import QWidget, QSizePolicy

_POINTS16 = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
             "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
_CARDINALS = [("N", 0), ("NE", 45), ("E", 90), ("SE", 135),
              ("S", 180), ("SW", 225), ("W", 270), ("NW", 315)]


class QCustomCompass(QWidget):

    headingChanged = Signal(float)

    WIDGET_ICON = "components/icons/compass.png"
    WIDGET_TOOLTIP = "A heading / compass rose"
    WIDGET_MODULE = "Custom_Widgets.QCustomCompass"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCompass' name='customCompass'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>200</width><height>200</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCompass",
        "props": {
            "heading": {"type": "float", "default": 315.0},
            "rotateBezel": {"type": "bool", "default": False},
            "showIntercardinals": {"type": "bool", "default": True},
            "showReadout": {"type": "bool", "default": True},
            "animated": {"type": "bool", "default": True},
            "interactive": {"type": "bool", "default": True},
            "northColor": {"type": "color", "default": "#e0463c"},
            "southColor": {"type": "color", "default": "#cfd4de"},
            "ringColor": {"type": "color", "default": "#2b3145"},
            "tickColor": {"type": "color", "default": "#6b7280"},
            "cardinalColor": {"type": "color", "default": "#f4f6fb"},
            "readoutColor": {"type": "color", "default": "#f4f6fb"},
            "hubColor": {"type": "color", "default": "#141826"},
        },
        "signals": ["headingChanged"],
        "tokens_used": ["accent", "down"],
    }

    def __init__(self, parent=None, heading=315.0):
        super().__init__(parent)
        self.setObjectName("QCustomCompass")
        self._heading = float(heading) % 360.0
        self._disp = self._heading
        self._rotate_bezel = False
        self._show_inter = True
        self._show_readout = True
        self._animated = True
        self._interactive = True
        self._north = QColor("#e0463c")
        self._south = QColor("#cfd4de")
        self._ring = QColor("#2b3145")
        self._tick = QColor("#6b7280")
        self._cardinal = QColor("#f4f6fb")
        self._readout = QColor("#f4f6fb")
        self._hub = QColor("#141826")
        self._timer = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(90, 90)

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setHeading(self, deg):
        h = float(deg) % 360.0
        if h == self._heading:
            return
        self._heading = h
        self.headingChanged.emit(h)
        if self._animated:
            self._start_anim()
        else:
            self._disp = h
            self.update()

    @staticmethod
    def cardinal16(deg):
        return _POINTS16[int((deg % 360) / 22.5 + 0.5) % 16]

    def _start_anim(self):
        if self._timer is None:
            self._timer = QTimer(self)
            self._timer.setInterval(16)
            self._timer.timeout.connect(self._tick_anim)
        self._timer.start()

    def _tick_anim(self):
        # ease along the SHORTEST angular path (handles the 0/360 wrap)
        diff = (self._heading - self._disp + 540.0) % 360.0 - 180.0
        if abs(diff) < 0.4:
            self._disp = self._heading
            self._timer.stop()
        else:
            self._disp = (self._disp + diff * 0.22) % 360.0
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _geom(self):
        side = min(self.width(), self.height())
        r = side * 0.44
        return QPointF(self.width() / 2.0, self.height() / 2.0), max(r, 8.0)

    def _dir(self, compass_deg):
        """Unit vector for a compass angle (0 = North = up, clockwise)."""
        a = math.radians(compass_deg)
        return math.sin(a), -math.cos(a)

    def _rose_angle(self, a):
        """Screen compass angle of a rose element at bearing a."""
        return (a - self._disp) if self._rotate_bezel else a

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def _f(self, size, bold=False):
        f = QFont(self.font()); f.setPointSizeF(size); f.setBold(bold)
        return f

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        c, r = self._geom()
        cx, cy = c.x(), c.y()

        # outer ring
        p.setPen(QPen(self._ring, max(2.0, r * 0.05)))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(c, r, r)

        # tick marks every 15°, majors at the 8 cardinal/intercardinal points
        for a in range(0, 360, 15):
            sa = self._rose_angle(a)
            dx, dy = self._dir(sa)
            major = (a % 45 == 0)
            r_in = r * (0.84 if major else 0.90)
            col = self._cardinal if major else self._tick
            p.setPen(QPen(col, 2.0 if major else 1.0))
            p.drawLine(QPointF(cx + dx * r_in, cy + dy * r_in),
                       QPointF(cx + dx * r * 0.97, cy + dy * r * 0.97))

        # cardinal labels — rect sized to the measured text so 2-letter points
        # (NE/SE/SW/NW) never truncate at any widget size
        p.setFont(self._f(max(8.0, r * 0.16), bold=True))
        fm = p.fontMetrics()
        for name, a in _CARDINALS:
            if len(name) == 2 and not self._show_inter:
                continue
            sa = self._rose_angle(a)
            dx, dy = self._dir(sa)
            lx, ly = cx + dx * r * 0.70, cy + dy * r * 0.70
            col = self._north if name == "N" else self._cardinal
            p.setPen(QPen(col))
            tw = fm.horizontalAdvance(name) + 4
            p.drawText(QRectF(lx - tw / 2.0, ly - fm.height() / 2.0, tw, fm.height()),
                       Qt.AlignCenter, name)

        self._paint_needle(p, c, r)

        # hub + centre readout (drawn over the needle's centre crossing)
        hub = r * 0.37
        p.setPen(QPen(self._ring, 1.5))
        p.setBrush(QBrush(self._hub))
        p.drawEllipse(c, hub, hub)
        if self._show_readout:
            card = self.cardinal16(self._heading)
            bf = self._f(max(9.0, r * 0.28), bold=True)
            p.setFont(bf)
            adv = p.fontMetrics().horizontalAdvance(card)
            maxw = hub * 1.7                          # keep 3-letter points inside the hub
            if adv > maxw > 0:
                bf.setPointSizeF(bf.pointSizeF() * maxw / adv)
                p.setFont(bf)
            bfm = p.fontMetrics()
            p.setPen(QPen(self._readout))
            p.drawText(QRectF(cx - hub, cy - bfm.height() * 0.60, 2 * hub, bfm.height()),
                       Qt.AlignCenter, card)
            p.setFont(self._f(max(7.0, r * 0.12)))
            p.setPen(QPen(QColor(self._readout).darker(160) if self._readout.lightness() > 128
                          else QColor(self._readout).lighter(160)))
            p.drawText(QRectF(cx - hub, cy + bfm.height() * 0.20, 2 * hub, r * 0.16),
                       Qt.AlignCenter, "%d°" % round(self._heading))
        p.end()

    def _paint_needle(self, p, c, r):
        cx, cy = c.x(), c.y()
        # in bezel mode the needle is fixed pointing up; else it points to heading
        ang = 0.0 if self._rotate_bezel else self._disp
        dx, dy = self._dir(ang)          # tip direction (north half)
        px, py = -dy, dx                 # perpendicular
        tip = r * 0.80
        base = r * 0.12
        tail = r * 0.62
        p.setPen(Qt.NoPen)
        # north (coloured) half
        path = QPainterPath()
        path.moveTo(cx + dx * tip, cy + dy * tip)
        path.lineTo(cx + px * base, cy + py * base)
        path.lineTo(cx - px * base, cy - py * base)
        path.closeSubpath()
        p.setBrush(QBrush(self._north))
        p.drawPath(path)
        # south (muted) half
        path2 = QPainterPath()
        path2.moveTo(cx - dx * tail, cy - dy * tail)
        path2.lineTo(cx + px * base, cy + py * base)
        path2.lineTo(cx - px * base, cy - py * base)
        path2.closeSubpath()
        p.setBrush(QBrush(self._south))
        p.drawPath(path2)

    # ------------------------------------------------------------------ #
    ## Interaction (drag around the centre to set the heading)
    # ------------------------------------------------------------------ #
    def _heading_at(self, pos):
        c, _ = self._geom()
        return math.degrees(math.atan2(pos.x() - c.x(), -(pos.y() - c.y()))) % 360.0

    def mousePressEvent(self, e):
        if self._interactive and e.button() == Qt.LeftButton:
            pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
            self.setHeading(self._heading_at(pos))
            return
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self._interactive and (e.buttons() & Qt.LeftButton):
            pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
            self.setHeading(self._heading_at(pos))
            return
        super().mouseMoveEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(float)
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, v):
        self.setHeading(v)

    @Property(bool)
    def rotateBezel(self):
        return self._rotate_bezel

    @rotateBezel.setter
    def rotateBezel(self, v):
        self._rotate_bezel = bool(v)
        self.update()

    @Property(bool)
    def showIntercardinals(self):
        return self._show_inter

    @showIntercardinals.setter
    def showIntercardinals(self, v):
        self._show_inter = bool(v)
        self.update()

    @Property(bool)
    def showReadout(self):
        return self._show_readout

    @showReadout.setter
    def showReadout(self, v):
        self._show_readout = bool(v)
        self.update()

    @Property(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, v):
        self._animated = bool(v)

    @Property(bool)
    def interactive(self):
        return self._interactive

    @interactive.setter
    def interactive(self, v):
        self._interactive = bool(v)
        self.setCursor(Qt.PointingHandCursor if v else Qt.ArrowCursor)

    @Property(QColor)
    def northColor(self):
        return self._north

    @northColor.setter
    def northColor(self, c):
        self._north = QColor(c); self.update()

    @Property(QColor)
    def southColor(self):
        return self._south

    @southColor.setter
    def southColor(self, c):
        self._south = QColor(c); self.update()

    @Property(QColor)
    def ringColor(self):
        return self._ring

    @ringColor.setter
    def ringColor(self, c):
        self._ring = QColor(c); self.update()

    @Property(QColor)
    def tickColor(self):
        return self._tick

    @tickColor.setter
    def tickColor(self, c):
        self._tick = QColor(c); self.update()

    @Property(QColor)
    def cardinalColor(self):
        return self._cardinal

    @cardinalColor.setter
    def cardinalColor(self, c):
        self._cardinal = QColor(c); self.update()

    @Property(QColor)
    def readoutColor(self):
        return self._readout

    @readoutColor.setter
    def readoutColor(self, c):
        self._readout = QColor(c); self.update()

    @Property(QColor)
    def hubColor(self):
        return self._hub

    @hubColor.setter
    def hubColor(self, c):
        self._hub = QColor(c); self.update()
