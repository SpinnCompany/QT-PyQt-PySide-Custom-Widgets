########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomRangeSlider - a dual-handle range selector.
##
## Two handles select a [lower, upper] range on a track; the selected span is
## filled. Drag a handle (or click the track to move the nearest one).
## Tokenized colours via qproperty. Emits valuesChanged(lower, upper).
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QPen, QBrush
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomRangeSlider(QWidget):
    valuesChanged = Signal(int, int)       # lower, upper

    HANDLE = 9

    WIDGET_ICON = "components/icons/rangeslider.png"
    WIDGET_TOOLTIP = "A dual-handle range slider"
    WIDGET_MODULE = "Custom_Widgets.QCustomRangeSlider"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRangeSlider' name='customRangeSlider'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>240</width><height>28</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRangeSlider",
        "props": {"minimum": {"type": "int", "default": 0},
                  "maximum": {"type": "int", "default": 100},
                  "lowerValue": {"type": "int", "default": 0},
                  "upperValue": {"type": "int", "default": 100}},
        "signals": ["valuesChanged"],
        "tokens_used": ["outline", "accent", "surface"],
    }

    def __init__(self, parent=None, minimum=0, maximum=100):
        super().__init__(parent)
        self.setObjectName("QCustomRangeSlider")
        self._min = int(minimum)
        self._max = int(maximum)
        self._low = self._min
        self._high = self._max
        self._active = None            # "low" | "high" | None
        self._track = QColor("#cbd5e1")
        self._fill = QColor("#2563eb")
        self._handle = QColor("#ffffff")
        self._handleBorder = QColor("#2563eb")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(24)
        self.setCursor(Qt.PointingHandCursor)

    # ------------------------------------------------------------------ #
    ## Geometry helpers
    # ------------------------------------------------------------------ #
    def _margin(self):
        return self.HANDLE + 2

    def _usable(self):
        return max(1, self.width() - 2 * self._margin())

    def _valueToX(self, v):
        span = max(1, self._max - self._min)
        return self._margin() + (v - self._min) / span * self._usable()

    def _xToValue(self, x):
        span = self._max - self._min
        frac = (x - self._margin()) / self._usable()
        return int(round(self._min + frac * span))

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        cy = self.height() / 2.0
        x0, x1 = self._margin(), self.width() - self._margin()
        xlo, xhi = self._valueToX(self._low), self._valueToX(self._high)

        p.setPen(QPen(self._track, 4, Qt.SolidLine, Qt.RoundCap))
        p.drawLine(int(x0), int(cy), int(x1), int(cy))
        p.setPen(QPen(self._fill, 4, Qt.SolidLine, Qt.RoundCap))
        p.drawLine(int(xlo), int(cy), int(xhi), int(cy))

        p.setPen(QPen(self._handleBorder, 2))
        p.setBrush(QBrush(self._handle))
        rad = self.HANDLE
        for xh in (xlo, xhi):
            p.drawEllipse(QRectF(xh - rad, cy - rad, 2 * rad, 2 * rad))

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        x = e.position().x() if hasattr(e, "position") else e.x()
        dlo = abs(x - self._valueToX(self._low))
        dhi = abs(x - self._valueToX(self._high))
        self._active = "low" if dlo <= dhi else "high"
        self._moveActive(self._xToValue(x))

    def mouseMoveEvent(self, e):
        if self._active is None:
            return
        x = e.position().x() if hasattr(e, "position") else e.x()
        self._moveActive(self._xToValue(x))

    def mouseReleaseEvent(self, e):
        self._active = None

    def _moveActive(self, value):
        if self._active == "low":
            self.setLowerValue(value)
        elif self._active == "high":
            self.setUpperValue(value)

    # ------------------------------------------------------------------ #
    ## Values
    # ------------------------------------------------------------------ #
    def _emit(self):
        self.valuesChanged.emit(self._low, self._high)

    def setRange(self, minimum, maximum):
        self._min, self._max = int(minimum), int(maximum)
        self.setValues(self._low, self._high)

    def setValues(self, lower, upper):
        lower = max(self._min, min(int(lower), self._max))
        upper = max(self._min, min(int(upper), self._max))
        if lower > upper:
            lower, upper = upper, lower
        changed = (lower, upper) != (self._low, self._high)
        self._low, self._high = lower, upper
        self.update()
        if changed:
            self._emit()

    def values(self):
        return self._low, self._high

    def setLowerValue(self, v):
        self.setValues(min(int(v), self._high), self._high)

    def setUpperValue(self, v):
        self.setValues(self._low, max(int(v), self._low))

    @Property(int)
    def minimum(self):
        return self._min

    @minimum.setter
    def minimum(self, v):
        self.setRange(int(v), self._max)

    @Property(int)
    def maximum(self):
        return self._max

    @maximum.setter
    def maximum(self, v):
        self.setRange(self._min, int(v))

    @Property(int)
    def lowerValue(self):
        return self._low

    @lowerValue.setter
    def lowerValue(self, v):
        self.setLowerValue(v)

    @Property(int)
    def upperValue(self):
        return self._high

    @upperValue.setter
    def upperValue(self, v):
        self.setUpperValue(v)

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def trackColor(self):
        return self._track

    @trackColor.setter
    def trackColor(self, c):
        self._track = QColor(c); self.update()

    @Property(QColor)
    def fillColor(self):
        return self._fill

    @fillColor.setter
    def fillColor(self, c):
        self._fill = QColor(c); self.update()

    @Property(QColor)
    def handleColor(self):
        return self._handle

    @handleColor.setter
    def handleColor(self, c):
        self._handle = QColor(c); self.update()

    @Property(QColor)
    def handleBorderColor(self):
        return self._handleBorder

    @handleBorderColor.setter
    def handleBorderColor(self, c):
        self._handleBorder = QColor(c); self.update()
