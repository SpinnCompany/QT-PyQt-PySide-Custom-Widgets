########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomGradientText - text filled with a gradient.
##
## The headline treatment every landing page wants and QSS cannot do: Qt
## stylesheets have no text-fill gradient, so the only route is painting the
## text with a gradient pen.
##
## Optionally animated, sliding the gradient along the text. The animation is
## off by default - a permanently shimmering headline is a distraction, and it
## costs a repaint per frame.
##
## Reuses the multi-stop CSV convention from QCustomGradientPicker, so a
## gradient authored there drops straight in.
########################################################################
from qtpy.QtCore import (Qt, Signal, Property, QRectF, QSize, QPointF, QTimer)
from qtpy.QtGui import (QColor, QPainter, QPen, QLinearGradient, QFontMetrics,
                        QFont)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomGradientText(QWidget):
    clicked = Signal()

    WIDGET_ICON = "components/icons/gradient.png"
    WIDGET_TOOLTIP = "Text filled with a gradient"
    WIDGET_MODULE = "Custom_Widgets.QCustomGradientText"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomGradientText' name='customGradientText'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>52</height></rect></property>
            <property name='text'><string>Build something great</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomGradientText",
        "props": {"text": {"type": "string", "default": ""},
                  "stopsCsv": {"type": "string", "default": "0:#2563eb,1:#a855f7"},
                  "angle": {"type": "int", "default": 0},
                  "animated": {"type": "bool", "default": False},
                  "animationSpeed": {"type": "int", "default": 40},
                  "fontScale": {"type": "float", "default": 1.6},
                  "bold": {"type": "bool", "default": True},
                  "alignment": {"type": "enum",
                                "values": ["left", "center", "right"],
                                "default": "center"},
                  "wordWrap": {"type": "bool", "default": False}},
        "signals": ["clicked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, text="", stops=None):
        super().__init__(parent)
        self.setObjectName("QCustomGradientText")
        self._text = str(text)
        self._stops = []
        self._angle = 0
        self._animated = False
        self._speed = 40
        self._offset = 0.0
        self._fontScale = 1.6
        self._bold = True
        self._alignment = "center"
        self._wordWrap = False

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)

        self.setStops(stops or [(0.0, "#2563eb"), (1.0, "#a855f7")])

    # ------------------------------------------------------------------ #
    ## Gradient
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coerceStop(stop):
        if isinstance(stop, dict):
            pos, colour = stop.get("position"), stop.get("color")
        elif isinstance(stop, (tuple, list)) and len(stop) >= 2:
            pos, colour = stop[0], stop[1]
        else:
            return None
        try:
            pos = float(pos)
        except (TypeError, ValueError):
            return None
        colour = QColor(colour)
        if not colour.isValid():
            return None
        return (min(1.0, max(0.0, pos)), colour)

    def setStops(self, stops):
        """Replace the gradient stops. Fewer than two is rejected.

        Same rule as QCustomGradientPicker: one stop is a fill, and allowing
        it would make every consumer handle a degenerate gradient.
        """
        parsed = [s for s in (self._coerceStop(x) for x in (stops or [])) if s]
        if len(parsed) < 2:
            return False
        parsed.sort(key=lambda s: s[0])
        self._stops = parsed
        self.update()
        return True

    def stops(self):
        return [(pos, QColor(colour)) for pos, colour in self._stops]

    def gradientFor(self, rect):
        """The gradient across a rect, including the animation offset."""
        import math
        radians = math.radians(self._angle)
        dx, dy = math.cos(radians), math.sin(radians)
        cx, cy = rect.center().x(), rect.center().y()
        half_w, half_h = rect.width() / 2.0, rect.height() / 2.0
        gradient = QLinearGradient(QPointF(cx - dx * half_w, cy - dy * half_h),
                                   QPointF(cx + dx * half_w, cy + dy * half_h))
        if self._animated and self._offset:
            # Wrap the stops so the gradient slides seamlessly rather than
            # snapping back when the offset passes 1.
            for pos, colour in self._stops:
                gradient.setColorAt((pos + self._offset) % 1.0, colour)
        else:
            for pos, colour in self._stops:
                gradient.setColorAt(pos, colour)
        return gradient

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
        self._offset = (self._offset + 0.02) % 1.0
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _scaledFont(self):
        font = QFont(self.font())
        font.setBold(self._bold)
        size = font.pointSizeF()
        if size > 0:
            font.setPointSizeF(size * max(0.1, self._fontScale))
        return font

    def sizeHint(self):
        fm = QFontMetrics(self._scaledFont())
        if self._wordWrap:
            return QSize(320, fm.height() * 2 + 12)
        return QSize(fm.horizontalAdvance(self._text) + 16, fm.height() + 12)

    minimumSizeHint = sizeHint

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if not self._text or len(self._stops) < 2:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setFont(self._scaledFont())
        rect = QRectF(8, 4, max(1.0, self.width() - 16),
                      max(1.0, self.height() - 8))
        # A gradient PEN fills the glyphs themselves; a gradient brush would
        # fill the background behind them instead.
        pen = QPen()
        pen.setBrush(self.gradientFor(rect))
        p.setPen(pen)
        flags = {"left": Qt.AlignLeft, "right": Qt.AlignRight}.get(
            self._alignment, Qt.AlignHCenter)
        if self._wordWrap:
            flags |= Qt.TextWordWrap
        p.drawText(rect, int(flags | Qt.AlignVCenter), self._text)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(e)

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
    def stopsCsv(self):
        return ",".join("%g:%s" % (pos, colour.name())
                        for pos, colour in self._stops)

    @stopsCsv.setter
    def stopsCsv(self, text):
        parsed = []
        for token in str(text).replace(";", ",").split(","):
            token = token.strip()
            if not token or ":" not in token:
                continue
            pos, _, colour = token.partition(":")
            parsed.append((pos.strip(), colour.strip()))
        self.setStops(parsed)

    @Property(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = int(value) % 360
        self.update()

    @Property(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, value):
        self._animated = bool(value)
        if self._animated:
            self.start()
        else:
            self.stop()
            self._offset = 0.0
            self.update()

    @Property(int)
    def animationSpeed(self):
        return self._speed

    @animationSpeed.setter
    def animationSpeed(self, value):
        self._speed = max(0, int(value))
        if self._timer.isActive():
            self.start()

    @Property(float)
    def fontScale(self):
        return self._fontScale

    @fontScale.setter
    def fontScale(self, value):
        self._fontScale = max(0.1, float(value))
        self.updateGeometry(); self.update()

    @Property(bool)
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, value):
        self._bold = bool(value)
        self.updateGeometry(); self.update()

    @Property(str)
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        value = str(value)
        self._alignment = value if value in ("left", "center", "right") else "center"
        self.update()

    @Property(bool)
    def wordWrap(self):
        return self._wordWrap

    @wordWrap.setter
    def wordWrap(self, value):
        self._wordWrap = bool(value)
        self.updateGeometry(); self.update()
