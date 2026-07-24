########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomMessageStatus - a delivery-state tick indicator.
##
## The little "read receipt" ticks next to an outgoing message's time:
##   sending    -> a small clock
##   sent       -> one check
##   delivered  -> two checks
##   read       -> two checks in the accent/read colour
## The ticks are PAINTED (crisp at any size, no glyph/asset) and the colours are
## qproperties so they track the theme. Set the state with the `status` Designer
## property or setStatus("read").
########################################################################
from qtpy.QtCore import Qt, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QPen, QPolygonF
from qtpy.QtCore import QPointF
from qtpy.QtWidgets import QWidget, QSizePolicy


_STATES = ("sending", "sent", "delivered", "read")


class QCustomMessageStatus(QWidget):

    WIDGET_ICON = "components/icons/message_status.png"
    WIDGET_TOOLTIP = "A delivery-state tick indicator (sent / delivered / read)"
    WIDGET_MODULE = "Custom_Widgets.QCustomMessageStatus"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomMessageStatus' name='customMessageStatus'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>22</width><height>14</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomMessageStatus",
        "props": {
            "status": {"type": "enum", "values": list(_STATES), "default": "read"},
            "tickColor": {"type": "color", "default": "#99a0b0"},
            "readColor": {"type": "color", "default": "#1b74e4"},
            "tickSize": {"type": "int", "default": 13},
        },
        "signals": [],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomMessageStatus")
        self._status = "read"
        self._tick = QColor("#99a0b0")
        self._read = QColor("#1b74e4")
        self._size = 13
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._updateFixed()

    def _updateFixed(self):
        double = self._status in ("delivered", "read")
        w = self._size + (self._size * 0.42 if double else 0) + 4
        self.setFixedSize(int(w), int(self._size + 2))
        self.update()

    def setStatus(self, s):
        s = str(s)
        self._status = s if s in _STATES else "sent"
        self._updateFixed()

    # ------------------------------------------------------------------ #
    ## Paint
    # ------------------------------------------------------------------ #
    def _drawCheck(self, p, x, cy, s, color):
        pen = QPen(color, max(1.4, s * 0.13))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.drawPolyline(QPolygonF([
            QPointF(x, cy + s * 0.06),
            QPointF(x + s * 0.34, cy + s * 0.36),
            QPointF(x + s * 0.98, cy - s * 0.34),
        ]))

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        s = float(self._size)
        cy = self.height() / 2.0
        if self._status == "sending":
            # a small clock: circle + two hands
            col = QColor(self._tick)
            pen = QPen(col, max(1.3, s * 0.11))
            pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            d = s * 0.86
            rect = QRectF(1, cy - d / 2, d, d)
            p.drawEllipse(rect)
            c = rect.center()
            p.drawLine(c, QPointF(c.x(), c.y() - d * 0.28))
            p.drawLine(c, QPointF(c.x() + d * 0.22, c.y()))
            p.end()
            return
        color = self._read if self._status == "read" else self._tick
        if self._status in ("delivered", "read"):
            self._drawCheck(p, 1, cy, s, color)
            self._drawCheck(p, 1 + s * 0.42, cy, s, color)
        else:  # sent
            self._drawCheck(p, 1 + s * 0.20, cy, s, color)
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def status(self):
        return self._status

    @status.setter
    def status(self, v):
        self.setStatus(v)

    @Property(QColor)
    def tickColor(self):
        return self._tick

    @tickColor.setter
    def tickColor(self, c):
        self._tick = QColor(c)
        self.update()

    @Property(QColor)
    def readColor(self):
        return self._read

    @readColor.setter
    def readColor(self, c):
        self._read = QColor(c)
        self.update()

    @Property(int)
    def tickSize(self):
        return self._size

    @tickSize.setter
    def tickSize(self, v):
        self._size = max(8, int(v))
        self._updateFixed()
