########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomCompassDial - a PREMIUM beveled instrument compass.
##
## The skeuomorphic-modern map compass (the Haulix "NW" dial): a beveled metal
## RIM (top-lit / bottom-shadowed gradient), a domed glass FACE (radial gradient),
## a fine watch-bezel TICK ring with brass majors at the cardinals, N/E/S/W (+
## intercardinals), a slim two-tone needle and a metallic CENTRE CAP carrying the
## 16-point heading readout + degrees. All painted (gradients, not effects), so it
## recolours with the theme and stays crisp.
##
## Sibling of the flat QCustomCompass — same API (heading 0-360, rotateBezel,
## animated shortest-path ease, drag-to-set, headingChanged) with the premium
## look. Text is measured to fit (never overflows / truncates).
########################################################################
import math

from qtpy.QtCore import Qt, Property, Signal, QRectF, QPointF, QTimer
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QFont, QPainterPath,
                        QLinearGradient, QRadialGradient)
from qtpy.QtWidgets import QWidget, QSizePolicy

_POINTS16 = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
             "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
_CARDINALS = [("N", 0), ("NE", 45), ("E", 90), ("SE", 135),
              ("S", 180), ("SW", 225), ("W", 270), ("NW", 315)]


class QCustomCompassDial(QWidget):

    headingChanged = Signal(float)

    WIDGET_ICON = "components/icons/compass.png"
    WIDGET_TOOLTIP = "A premium beveled instrument compass"
    WIDGET_MODULE = "Custom_Widgets.QCustomCompassDial"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCompassDial' name='customCompassDial'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>220</width><height>220</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCompassDial",
        "props": {
            "heading": {"type": "float", "default": 315.0},
            "rotateBezel": {"type": "bool", "default": False},
            "showIntercardinals": {"type": "bool", "default": True},
            "showReadout": {"type": "bool", "default": True},
            "animated": {"type": "bool", "default": True},
            "interactive": {"type": "bool", "default": True},
            "bezelColor": {"type": "color", "default": "#2a303c"},
            "faceColor": {"type": "color", "default": "#20262f"},
            "accentColor": {"type": "color", "default": "#c8a24a"},
            "tickColor": {"type": "color", "default": "#5b6472"},
            "cardinalColor": {"type": "color", "default": "#e7ecf4"},
            "northColor": {"type": "color", "default": "#e0463c"},
            "southColor": {"type": "color", "default": "#aeb6c2"},
            "capColor": {"type": "color", "default": "#272e39"},
            "readoutColor": {"type": "color", "default": "#f4f6fb"},
        },
        "signals": ["headingChanged"],
        "tokens_used": ["accent", "down"],
    }

    def __init__(self, parent=None, heading=315.0):
        super().__init__(parent)
        self.setObjectName("QCustomCompassDial")
        self._heading = float(heading) % 360.0
        self._disp = self._heading
        self._rotate_bezel = False
        self._show_inter = True
        self._show_readout = True
        self._animated = True
        self._interactive = True
        self._bezel = QColor("#2a303c")
        self._face = QColor("#20262f")
        self._accent = QColor("#c8a24a")
        self._tick = QColor("#5b6472")
        self._cardinal = QColor("#e7ecf4")
        self._north = QColor("#e0463c")
        self._south = QColor("#aeb6c2")
        self._cap = QColor("#272e39")
        self._readout = QColor("#f4f6fb")
        self._timer = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(96, 96)

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
        r = side * 0.46
        return QPointF(self.width() / 2.0, self.height() / 2.0), max(r, 10.0)

    def _dir(self, compass_deg):
        a = math.radians(compass_deg)
        return math.sin(a), -math.cos(a)

    def _rose_angle(self, a):
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

        # 1) beveled metal rim — top-lit, bottom-shadowed gradient
        rim_w = r * 0.15
        lg = QLinearGradient(cx, cy - r, cx, cy + r)
        lg.setColorAt(0.0, self._bezel.lighter(175))
        lg.setColorAt(0.5, self._bezel)
        lg.setColorAt(1.0, self._bezel.darker(200))
        pen = QPen(QBrush(lg), rim_w)
        p.setPen(pen); p.setBrush(Qt.NoBrush)
        p.drawEllipse(c, r - rim_w / 2.0, r - rim_w / 2.0)

        # 2) domed glass face — radial gradient, light from the top
        face_r = r - rim_w
        rg = QRadialGradient(cx, cy - face_r * 0.4, face_r * 1.35)
        rg.setColorAt(0.0, self._face.lighter(135))
        rg.setColorAt(1.0, self._face.darker(115))
        p.setPen(Qt.NoPen); p.setBrush(QBrush(rg))
        p.drawEllipse(c, face_r, face_r)
        # thin bright inner edge where the rim meets the face
        p.setPen(QPen(QColor(255, 255, 255, 26), 1.0)); p.setBrush(Qt.NoBrush)
        p.drawEllipse(c, face_r - 1, face_r - 1)

        # 3) fine watch-bezel ticks, brass majors at the 8 cardinal points
        for a in range(0, 360, 6):
            sa = self._rose_angle(a)
            dx, dy = self._dir(sa)
            major = (a % 45 == 0)
            r_in = face_r * (0.84 if major else 0.91)
            p.setPen(QPen(self._accent if major else self._tick, 2.2 if major else 1.0))
            p.drawLine(QPointF(cx + dx * r_in, cy + dy * r_in),
                       QPointF(cx + dx * face_r * 0.97, cy + dy * face_r * 0.97))

        # 4) cardinal labels (rect sized to the string -> never truncates)
        p.setFont(self._f(max(8.0, face_r * 0.16), bold=True))
        fm = p.fontMetrics()
        for name, a in _CARDINALS:
            if len(name) == 2 and not self._show_inter:
                continue
            sa = self._rose_angle(a)
            dx, dy = self._dir(sa)
            lx, ly = cx + dx * face_r * 0.70, cy + dy * face_r * 0.70
            p.setPen(QPen(self._accent if name == "N" else self._cardinal))
            tw = fm.horizontalAdvance(name) + 4
            p.drawText(QRectF(lx - tw / 2.0, ly - fm.height() / 2.0, tw, fm.height()),
                       Qt.AlignCenter, name)

        self._paint_needle(p, c, face_r)
        self._paint_cap(p, c, face_r)
        p.end()

    def _paint_needle(self, p, c, r):
        cx, cy = c.x(), c.y()
        ang = 0.0 if self._rotate_bezel else self._disp
        dx, dy = self._dir(ang)
        px, py = -dy, dx
        tip = r * 0.78
        base = r * 0.09
        tail = r * 0.58
        p.setPen(Qt.NoPen)
        north = QPainterPath()
        north.moveTo(cx + dx * tip, cy + dy * tip)
        north.lineTo(cx + px * base, cy + py * base)
        north.lineTo(cx - px * base, cy - py * base)
        north.closeSubpath()
        p.setBrush(QBrush(self._north)); p.drawPath(north)
        south = QPainterPath()
        south.moveTo(cx - dx * tail, cy - dy * tail)
        south.lineTo(cx + px * base, cy + py * base)
        south.lineTo(cx - px * base, cy - py * base)
        south.closeSubpath()
        p.setBrush(QBrush(self._south)); p.drawPath(south)

    def _paint_cap(self, p, c, r):
        cx, cy = c.x(), c.y()
        cap = r * 0.36
        rg = QRadialGradient(cx, cy - cap * 0.4, cap * 1.4)
        rg.setColorAt(0.0, self._cap.lighter(150))
        rg.setColorAt(1.0, self._cap.darker(120))
        p.setPen(QPen(self._bezel.darker(150), 1.2))
        p.setBrush(QBrush(rg))
        p.drawEllipse(c, cap, cap)
        if not self._show_readout:
            return
        card = self.cardinal16(self._heading)
        bf = self._f(max(9.0, r * 0.24), bold=True)
        p.setFont(bf)
        adv = p.fontMetrics().horizontalAdvance(card)
        maxw = cap * 1.66
        if adv > maxw > 0:
            bf.setPointSizeF(bf.pointSizeF() * maxw / adv)
            p.setFont(bf)
        bfm = p.fontMetrics()
        p.setPen(QPen(self._readout))
        p.drawText(QRectF(cx - cap, cy - bfm.height() * 0.62, 2 * cap, bfm.height()),
                   Qt.AlignCenter, card)
        p.setFont(self._f(max(7.0, r * 0.11)))
        p.setPen(QPen(self._accent))
        p.drawText(QRectF(cx - cap, cy + bfm.height() * 0.18, 2 * cap, r * 0.16),
                   Qt.AlignCenter, "%d°" % round(self._heading))

    # ------------------------------------------------------------------ #
    ## Interaction
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
        self._rotate_bezel = bool(v); self.update()

    @Property(bool)
    def showIntercardinals(self):
        return self._show_inter

    @showIntercardinals.setter
    def showIntercardinals(self, v):
        self._show_inter = bool(v); self.update()

    @Property(bool)
    def showReadout(self):
        return self._show_readout

    @showReadout.setter
    def showReadout(self, v):
        self._show_readout = bool(v); self.update()

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
    def bezelColor(self):
        return self._bezel

    @bezelColor.setter
    def bezelColor(self, c):
        self._bezel = QColor(c); self.update()

    @Property(QColor)
    def faceColor(self):
        return self._face

    @faceColor.setter
    def faceColor(self, c):
        self._face = QColor(c); self.update()

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c); self.update()

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
    def capColor(self):
        return self._cap

    @capColor.setter
    def capColor(self, c):
        self._cap = QColor(c); self.update()

    @Property(QColor)
    def readoutColor(self):
        return self._readout

    @readoutColor.setter
    def readoutColor(self, c):
        self._readout = QColor(c); self.update()
