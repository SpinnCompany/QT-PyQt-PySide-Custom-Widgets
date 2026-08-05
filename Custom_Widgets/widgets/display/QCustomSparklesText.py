########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomSparklesText - text with drifting sparkle particles.
##
## The "magic"/AI accent: small four-point stars twinkling around a headline.
##
## The particles are DETERMINISTIC given a seed. That is deliberate: a random
## sparkle field cannot be tested, cannot be screenshotted reproducibly, and
## makes two runs of the same demo look different for no reason. Seeded, the
## motion is still organic but the widget is verifiable.
##
## Stars are painted as real polygons, not a unicode glyph - the design lint
## rejects glyph icons, and a real polygon scales and tints properly.
##
## Animation stops while hidden, like QCustomRainbowButton.
########################################################################
import math

from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF, QTimer
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QPolygonF, QFontMetrics, QFont
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomSparklesText(QWidget):
    clicked = Signal()

    WIDGET_ICON = "components/icons/auto_awesome.png"
    WIDGET_TOOLTIP = "Text with drifting sparkle particles"
    WIDGET_MODULE = "Custom_Widgets.QCustomSparklesText"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSparklesText' name='customSparklesText'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>300</width><height>60</height></rect></property>
            <property name='text'><string>Powered by AI</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomSparklesText",
        "props": {"text": {"type": "string", "default": ""},
                  "sparkleCount": {"type": "int", "default": 14},
                  "sparkleSize": {"type": "float", "default": 7.0},
                  "speed": {"type": "int", "default": 60},
                  "animated": {"type": "bool", "default": True},
                  "seed": {"type": "int", "default": 7},
                  "fontScale": {"type": "float", "default": 1.5},
                  "bold": {"type": "bool", "default": True},
                  "colorsCsv": {"type": "string",
                                "default": "#f59e0b,#a855f7,#2563eb"},
                  "textColor": {"type": "color", "default": "#0f172a"}},
        "signals": ["clicked"],
        "tokens_used": ["on-surface", "accent"],
    }

    _DEFAULT_COLORS = ["#f59e0b", "#a855f7", "#2563eb"]

    def __init__(self, parent=None, text="", sparkleCount=14):
        super().__init__(parent)
        self.setObjectName("QCustomSparklesText")
        self._text = str(text)
        self._count = max(0, int(sparkleCount))
        self._size = 7.0
        self._speed = 60
        self._animated = True
        self._seed = 7
        self._phase = 0.0
        self._fontScale = 1.5
        self._bold = True
        self._colors = [QColor(c) for c in self._DEFAULT_COLORS]
        self._textColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)

    # ------------------------------------------------------------------ #
    ## Particles
    # ------------------------------------------------------------------ #
    def sparkles(self):
        """[(x, y, size, opacity, colour), ...] for the current phase.

        Derived purely from the seed, the index and the phase — no RNG state —
        so the same phase always produces the same field. That is what makes
        the widget screenshot-stable and testable.
        """
        out = []
        if self._count <= 0 or self.width() <= 0 or self.height() <= 0:
            return out
        for index in range(self._count):
            # A cheap hash of (seed, index) gives each particle a stable but
            # unrelated position and rhythm.
            base = (self._seed * 7919 + index * 104729) % 100000
            fx = ((base % 997) / 997.0)
            fy = (((base // 997) % 991) / 991.0)
            rate = 0.4 + ((base // 13) % 100) / 100.0
            offset = ((base // 7) % 100) / 100.0

            # Twinkle: a sine on the particle's own rhythm, clamped to >= 0 so
            # a sparkle fades out rather than inverting.
            twinkle = math.sin((self._phase * rate + offset) * math.pi * 2.0)
            opacity = max(0.0, twinkle)
            drift = math.sin((self._phase * rate * 0.5 + offset) * math.pi * 2.0)

            x = fx * self.width()
            y = fy * self.height() + drift * 3.0
            size = self._size * (0.6 + 0.4 * opacity)
            colour = self._colors[index % len(self._colors)]
            out.append((x, y, size, opacity, QColor(colour)))
        return out

    def setColors(self, colors):
        parsed = [QColor(c) for c in (colors or [])]
        parsed = [c for c in parsed if c.isValid()]
        if not parsed:
            return False
        self._colors = parsed
        self.update()
        return True

    def colors(self):
        return [QColor(c) for c in self._colors]

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
        self._phase = (self._phase + 0.02) % 1.0
        self.update()

    def showEvent(self, e):
        super().showEvent(e)
        self.start()

    def hideEvent(self, e):
        self.stop()
        super().hideEvent(e)

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
        return QSize(fm.horizontalAdvance(self._text) + 40, fm.height() + 24)

    minimumSizeHint = sizeHint

    @staticmethod
    def _starPolygon(cx, cy, size):
        """A four-point star. Drawn, not a glyph — the lint rejects glyphs."""
        half = size / 2.0
        waist = size / 6.0
        return QPolygonF([
            QPointF(cx, cy - half), QPointF(cx + waist, cy - waist),
            QPointF(cx + half, cy), QPointF(cx + waist, cy + waist),
            QPointF(cx, cy + half), QPointF(cx - waist, cy + waist),
            QPointF(cx - half, cy), QPointF(cx - waist, cy - waist)])

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(Qt.NoPen)
        for x, y, size, opacity, colour in self.sparkles():
            if opacity <= 0.01:
                continue
            tint = QColor(colour)
            tint.setAlphaF(min(1.0, opacity))
            p.setBrush(QBrush(tint))
            p.drawPolygon(self._starPolygon(x, y, size))

        if not self._text:
            return
        p.setFont(self._scaledFont())
        p.setPen(QPen(self._textColor))
        p.drawText(QRectF(0, 0, self.width(), self.height()),
                   int(Qt.AlignCenter), self._text)

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

    @Property(int)
    def sparkleCount(self):
        return self._count

    @sparkleCount.setter
    def sparkleCount(self, value):
        self._count = max(0, int(value)); self.update()

    @Property(float)
    def sparkleSize(self):
        return self._size

    @sparkleSize.setter
    def sparkleSize(self, value):
        self._size = max(1.0, float(value)); self.update()

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

    @Property(int)
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = int(value); self.update()

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
    def colorsCsv(self):
        return ",".join(c.name() for c in self._colors)

    @colorsCsv.setter
    def colorsCsv(self, text):
        self.setColors([t.strip() for t in str(text).replace(";", ",").split(",")
                        if t.strip()])

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()
