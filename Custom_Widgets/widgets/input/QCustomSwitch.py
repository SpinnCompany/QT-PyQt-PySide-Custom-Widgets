########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomSwitch - an on/off toggle switch.
##
## A painted sliding switch (iOS/Material style): a rounded track with a thumb
## that slides between off (left) and on (right). Click or press Space/Enter to
## toggle. Tokenized colours via qproperty; three sizes via `sizeVariant`
## (sm / md / lg). Emits toggled(bool).
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QPropertyAnimation, QEasingCurve
from qtpy.QtGui import QColor, QPainter, QPen, QBrush
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomSwitch(QWidget):
    toggled = Signal(bool)

    WIDGET_ICON = "components/icons/switch.png"
    WIDGET_TOOLTIP = "An on/off toggle switch"
    WIDGET_MODULE = "Custom_Widgets.QCustomSwitch"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSwitch' name='customSwitch'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>44</width><height>26</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomSwitch",
        "props": {"checked": {"type": "bool", "default": False},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"}},
        "signals": ["toggled"],
        "tokens_used": ["accent", "outline", "surface"],
    }

    # (track width, track height, thumb margin) per size
    _SIZES = {"sm": (34, 20, 2), "md": (44, 26, 3), "lg": (56, 32, 4)}

    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self.setObjectName("QCustomSwitch")
        self._checked = bool(checked)
        self._sizeVariant = "md"
        self._pos = 1.0 if self._checked else 0.0     # thumb 0=off .. 1=on
        self._trackOn = QColor("#2563eb")
        self._trackOff = QColor("#cbd5e1")
        self._thumb = QColor("#ffffff")
        self._thumbBorder = QColor("#00000022")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self._anim = QPropertyAnimation(self, b"thumbPosition", self)
        self._anim.setDuration(140)
        self._anim.setEasingCurve(QEasingCurve.InOutCubic)

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _dims(self):
        return self._SIZES.get(self._sizeVariant, self._SIZES["md"])

    def sizeHint(self):
        w, h, _ = self._dims()
        from qtpy.QtCore import QSize
        return QSize(w, h)

    minimumSizeHint = sizeHint

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        w, h, margin = self._dims()
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(0, 0, w, h)
        radius = h / 2.0

        track = QColor(self._trackOff)
        # blend toward the on-colour by the thumb position for a smooth flip
        track = self._blend(self._trackOff, self._trackOn, self._pos)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(track))
        p.drawRoundedRect(rect, radius, radius)

        d = h - 2 * margin
        x = margin + self._pos * (w - 2 * margin - d)
        p.setPen(QPen(self._thumbBorder, 1))
        p.setBrush(QBrush(self._thumb))
        p.drawEllipse(QRectF(x, margin, d, d))

    @staticmethod
    def _blend(c0, c1, t):
        t = max(0.0, min(1.0, t))
        return QColor(int(c0.red() + (c1.red() - c0.red()) * t),
                      int(c0.green() + (c1.green() - c0.green()) * t),
                      int(c0.blue() + (c1.blue() - c0.blue()) * t))

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.toggle()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.toggle()
        else:
            super().keyPressEvent(e)

    # ------------------------------------------------------------------ #
    ## State
    # ------------------------------------------------------------------ #
    def toggle(self):
        self.setChecked(not self._checked)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        checked = bool(checked)
        if checked == self._checked:
            return
        self._checked = checked
        self._anim.stop()
        self._anim.setStartValue(self._pos)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()
        self.toggled.emit(checked)

    @Property(bool)
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        self.setChecked(value)

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self.updateGeometry()
        self.update()

    # thumb position (animated) --------------------------------------------
    @Property(float)
    def thumbPosition(self):
        return self._pos

    @thumbPosition.setter
    def thumbPosition(self, value):
        self._pos = float(value)
        self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def trackOnColor(self):
        return self._trackOn

    @trackOnColor.setter
    def trackOnColor(self, c):
        self._trackOn = QColor(c); self.update()

    @Property(QColor)
    def trackOffColor(self):
        return self._trackOff

    @trackOffColor.setter
    def trackOffColor(self, c):
        self._trackOff = QColor(c); self.update()

    @Property(QColor)
    def thumbColor(self):
        return self._thumb

    @thumbColor.setter
    def thumbColor(self, c):
        self._thumb = QColor(c); self.update()
