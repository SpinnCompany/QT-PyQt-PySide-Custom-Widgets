########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomTextArea - a multi-line text input.
##
## The catalog had no multi-line input at all: QCustomInput extends QLineEdit,
## which is single-line by construction, so any form needing a comment,
## description or message body had to drop to a bare QPlainTextEdit and lose
## the token styling.
##
## Built on QPlainTextEdit rather than QTextEdit: this is a plain-text control,
## and QPlainTextEdit's line-based layout stays fast on long input where
## QTextEdit's rich document does not.
##
## Adds over the stock widget:
##   - variant / sizeVariant / state, mirroring QCustomInput
##   - maxLength with a live character counter
##   - autoGrow, so the field grows with its content between minRows and maxRows
##
## Emits lengthChanged(int) and limitReached(bool) alongside the inherited
## textChanged.
########################################################################
from qtpy.QtCore import Qt, Signal, Property
from qtpy.QtGui import QColor, QFontMetrics
from qtpy.QtWidgets import QPlainTextEdit, QSizePolicy, QLabel


class QCustomTextArea(QPlainTextEdit):
    lengthChanged = Signal(int)
    limitReached = Signal(bool)

    WIDGET_ICON = "components/icons/text_input.png"
    WIDGET_TOOLTIP = "A multi-line text input with counter and auto-grow"
    WIDGET_MODULE = "Custom_Widgets.QCustomTextArea"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTextArea' name='customTextArea'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>280</width><height>96</height></rect></property>
            <property name='placeholderText'><string>Enter text...</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomTextArea",
        "props": {
            "variant": {"type": "enum",
                        "values": ["primary", "secondary", "outline", "ghost"],
                        "default": "outline"},
            "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                            "default": "md"},
            "state": {"type": "enum",
                      "values": ["default", "focused", "error", "disabled"],
                      "default": "default"},
            "placeholderText": {"type": "string", "default": ""},
            "maxLength": {"type": "int", "default": 0},
            "showCounter": {"type": "bool", "default": False},
            "autoGrow": {"type": "bool", "default": False},
            "minRows": {"type": "int", "default": 3},
            "maxRows": {"type": "int", "default": 8},
        },
        "signals": ["textChanged", "lengthChanged", "limitReached"],
        "tokens_used": ["surface", "on-surface", "outline", "focus-ring",
                        "destructive"],
    }

    # padding per size variant, matching QCustomInput's 28 / 36 / 44 heights
    _PADDING = {"sm": 4, "md": 7, "lg": 10}

    def __init__(self, parent=None, placeholder="", maxLength=0):
        super().__init__(parent)
        self.setObjectName("QCustomTextArea")
        self._variant = "outline"
        self._sizeVariant = "md"
        self._state = "default"
        self._maxLength = int(maxLength)
        self._showCounter = False
        self._autoGrow = False
        self._minRows = 3
        self._maxRows = 8
        self._counterColor = QColor("#64748b")
        self._counterOverColor = QColor("#dc2626")
        self._guard = False           # re-entrancy guard for truncation

        self._counterLabel = QLabel(self)
        self._counterLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._counterLabel.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._counterLabel.hide()

        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.textChanged.connect(self._onTextChanged)
        self._applyRows()
        self._syncCounter()

    # ------------------------------------------------------------------ #
    ## Rows / geometry
    # ------------------------------------------------------------------ #
    def _rowHeight(self):
        return QFontMetrics(self.font()).lineSpacing()

    def _chromeHeight(self):
        """Everything that is not text: frame, padding and the counter strip."""
        pad = self._PADDING.get(self._sizeVariant, self._PADDING["md"])
        return 2 * self.frameWidth() + 2 * pad + self._counterStripHeight()

    def _counterStripHeight(self):
        if not self._showCounter:
            return 0
        return QFontMetrics(self.font()).height() + 4

    def _heightForRows(self, rows):
        return int(self._rowHeight() * max(1, rows) + self._chromeHeight())

    def _applyRows(self):
        """Reserve the counter strip and size the field to its row range."""
        self.setViewportMargins(0, 0, 0, self._counterStripHeight())
        self.setMinimumHeight(self._heightForRows(self._minRows))
        if self._autoGrow:
            self._grow()
        else:
            self.setMaximumHeight(16777215)
        self.updateGeometry()

    def _grow(self):
        """Resize to fit the content, clamped between minRows and maxRows."""
        if not self._autoGrow:
            return
        doc = self.document()
        doc.setTextWidth(max(1, self.viewport().width()))
        rows = max(self._minRows,
                   min(self._maxRows, int(doc.size().height()) or self._minRows))
        h = self._heightForRows(rows)
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._grow()
        self._placeCounter()

    # ------------------------------------------------------------------ #
    ## Text / limit
    # ------------------------------------------------------------------ #
    def _onTextChanged(self):
        if self._guard:
            return
        text = self.toPlainText()
        if self._maxLength > 0 and len(text) > self._maxLength:
            # Truncate and put the cursor back at the end, so a paste that
            # overshoots does not silently swallow the whole edit.
            self._guard = True
            cursor = self.textCursor()
            at_end = cursor.position() >= len(text)
            self.setPlainText(text[:self._maxLength])
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            if at_end:
                self.setTextCursor(cursor)
            self._guard = False
            text = self.toPlainText()
            self.limitReached.emit(True)
        elif self._maxLength > 0 and len(text) == self._maxLength:
            self.limitReached.emit(True)
        self.lengthChanged.emit(len(text))
        self._grow()
        self._syncCounter()

    def length(self):
        return len(self.toPlainText())

    def remaining(self):
        """Characters left, or -1 when no limit is set."""
        if self._maxLength <= 0:
            return -1
        return max(0, self._maxLength - self.length())

    def isOverLimit(self):
        return self._maxLength > 0 and self.length() >= self._maxLength

    def clearText(self):
        self.setPlainText("")

    # ------------------------------------------------------------------ #
    ## Counter
    # ------------------------------------------------------------------ #
    ## A child QLabel rather than a QPainter call. QPlainTextEdit is a
    ## QAbstractScrollArea: its paintEvent fires for the *viewport*, so
    ## QPainter(self) there is never active and silently draws nothing. The
    ## reserved strip also sits outside the viewport, so painting on the
    ## viewport cannot reach it either.
    def _syncCounter(self):
        if not self._showCounter:
            self._counterLabel.hide()
            return
        text = ("%d/%d" % (self.length(), self._maxLength)
                if self._maxLength > 0 else str(self.length()))
        colour = self._counterOverColor if self.isOverLimit() else self._counterColor
        self._counterLabel.setText(text)
        self._counterLabel.setStyleSheet(
            "background: transparent; color: %s;" % colour.name())
        self._counterLabel.show()
        self._placeCounter()

    def _placeCounter(self):
        strip = self._counterStripHeight()
        if not strip:
            return
        frame = self.frameWidth()
        self._counterLabel.setGeometry(
            frame, self.height() - strip - frame,
            max(0, self.width() - 2 * frame - 6), strip)

    # ------------------------------------------------------------------ #
    ## State
    # ------------------------------------------------------------------ #
    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def setError(self, error_text=None):
        if error_text:
            self._state = "error"
            self.setToolTip(error_text)
        else:
            self._state = "default"
            self.setToolTip("")
        self._repolish()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if self._state != "error":
            self._state = "focused"
            self._repolish()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if self._state != "error":
            self._state = "default"
            self._repolish()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        self._variant = str(value)
        self._repolish()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self._applyRows()
        self._repolish()

    @Property(str)
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = str(value)
        self._repolish()

    @Property(int)
    def maxLength(self):
        return self._maxLength

    @maxLength.setter
    def maxLength(self, value):
        self._maxLength = max(0, int(value))
        self._onTextChanged()

    @Property(bool)
    def showCounter(self):
        return self._showCounter

    @showCounter.setter
    def showCounter(self, value):
        self._showCounter = bool(value)
        self._applyRows()
        self._syncCounter()

    @Property(bool)
    def autoGrow(self):
        return self._autoGrow

    @autoGrow.setter
    def autoGrow(self, value):
        self._autoGrow = bool(value)
        self._applyRows()

    @Property(int)
    def minRows(self):
        return self._minRows

    @minRows.setter
    def minRows(self, value):
        self._minRows = max(1, int(value))
        if self._maxRows < self._minRows:
            self._maxRows = self._minRows
        self._applyRows()

    @Property(int)
    def maxRows(self):
        return self._maxRows

    @maxRows.setter
    def maxRows(self, value):
        self._maxRows = max(1, int(value))
        if self._maxRows < self._minRows:
            self._minRows = self._maxRows
        self._applyRows()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def counterColor(self):
        return self._counterColor

    @counterColor.setter
    def counterColor(self, c):
        self._counterColor = QColor(c); self._syncCounter()

    @Property(QColor)
    def counterOverColor(self):
        return self._counterOverColor

    @counterOverColor.setter
    def counterOverColor(self, c):
        self._counterOverColor = QColor(c); self._syncCounter()
