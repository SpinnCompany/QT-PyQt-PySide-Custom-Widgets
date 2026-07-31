########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomPaymentCard - a painted credit / debit card surface.
##
## A rounded card with a brand mark, a big amount and a masked card number,
## drawn entirely with QPainter so it stays crisp at any size and needs no
## child widgets. Two looks:
##   variant="gradient" (default) - a diagonal two-stop gradient (e.g. an accent
##       "active" card) with light text.
##   variant="flat" - a single flat fill (e.g. a muted secondary card) whose
##       text colour you control.
## Colours come from qproperties so a theme/manager can tokenise them. An
## optional EMV-style chip can be shown. Set content with setBrand/setAmount/
## setNumber (or the Designer properties).
########################################################################
from qtpy.QtCore import Qt, Property, QRectF, Signal
from qtpy.QtGui import QColor, QPainter, QBrush, QLinearGradient, QPen, QFont
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomPaymentCard(QWidget):

    # Emitted when the eye toggles the full number on/off.
    numberRevealed = Signal(bool)

    WIDGET_ICON = "components/icons/card.png"
    WIDGET_TOOLTIP = "A painted credit / debit card surface"
    WIDGET_MODULE = "Custom_Widgets.QCustomPaymentCard"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomPaymentCard' name='customPaymentCard'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>270</width><height>150</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomPaymentCard",
        "props": {"brand": {"type": "string", "default": "VISA"},
                  "amount": {"type": "string", "default": "$5 400.55"},
                  "number": {"type": "string", "default": "4558"},
                  "variant": {"type": "enum", "values": ["gradient", "flat"], "default": "gradient"},
                  "gradientStart": {"type": "color", "default": "#3f6bff"},
                  "gradientEnd": {"type": "color", "default": "#1c33c4"},
                  "flatColor": {"type": "color", "default": "#e7e9f0"},
                  "textColor": {"type": "color", "default": "#ffffff"},
                  "cornerRadius": {"type": "int", "default": 18},
                  "showChip": {"type": "bool", "default": False},
                  "fullNumber": {"type": "string", "default": ""},
                  "revealable": {"type": "bool", "default": False}},
        "signals": ["numberRevealed"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, brand="VISA", amount="$5 400.55", number="4558"):
        super().__init__(parent)
        self.setObjectName("QCustomPaymentCard")
        self._brand = brand
        self._amount = amount
        self._number = number
        self._variant = "gradient"
        self._grad_start = QColor("#3f6bff")
        self._grad_end = QColor("#1c33c4")
        self._flat = QColor("#e7e9f0")
        self._text = QColor("#ffffff")
        self._radius = 18
        self._show_chip = False
        self._full_number = ""          # complete PAN; enables real reveal
        self._revealable = False        # show an eye toggle
        self._revealed = False
        self._eye_rect = QRectF()       # hit-test area (set in paintEvent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMinimumSize(220, 140)

    # ------------------------------------------------------------------ #
    ## Content API
    # ------------------------------------------------------------------ #
    def setBrand(self, text):
        self._brand = str(text)
        self.update()

    def setAmount(self, text):
        self._amount = str(text)
        self.update()

    def setNumber(self, text):
        self._number = str(text)
        self.update()

    def setColors(self, start, end=None):
        """Set the gradient (start, end) — or a single flat colour if end is None."""
        self._grad_start = QColor(start)
        self._grad_end = QColor(end if end is not None else start)
        self.update()

    def setVariant(self, variant):
        self._variant = "flat" if str(variant) == "flat" else "gradient"
        self.update()

    def setFullNumber(self, number):
        """The complete PAN — enables a real reveal (otherwise the eye just
        toggles between masked and the last-4)."""
        self._full_number = str(number)
        self.update()

    def setRevealable(self, on):
        self._revealable = bool(on)
        if not self._revealable:
            self._revealed = False
        self.update()

    def setRevealed(self, on):
        on = bool(on)
        if on != self._revealed:
            self._revealed = on
            self.numberRevealed.emit(self._revealed)
            self.update()

    def toggleReveal(self):
        self.setRevealed(not self._revealed)

    def _last4(self):
        src = self._full_number or self._number
        return (src[-4:] if src else "0000")

    def _masked(self):
        return "••••  ••••  ••••  %s" % self._last4()

    def _grouped_full(self):
        digits = "".join(ch for ch in self._full_number if ch.isdigit())
        if not digits:
            return self._masked()
        return "  ".join(digits[i:i + 4] for i in range(0, len(digits), 4))

    def _display_number(self):
        if self._revealable and self._revealed and self._full_number:
            return self._grouped_full()
        return self._masked()

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        rect = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)

        if self._variant == "flat":
            p.setBrush(QBrush(self._flat))
        else:
            grad = QLinearGradient(0, 0, self.width(), self.height())
            grad.setColorAt(0.0, self._grad_start)
            grad.setColorAt(1.0, self._grad_end)
            p.setBrush(QBrush(grad))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(rect, self._radius, self._radius)

        pad = 22
        # brand (italic bold, top-left)
        p.setPen(QPen(self._text))
        bf = QFont(self.font())
        bf.setPointSize(12)
        bf.setBold(True)
        bf.setItalic(True)
        p.setFont(bf)
        p.drawText(QRectF(pad, 18, self.width() - 2 * pad, 24),
                   Qt.AlignLeft | Qt.AlignVCenter, self._brand)

        # optional chip
        if self._show_chip:
            chip = QRectF(pad, 52, 34, 26)
            cc = QColor(self._text)
            cc.setAlphaF(0.85 if self._variant == "gradient" else 0.4)
            p.setBrush(QBrush(cc))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(chip, 6, 6)

        # amount (big bold, lower area)
        p.setPen(QPen(self._text))
        af = QFont(self.font())
        af.setPointSize(21)
        af.setBold(True)
        p.setFont(af)
        p.drawText(QRectF(pad, self.height() - 66, self.width() - 2 * pad, 34),
                   Qt.AlignLeft | Qt.AlignVCenter, self._amount)

        # card number (masked or revealed)
        nf = QFont(self.font())
        nf.setPointSize(10)
        p.setFont(nf)
        nc = QColor(self._text)
        nc.setAlphaF(0.75)
        p.setPen(QPen(nc))
        p.drawText(QRectF(pad, self.height() - 32, self.width() - 2 * pad, 20),
                   Qt.AlignLeft | Qt.AlignVCenter, self._display_number())

        # eye reveal toggle (top-right)
        if self._revealable:
            eye = QRectF(self.width() - pad - 22, 18, 22, 22)
            self._eye_rect = eye
            self._draw_eye(p, eye, self._revealed)
        else:
            self._eye_rect = QRectF()
        p.end()

    def _draw_eye(self, p, box, revealed):
        """Draw an eye (revealed shows an eye with a slash = 'tap to hide')."""
        c = QColor(self._text)
        c.setAlphaF(0.85)
        pen = QPen(c, 1.8)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        cx, cy = box.center().x(), box.center().y()
        w = box.width() * 0.5
        h = box.height() * 0.32
        # almond outline (two quad curves)
        from qtpy.QtGui import QPainterPath
        path = QPainterPath()
        path.moveTo(cx - w, cy)
        path.quadTo(cx, cy - h * 1.9, cx + w, cy)
        path.quadTo(cx, cy + h * 1.9, cx - w, cy)
        p.drawPath(path)
        # pupil
        p.setBrush(QBrush(c))
        r = h * 0.72
        p.drawEllipse(QRectF(cx - r, cy - r, 2 * r, 2 * r))
        if revealed:
            p.setBrush(Qt.NoBrush)
            p.drawLine(box.left() + 2, box.top() + 2, box.right() - 2, box.bottom() - 2)

    def mousePressEvent(self, e):
        if self._revealable and not self._eye_rect.isNull() \
                and self._eye_rect.adjusted(-6, -6, 6, 6).contains(e.position()
                    if hasattr(e, "position") else e.pos()):
            self.toggleReveal()
            e.accept()
            return
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, v):
        self.setBrand(v)

    @Property(str)
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, v):
        self.setAmount(v)

    @Property(str)
    def number(self):
        return self._number

    @number.setter
    def number(self, v):
        self.setNumber(v)

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, v):
        self.setVariant(v)

    @Property(QColor)
    def gradientStart(self):
        return self._grad_start

    @gradientStart.setter
    def gradientStart(self, c):
        self._grad_start = QColor(c)
        self.update()

    @Property(QColor)
    def gradientEnd(self):
        return self._grad_end

    @gradientEnd.setter
    def gradientEnd(self, c):
        self._grad_end = QColor(c)
        self.update()

    @Property(QColor)
    def flatColor(self):
        return self._flat

    @flatColor.setter
    def flatColor(self, c):
        self._flat = QColor(c)
        self.update()

    @Property(QColor)
    def textColor(self):
        return self._text

    @textColor.setter
    def textColor(self, c):
        self._text = QColor(c)
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(bool)
    def showChip(self):
        return self._show_chip

    @showChip.setter
    def showChip(self, v):
        self._show_chip = bool(v)
        self.update()

    @Property(str)
    def fullNumber(self):
        return self._full_number

    @fullNumber.setter
    def fullNumber(self, v):
        self.setFullNumber(v)

    @Property(bool)
    def revealable(self):
        return self._revealable

    @revealable.setter
    def revealable(self, v):
        self.setRevealable(v)

    @Property(bool)
    def revealed(self):
        return self._revealed

    @revealed.setter
    def revealed(self, v):
        self.setRevealed(v)
