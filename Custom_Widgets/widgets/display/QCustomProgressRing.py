########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomProgressRing - a circular (determinate) progress indicator.
##
## A painted ring: a full track arc with a progress arc drawn on top, sweeping
## clockwise from 12 o'clock, plus an optional percentage in the centre. Unlike
## the indeterminate arc spinner in QCustomLoadingIndicators, this shows a
## known value. Tokenized colours + thickness via qproperty. Emits
## valueChanged(int).
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QPen, QFont
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomProgressRing(QWidget):
    valueChanged = Signal(int)

    WIDGET_ICON = "components/icons/data_usage.png"
    WIDGET_TOOLTIP = "A circular progress ring"
    WIDGET_MODULE = "Custom_Widgets.QCustomProgressRing"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomProgressRing' name='customProgressRing'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>96</width><height>96</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomProgressRing",
        "props": {"value": {"type": "int", "default": 0},
                  "minimum": {"type": "int", "default": 0},
                  "maximum": {"type": "int", "default": 100},
                  "showText": {"type": "bool", "default": True}},
        "signals": ["valueChanged"],
        "tokens_used": ["accent", "outline", "on-surface"],
    }

    def __init__(self, parent=None, minimum=0, maximum=100, value=0):
        super().__init__(parent)
        self.setObjectName("QCustomProgressRing")
        self._min = int(minimum)
        self._max = int(maximum)
        self._value = self._min
        self._showText = True
        self._thickness = 8
        self._ring = QColor("#2563eb")
        self._track = QColor("#e2e8f0")
        self._text = QColor("#0f172a")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMinimumSize(48, 48)
        self.setValue(value)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def _fraction(self):
        span = self._max - self._min
        if span <= 0:
            return 0.0
        return max(0.0, min(1.0, (self._value - self._min) / float(span)))

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        side = min(self.width(), self.height())
        pad = self._thickness / 2.0 + 1
        rect = QRectF((self.width() - side) / 2.0 + pad,
                      (self.height() - side) / 2.0 + pad,
                      side - 2 * pad, side - 2 * pad)

        track = QPen(self._track, self._thickness)
        track.setCapStyle(Qt.RoundCap)
        p.setPen(track)
        p.drawArc(rect, 0, 360 * 16)

        frac = self._fraction()
        if frac > 0:
            pen = QPen(self._ring, self._thickness)
            pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            # start at 12 o'clock (90deg), sweep clockwise (negative)
            p.drawArc(rect, 90 * 16, -int(round(frac * 360)) * 16)

        if self._showText:
            p.setPen(self._text)
            font = QFont(self.font())
            font.setPixelSize(max(10, int(side * 0.22)))
            font.setBold(True)
            p.setFont(font)
            p.drawText(rect, Qt.AlignCenter, "%d%%" % int(round(frac * 100)))

    # ------------------------------------------------------------------ #
    ## Value API
    # ------------------------------------------------------------------ #
    def value(self):
        return self._value

    def setValue(self, value):
        value = max(self._min, min(int(value), self._max))
        if value == self._value:
            return
        self._value = value
        self.update()
        self.valueChanged.emit(value)

    def setRange(self, minimum, maximum):
        self._min, self._max = int(minimum), int(maximum)
        if self._min > self._max:
            self._min, self._max = self._max, self._min
        self.setValue(self._value)
        self.update()

    def setMinimum(self, m):
        self.setRange(m, self._max)

    def setMaximum(self, m):
        self.setRange(self._min, m)

    def setShowText(self, show):
        self._showText = bool(show)
        self.update()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    # NB: no `value` Q_PROPERTY - it would collide with the value() method
    # (Qt-idiomatic getter). Use setValue() in code.
    @Property(int)
    def minimum(self):
        return self._min

    @minimum.setter
    def minimum(self, m):
        self.setMinimum(m)

    @Property(int)
    def maximum(self):
        return self._max

    @maximum.setter
    def maximum(self, m):
        self.setMaximum(m)

    @Property(bool)
    def showText(self):
        return self._showText

    @showText.setter
    def showText(self, v):
        self.setShowText(v)

    # -- colours + thickness (from tokens via qproperty) --
    @Property(QColor)
    def ringColor(self):
        return self._ring

    @ringColor.setter
    def ringColor(self, c):
        self._ring = QColor(c); self.update()

    @Property(QColor)
    def trackColor(self):
        return self._track

    @trackColor.setter
    def trackColor(self, c):
        self._track = QColor(c); self.update()

    @Property(QColor)
    def textColor(self):
        return self._text

    @textColor.setter
    def textColor(self, c):
        self._text = QColor(c); self.update()

    @Property(int)
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, t):
        self._thickness = max(1, int(t)); self.update()
