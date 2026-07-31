########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomNumberCounter - a number that animates to its new value.
##
## The count-up on a landing page or a KPI tile. The animation is the widget:
## a number that simply changes reads as a redraw, one that counts draws the
## eye and communicates that it moved.
##
## Formatting is deliberate - prefix, suffix, thousands separator, fixed
## decimals - because a counter that animates to "1234567.891" is worse than
## one that does not animate at all.
##
## Emits valueChanged(float) continuously during the animation and finished()
## once it settles.
########################################################################
from qtpy.QtCore import (Qt, Signal, Property, QRectF, QSize, QPropertyAnimation,
                         QEasingCurve)
from qtpy.QtGui import QColor, QPainter, QPen, QFontMetrics, QFont
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomNumberCounter(QWidget):
    valueChanged = Signal(float)
    finished = Signal()

    WIDGET_ICON = "components/icons/123.png"
    WIDGET_TOOLTIP = "A number that animates to its new value"
    WIDGET_MODULE = "Custom_Widgets.QCustomNumberCounter"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomNumberCounter' name='customNumberCounter'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>180</width><height>60</height></rect></property>
            <property name='value'><double>1250</double></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomNumberCounter",
        "props": {"value": {"type": "float", "default": 0.0},
                  "prefix": {"type": "string", "default": ""},
                  "suffix": {"type": "string", "default": ""},
                  "decimals": {"type": "int", "default": 0},
                  "separator": {"type": "string", "default": ","},
                  "duration": {"type": "int", "default": 900},
                  "fontScale": {"type": "float", "default": 1.0},
                  "bold": {"type": "bool", "default": True},
                  "alignment": {"type": "enum",
                                "values": ["left", "center", "right"],
                                "default": "center"},
                  "textColor": {"type": "color", "default": "#0f172a"}},
        "signals": ["valueChanged", "finished"],
        "tokens_used": ["on-surface"],
    }

    def __init__(self, parent=None, value=0.0, prefix="", suffix=""):
        super().__init__(parent)
        self.setObjectName("QCustomNumberCounter")
        self._value = float(value)
        self._display = float(value)
        self._prefix = str(prefix)
        self._suffix = str(suffix)
        self._decimals = 0
        self._separator = ","
        self._duration = 900
        self._fontScale = 1.0
        self._bold = True
        self._alignment = "center"
        self._textColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self._anim = QPropertyAnimation(self, b"displayValue", self)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.finished.connect(self.finished.emit)

    # ------------------------------------------------------------------ #
    ## Value
    # ------------------------------------------------------------------ #
    def setValue(self, value, animate=True):
        """Animate to a new value. `animate=False` jumps, for initial state."""
        value = float(value)
        if value == self._value and self._display == value:
            return
        self._value = value
        if not animate or self._duration <= 0:
            self._anim.stop()
            self.displayValue = value
            self.finished.emit()
            return
        self._anim.stop()
        self._anim.setDuration(self._duration)
        self._anim.setStartValue(self._display)
        self._anim.setEndValue(value)
        self._anim.start()

    # No value() method: `value` is a Qt Property below and would shadow it,
    # so `counter.value()` would try to call a float. Read `counter.value`.
    def displayedValue(self):
        return self._display

    def isAnimating(self):
        return self._anim.state() == QPropertyAnimation.Running

    def reset(self, value=0.0):
        self._anim.stop()
        self._value = float(value)
        self.displayValue = float(value)

    def formattedText(self):
        """The exact string painted, including prefix and suffix."""
        magnitude = abs(self._display)
        text = "%.*f" % (self._decimals, magnitude)
        if self._separator:
            whole, _, fraction = text.partition(".")
            grouped = ""
            while len(whole) > 3:
                grouped = self._separator + whole[-3:] + grouped
                whole = whole[:-3]
            text = whole + grouped + ("." + fraction if fraction else "")
        sign = "-" if self._display < 0 else ""
        return "%s%s%s%s" % (sign, self._prefix, text, self._suffix)

    # ------------------------------------------------------------------ #
    ## Painting
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
        # Measured against the TARGET value, not the animating one, so the
        # widget does not resize on every frame of the count.
        sample = self._sampleText()
        return QSize(fm.horizontalAdvance(sample) + 12, fm.height() + 8)

    minimumSizeHint = sizeHint

    def _sampleText(self):
        current, self._display = self._display, self._value
        try:
            return self.formattedText()
        finally:
            self._display = current

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self._scaledFont())
        p.setPen(QPen(self._textColor))
        flags = {"left": Qt.AlignLeft, "right": Qt.AlignRight}.get(
            self._alignment, Qt.AlignHCenter)
        p.drawText(QRectF(4, 0, self.width() - 8, self.height()),
                   int(flags | Qt.AlignVCenter), self.formattedText())

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(float)
    def displayValue(self):
        return self._display

    @displayValue.setter
    def displayValue(self, value):
        self._display = float(value)
        self.update()
        self.valueChanged.emit(self._display)

    @Property(float)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self.setValue(v)

    @Property(str)
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, text):
        self._prefix = str(text)
        self.updateGeometry(); self.update()

    @Property(str)
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, text):
        self._suffix = str(text)
        self.updateGeometry(); self.update()

    @Property(int)
    def decimals(self):
        return self._decimals

    @decimals.setter
    def decimals(self, value):
        self._decimals = max(0, min(10, int(value)))
        self.updateGeometry(); self.update()

    @Property(str)
    def separator(self):
        return self._separator

    @separator.setter
    def separator(self, value):
        self._separator = str(value)
        self.updateGeometry(); self.update()

    @Property(int)
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = max(0, int(value))

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

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()
