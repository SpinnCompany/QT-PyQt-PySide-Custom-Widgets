########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomVerificationCode - a segmented one-time-code input.
##
## The row of single-character boxes used for 2FA / OTP / email confirmation
## codes. Painted as one widget rather than assembled from N QLineEdits, so
## focus, paste and backspace behave as users expect instead of fighting Qt's
## per-field focus chain.
##
## Behaviour that the naive N-QLineEdit version gets wrong and this does not:
##   - pasting a whole code fills every box, however it is formatted
##   - backspace on an empty box steps back and clears the previous one
##   - arrow keys and Home/End move the caret without destroying input
##   - only characters permitted by `inputMode` are accepted at all
##
## Emits codeChanged(str) on every edit and completed(str) once the last box is
## filled.
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QTimer
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QFontMetrics,
                        QKeySequence)
from qtpy.QtWidgets import QWidget, QSizePolicy, QApplication


class QCustomVerificationCode(QWidget):
    codeChanged = Signal(str)
    completed = Signal(str)

    WIDGET_ICON = "components/icons/dialpad.png"
    WIDGET_TOOLTIP = "A segmented one-time-code (OTP / 2FA) input"
    WIDGET_MODULE = "Custom_Widgets.QCustomVerificationCode"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomVerificationCode' name='customVerificationCode'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>280</width><height>56</height></rect></property>
            <property name='digits'><number>6</number></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomVerificationCode",
        "props": {"digits": {"type": "int", "default": 6},
                  "inputMode": {"type": "enum",
                                "values": ["numeric", "alphanumeric", "alpha"],
                                "default": "numeric"},
                  "code": {"type": "string", "default": ""},
                  "masked": {"type": "bool", "default": False},
                  "uppercase": {"type": "bool", "default": True},
                  "separatorAfter": {"type": "int", "default": 0},
                  "boxWidth": {"type": "int", "default": 40},
                  "boxHeight": {"type": "int", "default": 48},
                  "boxSpacing": {"type": "int", "default": 8},
                  "state": {"type": "enum", "values": ["default", "error"],
                            "default": "default"}},
        "signals": ["codeChanged", "completed"],
        "tokens_used": ["surface", "on-surface", "outline", "focus-ring",
                        "destructive"],
    }

    _ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    _NUMERIC = "0123456789"

    def __init__(self, parent=None, digits=6, inputMode="numeric"):
        super().__init__(parent)
        self.setObjectName("QCustomVerificationCode")
        self._digits = max(1, int(digits))
        self._inputMode = inputMode if inputMode in ("numeric", "alphanumeric", "alpha") else "numeric"
        self._chars = [""] * self._digits
        self._caret = 0
        self._masked = False
        self._uppercase = True
        self._separatorAfter = 0
        self._boxW = 40
        self._boxH = 48
        self._spacing = 8
        self._state = "default"
        self._caretOn = True

        self._boxBg = QColor("#ffffff")
        self._boxBorder = QColor("#cbd5e1")
        self._boxBorderActive = QColor("#2563eb")
        self._boxBorderError = QColor("#dc2626")
        self._textColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursor(Qt.IBeamCursor)

        self._blink = QTimer(self)
        self._blink.setInterval(530)
        self._blink.timeout.connect(self._toggleCaret)

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _separatorWidth(self):
        return self._spacing * 2 if self._separatorAfter > 0 else 0

    def _separatorCount(self):
        if self._separatorAfter <= 0:
            return 0
        # a separator after every Nth box, but never a trailing one
        return max(0, (self._digits - 1) // self._separatorAfter)

    def sizeHint(self):
        w = (self._digits * self._boxW
             + (self._digits - 1) * self._spacing
             + self._separatorCount() * self._separatorWidth())
        return QSize(int(w), int(self._boxH))

    minimumSizeHint = sizeHint

    def _boxRect(self, index):
        x = 0.0
        for i in range(index):
            x += self._boxW + self._spacing
            if self._separatorAfter > 0 and (i + 1) % self._separatorAfter == 0 \
                    and (i + 1) < self._digits:
                x += self._separatorWidth()
        top = (self.height() - self._boxH) / 2.0
        return QRectF(x, top, self._boxW, self._boxH)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        fm = QFontMetrics(self.font())
        focused = self.hasFocus()

        for i in range(self._digits):
            rect = self._boxRect(i)
            active = focused and i == self._caret
            if self._state == "error":
                border = self._boxBorderError
            elif active:
                border = self._boxBorderActive
            else:
                border = self._boxBorder

            p.setPen(QPen(border, 2 if active or self._state == "error" else 1))
            p.setBrush(QBrush(self._boxBg))
            p.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 8, 8)

            ch = self._chars[i]
            if ch:
                shown = "•" if self._masked else ch
                p.setPen(QPen(self._textColor))
                p.drawText(rect, int(Qt.AlignCenter), shown)
            elif active and self._caretOn:
                # caret in the empty active box
                cx = rect.center().x()
                cy = rect.center().y()
                half = fm.height() * 0.35
                p.setPen(QPen(self._textColor, 1.5))
                p.drawLine(int(cx), int(cy - half), int(cx), int(cy + half))

        # separators
        if self._separatorAfter > 0:
            p.setPen(QPen(self._boxBorder, 2))
            for i in range(self._digits - 1):
                if (i + 1) % self._separatorAfter:
                    continue
                a = self._boxRect(i)
                b = self._boxRect(i + 1)
                y = a.center().y()
                mid = (a.right() + b.left()) / 2.0
                p.drawLine(int(mid - 4), int(y), int(mid + 4), int(y))

    # ------------------------------------------------------------------ #
    ## Input
    # ------------------------------------------------------------------ #
    def _allowed(self):
        if self._inputMode == "numeric":
            return self._NUMERIC
        if self._inputMode == "alpha":
            return self._ALPHA
        return self._NUMERIC + self._ALPHA

    def _accepts(self, ch):
        return len(ch) == 1 and ch in self._allowed()

    def _normalise(self, ch):
        return ch.upper() if self._uppercase else ch

    def keyPressEvent(self, e):
        key = e.key()
        if e.matches(QKeySequence.Paste):
            self.pasteFromClipboard()
            return
        if e.matches(QKeySequence.SelectAll):
            self._caret = 0
            self.update()
            return
        if key in (Qt.Key_Backspace,):
            if self._chars[self._caret]:
                self._chars[self._caret] = ""
            elif self._caret > 0:
                # stepping back and clearing is what users expect here
                self._caret -= 1
                self._chars[self._caret] = ""
            self._emitChanged()
            return
        if key == Qt.Key_Delete:
            self._chars[self._caret] = ""
            self._emitChanged()
            return
        if key == Qt.Key_Left:
            self._caret = max(0, self._caret - 1); self.update(); return
        if key == Qt.Key_Right:
            self._caret = min(self._digits - 1, self._caret + 1); self.update(); return
        if key == Qt.Key_Home:
            self._caret = 0; self.update(); return
        if key == Qt.Key_End:
            self._caret = self._digits - 1; self.update(); return
        text = e.text()
        if text and self._accepts(text):
            self._chars[self._caret] = self._normalise(text)
            if self._caret < self._digits - 1:
                self._caret += 1
            self._emitChanged()
            return
        super().keyPressEvent(e)

    def _emitChanged(self):
        self.update()
        code = self.code
        self.codeChanged.emit(code)
        if len(code) == self._digits:
            self.completed.emit(code)

    def setCodeText(self, text):
        """Fill from a string, ignoring anything the input mode disallows.

        This is also the paste path: a code copied as "123 456" or "123-456"
        should land correctly rather than being rejected wholesale.
        """
        kept = [self._normalise(ch) for ch in str(text) if self._accepts(ch)]
        kept = kept[:self._digits]
        self._chars = kept + [""] * (self._digits - len(kept))
        self._caret = min(len(kept), self._digits - 1)
        self._emitChanged()

    def pasteFromClipboard(self):
        """Fill from the clipboard. Bound to Ctrl+V."""
        clip = QApplication.clipboard()
        if clip is not None:
            self.setCodeText(clip.text())

    def clear(self):
        self._chars = [""] * self._digits
        self._caret = 0
        self._emitChanged()

    def isComplete(self):
        return all(self._chars)

    def mousePressEvent(self, e):
        for i in range(self._digits):
            if self._boxRect(i).contains(e.pos()):
                self._caret = i
                self.update()
                break
        self.setFocus(Qt.MouseFocusReason)
        super().mousePressEvent(e)

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self._caretOn = True
        self._blink.start()
        self.update()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self._blink.stop()
        self._caretOn = False
        self.update()

    def _toggleCaret(self):
        self._caretOn = not self._caretOn
        self.update()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def code(self):
        return "".join(self._chars)

    @code.setter
    def code(self, text):
        self.setCodeText(text)

    @Property(int)
    def digits(self):
        return self._digits

    @digits.setter
    def digits(self, value):
        value = max(1, int(value))
        if value == self._digits:
            return
        existing = self.code
        self._digits = value
        self._chars = [""] * value
        self.setCodeText(existing)          # keep what still fits
        self.updateGeometry()
        self.update()

    @Property(str)
    def inputMode(self):
        return self._inputMode

    @inputMode.setter
    def inputMode(self, value):
        value = str(value)
        self._inputMode = value if value in ("numeric", "alphanumeric", "alpha") else "numeric"
        # Re-filter what is already there, so a mode change cannot leave
        # characters the mode forbids sitting in the boxes.
        self.setCodeText(self.code)

    @Property(bool)
    def masked(self):
        return self._masked

    @masked.setter
    def masked(self, value):
        self._masked = bool(value); self.update()

    @Property(bool)
    def uppercase(self):
        return self._uppercase

    @uppercase.setter
    def uppercase(self, value):
        self._uppercase = bool(value)
        if self._uppercase:
            self._chars = [c.upper() for c in self._chars]
        self.update()

    @Property(int)
    def separatorAfter(self):
        return self._separatorAfter

    @separatorAfter.setter
    def separatorAfter(self, value):
        self._separatorAfter = max(0, int(value))
        self.updateGeometry(); self.update()

    @Property(int)
    def boxWidth(self):
        return self._boxW

    @boxWidth.setter
    def boxWidth(self, value):
        self._boxW = max(8, int(value)); self.updateGeometry(); self.update()

    @Property(int)
    def boxHeight(self):
        return self._boxH

    @boxHeight.setter
    def boxHeight(self, value):
        self._boxH = max(8, int(value)); self.updateGeometry(); self.update()

    @Property(int)
    def boxSpacing(self):
        return self._spacing

    @boxSpacing.setter
    def boxSpacing(self, value):
        self._spacing = max(0, int(value)); self.updateGeometry(); self.update()

    @Property(str)
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = "error" if str(value) == "error" else "default"
        self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def boxBackgroundColor(self):
        return self._boxBg

    @boxBackgroundColor.setter
    def boxBackgroundColor(self, c):
        self._boxBg = QColor(c); self.update()

    @Property(QColor)
    def boxBorderColor(self):
        return self._boxBorder

    @boxBorderColor.setter
    def boxBorderColor(self, c):
        self._boxBorder = QColor(c); self.update()

    @Property(QColor)
    def boxBorderActiveColor(self):
        return self._boxBorderActive

    @boxBorderActiveColor.setter
    def boxBorderActiveColor(self, c):
        self._boxBorderActive = QColor(c); self.update()

    @Property(QColor)
    def boxBorderErrorColor(self):
        return self._boxBorderError

    @boxBorderErrorColor.setter
    def boxBorderErrorColor(self, c):
        self._boxBorderError = QColor(c); self.update()

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()
