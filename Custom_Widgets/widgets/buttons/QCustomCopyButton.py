########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomCopyButton - copy-to-clipboard with confirmation.
##
## The small button beside a code block, an API key or a share link. The whole
## value of the control is the FEEDBACK: a copy that gives no acknowledgement
## leaves the user pressing it again to be sure, so this flips to a "Copied!"
## state and returns on a timer.
##
## Painted so the confirmation can morph rather than swapping stylesheets, and
## so the tick is drawn rather than being a unicode glyph (the design lint
## rejects glyph icons).
##
## Emits copied(str) with the text that was placed on the clipboard.
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QTimer
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy, QApplication


from Custom_Widgets.accessibility import set_accessibility, QAccessible


class QCustomCopyButton(QWidget):
    copied = Signal(str)

    WIDGET_ICON = "components/icons/content_copy.png"
    WIDGET_TOOLTIP = "A copy-to-clipboard button with confirmation"
    WIDGET_MODULE = "Custom_Widgets.QCustomCopyButton"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCopyButton' name='customCopyButton'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>110</width><height>34</height></rect></property>
            <property name='text'><string>Copy</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCopyButton",
        "props": {"payload": {"type": "string", "default": ""},
                  "text": {"type": "string", "default": "Copy"},
                  "copiedText": {"type": "string", "default": "Copied!"},
                  "resetDelay": {"type": "int", "default": 1600},
                  "variant": {"type": "enum", "values": ["outline", "ghost", "solid"],
                              "default": "outline"},
                  "iconOnly": {"type": "bool", "default": False},
                  "accentColor": {"type": "color", "default": "#2563eb"},
                  "successColor": {"type": "color", "default": "#16a34a"},
                  "textColor": {"type": "color", "default": "#0f172a"},
                  "surfaceColor": {"type": "color", "default": "#ffffff"}},
        "signals": ["copied"],
        "tokens_used": ["accent", "success", "on-surface", "surface", "outline"],
    }

    def __init__(self, parent=None, payload="", text="Copy"):
        super().__init__(parent)
        self.setObjectName("QCustomCopyButton")
        self._payload = str(payload)
        self._text = str(text)
        self._copiedText = "Copied!"
        self._resetDelay = 1600
        self._variant = "outline"
        self._iconOnly = False
        self._confirming = False
        self._hovered = False

        self._accent = QColor("#2563eb")
        self._success = QColor("#16a34a")
        self._textColor = QColor("#0f172a")
        self._surface = QColor("#ffffff")

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._reset)
        set_accessibility(self, QAccessible.Button, self._text)

    # ------------------------------------------------------------------ #
    ## Copying
    # ------------------------------------------------------------------ #
    def copy(self):
        """Put the payload on the clipboard and confirm. False if empty.

        An empty payload is a no-op rather than a silent success: confirming a
        copy that put nothing on the clipboard is worse than not confirming.
        """
        if not self._payload:
            return False
        clipboard = QApplication.clipboard()
        if clipboard is None:                        # pragma: no cover
            return False
        clipboard.setText(self._payload)
        self._confirming = True
        self.update()
        if self._resetDelay > 0:
            self._timer.start(self._resetDelay)
        self.copied.emit(self._payload)
        return True

    def isConfirming(self):
        return self._confirming

    def _reset(self):
        self._confirming = False
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _label(self):
        return self._copiedText if self._confirming else self._text

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        height = fm.height() + 16
        if self._iconOnly:
            return QSize(height, height)
        # Sized against the LONGER of the two captions so the button does not
        # resize when it flips to "Copied!" and shove the layout sideways.
        widest = max(fm.horizontalAdvance(self._text),
                     fm.horizontalAdvance(self._copiedText))
        return QSize(widest + height + 18, height)

    minimumSizeHint = sizeHint

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        rect = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)
        accent = self._success if self._confirming else self._accent

        if self._variant == "solid":
            fill = accent.lighter(108) if self._hovered else accent
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(fill))
            foreground = self._surface
        elif self._variant == "ghost":
            p.setPen(Qt.NoPen)
            tint = QColor(accent)
            tint.setAlphaF(0.14 if self._hovered else 0.0)
            p.setBrush(QBrush(tint))
            foreground = accent
        else:
            p.setPen(QPen(accent, 1.4))
            p.setBrush(QBrush(self._surface))
            foreground = accent if self._confirming else self._textColor
        p.drawRoundedRect(rect, 8, 8)

        fm = QFontMetrics(self.font())
        glyph = fm.height() * 0.62
        if self._iconOnly:
            self._paintGlyph(p, rect.center().x(), rect.center().y(), glyph,
                             foreground)
            return

        text = self._label()
        width = fm.horizontalAdvance(text)
        total = glyph + 8 + width
        x = rect.center().x() - total / 2.0
        self._paintGlyph(p, x + glyph / 2.0, rect.center().y(), glyph, foreground)
        p.setPen(QPen(foreground))
        p.drawText(QRectF(x + glyph + 8, rect.top(), width + 2, rect.height()),
                   int(Qt.AlignVCenter | Qt.AlignLeft), text)

    def _paintGlyph(self, p, cx, cy, size, colour):
        """Draw the copy pages, or a tick once confirmed.

        Drawn rather than using a unicode glyph: the design lint rejects glyph
        icons, and a real tick scales with the font.
        """
        half = size / 2.0
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(colour, 1.6))
        if self._confirming:
            p.drawLine(QRectF(cx - half, cy, 0, 0).topLeft(),
                       QRectF(cx - half * 0.15, cy + half * 0.55, 0, 0).topLeft())
            p.drawLine(QRectF(cx - half * 0.15, cy + half * 0.55, 0, 0).topLeft(),
                       QRectF(cx + half, cy - half * 0.6, 0, 0).topLeft())
            return
        back = QRectF(cx - half, cy - half, size * 0.72, size * 0.72)
        front = QRectF(cx - half + size * 0.28, cy - half + size * 0.28,
                       size * 0.72, size * 0.72)
        p.drawRoundedRect(back, 2, 2)
        p.drawRoundedRect(front, 2, 2)

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
            self.copy()
        super().mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.copy()
            return
        super().keyPressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = str(value)

    @Property(str)
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self.updateGeometry(); self.update()

    @Property(str)
    def copiedText(self):
        return self._copiedText

    @copiedText.setter
    def copiedText(self, value):
        self._copiedText = str(value)
        self.updateGeometry(); self.update()

    @Property(int)
    def resetDelay(self):
        return self._resetDelay

    @resetDelay.setter
    def resetDelay(self, value):
        self._resetDelay = max(0, int(value))

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        value = str(value)
        self._variant = value if value in ("outline", "ghost", "solid") else "outline"
        self.update()

    @Property(bool)
    def iconOnly(self):
        return self._iconOnly

    @iconOnly.setter
    def iconOnly(self, value):
        self._iconOnly = bool(value)
        self.updateGeometry(); self.update()

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c); self.update()

    @Property(QColor)
    def successColor(self):
        return self._success

    @successColor.setter
    def successColor(self, c):
        self._success = QColor(c); self.update()

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
