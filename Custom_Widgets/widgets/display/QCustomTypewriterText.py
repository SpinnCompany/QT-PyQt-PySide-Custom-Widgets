########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomTypewriterText - text that types itself in.
##
## The hero headline that writes itself, or a rotating list of taglines. A
## caret blinks while typing and can keep blinking after.
##
## Two things this gets right that a naive timer loop does not:
##   * the widget is sized against the LONGEST phrase, so the layout does not
##     jump on every character or when the phrase rotates
##   * the caret is painted, not a "|" character, so it does not shift the
##     text as it blinks
##
## Emits phraseFinished(str) when a phrase completes and cycled(int) when it
## moves to the next one.
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QTimer
from qtpy.QtGui import QColor, QPainter, QPen, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomTypewriterText(QWidget):
    phraseFinished = Signal(str)
    cycled = Signal(int)

    WIDGET_ICON = "components/icons/keyboard_alt.png"
    WIDGET_TOOLTIP = "Text that types itself in, with a blinking caret"
    WIDGET_MODULE = "Custom_Widgets.QCustomTypewriterText"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTypewriterText' name='customTypewriterText'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>40</height></rect></property>
            <property name='phrasesCsv'><string>Build faster,Ship sooner,Sleep better</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomTypewriterText",
        "props": {"phrasesCsv": {"type": "string", "default": ""},
                  "typeSpeed": {"type": "int", "default": 65},
                  "eraseSpeed": {"type": "int", "default": 35},
                  "holdDelay": {"type": "int", "default": 1200},
                  "loop": {"type": "bool", "default": True},
                  "erase": {"type": "bool", "default": True},
                  "showCaret": {"type": "bool", "default": True},
                  "caretBlinkRate": {"type": "int", "default": 530},
                  "alignment": {"type": "enum",
                                "values": ["left", "center", "right"],
                                "default": "left"},
                  "textColor": {"type": "color", "default": "#0f172a"},
                  "caretColor": {"type": "color", "default": "#2563eb"}},
        "signals": ["phraseFinished", "cycled"],
        "tokens_used": ["on-surface", "accent"],
    }

    def __init__(self, parent=None, phrases=None, autoStart=True):
        super().__init__(parent)
        self.setObjectName("QCustomTypewriterText")
        self._phrases = [str(p) for p in (phrases or [])]
        self._index = 0
        self._shown = 0
        self._erasing = False
        self._typeSpeed = 65
        self._eraseSpeed = 35
        self._holdDelay = 1200
        self._loop = True
        self._erase = True
        self._showCaret = True
        self._blinkRate = 530
        self._caretOn = True
        self._alignment = "left"

        self._textColor = QColor("#0f172a")
        self._caretColor = QColor("#2563eb")

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self._tick = QTimer(self)
        self._tick.timeout.connect(self._step)
        self._blink = QTimer(self)
        self._blink.timeout.connect(self._toggleCaret)

        if self._phrases and autoStart:
            self.start()

    # ------------------------------------------------------------------ #
    ## Phrases
    # ------------------------------------------------------------------ #
    def setPhrases(self, phrases, restart=True):
        self._phrases = [str(p) for p in (phrases or [])]
        self._index = 0
        self._shown = 0
        self._erasing = False
        self.updateGeometry()
        if restart and self._phrases:
            self.start()
        else:
            self.update()

    def phrases(self):
        return list(self._phrases)

    def currentPhrase(self):
        if not self._phrases:
            return ""
        return self._phrases[self._index % len(self._phrases)]

    def visibleText(self):
        return self.currentPhrase()[:self._shown]

    def isRunning(self):
        return self._tick.isActive()

    # ------------------------------------------------------------------ #
    ## Animation
    # ------------------------------------------------------------------ #
    def start(self):
        if not self._phrases:
            return False
        self._tick.start(max(1, self._typeSpeed))
        if self._showCaret and self._blinkRate > 0:
            self._blink.start(max(1, self._blinkRate))
        return True

    def stop(self):
        self._tick.stop()
        self._blink.stop()
        self._caretOn = True
        self.update()

    def skip(self):
        """Jump to the end of the current phrase."""
        self._shown = len(self.currentPhrase())
        self._erasing = False
        self.update()

    def _step(self):
        phrase = self.currentPhrase()
        if not phrase:
            self._tick.stop()
            return

        if self._erasing:
            self._shown -= 1
            if self._shown <= 0:
                self._shown = 0
                self._erasing = False
                self._advance()
            self.update()
            return

        if self._shown < len(phrase):
            self._shown += 1
            self.update()
            if self._shown == len(phrase):
                self.phraseFinished.emit(phrase)
                # Hold the finished phrase before erasing or moving on, or the
                # text is unreadable at any speed.
                self._tick.start(max(1, self._holdDelay))
            return

        if not self._loop and self._index >= len(self._phrases) - 1:
            self._tick.stop()
            return
        if self._erase:
            self._erasing = True
            self._tick.start(max(1, self._eraseSpeed))
        else:
            self._shown = 0
            self._advance()
            self.update()

    def _advance(self):
        self._index = (self._index + 1) % max(1, len(self._phrases))
        self._tick.start(max(1, self._typeSpeed))
        self.cycled.emit(self._index)

    def _toggleCaret(self):
        self._caretOn = not self._caretOn
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        fm = QFontMetrics(self.font())
        # Sized against the LONGEST phrase: sizing to the visible text would
        # resize the widget on every character and shove the layout about.
        widest = max((fm.horizontalAdvance(p) for p in self._phrases), default=0)
        return QSize(widest + 16, fm.height() + 8)

    minimumSizeHint = sizeHint

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        fm = QFontMetrics(self.font())
        text = self.visibleText()
        width = fm.horizontalAdvance(text)

        if self._alignment == "center":
            x = (self.width() - width) / 2.0
        elif self._alignment == "right":
            x = self.width() - width - 8
        else:
            x = 8.0

        p.setPen(QPen(self._textColor))
        p.drawText(QRectF(x, 0, width + 2, self.height()),
                   int(Qt.AlignVCenter | Qt.AlignLeft), text)

        if self._showCaret and self._caretOn:
            # Painted, not a "|" character: a text caret changes the string
            # width and makes the whole line jitter as it blinks.
            p.setPen(QPen(self._caretColor, 2))
            top = (self.height() - fm.height() * 0.7) / 2.0
            p.drawLine(QRectF(x + width + 2, top, 0, 0).topLeft(),
                       QRectF(x + width + 2, top + fm.height() * 0.7, 0, 0).topLeft())

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def phrasesCsv(self):
        return ",".join(self._phrases)

    @phrasesCsv.setter
    def phrasesCsv(self, text):
        self.setPhrases([t.strip() for t in str(text).split(",") if t.strip()])

    @Property(int)
    def typeSpeed(self):
        return self._typeSpeed

    @typeSpeed.setter
    def typeSpeed(self, value):
        self._typeSpeed = max(1, int(value))

    @Property(int)
    def eraseSpeed(self):
        return self._eraseSpeed

    @eraseSpeed.setter
    def eraseSpeed(self, value):
        self._eraseSpeed = max(1, int(value))

    @Property(int)
    def holdDelay(self):
        return self._holdDelay

    @holdDelay.setter
    def holdDelay(self, value):
        self._holdDelay = max(0, int(value))

    @Property(bool)
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value):
        self._loop = bool(value)

    @Property(bool)
    def erase(self):
        return self._erase

    @erase.setter
    def erase(self, value):
        self._erase = bool(value)

    @Property(bool)
    def showCaret(self):
        return self._showCaret

    @showCaret.setter
    def showCaret(self, value):
        self._showCaret = bool(value)
        if not value:
            self._blink.stop()
        self.update()

    @Property(int)
    def caretBlinkRate(self):
        return self._blinkRate

    @caretBlinkRate.setter
    def caretBlinkRate(self, value):
        self._blinkRate = max(0, int(value))
        if self._blink.isActive() and self._blinkRate > 0:
            self._blink.start(self._blinkRate)

    @Property(str)
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        value = str(value)
        self._alignment = value if value in ("left", "center", "right") else "left"
        self.update()

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()

    @Property(QColor)
    def caretColor(self):
        return self._caretColor

    @caretColor.setter
    def caretColor(self, c):
        self._caretColor = QColor(c); self.update()
