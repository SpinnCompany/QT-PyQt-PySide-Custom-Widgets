########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomTrendChip - a directional delta / trend indicator.
##
## A painted up/down/flat arrow that colour-codes a change (green up, red down,
## grey flat) with an optional value label. Three looks:
##   variant="circle" (default) - just the arrow in a tinted circle (the classic
##       income/expense chip); square, icon-only.
##   variant="soft"   - a rounded pill: tinted background + arrow + text.
##   variant="plain"  - arrow + text, no background.
## Direction is set explicitly or inferred from a numeric value's sign. The arrow
## is drawn with QPainter (no glyph font), so it is crisp and theme-tokenisable.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF, QPointF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFont
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomTrendChip(QWidget):

    WIDGET_ICON = "components/icons/trend.png"
    WIDGET_TOOLTIP = "A directional delta / trend chip (up/down arrow)"
    WIDGET_MODULE = "Custom_Widgets.QCustomTrendChip"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTrendChip' name='customTrendChip'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>90</width><height>30</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomTrendChip",
        "props": {"text": {"type": "string", "default": ""},
                  "direction": {"type": "enum", "values": ["up", "down", "flat"], "default": "up"},
                  "variant": {"type": "enum", "values": ["circle", "soft", "plain"], "default": "circle"},
                  "upColor": {"type": "color", "default": "#22c07e"},
                  "downColor": {"type": "color", "default": "#f2704e"},
                  "flatColor": {"type": "color", "default": "#8b909e"},
                  "tintOpacity": {"type": "float", "default": 0.14},
                  "cornerRadius": {"type": "int", "default": 15}},
        "signals": [],
        "tokens_used": ["up", "down"],
    }

    def __init__(self, parent=None, direction="up", text="", variant="circle"):
        super().__init__(parent)
        self.setObjectName("QCustomTrendChip")
        self._direction = direction if direction in ("up", "down", "flat") else "up"
        self._text = str(text)
        self._variant = variant if variant in ("circle", "soft", "plain") else "circle"
        self._up = QColor("#22c07e")
        self._down = QColor("#f2704e")
        self._flat = QColor("#8b909e")
        self._tint = 0.14
        self._radius = 15
        self._arrow_w = 2.4
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._sync_size_policy()

    def _sync_size_policy(self):
        if self._variant == "circle":
            self.setMinimumSize(28, 28)
        else:
            self.setMinimumSize(48, 26)

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setDirection(self, direction):
        if direction in ("up", "down", "flat"):
            self._direction = direction
            self.update()

    def setValue(self, value, text=None):
        """Set direction from a number's sign; optionally format the label."""
        v = float(value)
        self._direction = "up" if v > 0 else "down" if v < 0 else "flat"
        if text is not None:
            self._text = str(text)
        self.update()

    def setText(self, text):
        self._text = str(text)
        self.update()

    def setVariant(self, variant):
        if variant in ("circle", "soft", "plain"):
            self._variant = variant
            self._sync_size_policy()
            self.updateGeometry()
            self.update()

    def _color(self):
        return {"up": self._up, "down": self._down, "flat": self._flat}[self._direction]

    def sizeHint(self):
        from qtpy.QtCore import QSize
        if self._variant == "circle":
            return QSize(30, 30)
        w = 54
        if self._text:
            fm = self.fontMetrics()
            w = 40 + fm.horizontalAdvance(self._text)
        return QSize(w, 30)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def _draw_arrow(self, p, box, color):
        """Draw a directional arrow inside the square ``box`` (QRectF)."""
        pen = QPen(color, self._arrow_w)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        pad = box.width() * 0.26
        x0, y0 = box.left() + pad, box.top() + pad
        x1, y1 = box.right() - pad, box.bottom() - pad
        head = box.width() * 0.30
        if self._direction == "up":
            a, b = QPointF(x0, y1), QPointF(x1, y0)        # bottom-left -> top-right
            p.drawLine(a, b)
            p.drawLine(b, QPointF(b.x() - head, b.y()))
            p.drawLine(b, QPointF(b.x(), b.y() + head))
        elif self._direction == "down":
            a, b = QPointF(x0, y0), QPointF(x1, y1)        # top-left -> bottom-right
            p.drawLine(a, b)
            p.drawLine(b, QPointF(b.x() - head, b.y()))
            p.drawLine(b, QPointF(b.x(), b.y() - head))
        else:
            my = box.center().y()
            a, b = QPointF(x0, my), QPointF(x1, my)        # flat ->
            p.drawLine(a, b)
            p.drawLine(b, QPointF(b.x() - head, b.y() - head * 0.7))
            p.drawLine(b, QPointF(b.x() - head, b.y() + head * 0.7))

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        color = self._color()
        tint = QColor(color)
        tint.setAlphaF(self._tint)
        h = self.height()

        if self._variant == "circle":
            side = min(self.width(), h)
            box = QRectF((self.width() - side) / 2.0, (h - side) / 2.0, side, side)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(tint))
            p.drawEllipse(box)
            self._draw_arrow(p, box, color)
            p.end()
            return

        # soft / plain: [arrow box][text]
        box_side = min(h, 24)
        if self._variant == "soft":
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(tint))
            p.drawRoundedRect(QRectF(0.5, 0.5, self.width() - 1, h - 1),
                              self._radius, self._radius)
        pad = 8 if self._variant == "soft" else 0
        box = QRectF(pad, (h - box_side) / 2.0, box_side, box_side)
        self._draw_arrow(p, box, color)
        if self._text:
            f = QFont(self.font())
            f.setBold(True)
            p.setFont(f)
            p.setPen(QPen(color))
            tx = box.right() + 6
            p.drawText(QRectF(tx, 0, self.width() - tx - pad, h),
                       Qt.AlignLeft | Qt.AlignVCenter, self._text)
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def text(self):
        return self._text

    @text.setter
    def text(self, v):
        self.setText(v)

    @Property(str)
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, v):
        self.setDirection(str(v))

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, v):
        self.setVariant(str(v))

    @Property(QColor)
    def upColor(self):
        return self._up

    @upColor.setter
    def upColor(self, c):
        self._up = QColor(c)
        self.update()

    @Property(QColor)
    def downColor(self):
        return self._down

    @downColor.setter
    def downColor(self, c):
        self._down = QColor(c)
        self.update()

    @Property(QColor)
    def flatColor(self):
        return self._flat

    @flatColor.setter
    def flatColor(self, c):
        self._flat = QColor(c)
        self.update()

    @Property(float)
    def tintOpacity(self):
        return self._tint

    @tintOpacity.setter
    def tintOpacity(self, v):
        self._tint = max(0.0, min(1.0, float(v)))
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()
