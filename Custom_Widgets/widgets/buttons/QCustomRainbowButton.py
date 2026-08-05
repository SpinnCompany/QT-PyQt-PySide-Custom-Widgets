########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomRainbowButton - a button with an animated conic border.
##
## The "shiny" call-to-action: a colour wheel rotating around the rim. QSS
## cannot animate a gradient, so the border is painted and the rotation driven
## by a timer.
##
## The animation stops when the widget is hidden. A permanently repainting
## button on an invisible page is pure battery drain, and it is the kind of
## thing nobody notices until a laptop fan tells them.
##
## Emits clicked().
########################################################################
import math

from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QTimer
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QConicalGradient,
                        QFontMetrics, QPainterPath)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomRainbowButton(QWidget):
    clicked = Signal()

    WIDGET_ICON = "components/icons/auto_awesome.png"
    WIDGET_TOOLTIP = "A button with an animated rainbow border"
    WIDGET_MODULE = "Custom_Widgets.QCustomRainbowButton"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRainbowButton' name='customRainbowButton'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>180</width><height>44</height></rect></property>
            <property name='text'><string>Get started</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRainbowButton",
        "props": {"text": {"type": "string", "default": "Get started"},
                  "colorsCsv": {"type": "string",
                                "default": "#2563eb,#a855f7,#ec4899,#f59e0b,#16a34a,#2563eb"},
                  "borderWidth": {"type": "int", "default": 3},
                  "cornerRadius": {"type": "int", "default": 10},
                  "speed": {"type": "int", "default": 40},
                  "animated": {"type": "bool", "default": True},
                  "glow": {"type": "bool", "default": False},
                  "filled": {"type": "bool", "default": False},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"},
                  "textColor": {"type": "color", "default": "#0f172a"},
                  "surfaceColor": {"type": "color", "default": "#ffffff"}},
        "signals": ["clicked"],
        "tokens_used": ["surface", "on-surface"],
    }

    _DEFAULT_COLORS = ["#2563eb", "#a855f7", "#ec4899", "#f59e0b", "#16a34a",
                       "#2563eb"]
    _HEIGHTS = {"sm": 34, "md": 44, "lg": 54}

    def __init__(self, parent=None, text="Get started"):
        super().__init__(parent)
        self.setObjectName("QCustomRainbowButton")
        self._text = str(text)
        self._colors = [QColor(c) for c in self._DEFAULT_COLORS]
        self._borderWidth = 3
        self._radius = 10
        self._speed = 40
        self._animated = True
        self._glow = False
        self._filled = False
        self._sizeVariant = "md"
        self._angle = 0.0
        self._hovered = False

        self._textColor = QColor("#0f172a")
        self._surface = QColor("#ffffff")

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)

    # ------------------------------------------------------------------ #
    ## Animation
    # ------------------------------------------------------------------ #
    def start(self):
        if self._animated and self._speed > 0:
            self._timer.start(max(16, self._speed))
            return True
        return False

    def stop(self):
        self._timer.stop()

    def isAnimating(self):
        return self._timer.isActive()

    def _advance(self):
        self._angle = (self._angle + 4.0) % 360.0
        self.update()

    def showEvent(self, e):
        super().showEvent(e)
        self.start()

    def hideEvent(self, e):
        # Repainting a button nobody can see is pure battery drain.
        self.stop()
        super().hideEvent(e)

    # ------------------------------------------------------------------ #
    ## Colours
    # ------------------------------------------------------------------ #
    def setColors(self, colors):
        """Replace the wheel. Fewer than two valid colours is rejected."""
        parsed = [QColor(c) for c in (colors or [])]
        parsed = [c for c in parsed if c.isValid()]
        if len(parsed) < 2:
            return False
        self._colors = parsed
        self.update()
        return True

    def colors(self):
        return [QColor(c) for c in self._colors]

    def _conical(self, rect):
        gradient = QConicalGradient(rect.center(), self._angle)
        count = len(self._colors)
        for index, colour in enumerate(self._colors):
            gradient.setColorAt(index / float(max(1, count - 1)), colour)
        return gradient

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _height(self):
        return self._HEIGHTS.get(self._sizeVariant, self._HEIGHTS["md"])

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        height = self._height()
        return QSize(fm.horizontalAdvance(self._text) + height + 24, height)

    def minimumSizeHint(self):
        return QSize(self._height(), self._height())

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        border = float(self._borderWidth)
        outer = QRectF(border / 2.0, border / 2.0,
                       self.width() - border, self.height() - border)
        gradient = self._conical(outer)

        if self._glow:
            # A soft outer echo, painted rather than a drop shadow (the design
            # bar rejects QGraphicsDropShadowEffect).
            glow = QRectF(0, 0, self.width(), self.height())
            pen = QPen(QBrush(gradient), border * 2.5)
            pen.setCapStyle(Qt.RoundCap)
            colour = QColor(self._colors[0])
            colour.setAlphaF(0.22)
            p.setPen(QPen(colour, border * 2.5))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(glow.adjusted(1, 1, -1, -1),
                              self._radius + 2, self._radius + 2)

        if self._filled:
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(gradient))
            p.drawRoundedRect(outer, self._radius, self._radius)
            foreground = self._surface
        else:
            p.setPen(QPen(QBrush(gradient), border))
            p.setBrush(QBrush(self._surface if not self._hovered
                              else self._surface.darker(103)))
            p.drawRoundedRect(outer, self._radius, self._radius)
            foreground = self._textColor

        p.setPen(QPen(foreground))
        p.drawText(outer, int(Qt.AlignCenter), self._text)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def enterEvent(self, e):
        self._hovered = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovered = False
        self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.clicked.emit()
            return
        super().keyPressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self.updateGeometry(); self.update()

    @Property(str)
    def colorsCsv(self):
        return ",".join(c.name() for c in self._colors)

    @colorsCsv.setter
    def colorsCsv(self, text):
        self.setColors([t.strip() for t in str(text).replace(";", ",").split(",")
                        if t.strip()])

    @Property(int)
    def borderWidth(self):
        return self._borderWidth

    @borderWidth.setter
    def borderWidth(self, value):
        self._borderWidth = max(1, int(value)); self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, value):
        self._radius = max(0, int(value)); self.update()

    @Property(int)
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = max(0, int(value))
        if self._timer.isActive():
            self.start()

    @Property(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, value):
        self._animated = bool(value)
        if self._animated and self.isVisible():
            self.start()
        elif not self._animated:
            self.stop()

    @Property(bool)
    def glow(self):
        return self._glow

    @glow.setter
    def glow(self, value):
        self._glow = bool(value); self.update()

    @Property(bool)
    def filled(self):
        return self._filled

    @filled.setter
    def filled(self, value):
        self._filled = bool(value); self.update()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self.updateGeometry(); self.update()

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()

    @Property(QColor)
    def surfaceColor(self):
        return self._surface

    @surfaceColor.setter
    def surfaceColor(self, c):
        self._surface = QColor(c); self.update()
