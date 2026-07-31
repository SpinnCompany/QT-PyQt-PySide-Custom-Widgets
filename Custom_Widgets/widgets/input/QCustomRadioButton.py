########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomRadioButton - a painted single-choice radio button.
##
## A painted ring with an inner dot that grows in when selected, plus an
## optional label. Click or press Space/Enter to select. Unlike QCheckBox a
## radio cannot be un-selected by clicking it again - that is the whole point
## of the control, so `toggle()` is deliberately absent.
##
## Auto-exclusive by default: selecting one clears every sibling
## QCustomRadioButton that shares its parent, matching QRadioButton. Set
## `autoExclusive` to False when a QCustomRadioGroup (or your own code) owns
## the mutual exclusion instead.
##
## Tokenized colours via qproperty; three sizes via `sizeVariant` (sm/md/lg).
## Emits toggled(bool) on every state change and selected(str) carrying the
## widget's `value` when it becomes the chosen option.
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPropertyAnimation, QEasingCurve
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomRadioButton(QWidget):
    toggled = Signal(bool)
    selected = Signal(str)

    WIDGET_ICON = "components/icons/radio_button_checked.png"
    WIDGET_TOOLTIP = "A single-choice radio button"
    WIDGET_MODULE = "Custom_Widgets.QCustomRadioButton"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRadioButton' name='customRadioButton'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>140</width><height>24</height></rect></property>
            <property name='text'><string>Option</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRadioButton",
        "props": {"checked": {"type": "bool", "default": False},
                  "text": {"type": "str", "default": ""},
                  "value": {"type": "str", "default": ""},
                  "autoExclusive": {"type": "bool", "default": True},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"}},
        "signals": ["toggled", "selected"],
        "tokens_used": ["accent", "outline", "on-surface"],
    }

    # (ring diameter, gap between ring and label, font point size) per size
    _SIZES = {"sm": (14, 6, 9), "md": (18, 8, 10), "lg": (22, 10, 12)}

    def __init__(self, parent=None, text="", checked=False, value=""):
        super().__init__(parent)
        self.setObjectName("QCustomRadioButton")
        self._checked = bool(checked)
        self._text = str(text)
        self._value = str(value)
        self._autoExclusive = True
        self._sizeVariant = "md"
        # inner dot scale 0=empty .. 1=selected
        self._dot = 1.0 if self._checked else 0.0
        self._ring = QColor("#cbd5e1")
        self._ringChecked = QColor("#2563eb")
        self._dotColor = QColor("#2563eb")
        self._textColor = QColor("#0f172a")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self._anim = QPropertyAnimation(self, b"dotScale", self)
        self._anim.setDuration(120)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _dims(self):
        return self._SIZES.get(self._sizeVariant, self._SIZES["md"])

    def _labelFont(self):
        d, gap, pt = self._dims()
        f = self.font()
        f.setPointSize(pt)
        return f

    def sizeHint(self):
        d, gap, pt = self._dims()
        h = max(d, QFontMetrics(self._labelFont()).height())
        if not self._text:
            return QSize(d, h)
        w = d + gap + QFontMetrics(self._labelFont()).horizontalAdvance(self._text)
        return QSize(w, h)

    minimumSizeHint = sizeHint

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        d, gap, pt = self._dims()
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Ring is vertically centred so the control lines up with its label
        # however tall the widget has been stretched.
        top = (self.height() - d) / 2.0
        ring = QRectF(0.5, top + 0.5, d - 1, d - 1)

        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(self._ringChecked if self._checked else self._ring, 2))
        p.drawEllipse(ring)

        if self._dot > 0.0:
            # Full dot spans half the ring; scale it for the grow-in animation.
            full = d * 0.5
            size = full * self._dot
            c = ring.center()
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._dotColor))
            p.drawEllipse(QRectF(c.x() - size / 2.0, c.y() - size / 2.0, size, size))

        if self._text:
            p.setPen(QPen(self._textColor))
            p.setFont(self._labelFont())
            p.drawText(QRectF(d + gap, 0, max(0.0, self.width() - d - gap), self.height()),
                       int(Qt.AlignVCenter | Qt.AlignLeft), self._text)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.setChecked(True)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.setChecked(True)
        else:
            super().keyPressEvent(e)

    # ------------------------------------------------------------------ #
    ## State
    # ------------------------------------------------------------------ #
    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        checked = bool(checked)
        if checked == self._checked:
            return
        self._checked = checked
        self._anim.stop()
        self._anim.setStartValue(self._dot)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()
        self.update()
        if checked:
            self._clearSiblings()
        self.toggled.emit(checked)
        if checked:
            self.selected.emit(self._value or self._text)

    def _clearSiblings(self):
        """Uncheck every auto-exclusive sibling radio sharing our parent."""
        if not self._autoExclusive:
            return
        parent = self.parentWidget()
        if parent is None:
            return
        for sib in parent.findChildren(QCustomRadioButton):
            if sib is not self and sib.parentWidget() is parent \
                    and sib.autoExclusive and sib.isChecked():
                sib.setChecked(False)

    # -- properties --------------------------------------------------------
    @Property(bool)
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        self.setChecked(value)

    @Property(str)
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self.updateGeometry()
        self.update()

    @Property(str)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = str(v)

    @Property(bool)
    def autoExclusive(self):
        return self._autoExclusive

    @autoExclusive.setter
    def autoExclusive(self, v):
        self._autoExclusive = bool(v)

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self.updateGeometry()
        self.update()

    # dot scale (animated) -------------------------------------------------
    @Property(float)
    def dotScale(self):
        return self._dot

    @dotScale.setter
    def dotScale(self, value):
        self._dot = float(value)
        self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def ringColor(self):
        return self._ring

    @ringColor.setter
    def ringColor(self, c):
        self._ring = QColor(c); self.update()

    @Property(QColor)
    def ringCheckedColor(self):
        return self._ringChecked

    @ringCheckedColor.setter
    def ringCheckedColor(self, c):
        self._ringChecked = QColor(c); self.update()

    @Property(QColor)
    def dotColor(self):
        return self._dotColor

    @dotColor.setter
    def dotColor(self, c):
        self._dotColor = QColor(c); self.update()

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()
